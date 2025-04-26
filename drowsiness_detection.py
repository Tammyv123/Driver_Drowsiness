import cv2
import pygame
import time

# Initialize Alarm
pygame.mixer.init()
pygame.mixer.music.load('alarm.mp3')  # Ensure this path is correct

# Haar Cascade files
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Alarm Settings
frame_count = 0
CLOSED_FRAMES_THRESHOLD = 2*30  # 5 seconds assuming 30 FPS (5 * 30 = 150 frames)
alarm_on = False
fps = cap.get(cv2.CAP_PROP_FPS)

# Check for zero FPS and assign default value if nescessary
if fps == 0:
    fps = 30  # Default FPS
frame_time = 1 / fps  # Time per frame in seconds

# Button Settings
BUTTON_POS = (20, 60)
BUTTON_SIZE = (150, 50)
BUTTON_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (0, 0, 0)

# Global variable to track mouse click
mouse_click = False

def draw_button(frame, text):
    x, y = BUTTON_POS
    w, h = BUTTON_SIZE
    cv2.rectangle(frame, (x, y), (x+w, y+h), BUTTON_COLOR, -1)
    cv2.putText(frame, text, (x + 10, y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, BUTTON_TEXT_COLOR, 2)

def is_button_clicked(x, y):
    btn_x, btn_y = BUTTON_POS
    btn_w, btn_h = BUTTON_SIZE
    return btn_x <= x <= btn_x + btn_w and btn_y <= y <= btn_y + btn_h

def mouse_callback(event, x, y, flags, param):
    global mouse_click
    if event == cv2.EVENT_LBUTTONDOWN:  # If left mouse button is clicked
        if is_button_clicked(x, y):
            mouse_click = True

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    eyes_detected = False
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Debugging: Output the number of eyes detected in the frame
        print(f"Eyes detected: {len(eyes)}")

        if len(eyes) >= 2:  # Assuming 2 eyes should be detected for the person to be awake
            eyes_detected = True
            break

    # Debugging print statements
    if eyes_detected:
        print("Eyes detected")
    else:
        print("No eyes detected")

    if eyes_detected:
        frame_count = 0  # Reset the count if eyes are detected
    else:
        frame_count += 1
        if frame_count * frame_time >= 5 and not alarm_on:  # Check if 5 seconds passed
            print("No eyes detected for 5 seconds. Triggering alarm!")
            alarm_on = True
            pygame.mixer.music.play(-1)  # Looping alarm

    if alarm_on:
        draw_button(frame, "STOP ALARM")

    # Display the frame
    cv2.imshow('Drowsiness Detection', frame)

    # Set mouse callback function to track clicks
    cv2.setMouseCallback('Drowsiness Detection', mouse_callback)

    key = cv2.waitKey(1)

    if key == 27:  # ESC key
        break

    # Stop alarm if mouse click on STOP ALARM button
    if mouse_click:
        if alarm_on:
            pygame.mixer.music.stop()
            alarm_on = False
            mouse_click = False  # Reset mouse click flag
            print("Alarm stopped")

cap.release()
cv2.destroyAllWindows()
