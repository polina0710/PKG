import numpy as np
import cv2 as cv
from tkinter import ttk
from tkinter import *
from PIL import ImageTk
import PIL
from matplotlib import pyplot as plt
import os

class MainSolution():
    def __init__(self):
      self.image = cv.imread('Fig10.15(a).BMP',cv.IMREAD_GRAYSCALE)
      self.imgray = cv.imread('Fig3.15(a)4.bmp',cv.IMREAD_GRAYSCALE)
      self.lowcontrast = cv.imread('Fig10.15(a).BMP',cv.IMREAD_GRAYSCALE)

    def log(self):
      kernel = np.array([[0,0,-1,0,0], [0,-1,-2,-1,0], [-1,-2,16,-2,-1],[0,-1,-2,-1,0],[0,0,-1,0,0]])
      log = cv.filter2D(self.imgray, -1, kernel)
      log = PIL.Image.fromarray(log)
      img = log.resize((230, 230))
      return ImageTk.PhotoImage(img)

    def laplasian(self):
      kernel = np.array([[-1,-1,-1], [-1,9,-1],[-1,-1,-1]])
      laplasian = cv.filter2D(self.imgray, -1, kernel)
      laplasian = PIL.Image.fromarray(laplasian)
      img = laplasian.resize((230, 230))
      return ImageTk.PhotoImage(img)

    def histogram(self):
      imforh = self.image
      h = cv.calcHist([imforh], [0], None, [256], [0,256])
      plt.plot(h,color = 'red')
      plt.savefig('histogram.jpg')
      img = PIL.Image.fromarray(cv.imread('histogram.jpg'))
      img= img.resize((230,230))
      #########  
      dst = cv.equalizeHist(imforh)
      h = cv.calcHist([dst], [0], None, [256], [0,256])
      dst = PIL.Image.fromarray(dst)
      dst = dst.resize((230,230))
      ##########     
      plt.clf()
      plt.plot(h,color = 'blue')
      plt.savefig('histogram2.jpg')
      img2 = PIL.Image.fromarray(cv.imread('histogram2.jpg'))
      img2 = img2.resize((230,230))
      os.remove('histogram2.jpg')
      os.remove('histogram.jpg')
      return ImageTk.PhotoImage(img),ImageTk.PhotoImage(dst),ImageTk.PhotoImage(img2)

    def lincontast(self):
      minVal,maxVal,a,b = cv.minMaxLoc(self.lowcontrast)
      max_type = 255 
      a = max_type / (maxVal - minVal)
      image_of_doubles = a*(self.lowcontrast - minVal)
      image_of_doubles = PIL.Image.fromarray(image_of_doubles)
      img = image_of_doubles.resize((230, 230))
      return ImageTk.PhotoImage(img)

    def getorigs(self):
      img1 = PIL.Image.fromarray(self.imgray)
      img1 = img1.resize((230, 230))
      img2 = PIL.Image.fromarray(self.lowcontrast)
      img2 = img2.resize((230, 230))
      img3 = PIL.Image.fromarray(self.image)
      img3 = img3.resize((230, 230))
      return ImageTk.PhotoImage(img1),ImageTk.PhotoImage(img2),ImageTk.PhotoImage(img3)

if __name__ == "__main__":
    root = Tk()
    ms = MainSolution()
    
    # Получаем обработанные изображения
    img_hist, img_hist_eq, img_hist_plot = ms.histogram()
    img_log = ms.log()
    img_lap = ms.laplasian()
    img_lin = ms.lincontast()
    img_orig1, img_orig2, img_orig3 = ms.getorigs()
    
    # Определяем размер окна и изображений
    window_width = 790
    window_height = 790
    image_size = 230
    padding = 25 # Отступ между изображениями
    root.geometry(f"{window_width}x{window_height}")
    
    # Создаем список изображений и их меток
    images = [img_orig1, img_lap, img_log, img_hist, img_orig2, img_orig3,img_hist_plot, img_hist_eq, img_lin]
    labels = ["Оригинал 1", "Лапласиан", "Лог", "Гистограмма", "Оригинал 2", "Оригинал 3", "Гистограмма экв.", "Эквализация", "Контраст"]

    # Размещаем изображения и метки в сетке
    for i, (img, label_text) in enumerate(zip(images, labels)):
        row = i // 3
        col = i % 3
        x = col * (image_size + padding) + padding
        y = row * (image_size + padding) + padding
        
        # Метка для изображения
        label = Label(root, text=label_text)
        label.place(x=x, y=y)
        
        # Создаем и размещаем виджет Label для изображения
        lbl_img = Label(root, image=img)
        lbl_img.image = img  # Сохраняем ссылку на изображение
        lbl_img.place(x=x, y=y + 20, width=image_size, height=image_size)

    root.mainloop()
