import numpy as np
import cv2 as cv
from PIL import Image
from util import get_limits # Assumes this function is correctly implemented

## --- Color Name Mapping ---
# Define a dictionary mapping color names to their BGR values (OpenCV format)
COLOR_MAP = {
    "red": [0, 0, 255],
    "green": [0, 255, 0],
    "blue": [255, 0, 0],
    "yellow": [0, 255, 255],
    "cyan": [255, 255, 0],
    "magenta": [255, 0, 255],
    "white": [255, 255, 255],
    "black": [0, 0, 0]
}
## --- End Color Name Mapping ---

## --- Color Selection Function ---
def get_user_color_by_name():
    """
    Prompts the user to enter a color name and returns the corresponding BGR value.
    """
    available_colors = ", ".join(COLOR_MAP.keys())
    print("\nColor Tracking Setup:")
    print(f"Available colors: **{available_colors}**")
    
    while True:
        color_name = input("Enter the name of the color you want to track: ").strip().lower()

        if color_name in COLOR_MAP:
            return COLOR_MAP[color_name]
        else:
            print(f"'{color_name}' is not recognized. Please enter one of the available color names.")

# Get the color input from the user by name
target_color_bgr = get_user_color_by_name()
print(f"Tracking color (BGR): {target_color_bgr}")
## --- End Color Selection ---

# Initialize the camera
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    # 1. Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to read frame from camera.")
        break

    # 2. Convert to HSV
    hsvImage = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # 3. Get the color limits based on the user's input color (BGR)
    lowerLimit, upperLimit = get_limits(color=target_color_bgr) 

    # 4. Create a mask
    mask = cv.inRange(hsvImage, lowerLimit, upperLimit)

    # 5. Find bounding box (using PIL as in original code)
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    # 6. Draw rectangle if the color is found
    if bbox is not None:
        x1, y1, x2, y2 = bbox

        # Draw a rectangle around the detected area, using a green outline
        frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5) 

    # 7. Display the resulting frame
    cv.imshow('Named Color Tracker', frame)

    # 8. Exit condition
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 9. Cleanup
cap.release()
cv.destroyAllWindows()