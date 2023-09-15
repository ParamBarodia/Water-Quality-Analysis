import cv2
import numpy as np
import webcolors
import streamlit as st

# Define your name for the watermark
author_name = "Param Barodia"

# Define function to display image
def display_image(image):
    st.image(image, channels="BGR")

# Streamlit layout
st.set_page_config(page_title="Water Quality Analysis", layout="wide")
st.title("Water Quality Analysis for Checking Physical Characteristics of Water")
st.markdown("---")

# Temperature input
st.sidebar.title("Settings")
atmt = st.sidebar.number_input("Enter the temperature of the atmosphere when the image was captured (in °C): ")
water_temp = 0.6 * atmt

# Image upload
uploaded = st.file_uploader("Upload an image")

if uploaded is not None:
    # Read image file
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Convert image to HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range of colors to be detected
    colors = {
        'red': ([0, 100, 100], [10, 255, 255]),
        'yellow': ([20, 100, 100], [30, 255, 255]),
        'green': ([36, 25, 25], [70, 255, 255]),
        'blue': ([90, 25, 25], [130, 255, 255]),
        'purple': ([130, 25, 25], [170, 255, 255]),
        'pink': ([170, 25, 25], [180, 255, 255])
    }

    # Create empty list for colors detected
    detected_colors = []

    # Iterate over each color range and detect colors in image
    for color, (lower, upper) in colors.items():
        # Create mask for color range
        mask = cv2.inRange(hsv_img, np.array(lower), np.array(upper))
        # Count number of pixels that match the mask
        num_pixels = cv2.countNonZero(mask)
        # If there are any matching pixels, add color name and count to list
        if num_pixels > 0:
            detected_colors.append((color, num_pixels))

    # Determine the color of water
    water_color = None
    water_pixels = 0
    if detected_colors:
        for color, num_pixels in detected_colors:
            if color == 'blue':
                water_color = 'clear'
                water_pixels = num_pixels
                break
            elif color == 'green':
                water_color = 'high organic content'
                water_pixels = num_pixels
                break
        else:
            water_color = 'white'
            water_pixels = sum([num_pixels for _, num_pixels in detected_colors if _ == 'white'])

    # Determine the color of sediment
    sediment_color = None
    sediment_pixels = 0
    if detected_colors:
        for color, num_pixels in detected_colors:
            if color == 'brown':
                sediment_color = 'brown'
                sediment_pixels = num_pixels
                break
        else:
            sediment_color = 'not detected'

    # Display detected colors and their respective names
    st.sidebar.subheader("Detected Colors")
    for color, num_pixels in detected_colors:
        # Convert color from name to RGB value
        rgb = webcolors.name_to_rgb(color)
        # Create color swatch image
        swatch = np.zeros((100, 100, 3), dtype=np.uint8)
        swatch[:, :] = rgb
        # Display color name and swatch image
        st.sidebar.write(f'{color}: {num_pixels} pixels')
        st.sidebar.image(swatch)

    # Show original image
    st.subheader("Original Image")
    display_image(img)

    # Perform image processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 100, 200)

    edge_mean = np.mean(edges)
    turbidity = 100 - (edge_mean / 2.55)

    # Dilate the edges to fill gaps and improve object detection
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)

    # Find contours in the dilated image
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around detected objects
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the final image with detected objects
    st.subheader("Final Image with Detected Objects")
    
    # Add watermark with author's name
    watermarked_img = img.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_color = (0, 0, 0)  # Black color
    font_thickness = 2
    position = (10, img.shape[0] - 10)  # Adjust position as needed

    cv2.putText(watermarked_img, f"Author: {author_name}", position, font, font_scale, font_color, font_thickness)

    # Display the final image with detected objects and the author watermark
    display_image(watermarked_img)

    # Print water and sediment color information
    st.subheader("Water and Sediment Analysis")
    st.write(f'Water color: {water_color} ({water_pixels} pixels)')
    st.write(f'Sediment color: {sediment_color} ({sediment_pixels} pixels)')
    st.write('Turbidity:', turbidity)
    st.write('Water Temperature:', water_temp)
