import tkinter as tk
from tkinter import filedialog, scrolledtext
import pyttsx3
import threading
import re
import time

engine = pyttsx3.init()
engine.setProperty('rate', 150)

is_playing = False
is_paused = False
stop_flag = False
current_index = 0
sentences = []
speech_thread = None
lock = threading.Lock()

def split_into_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)

def speak_from_index(start_index):
    global is_playing, current_index, is_paused, stop_flag, speech_thread

    with lock:
        is_playing = True
        stop_flag = False

        for i in range(start_index, len(sentences)):
            if stop_flag:
                break
            while is_paused:
                time.sleep(0.1)
            try:
                engine.say(sentences[i])
                engine.runAndWait()
            except RuntimeError:
                break
            current_index = i + 1

        is_playing = False
        speech_thread = None  # reset thread reference

def read_text():
    global current_index, sentences, speech_thread, is_paused

    text = text_area.get("1.0", tk.END).strip()
    if text:
        stop_reading()
        sentences = split_into_sentences(text)
        current_index = 0
        is_paused = False
        speech_thread = threading.Thread(target=speak_from_index, args=(current_index,))
        speech_thread.start()

def pause_reading():
    global is_paused, is_playing
    if is_playing and not is_paused:
        is_paused = True
        is_playing = False
        engine.stop()

def resume_reading():
    global is_paused, speech_thread
    if is_paused and speech_thread is None:
        is_paused = False
        speech_thread = threading.Thread(target=speak_from_index, args=(current_index,))
        speech_thread.start()

def stop_reading():
    global is_playing, is_paused, current_index, stop_flag, speech_thread
    stop_flag = True
    engine.stop()
    is_playing = False
    is_paused = False
    current_index = 0
    speech_thread = None

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, content)

# GUI Setup
root = tk.Tk()
root.title("Text-to-Speech Reader (Fully Functional)")
root.geometry("800x550")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=20, font=("Arial", 12))
text_area.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Open File", command=open_file, width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Read Aloud", command=read_text, width=12).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Pause", command=pause_reading, width=12).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Resume", command=resume_reading, width=12).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Stop", command=stop_reading, width=12).grid(row=0, column=4, padx=5)

root.mainloop()