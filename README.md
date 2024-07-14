# Mouth Speech Recognition

This Python script captures video from the webcam, detects mouth movements, and uses speech recognition to print recognized words. It is designed to assist individuals who cannot talk by displaying their spoken words in real-time through a graphical user interface (GUI). 

## Features

- **Mouth Movement Detection**: Uses Mediapipe to detect if the mouth is open by analyzing facial landmarks.
- **Speech Recognition in a Separate Thread**: Ensures the video feed remains smooth and responsive while processing speech recognition.
- **GUI Interface**: Provides a simple interface with buttons to start and stop the video feed and a scrollable text box to display recognized words.
- **Logging**: Includes logging to help track the application’s flow and debug issues.
- **Thread Management**: Efficiently handles threading to ensure smooth operation and clean termination of processes.

## Usage

1. **Start the Application**: Run the script to launch the GUI.
2. **Start Video Feed**: Click the "Start" button to begin capturing video from the webcam.
3. **Speech Recognition**: When the mouth is detected as open for a significant duration, the application will capture audio and print the recognized text in the scrollable text box.
4. **Stop Video Feed**: Click the "Stop" button to end the video feed.

## Installation Requirements

To run this script, ensure you have the required Python libraries installed:

```bash
pip install opencv-python mediapipe speechrecognition pyaudio
```
## Acknowledgements

- [OpenCV](https://opencv.org/)
- [Mediapipe](https://mediapipe.dev/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
