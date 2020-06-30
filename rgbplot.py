import cv2
import numpy as np
import matplotlib.pyplot as plt

rowNum = 0

#img 1 (left)

img1 = cv2.imread(r"C:\Users\sarah\OneDrive - Rutgers University\aresty\solar forecasting - summer science 2020\june29\20200607_170050.jpg")

rows, cols, channels = img1.shape
#print(rows)
#print(cols)

red1 = []
green1 = []
blue1 = []

for i in range(cols):
    pixel = img1[int(rowNum), i]
    red1.append(pixel[2])
    green1.append(pixel[1])
    blue1.append(pixel[0])

#img 2 (right) - assumes same dimensions

img2 = cv2.imread(r"C:\Users\sarah\OneDrive - Rutgers University\aresty\solar forecasting - summer science 2020\june29\20200607_170055.jpg")

red2 = []
green2 = []
blue2 = []

for i in range(cols):
    pixel2 = img2[int(rowNum), i]
    red2.append(pixel2[2])
    green2.append(pixel2[1])
    blue2.append(pixel2[0])


plt.figure(1)
plt.ylim(0, 255)
plt.title("RGB Plot (Red): Row " + str(rowNum), fontdict=None, loc='center')
plt.plot(range(0,cols), red1, linewidth=1, label='Left')
plt.plot(range(0,cols), red2, linewidth=1, label='Right')
plt.legend()

plt.figure(2)
plt.ylim(0, 255)
plt.title("RGB Plot (Green): Row " + str(rowNum), fontdict=None, loc='center')
plt.plot(range(0,cols), green1, linewidth=1, label='Left')
plt.plot(range(0,cols), green2, linewidth=1, label='Right')
plt.legend()


plt.figure(3)
plt.ylim(0, 255)
plt.title("RGB Plot (Blue): Row " + str(rowNum), fontdict=None, loc='center')
plt.plot(range(0,cols), blue1, linewidth=1, label='Left')
plt.plot(range(0,cols), blue2, linewidth=1, label='Right')
plt.legend()

plt.show()
