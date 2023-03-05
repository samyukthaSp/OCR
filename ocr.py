import cv2
import pytesseract
from gtts import gTTS
import pygame
import speech_recognition as sr
from playsound import playsound
import numpy as np
import os
import streamlit as st

button3=st.button('OCR')


# URL of the IP webcam
ip_url = "http://192.168.1.33:8080/video"

capture_new_frame = True

while True :

    pygame.init()
    pygame.mixer.init()
    text1 = "Starting capture"

    tts = gTTS(text1, lang='en')
    tts.save("startcapture.mp3")
    pygame.mixer.music.load("startcapture.mp3")
    pygame.mixer.music.play()


    if capture_new_frame:
        # initialize the IP webcam
        cap = cv2.VideoCapture(ip_url)

        # set the tesseract configuration
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
        config = ('-l eng --oem 1 --psm 11')


        #take a snap of the IP webcam frame
        ret, frame = cap.read()
        # frame = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)

        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Perform binarization
        threshold_value, binarized_image = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # perform text detection using pytesseract
        data4 = pytesseract.image_to_data(gray)
        filewrite = open("String.txt", "w")
        for z, a in enumerate(data4.splitlines()):
            # Counter
            if z != 0:
                # Converts 'data1' string into a list stored in 'a'
                a = a.split()
                # Checking if array contains a word
                if len(a) == 12:
                    # Storing values in the right variables
                    x, y = int(a[6]), int(a[7])
                    w, h = int(a[8]), int(a[9])
                    # Display bounding box of each word
                    cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    # Display detected word under each bounding box
                    cv2.putText(gray, a[11], (x - 15, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
                    filewrite.write(a[11] + " ")
        filewrite.close()
        fileread = open("String.txt", "r")
        language = 'en'
        # Output the bounding box with the image
        gray = cv2.resize(gray, (0, 0), fx=1.5, fy=1.5)
        # cv2.imshow('Video output', gray)
        st.image(gray, width = 500, use_column_width=None, clamp=False)
        cv2.waitKey(0)

        line = fileread.read()
        # text = pytesseract.image_to_string(img, config=config)

        # convert the text to speech using gTTS
        if line != '':
            speech = gTTS(text=line, lang='en', slow=False)
            speech.save("speech.mp3")
            # os.system("start speech.mp3")
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load("speech.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    text = "Do you want to turn to another page or stop?"

    tts = gTTS(text, lang='en')
    tts.save("question.mp3")
    pygame.mixer.music.load("question.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    r = sr.Recognizer()

    # open the microphone and start listening for the user's voice
    with sr.Microphone() as source:
        print("do u want to turn or stop?")
        audio = r.listen(source)

    # use the recognizer to transcribe the user's voice input
    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("turn")

    if text == 'stop':
        text = "Redirecting to main menu , Thankyou for using the service"
        print(text)
        tts = gTTS(text, lang='en')
        tts.save("question1.mp3")
        pygame.mixer.music.load("question1.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        break

    else:
        # set flag to True to capture a new frame
        capture_new_frame = True
        print("Capturing a new frame !")