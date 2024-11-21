# maker_exam

# Image Intersection Detection

This project is a Python-based tool that detects intersections between horizontal and vertical lines on scanned forms or documents. It uses OpenCV for image processing and outputs results as images and JSON files.

## Features
- Automatically detects horizontal and vertical markers using templates.
- Draws detected horizontal and vertical lines on the input images.
- Highlights intersection points with circles.
- Saves intersection points as a JSON file with coordinates for each image.
- Processes multiple images from a specified folder.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bjakapong416/maker_exam.git
   cd maker_exam





## How it Works
- The script processes all images in the `input_images` folder.
- It uses the templates from the `templates` folder to detect horizontal and vertical markers.
- Detected markers are used to draw lines, and intersection points are identified and saved as JSON.

## Folder Structure
.
├── input_images/        # Folder containing input images
├── templates/           # Folder containing template images
│   ├── M1.JPG           # Template for horizontal markers
│   ├── M3.JPG           # Template for vertical markers
├── output_images/       # Folder for processed images
├── output_points.json   # JSON file containing intersection points
├── Myclassbot.py        # Class for template matching and image processing
├── singlemarker.py      # Main script to process images
├── requirements.txt     # Required Python packages
└── README.md            # Documentation
