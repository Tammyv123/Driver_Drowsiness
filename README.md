Drowsiness Detection System
This project is a real-time drowsiness detection system using a webcam. It monitors a user's face and eyes to detect signs of drowsiness. If the system detects that the user's eyes have been closed continuously for more than 5 seconds, it triggers a loud alarm sound to alert the user. The alarm can be manually stopped by clicking a "STOP ALARM" button displayed on the screen.

Features
Real-time face and eye detection using OpenCV's Haar Cascade classifiers.
Automatic alarm trigger if eyes are closed for a continuous duration.
Interactive STOP ALARM button to manually turn off the alarm.
Smooth handling of frame rate and alarm timing.
Mouse click support for user interaction.

How It Works
The system uses the webcam feed to continuously scan for faces and eyes.
If no eyes are detected for more than 5 seconds, an alarm sound starts playing.
The user can stop the alarm by clicking the STOP ALARM button drawn on the video feed.
The system resets and continues monitoring after the alarm is stopped.

Technologies Used
Python
OpenCV (for video capture and face/eye detection)
Pygame (for playing the alarm sound)

Requirements
Python 3.x
OpenCV (opencv-python)
Pygame (pygame)
