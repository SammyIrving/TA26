import cv2
import numpy as np
from picamera2 import Picamera2

# Global variables
clicked_points = []
image_display = None
resolution = None  # mm per pixel

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

# Mouse callback to collect points
def click_event(event, x, y, flags, param):
    global clicked_points, image_display
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        cv2.circle(image_display, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Image", image_display)

def capture_image():
    print("Capturing image...")
    image_path = "/home/samuel/captured_image.jpg"
    picam2.start()
    picam2.capture_file(image_path)
    picam2.stop()
    print("Image captured.")
    return cv2.imread(image_path)

def calculate_resolution(points):
    """Assumes last two points are reference with known distance (e.g., 10mm)."""
    ref_mm = 10.0  # reference length in mm
    if len(points) < 2:
        return None
    pt1, pt2 = points[-2], points[-1]
    dist_px = np.linalg.norm(np.array(pt1) - np.array(pt2))
    return ref_mm / dist_px if dist_px > 0 else None

def compute_distances(points, res):
    print("\n--- Measurements ---")
    for i in range(0, len(points) - 2, 2):  # excluding last two reference points
        pt1, pt2 = points[i], points[i+1]
        dist_px = np.linalg.norm(np.array(pt1) - np.array(pt2))
        dist_mm = dist_px * res
        print(f"Distance between point {i+1} and {i+2}: {dist_px:.2f} px = {dist_mm:.2f} mm")
        cv2.line(image_display, pt1, pt2, (0, 255, 0), 2)
        cv2.imshow("Image", image_display)

# Main program
def main():
    global image_display, resolution

    print("Press 'c' to capture a photo")
    print("Then click on suture points (in pairs), with last 2 clicks being a known 10mm reference")
    print("Press 'm' to measure")
    print("Press 'q' to quit")

    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            clicked_points.clear()
            image = capture_image()
            image_display = image.copy()
            cv2.imshow("Image", image_display)
            cv2.setMouseCallback("Image", click_event)

        elif key == ord('m'):
            if len(clicked_points) < 4:
                print("Need at least 2 suture points and 2 reference points.")
                continue
            resolution = calculate_resolution(clicked_points)
            if resolution:
                print(f"Resolution: {resolution:.4f} mm/pixel")
                compute_distances(clicked_points, resolution)
            else:
                print("Failed to compute resolution. Check your reference points.")

        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
