import cv2
import imutils
import numpy as np
import pytesseract
import smtplib

# Create a filename for the saved image
image_filename = "/home/pi/Desktop/captured_frame.jpg"

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to capture frame from the webcam")
        break

    # Preprocess the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    # Find contours in the edged image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    screenCnt = None

    # Loop over the contours to find the number plate contour
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is not None:
        # Draw the contours on the frame
        cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)

        # Extract the number plate region from the frame
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(frame, frame, mask=mask)
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

        # Perform OCR on the cropped number plate region
        text = pytesseract.image_to_string(cropped, config='--psm 11')

        # Remove trailing and leading spaces
        text = text.strip()

        # Split the string into a list
        word = text.split()

        # Check if the elements of words correspond to a valid vehicle registration number in India
        if len(word) == 4 and len(word[0]) == 2 and len(word[1]) == 2 and len(word[2]) <= 2 and len(word[3]) == 4 and word[0].isalpha() and word[1].isdigit() and word[2].isalpha() and word[3].isdigit():
            # Print the valid vehicle registration number
            print("Detected Number:", text)


            # Email configuration
            sender_email = "sender@gmail.com"
            receiver_email = "receiver@gmail.com"
            email_password = "password"

            # Establish a connection with the SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            try:
                # Login to your email account
                server.login(sender_email, email_password)

                # Compose the email message
                subject = "Detected Number Plate"
                body = f"The detected number is: {text}"
                message = f"Subject: {subject}\n\n{body}"

                # Send the email
                server.sendmail(sender_email, receiver_email, message)
                print("Email sent successfully!")
            except Exception as e:
                print("An error occurred while sending the email:", str(e))
                
            # Save the captured frame as an image on the desktop
            cv2.imwrite(image_filename, frame)
            cv2.imwrite("/home/pi/Desktop/cropped_img.jpg", cropped)
            print("Image saved on the desktop as 'captured_frame.jpg'")
            print("Image saved on the desktop as 'cropped_img.jpg'")


            # Close the connection to the SMTP server
            server.quit()

    # Display the frame
    cv2.imshow("Frame", frame)

    # Check for key press to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release the webcam and close OpenCV windows
camera.release()
cv2.destroyAllWindows()