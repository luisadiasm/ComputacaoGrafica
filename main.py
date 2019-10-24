import os
import mimetypes
import pandas as pd
import cv2

import numpy as np

max_height = 100
max_width = 100

def scale(max_height, max_width, img):
  height, width = img.shape[:2]
  if max_height < height or max_width < width:
    scaling_factor = max_height / float(height)
    if max_width/float(width) < scaling_factor:
      scaling_factor = max_width / float(width)
    img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
  return img

def compareImageVideo(image, video):
  cap = cv2.VideoCapture(video)
  mean = []
  while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
      break
    try:
      scaledImage = scale(max_height, max_width, frame)
      res = cv2.matchTemplate(image, scaledImage, cv2.TM_CCOEFF_NORMED)
      min_val, similaridade, min_loc, max_loc = cv2.minMaxLoc(res)
      mean.append(similaridade)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    except:
      pass
  cap.release()
  return np.mean(mean)

def compareImages(image1, image2):
  res = cv2.matchTemplate(image1, image2, cv2.TM_CCOEFF_NORMED)
  min_val, similaridade, min_loc, max_loc = cv2.minMaxLoc(res)
  return similaridade

def compareVideos(video1, video2):
  mean = []
  while(video1.isOpened()):
    ret, frame = video1.read()
    if ret == False:
      break
    try:
      scaledImage = scale(max_height, max_width, frame)
      similaridade = compareImageVideo(scaledImage, video2)
      mean.append(similaridade)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    except:
      pass
  return np.mean(mean)

def main():
  file_path = './files/video02.mp4'
  folder_selected = './files'
  files = os.listdir(folder_selected)

  similaridadeMinima = float(input('Informe o percentual mínimo de similaridade: '))
  comparacoesMaximas = int(input('Informe o número máximo de comparações: '))

  templateType = mimetypes.MimeTypes().guess_type(file_path)[0].split("/")[0]
  listaItemsComparacao = []
  listaSimilaridadeComparacao = []
  comparacoes = 0
  for itemFile in files:
    similaridade = 0
    itemType = mimetypes.MimeTypes().guess_type(folder_selected + "/" + itemFile)[0]
    if itemType != None and comparacoes < comparacoesMaximas:
      comparacoes = comparacoes + 1
      itemType = itemType.split("/")[0]

      if itemType == "image":
        img = cv2.imread(folder_selected + "/" + itemFile, cv2.IMREAD_COLOR)
        scaledImage = scale(max_height, max_width, img)
        if templateType == "image":
          template = cv2.imread(file_path, cv2.IMREAD_COLOR)
          template = scale(max_height,max_width,template)
          similaridade = compareImages(template, scaledImage)
        elif templateType == "video":
          similaridade = compareImageVideo(scaledImage, file_path)

      elif itemType == "video":
        video = folder_selected + "/" + itemFile
        if templateType == "image":
          img = cv2.imread(file_path, cv2.IMREAD_COLOR)
          scaledImage = scale(max_height, max_width, img)
          similaridade = compareImageVideo(scaledImage, video)
        
        elif templateType == "video":
          templateCap = cv2.VideoCapture(file_path)
          similaridade = compareVideos(templateCap, video)
      similaridade = similaridade * 100
      if similaridade > similaridadeMinima:
        listaItemsComparacao.append(itemFile)
        listaSimilaridadeComparacao.append(float("{0:.2f}".format(similaridade)) if similaridade > 0 else 0.0)
  data = {
    "Item": listaItemsComparacao,
    "Similaridade": listaSimilaridadeComparacao
  }
  df = pd.DataFrame(data)
  df.sort_values(by="Similaridade", ascending=False, inplace=True)
  print(df)

if __name__ == '__main__':
  main()  
