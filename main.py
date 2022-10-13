from tkinter import *
import cv2
import numpy as np
import imutils
import easyocr

def click():
    vvod1 = format(txt1.get())
    img = PhotoImage(file=vvod1)
    img = img.subsample(3, 3)

    imglb.PhotoImage = img
    imglb['image'] = img
    imglb.place(relx=.6, rely=.0, anchor="n")

def click3():
    txt1.delete(0, END)
    txt2.delete(0, END)
    imglb['image']=''


def click2():
    vvod2 = format(txt1.get())
    img = cv2.imread(vvod2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_filter = cv2.bilateralFilter(gray, 11, 15, 15)
    edges = cv2.Canny(img_filter, 30, 200)

    cont = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont = imutils.grab_contours(cont)
    cont = sorted(cont, key=cv2.contourArea, reverse=True)[:8]

    pos = None
    for c in cont:
        approx = cv2.approxPolyDP(c, 10, True)
        if len(approx) == 4:
            pos = approx
            break

    mask = np.zeros(gray.shape, np.uint8)
    new_img = cv2.drawContours(mask, [pos], 0, 255, 1)
    bitw_img = cv2.bitwise_and(img, img, mask=mask)

    x, y = np.where(mask == 255)
    x1, y1 = np.min(x), np.min(y)
    x2, y2 = np.max(x), np.max(y)
    crop = gray[x1:x2, y1:y2]

    text = easyocr.Reader(['en'])
    text = text.readtext(crop)

    res = text[0][-2]
    txt2.insert(0, str(res))




window = Tk()
window.title("Автознак")
window.geometry('700x300')







txt1 = Entry(window, width=15)
txt1.place(relx=.1, rely=.2, anchor="n")

txt2 = Entry(window, width=15)
txt2.place(relx=.1, rely=.7, anchor="n")

lbl1 = Label(window, text="Результат:", font=("Arial Bold", 9))
lbl1.place(relx=.1, rely=.6, anchor="n")

lbl2 = Label(window, text="Введите путь \n к изображению", font=("Arial Bold", 9))
lbl2.place(relx=.1, rely=.0, anchor="n")

imglb = Label(window)

btn = Button(window, text="Вывод \n изображения",command=click)
btn.place(relx=.1, rely=.3, anchor="n")

btn2 = Button(window, text="Вывод текста",command=click2)
btn2.place(relx=.1, rely=.5, anchor="n")

btn3 = Button(window, text="Очистка",command=click3)
btn3.place(relx=.1, rely=.8, anchor="n")



window.mainloop()