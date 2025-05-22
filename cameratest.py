import cv2
import numpy as np
from picamera2 import Picamera2
from time import sleep

# Globals
clicked_points = []
image_display = None
resolution = None  # mm per pixel

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

def camera_preview_and_capture(image_path):
    print("Starting camera preview... Press 'c' to capture, 'q' to cancel.")
    picam2.start()
    sleep(1)  # give sensor a moment

    while True:
        frame = picam2.capture_array()
        preview_frame = frame.copy()
        cv2.putText(preview_frame, "Press 'c' to capture, 'q' to skip", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Camera Preview", preview_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            picam2.capture_file(image_path)
            print(f"Image captured and saved to: {image_path}")
            break
        elif key == ord('q'):
            print("Capture canceled.")
            break

    cv2.destroyAllWindows()
    picam2.stop()
    sleep(0.5)

def click_event(event, x, y, flags, param):
    global clicked_points, image_display
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        cv2.circle(image_display, (x, y), 2, (0, 0, 255), -1)
        cv2.imshow("Image", image_display)

def calculate_resolution(points):
    ref_mm = 10
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
        print(f"Distance between point {i+1} and {i+2}: {dist_px:.2f} px = {dist_mm:.2f} mm")
        cv2.line(image_display, pt1, pt2, (0, 255, 0), 1)
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

    input("Press Enter to begin measuring the FIRST image...")
    measure_image(image1_path)

    input("Press Enter to begin measuring the SECOND image...")
    measure_image(image2_path)

    print("All done. Exiting.")

if __name__ == "__main__":
    main()
