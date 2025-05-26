import cv2
import numpy as np
from picamera2 import Picamera2
from time import sleep

# Globals
clicked_points = []
image_display = None
resolution = None  # mm per pixel
ref_mm = 1 # in mm
distance_measured = []

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
cv2.namedWindow("Captured Image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Captured Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
def resize_to_screen(image, screen_width=1920, screen_height=1080):
    img_h, img_w = image.shape[:2]
    scale_w = screen_width / img_w
    scale_h = screen_height / img_h
    scale = min(scale_w, scale_h)
    new_size = (int(img_w * scale), int(img_h * scale))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

def camera_preview_and_capture(image_path):
    print("Starting camera preview... Press 'c' to capture.")
    picam2.start()
    sleep(1)  # give sensor a moment

    while True:
        # Live preview loop
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        preview_frame = resize_to_screen(frame.copy())
        cv2.namedWindow("Camera Preview", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Camera Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.putText(preview_frame, "Press 'c' to capture", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        cv2.imshow("Camera Preview", preview_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            # Capture temporary image
            temp_image = picam2.capture_array()
            temp_image = cv2.cvtColor(temp_image, cv2.COLOR_RGB2BGR)
            resized_capture = resize_to_screen(temp_image)

            # Show captured image for confirmation
            cv2.destroyWindow("Camera Preview")
            cv2.namedWindow("Captured Image", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Captured Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Captured Image", resized_capture)
            print("Image captured. Press 'q' to confirm, 'r' to retake.")

            while True:
                confirm_key = cv2.waitKey(0) & 0xFF
                if confirm_key == ord('q'):
                    cv2.imwrite(image_path, temp_image)
                    print(f"Image confirmed and saved to: {image_path}")
                    cv2.destroyWindow("Captured Image")
                    picam2.stop()
                    return
                elif confirm_key == ord('r'):
                    print("Retaking photo...")
                    cv2.destroyWindow("Captured Image")
                    break  # Restart live preview loop



def click_event(event, x, y, flags, param):
    global clicked_points, image_display
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        cv2.circle(image_display, (x, y), 4, (0, 0, 255), -1)
        cv2.imshow("Image", image_display)

def calculate_resolution(points):
    
    if len(points) < 2:
        return None
    pt1, pt2 = points[-2], points[-1]
    dist_px = np.linalg.norm(np.array(pt1) - np.array(pt2))
    return ref_mm / dist_px if dist_px > 0 else None

def compute_distances(points, res):
    print("\n--- Measurements ---")
    for i in range(0, len(points) - 3, 1):
        pt1, pt2 = points[i], points[i + 1]
        dist_px = np.linalg.norm(np.array(pt1) - np.array(pt2))
        dist_mm = dist_px * res
        distance_measured.append(dist_mm)
        print(f"Distance between point {i+1} and {i+2}: {dist_px:.2f} px = {dist_mm:.2f} mm")
        cv2.line(image_display, pt1, pt2, (0, 255, 0), 3)
        cv2.imshow("Image", image_display)

def measure_image(image_path):
    global clicked_points, image_display, resolution
    clicked_points = []

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    image_display = image.copy()

    print(f"\n--- Measuring: {image_path} ---")
    print("Instructions:")
    print("  Click suture points in order")
    print("  Click last 2 points as 10mm reference")
    print("  Press 'm' to measure")
    print("  Press 'q' to finish")

    cv2.imshow("Image", image_display)
    cv2.setMouseCallback("Image", click_event)

    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == ord('m'):
            if len(clicked_points) < 4:
                print("Need at least 2 suture points and 2 reference points.")
                continue
            resolution = calculate_resolution(clicked_points)
            if resolution:
                print(f"Resolution: {resolution:.4f} mm/pixel")
                compute_distances(clicked_points, resolution)
                clicked_points = []
            else:
                print("Failed to compute resolution. Check reference points.")

        elif key == ord('q'):
            print("Finished measuring this image.")
            cv2.destroyAllWindows()
            break

def main():
    image1_path = "/home/samuel/captured_image1.jpg"
    image2_path = "/home/samuel/captured_image2.jpg"

    print("Previewing camera for FIRST image...")
    camera_preview_and_capture(image1_path)

    print("Previewing camera for SECOND image...")
    camera_preview_and_capture(image2_path)
    print(f"Resolution: {ref_mm:.4f} mm")

    input("Press Enter to begin measuring the FIRST image...")
    measure_image(image1_path)

    input("Press Enter to begin measuring the SECOND image...")
    measure_image(image2_path)

    print("All done. Exiting.")

if __name__ == "__main__":
    main()
