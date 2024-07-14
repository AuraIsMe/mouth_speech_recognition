# Mouth Speech Recognition

This Python script captures video from the webcam, detects mouth movements, and uses speech recognition to print recognized words. It is designed to assist individuals who cannot talk by displaying their spoken words in real-time through a graphical user interface (GUI). 

## Features

- **Mouth Movement Detection**: Uses Mediapipe to detect if the mouth is open by analyzing facial landmarks.
- **Speech Recognition in a Separate Thread**: Ensures the video feed remains smooth and responsive while processing speech recognition.
- **GUI Interface**: Provides a simple interface with buttons to start and stop the video feed and a scrollable text box to display recognized words.
- **Logging**: Includes logging to help track the application’s flow and debug issues.
- **Thread Management**: Efficiently handles threading to ensure smooth operation and clean termination of processes.

## Installation Requirements

To run this script, ensure you have the required Python libraries installed:

```bash
pip install opencv-python mediapipe speechrecognition pyaudio
