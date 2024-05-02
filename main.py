import cv2
import winsound
import smtplib
from email.message import EmailMessage
import time

first_timer = True

def text_alert(subject, body, to):
    message = EmailMessage()
    message.set_content(body)
    message['subject'] = subject
    message['to'] = to

    username = "ghimireoshil123@gmail.com"
    message['from'] = username
    password = "gfmpnckwpsyvblvw"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(username, password)
    server.send_message(message)
    server.quit()


camera = cv2.VideoCapture(0)
while camera.isOpened():
    ret, frame1 = camera.read()
    ret, frame2 = camera.read()
    difference = cv2.absdiff(frame1, frame2)
    grey_color = cv2.cvtColor(difference, cv2.COLOR_RGB2GRAY)
    blur_img = cv2.GaussianBlur(grey_color, (5, 5), 0)
    _, threshold = cv2.threshold(blur_img, 20, 255, cv2.THRESH_BINARY)
    dialation = cv2.dilate(threshold, None, iterations=4)
    contours, _ = cv2.findContours(dialation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame1, contours, -1, (255, 0, 0), 2)
    start = time.time()
    for c in contours:
        if cv2.contourArea(c) < 7500:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
        if first_timer:
            text_alert("Motion Detected", "Your camera is sensing some significant movements", "5715986989@txt.att.net")
            first_timer = False
        if time.time() - start > 300:
            text_alert("Motion Detected", "Your camera is sensing some significant movements", "5715986989@txt.att.net")
            start = start + 300
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Security Cam', frame1)

# text_alert("Motion Detected", "Your camera is sensing some significant movements", "5715986989@txt.att.net")
