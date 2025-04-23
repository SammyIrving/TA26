import cv2
import numpy as np
from picamera2 import Picamera2

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

# Capture image
image_path = "/home/samuel/captured_image.jpg"
picam2.capture_file(image_path)
picam2.stop()

# Read the captured image
img_cv2 = cv2.imread(image_path)

# Convert to grayscale
img_gray = cv2.cvtColor(img_cv2, cv2.COLOR_RGB2GRAY)
# img_resized = cv2.resize(img_gray, (600, 400))
img_resized = img_gray

# Apply GaussianBlur to reduce noise
blurred = cv2.GaussianBlur(img_resized, (5, 5), 0)

# Use Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if len(contours) < 2:
    print("Could not detect two objects.")
    exit()

contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0], reverse=False)
merged_contour = []
current_contour = contours[0]

for i in range(1, len(contours)):
    rect1 = cv2.boundingRect(current_contour)
    rect2 = cv2.boundingRect(contours[i])
    center1 = (rect1[0] + rect1[2] // 2, rect1[1] + rect1[3] // 2)
    center2 = (rect2[0] + rect2[2] // 2, rect2[1] + rect2[3] // 2)
    distance1 = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
    
    if distance1 < 7:
        current_contour = np.vstack((current_contour, contours[i]))
    else:
        merged_contour.append(current_contour)
        current_contour = contours[i]
merged_contour.append(current_contour)

# Last two dots is the reference point
reference = 10 # Reference in millimeter
rect1 = cv2.boundingRect(merged_contour[len(merged_contour)-2])
rect2 = cv2.boundingRect(merged_contour[len(merged_contour)-1])
center1 = (rect1[0] + rect1[2] // 2, rect1[1] + rect1[3] // 2)
center2 = (rect2[0] + rect2[2] // 2, rect2[1] + rect2[3] // 2)
distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2) # in Pixels
resolution = reference / distance # millimeter / pixel
print(f"resolusi yang diperoleh adalah {resolution} mm/pixel")

for i in range(len(merged_contour) - 3):
    rect1 = cv2.boundingRect(merged_contour[i])
    rect2 = cv2.boundingRect(merged_contour[i + 1])
    
    center1 = (rect1[0] + rect1[2] // 2, rect1[1] + rect1[3] // 2)
    center2 = (rect2[0] + rect2[2] // 2, rect2[1] + rect2[3] // 2)

    distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
    cv2.drawContours(img_resized, [contours[i]], -1, (0, 255, 0), 2)
    cv2.drawContours(img_resized, [contours[i+1]], -1, (0, 0, 255), 2)
    cv2.circle(img_resized, center1, 5, (255, 0, 0), -1)
    cv2.circle(img_resized, center2, 5, (255, 0, 0), -1)
    cv2.line(img_resized, center1, center2, (255, 255, 0), 2)
    distance_in_mm = distance * resolution
    print(f"Distance between objects: {distance} pixels")
    print(f"Distance in mm = {distance_in_mm} mm")
    
# Display the results
cv2.imshow("Image with Distance", img_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
