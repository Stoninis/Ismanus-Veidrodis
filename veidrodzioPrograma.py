from tkinter import *
import serial
import time

# Kintamieji elementu formatavimui
LangasSpalva = "black"
LangasVisas = True #ar langas uzima visa ekrana

LaikoFormatas = "%H:%M:%S"
res = [1920, 1080] # ekrano raiska
LaikoVieta = [res[0]/4, res[1]/4]

veikimoAtstumas = 50 # kokiu atstumu isijungia veidrodis (cm)
serialIn = 0 # informacija is arduino 

#USB sukurimas, parametrai
usb = serial.Serial() 
usb.baudrate = 9600
usb.port = "COM5"
usb.open()

langas = Tk()
langas.attributes('-fullscreen', LangasVisas)
langas.configure(bg = LangasSpalva)

tekstas = Label(fg = "white", bg = "black")
tekstas.place( x = LaikoVieta[0] , y = LaikoVieta[1], anchor = "center")
tekstas.configure(font=("Courier", 44))

def ekranas():
    serialIn = int(usb.readline().decode("utf-8")) #nuskaitom atstumo is arduino #bitai is arduino verciami i sveikuosius skaicius
    if serialIn <= 50: #jei atstumas iki jutiklio mazesnis nei vaikmoAtstumas
        tekstas.configure(text = time.strftime(LaikoFormatas, time.localtime()))
        langas.after(1000, ekranas)
    elif serialIn > 50: #jei atstumas iki jutiklio didesnis nei vaikmoAtstumas
        tekstas.configure(text = " ")
        langas.after(1000, ekranas)

langas.after(1000, ekranas)

langas.mainloop()