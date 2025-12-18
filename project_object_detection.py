import numpy as np
import cv2 as cv
from PIL import Image
from util import get_limits 

COLOR_MAP = {
    # Basic colors
    "red": [0, 0, 255],
    "green": [0, 255, 0],
    "blue": [255, 0, 0],
    "white": [255, 255, 255],
    "black": [0, 0, 0],
    "gray": [128, 128, 128],

    # Secondary colors
    "yellow": [0, 255, 255],
    "cyan": [255, 255, 0],
    "magenta": [255, 0, 255],

    # Shades of red
    "dark_red": [0, 0, 139],
    "light_red": [102, 102, 255],
    "maroon": [0, 0, 128],

    # Shades of green
    "dark_green": [0, 100, 0],
    "light_green": [144, 238, 144],
    "lime": [0, 255, 0],

    # Shades of blue
    "dark_blue": [139, 0, 0],
    "light_blue": [230, 216, 173],
    "navy": [128, 0, 0],

    # Brown / orange family
    "orange": [0, 165, 255],
    "dark_orange": [0, 140, 255],
    "brown": [42, 42, 165],

    # Purple / pink family
    "purple": [128, 0, 128],
    "violet": [238, 130, 238],
    "pink": [203, 192, 255],
    "hot_pink": [180, 105, 255],

    # Other useful colors
    "gold": [0, 215, 255],
    "silver": [192, 192, 192],
    "teal": [128, 128, 0],
    "olive": [0, 128, 128]
}

def get_user_color_by_name():
    
    available_colors = ", ".join(COLOR_MAP.keys())
    print("\nColor Tracking Setup:")
    print(f"Available colors: **{available_colors}**")
    
    while True:
        color_name = input("Enter the name of the color you want to track: ").strip().lower()

        if color_name in COLOR_MAP:
            return COLOR_MAP[color_name]
        else:
            print(f"'{color_name}' is not recognized. Please enter one of the available color names.")

target_color_bgr = get_user_color_by_name()
print(f"Tracking color (BGR): {target_color_bgr}")

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame from camera.")
        break
    hsvImage = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lowerLimit, upperLimit = get_limits(color=target_color_bgr) 
    mask = cv.inRange(hsvImage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5) 
    cv.imshow('Named Color Tracker', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
