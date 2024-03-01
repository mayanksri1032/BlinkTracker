import cv2
import dlib
import pandas as pd
import keyboard
from datetime import datetime

# Initialize face detector and facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download from http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize variables
employee_name = input("Enter employee name: ")
blink_count = 0

# Create DataFrame to store data
df = pd.DataFrame(columns=["Employee Name", "Blink Count", "Timestamp"])

while True:
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = detector(gray)

    for face in faces:
        # Get facial landmarks
        landmarks = predictor(gray, face)

        # Calculate Eye Aspect Ratio (EAR)
        left_eye_ratio = 0  # Implement logic to calculate left eye aspect ratio
        right_eye_ratio = 0  # Implement logic to calculate right eye aspect ratio

        # Assuming a blink when both eyes have low EAR
        if left_eye_ratio < threshold and right_eye_ratio < threshold:
            blink_count += 1

    # Check if the employee is working on the project (e.g., pressing a specific key)
    if keyboard.is_pressed("project_key"):
        # Record blink count and timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = df.append({"Employee Name": employee_name, "Blink Count": blink_count, "Timestamp": timestamp},
                       ignore_index=True)
        blink_count = 0  # Reset blink count

    # Display the frame (you may also save it or perform other actions)
    cv2.imshow("Frame", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save the DataFrame to an Excel file
df.to_excel("blink_data.xlsx", index=False)

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
