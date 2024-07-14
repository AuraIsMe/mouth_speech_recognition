import cv2
import mediapipe as mp
import speech_recognition as sr
import threading
import queue
import tkinter as tk
from tkinter import scrolledtext
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
recognizer = sr.Recognizer()

audio_queue = queue.Queue()

def is_mouth_open(landmarks):
    top_lip = landmarks[13].y
    bottom_lip = landmarks[14].y
    mouth_open_distance = bottom_lip - top_lip
    return mouth_open_distance > 0.02

def recognize_speech_from_queue(output_widget):
    while True:
        audio_data = audio_queue.get()
        if audio_data is None:
            break
        try:
            text = recognizer.recognize_google(audio_data)
            logging.info(f"Recognized: {text}")
            output_widget.insert(tk.END, f"Recognized: {text}\n")
            output_widget.see(tk.END)
        except sr.UnknownValueError:
            logging.warning("Could not understand audio")
        except sr.RequestError as e:
            logging.error(f"Could not request results; {e}")

def start_speech_thread(output_widget):
    speech_thread = threading.Thread(target=recognize_speech_from_queue, args=(output_widget,))
    speech_thread.daemon = True
    speech_thread.start()
    return speech_thread

def start_video(output_widget, stop_event):
    cap = cv2.VideoCapture(0)
    mouth_open_frames = 0
    mouth_open_threshold = 15

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_frame)

        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                mouth_open = is_mouth_open(face_landmarks.landmark)
                
                if mouth_open:
                    mouth_open_frames += 1
                else:
                    mouth_open_frames = 0
                
                if mouth_open_frames > mouth_open_threshold:
                    with sr.Microphone() as source:
                        logging.info("Listening...")
                        audio = recognizer.listen(source)
                        audio_queue.put(audio)
                    mouth_open_frames = 0

                for landmark in face_landmarks.landmark:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        cv2.imshow('Webcam Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    audio_queue.put(None)

def create_gui():
    root = tk.Tk()
    root.title("Speech Recognition from Webcam")
    root.geometry("800x600")

    output_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    output_widget.pack(pady=20)

    start_button = tk.Button(root, text="Start", command=lambda: start_video_thread(output_widget))
    start_button.pack(side=tk.LEFT, padx=20)

    stop_button = tk.Button(root, text="Stop", command=stop_video_thread)
    stop_button.pack(side=tk.RIGHT, padx=20)

    return root, output_widget

def start_video_thread(output_widget):
    global stop_event, video_thread
    stop_event.clear()
    video_thread = threading.Thread(target=start_video, args=(output_widget, stop_event))
    video_thread.daemon = True
    video_thread.start()

def stop_video_thread():
    global stop_event
    stop_event.set()

stop_event = threading.Event()
video_thread = None

if __name__ == "__main__":
    root, output_widget = create_gui()
    speech_thread = start_speech_thread(output_widget)
    root.mainloop()

    stop_video_thread()
    audio_queue.put(None)
    speech_thread.join()
