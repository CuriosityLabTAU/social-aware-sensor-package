import pyscreenshot as ImageGrab
import numpy as np
import cv2
import threading

while(True):
    img = ImageGrab.grab() #bbox specifies specific region (bbox= x,y,width,height)
    img.save('fixed.png')
    threading._sleep(0.5)
    # img_np = np.array(img)
    # frame = cv2.cvtColor(img_np)
    # cv2.imshow("test", frame)
    # cv2.waitKey(0)
cv2.destroyAllWindows()