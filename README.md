# 2IC80-GROUP 41- WhetsApp- The Trojan Keylogger

## DISCLAIMER 
This project is meant for educational purposes only. We take no responsibility in how the code is used. The use of the code is the complete responsibility of the end user. The developers of the code are in no way liable and responsbile for any misuse.

## Short Description
In this project we made a keylogger and also added our research about the filtering of the data that is done on the attacker's side after the receipt of the victim's data in python code. This data filtering is done with the help of machine learning. We have mainly looked into the credit card and login pages since that contains the most sensitive information in our opinion. The python script of the keylogger is contained in the conversion folder with the name as 'WhetsApp.pyw'. We have also additionally converted the python script file into an EXE file with the same name. There is also a data_analytics folder where the filtering of the data can be done for use by the attacker.

## Features of the Keylogger
- Taking screenshots with saved as a png with timestamp
- Logging of Keystrokes data with timestamp in a csv file
- Sending both of the data via email

## Requirements 
We require to install a few modules for this keylogger:
- pyinstaller
- pillow
- keyboard
- pyinstaller
The following is the libraries required for the data analytics part:
- pytesseract 
- regex 
- nltk 
- pickle 
- sklearn 
- pandas

