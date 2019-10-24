import os.path
import cv2
import numpy as np
#import matplotlib as plt
from matplotlib import pyplot as plt
#matplotlib.use('GTKAgg')

plt.rcParams['figure.figsize'] = (224, 224)
#Leitura da Imagem
video = cv2.VideoCapture('video.mp4')
face_cascade = cv2.CascadeClassifier('modelo/haarcascade_frontalface_default.xml')

frame_width = int(video.get(3))
frame_height = int(video.get(4))
cont = 1
contFrame = 1

if not os.path.exists('Pessoas'):
        os.makedirs('Pessoas')

if not os.path.exists('Hist'):
        os.makedirs('Hist')

if not os.path.exists('HistFace'):
        os.makedirs('HistFace')

#função para detectar as faces
def detect(img):
    global cont
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_color = img[y:y+h, x:x+w]
        cv2.imwrite("Pessoas/face%i.jpg" % cont, roi_color)
        histograma(roi_color, 'face')
    if len(faces) > 0:
        histograma(img, 'frame')

def histograma(img, variavel):
    global cont
    global contFrame
    histogram = cv2.calcHist([img],[0],None,[256],[0,256])
    if variavel == 'face':
        arquivo = open('HistFace/hist%i.txt' % cont, 'w')
        cont = cont + 1
    else:
        arquivo = open('Hist/histFrame%i.txt' % contFrame, 'w')
        contFrame = contFrame + 1
    arquivo.write(str(histogram))
    arquivo.close()

while(video.isOpened()):
    
    ret, frame = video.read()
    if ret == False:
        break
    detect(frame)
    
    # write the flipped frame
    #out.write(cinza)
    try:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        pass


video.release()
#out.release()
cv2.destroyAllWindows()