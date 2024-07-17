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
print(myList)

for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])

print(classNames)

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
    # Установка режима нумерации пинов (BOARD или BCM)
    # GPIO.setmode(GPIO.BCM)

    # Настройка пина как выхода
   # GPIO.setup(pin_number, GPIO.OUT)
   # print("OK")

    #try:
        # Активация выхода (подача высокого уровня)
     #   GPIO.output(pin_number, GPIO.HIGH)
      #  print(f"Выход {pin_number} активирован")

        # Ожидание указанной продолжительности
       # time.sleep(duration)

  #  finally:
        # Деактивация выхода
   #     GPIO.output(pin_number, GPIO.LOW)
    #    print(f"Выход {pin_number} деактивирован")

        # Очистка настроек GPIO
     #   GPIO.cleanup()
    # Установка режима GPIO пина 3 как выходной
    os.system("gpio mode 8 out")

    # Задание значения пина 3 в 1
    os.system("gpio write 8 1")
    print(f"pin {pin_number} high")
    time.sleep(duration)

    # Задание значения пина 3 в 0
    os.system("gpio write 8 0")
    print(f"pin {pin_number} low")


encodeListKnown = findEncodings(images)
print("Декодирование закончено")

cap = cv2.VideoCapture(1)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex]
            print(name)
            # y1, x2, y2, x1 = faceLoc
            # y1, x2, y2, x1 = y1 * 3, x2 * 4, y2 * 4, x1 * 4
            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            # cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)
            # markAttendance(name)
            activate_output(8, 2)

    # cv2.imshow("WebCam", img)
    # cv2.waitKey(1)

