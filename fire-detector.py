# Import necessary libraries
import cv2
import numpy as np
import smtplib
import playsound
import threading

# Initialize status flags and counters
Alarm_Status = False
Email_Status = False
Fire_Reported = 0

# Function to play the alarm sound in a loop
def play_alarm_sound_function():
    while True:
        playsound.playsound('alarm-sound.mp3', True)

# Function to send an email notification
def send_mail_function():
    recipientEmail = "prakritishrestha515@gmail.com"
    recipientEmail = recipientEmail.lower()

    try:
        # Set up an SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("test123@ismt.edu.np", '$+@r#1%3')
        server.sendmail('test123@ismt.edu.np', recipientEmail, "Subject: Fire Accident Warning\n\nWarning: A Fire Accident has been reported on ISMT College")
        print("Sent to {}".format(recipientEmail))
        server.quit()  # Close the connection
    except Exception as e:
        print(e)

# Call the function to send the email
send_mail_function()
# Open a video capture object using the specified video file or webcam
video = cv2.VideoCapture("video_file.mp4")  # If you want to use webcam, use Index like 0, 1.

# Main loop for processing video frames
while True:
    grabbed, frame = video.read()
    if not grabbed:
        break

    # Resize the frame for consistent processing
    frame = cv2.resize(frame, (960, 540))

    # Apply Gaussian blur and convert to HSV color space
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Define color range for detecting fire (red/orange)
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # Create a mask to detect fire color range
    mask = cv2.inRange(hsv, lower, upper)

    # Apply the mask to the original frame
    output = cv2.bitwise_and(frame, frame, mask=mask)

    # Count the number of non-zero pixels in the mask
    no_red = cv2.countNonZero(mask)

    # If a significant number of red pixels are detected, increment the fire report counter
    if int(no_red) > 15000:
        Fire_Reported += 1

    # Display the processed output frame
    cv2.imshow("output", output)

    # Check if a fire has been reported
    if Fire_Reported >= 1:
        # Start playing the alarm sound and sending email notifications (once)
        if not Alarm_Status:
            threading.Thread(target=play_alarm_sound_function).start()
            Alarm_Status = True

        if not Email_Status:
            threading.Thread(target=send_mail_function).start()
            Email_Status = True

    # Check if the 'q' key is pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close windows
cv2.destroyAllWindows()
video.release()