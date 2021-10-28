import os
import time
import pigpio
import cv2        # ИМПОРТИРУЕМ БИБЛИОТЕКУ OPENCV 
import numpy as np # ИМПОРТИРУЕМ БИБЛИОТЕКУ NUMPY КАК np

STEER = 18

line_min = np.array((0,0,0), dtype=np.uint8)        # МИНИМАЛЬНЫЙ ЦВЕТОВОЙ ПОРОГ ЛИНИИ
line_max = np.array((255,255,163), dtype=np.uint8)  # МАКСИМАЛЬНЫЙ ЦВЕТОВОЙ ПОРОГ ЛИНИИ 


cap = cv2.VideoCapture(0)# УКАЗЫВАЕМ ИСТОЧНИК ИЗОБРАЖЕНИЯ

while True:#
    ret, frame = cap.read()#СЧИТЫВАЕМ ИЗОБРАЖЖЕНИЕ В ПЕРЕПЕННУЮ frame

    frame = cv2.resize(frame, (640,640))#ИЗМЕНЯЕМ РАЗМЕР ДЛЯ УДОБСТВА
    frame = frame[200:400, 200:400]#ВЫРЕЗАЕМ КУСОК ИЗОБРАЖЕНИЕ С ЛИНИЕЙ (ДЛЯ УМЕНЬШЕНИЯ ВОЗДЕЙСТВИЯ ВНЕШНИХ ФАКТОРОВ)
    frame = cv2.resize(frame, (640,640))#ИЗМЕНЯЕМ РАЗМЕР ДЛЯ УЛУЧШЕНИЯ ТОЧНОСТИ(ОБЯЗАТЕЛЬНОЕ СООТНОШЕНИЕ СТОРОН 1:1)
    frame = cv2.flip(frame, 1)#ОТРАЖАЕМ ИЗОБРАЖЕНИЕ (НЕОБЯЗАТЕЛЬНО)

    blur = cv2.blur(frame, (7,7))#НАКЛАДЫВАЕМ РАЗМЫТИЕ НА ИЗОБРАЖЕНИЕ 
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)#ПРЕОБРАЗОВЫВАЕМ ИЗОБРАЖЕНИЕ В ПРОСТРАНСТВО HSV
    thresh = cv2.inRange(hsv, line_min, line_max)#БИНАРИЗУЕМ ИЗОБРАЖЕНИЕ 
    conts, heir = cv2.findContours(thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)# НАХОДИМ КОНТУРЫ В БИНАРИЗОВАННОМ ИЗОБРАЖЕНИИ 
    if conts:#ПРОВЕРЯЕМ НА КОНТУРЫ 
        conts = sorted(conts, key=cv2.contourArea, reverse=True)# СОРТИРУЕМ КОНТУРЫ
        (x,y,w,h) = cv2.boundingRect(conts[0])#НАХОДИМ КООРДИНИАТЫ ДЛЯ ПРЯМОУГОЛЬНИКА 
        cv2.rectangle(frame, (x,y), (x+w,y+h),  (255,0,255), 4)# РИСУЕМ ПРЯМОУГОЛЬНИК(ДЛЯ УДОБСТВА)
        
        centre_x = x + w / 2# НАХОДИМ ЦЕНТР ПРЯМОУГОЛЬНИКА ПО ГОРИЗОНТАЛИ

        cv2.circle(frame, (round(centre_x),320), 10, (0,255,255), 3)# РИСУЕМ КРУГ, ХАРАКТЕРИЗУЮЩИЙ ЦЕНТР ПРЯМОУГОЛЬНИКА 
        
    print(centre_x - 320)# ВЫВОДИ ЦЕНТР ПРЯМОУГОЛЬНИКА ПО ГОРИЗОНТАЛИ (ВЫЧИТАНИЕ ПОЛОВИНЫ ИЗОБРАЖЕНИЯ СДЕЛАНО ДЛЯ ОТРИЦАНИЯ КООРДИНАТ) 

    cv2.imshow("FRAME", frame)#ВЫВОДИМ ИЗОБРАЖЕНИЕ

    m = 90
    
    angle = m + centre_x  
    width_impulse = int(angle * 11.1 + 500)
    pi.set_servo_pulsewidth(STEER, width_impulse)

    print(m)


    if cv2.waitKey(1) == ord('q'):#ЕСЛЕ НАЖАТА КЛАВИША 'q' ТО
        break#ВЫХОДИМ ИЗ ЦИКЛА


cap.release()#ПРЕКРАЩАЕМ ЗАХВАТ ИЗОБРАЖЕНИЯ С КАМЕРЫ
cv2.destroyAllWindows()#УДАЛЯЕМ ВСЕ ОКНА
