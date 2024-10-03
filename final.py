from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from math import log10, sqrt

import cv2
from PIL import Image,ImageTk
import numpy as np

root = Tk()
root.title('IMAGE REGENERATION FOR OLD DAMAGED REEL PICTURES')
root.geometry('1920x1080')
style = Style()


def Input_Image():
    global img
    inputimage =  filedialog.askopenfilename(parent=root,initialdir = "/",title = "choose your file",filetypes = (("all files",".*"),("png files",".png")))
    file_path = inputimage

    img = cv2.imread(inputimage)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(img,(350,300))
   
    image = Image.fromarray(resized_image)
    image = ImageTk.PhotoImage(image)
    panelA = Label(image=image)
    panelA.image = image
    panelA.place(x=40 ,y=120)
   
def preprocessing_image():
    global mask
    maskedimage =  filedialog.askopenfilename(parent=root,initialdir = "/",title = "choose your file",filetypes = (("all files",".*"),("png files",".png")))
    maskedimg = cv2.imread(maskedimage,0)
    ret, thresh = cv2.threshold(maskedimg,254, 255, cv2.THRESH_BINARY)
    kernel = np.ones((7,7), np.uint8)
    mask = cv2.dilate(thresh, kernel, iterations = 1)
    mask1 = cv2.resize(mask,(350,300))

    image = Image.fromarray(mask1)
    image = ImageTk.PhotoImage(image)
    panelA = Label(image=image)
    panelA.image = image
    panelA.place(x=590 ,y=120)
   

def segment_image():
    global img
    global mask
    
    global res_red
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    Z = hsv.reshape((-1,3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 4
    ret,label,center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    khsv   = center[label.flatten()]
    khsv   = khsv.reshape((img.shape))
    res_red = cv2.bitwise_and(img,img, mask=mask)
    res_red = cv2.resize(res_red,(350,300))
 
    image = Image.fromarray(res_red)
    image = ImageTk.PhotoImage(image)
    panelA = Label(image=image)
    panelA.image = image
    panelA.place(x=590 ,y=120)

def regeneration_image():
    global img
    global mask
    global restoredd

    #restored = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    restoredd = cv2.inpaint(img,mask,3,cv2.INPAINT_NS)
    restored = cv2.resize(restoredd,(350,300))
    image = Image.fromarray(restored)
    image = ImageTk.PhotoImage(image)
    panelA = Label(image=image)
    panelA.image = image
    panelA.place(x=1140 ,y=120)

def download_image():
    global restoredd
    restoredimg = cv2.cvtColor(restoredd, cv2.COLOR_BGR2RGB)
    cv2.imwrite('D:/project/output.jpg',restoredimg)
    messagebox.showinfo("info","Image Downloaded Succesfully",)

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def measures():
    global img
    global restoredd
    value = PSNR(img,restoredd)
    val=round(value,2)
    vall=str(val)
    print(value)
    e1.delete(0, 'end')
    e1.insert(5,vall)


Label(root, text = 'IMAGE REGENERATION FOR OLD DAMAGED REEL PICTURES',foreground="red", font =('Verdana', 25)).pack(side = TOP, pady = 10)
 
v = Canvas(root, width=500, height=600)
label = Label(root, text ="INPUT IMAGE",foreground="red", font =('Verdana', 12))
label.place(x=160 ,y=90)
v.place(x=30 ,y=120)
v.create_rectangle(10, 10, 350, 300,outline='grey', fill="lightgray")

w = Canvas(root, width=500, height=600)
label = Label(root, text ="PREPROCESSING & SEGMENTATION",foreground="red", font =('Verdana', 12))
label.place(x=620 ,y=90)
w.place(x=590 ,y=120)
w.create_rectangle(10, 10, 350, 300,outline='grey', fill="lightgray")


x = Canvas(root, width=500, height=600)
label = Label(root, text ="REGENERATION",foreground="red", font =('Verdana', 12))
label.place(x=1250 ,y=90)
x.place(x=1140 ,y=120)
x.create_rectangle(10, 10, 350, 300,outline='grey', fill="lightgray")


y = Canvas(root, width=1460, height=600)
label = Label(root, text ="OUTPUT",foreground="red", font =('Verdana', 12))
label.place(x=730 ,y=520)
y.place(x=30 ,y=550)
y.create_rectangle(10, 10,1460, 200,outline='black',fill="lightgray",width=1)


style.configure('W.TButton',font =('Verdana', 12),foreground = 'red',background='lightgray')

b1=Button(root, text ="INPUT IMAGE",style='W.TButton',command = Input_Image)
b1.place(height=80, width=200,x=90 ,y=620)

b2=Button(root, text ="PREPROCESSING",style='W.TButton',command = preprocessing_image)
b2.place(height=80, width=233,x=330 ,y=620)

b3=Button(root, text ="SEGMENTATION",style='W.TButton',command = segment_image)
b3.place(height=80, width=233,x=570 ,y=620)

b4=Button(root, text ="REGENERATION",style='W.TButton',command = regeneration_image)
b4.place(height=80, width=200,x=810 ,y=620)

b5=Button(root, text ="DOWNLOAD IMAGE",style='W.TButton',command = download_image)
b5.place(height=80, width=200,x=1050 ,y=620)

b6=Button(root, text ="PSNR",style='W.TButton',command = measures)
b6.place(height=40, width=100,x=1290 ,y=620)
e1=Entry(root,font=('Verdana',12,'bold'),foreground='RED',justify=CENTER)
e1.place(height=40,width=100,x=1290,y=665)

mainloop()
