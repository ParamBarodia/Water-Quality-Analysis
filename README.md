# Water Quality Analysis

## Overview

This Python application analyzes the physical characteristics of water based on an input image. It employs the OpenCV library for image processing, NumPy for numerical operations, webcolors for color identification, and Streamlit for the user interface.

The application takes an image as input, detects and analyzes colors within the image to determine the color of water and sediment. It also calculates the turbidity of the water and estimates the water temperature based on the atmospheric temperature.

## Requirements

Before running the application, make sure you have the following Python libraries installed:

- `cv2` (OpenCV)
- `numpy`
- `webcolors`
- `streamlit`

You can install them using pip:

```shell
pip install opencv-python-headless
pip install numpy
pip install webcolors
pip install streamlit

Usage
Run the application by executing the Python script.
Access the application via a web browser (typically at http://localhost:8501).
Use the sidebar to configure settings:
Enter the temperature of the atmosphere when the image was captured (in °C) in the "Enter the temperature of the atmosphere" field.
Upload an image using the "Upload an image" button.
The application will perform the following steps:
Convert the uploaded image to the HSV color space.
Detect specific colors (red, yellow, green, blue, purple, and pink) in the image.
Determine the color of water based on the detected colors.
Determine the color of sediment based on the detected colors.
Calculate the turbidity of the water.
Estimate the water temperature based on the atmospheric temperature.
Display the original image, the image with detected objects outlined, and the analysis results.
Color Detection
The application detects the following colors in the image:

Red
Yellow
Green
Blue
Purple
Pink
These colors are used to determine the color of water and sediment in the image.

Water and Sediment Analysis
Water Color: The water color is determined based on the presence of blue and green colors in the image. If blue is detected, the water color is "clear." If green is detected, the water color is "high organic content." Otherwise, it is "white."
Sediment Color: The sediment color is determined based on the presence of brown color in the image. If brown is detected, the sediment color is "brown." Otherwise, it is "not detected."
Turbidity: Turbidity is calculated based on the edge intensity in the image. Higher turbidity values indicate less clear water.
Water Temperature: The water temperature is estimated as 60% of the atmospheric temperature provided in the settings.
Screenshots
Original Image


Final Image with Detected Objects


Detected Colors (Sidebar)


Note
This application provides a basic analysis of water quality based on color and turbidity. For more comprehensive water quality testing, additional parameters and chemical analysis may be required.

Please ensure that the uploaded images are of good quality and have appropriate lighting for accurate color detection and analysis.

## Author

This application was created by **Param Barodia**. If you have any questions or feedback, please contact **parambarodia26@gmail.com**.
