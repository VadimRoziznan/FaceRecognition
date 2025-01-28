import subprocess
import numpy as np
import face_recognition
import cv2
import os
from datetime import datetime
import OPi.GPIO as GPIO
import time



path = 'KnownFaces'
images = []
classNames = []
myList = os.listdir(path)

for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])


def findEncodings(images):
   encodeList = []
   for img in images:
       img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       encode = face_recognition.face_encodings(img)[0]
       encodeList.append(encode)
   return encodeList


def markAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name}, {dtString}')


def activate_output(pin_number, duration=1):
    os.system(f"gpio mode {pin_number} out")

    os.system(f"gpio write {pin_number} 0")
    time.sleep(duration)

    os.system(f"gpio write {pin_number} 1")


def reboot_device():
    subprocess.run(["sudo", "-S", "shutdown", "-r", "now"], input="Hn48/FaLB67x\n".encode())


def connection_to_camera(diapason):
    connection = False
    for el in range(diapason):
        try:
            connection = cv2.VideoCapture(el)
            if connection.isOpened():
                print("Камера найдена.")
                break
        except Exception as e:
            print(f"Ошибка подключения к камере {el}: {str(e)}")
    else:
        time.sleep(120)
        reboot_device()
    return connection


encodeListKnown = findEncodings(images)
cap = connection_to_camera(5)


def main(cap, encodeListKnown):
    print("status OK")

    while True:

        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        if facesCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    activate_output(8, 5)
                    name = classNames[matchIndex]
                    time.sleep(2)
                    cap.release()
                    cv2.destroyAllWindows()
                    cap = connection_to_camera(5)
                    break

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main(cap, encodeListKnown)

