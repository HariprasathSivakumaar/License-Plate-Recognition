# License Plate Recognition using Raspberry Pi and OpenCV

This project utilizes computer vision techniques to detect, localize, segment, and recognize license plates of the vehicles from the images captured by the Raspberry Pi. The recognized license plate numbers can be used for various applications, such as parking systems, access control, or vehicle monitoring.

The license plate recognition project involves several steps to preprocess the captured image and perform accurate recognition. The initial step is preprocessing the captured image. This step includes 
- converting the frame to grayscale
- applying bilateral filtering
- performing edge detection using the Canny algorithm.

Once the image is preprocessed, contours are detected in the frame.
Then the potential license plate regions are identified by sorting the contours based on their area. The contour with four corners, indicating a potential license plate region, is selected.

If a license plate contour is found, the code proceeds to extract the license plate region using a mask and bitwise operations. Subsequently, optical character recognition (OCR) is performed on the extracted license plate region using the pytesseract library. The recognized text is then validated to ensure it corresponds to a valid vehicle registration number based on specific criteria, such as format, character length, and alphanumeric pattern.

If a valid license plate is detected, the recognized number is printed on the console, and both the captured frame and cropped license plate image are saved. In addition to these results, an email notification is sent to the specified sender and receiver email addresses containing the recognized license plate number.


## Components Required
- Raspberry Pi
- Pi Camera / WebCam

## Hardware Installation
1. Connect a compatible camera module to your Raspberry Pi. (Here we are using WebCamera)
2. Ensure that the Raspberry Pi is properly powered and connected to the internet.

## Software Installation
1. Set up the Raspberry Pi with a Raspbian operating system.
   Refer this [video](https://youtu.be/CQtliTJ41ZE) for Setting up your Raspberry Pi.
2. Install Python and the necessary packages:
```bash
pip install imutils
pip install pytesseract
pip install opencv-python
```

## How to run
1. Clone the repository:
```bash
git clone https://github.com/HariprasathSivakumaar/License-Plate-Recognition.git
```
2. Run the script:
```bash
python3 recognition.py
```
