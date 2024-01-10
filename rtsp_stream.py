import cv2
import numpy as np
import datetime
import pytz

# Parameters
rtsp_stream_url = "rtsp://localhost:8554/mystream"  # Replace with your actual RTSP streaming link
output_folder = "output_images"
log_file = "motion_log.txt"
motion_threshold = 1000  # Adjust this threshold based on your needs

# Create output folder if it doesn't exist
import os
os.makedirs(output_folder, exist_ok=True)

# Create log file or clear existing content
with open(log_file, "w") as log:
    log.write("Motion Log:\n")

# Initialize video capture
cap = cv2.VideoCapture(rtsp_stream_url)

# Get the initial frame for motion detection
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the current frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference between the current and previous frame
    frame_delta = cv2.absdiff(prev_gray, gray)

    # Apply thresholding to identify regions with motion
    _, thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process each contour
    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > motion_threshold:
            motion_detected = True
            timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S IST")
            log_entry = f"Motion detected at {timestamp}"
            print(log_entry)

            # Save the frame with timestamp
            image_filename = f"{output_folder}/motion_{timestamp.replace(':', '-')}.jpg"
            cv2.imwrite(image_filename, frame)

            # Append log entry to the log file
            with open(log_file, "a") as log:
                log.write(log_entry + "\n")

    # Add timestamp to the bottom right corner
    timestamp_str = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S IST")
    cv2.putText(frame, timestamp_str, (frame.shape[1] - 300, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    
    # Display the frame
    cv2.imshow("Video Stream", frame)

    # Update the previous frame
    prev_gray = gray.copy()

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
