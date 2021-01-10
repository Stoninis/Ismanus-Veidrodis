from bs4 import BeautifulSoup
from tkinter import *
import requests
import serial
import time
import PIL
from PIL import Image, ImageTk

# narsykle
#Puslapis, is kurio traukiama informacija ir mano narsykles agentas
nuoroda = "https://www.accuweather.com/lt/lt/silute/228452/current-weather/228452"
agentas = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
atsakymas = requests.get(nuoroda, headers=agentas) 
soup = BeautifulSoup(atsakymas.content, "html.parser")

# Kintamieji
res = [1920, 1080] # ekrano raiska
veikimoAtstumas = 50 # kokiu atstumu isijungia veidrodis (cm)
atnaujinimas = 500 # po kiek ms is naujo pradedama funkcija

# Kintamieji elementu formatavimui
LangasSpalva = "black"
LangasVisas = True #ar langas uzima visa ekrana

LaikoFormatas = "%H:%M:%S" #"%H:%M:%S"
LaikoVieta = [res[0]/20, res[1]/10]
LaikrodisSpalva = ["white", "black"] #indeksas 0 - fg| 1 - bg
LaikrodisDydis = 44
LaikrodisSriftas = "calibri light"

tempIrOrasDabarVieta = [res[0]*0.86, res[1]*0.1+130]
tempIrOrasDabarSpalva = ["white", "black"] #indeksas 0 - fg| 1 - bg
tempIrOrasDabarDydis = 15
tempIrOrasDabarSriftas = "calibri light"

pavVieta = [ res[0]*0.87, res[1]*0.1]
pavBG = "black"

# USB sukurimas, parametrai
usb = serial.Serial() 
usb.baudrate = 9600
usb.port = "COM5"
usb.open()

# Labels
# Lango sukurimas
langas = Tk()
langas.attributes('-fullscreen', LangasVisas)
langas.configure(bg = LangasSpalva)

# Laikrodzio teksto sukurimas
laikrodis = Label(fg = LaikrodisSpalva[0], bg = LaikrodisSpalva[1])
laikrodis.place( x = LaikoVieta[0] , y = LaikoVieta[1], anchor = "nw")
laikrodis.configure(font=(LaikrodisSriftas, LaikrodisDydis))

# Dabartines temperaturos ir oroteksto sukurimas
tempIrOrasDabar = Label(fg = tempIrOrasDabarSpalva[0], bg = tempIrOrasDabarSpalva[1])
tempIrOrasDabar.place( x = tempIrOrasDabarVieta[0] , y = tempIrOrasDabarVieta[1], anchor = "center")
tempIrOrasDabar.configure(font=(tempIrOrasDabarSriftas, tempIrOrasDabarDydis))

#paveikslelis
img = ImageTk.PhotoImage(Image.open("C:\\Users\\Stoninis\\Desktop\\Oras ir Laikas\\oras clipart\\empty.png"))
panel = Label(image = img, bg = pavBG)
panel.place( x = pavVieta[0], y = pavVieta[1], anchor = "n")

# funkcijos    
def tempIrOrasDabarYra():
    pranesimas = soup.find(class_ = "phrase").get_text() + " " + soup.find(class_ = "display-temp").get_text()
    tempIrOrasDabar.configure(text = pranesimas)

def ikeltiPNG():
    img = ImageTk.PhotoImage(Image.open("C:\\Users\\Stoninis\\Desktop\\Oras ir Laikas\\oras clipart\\"+soup.find(class_ = "phrase").get_text()+".png"))
    panel.configure(image = img)
    panel.image = img


def visiIjungti():
    laikrodis.configure(text = time.strftime(LaikoFormatas, time.localtime()))
    tempIrOrasDabarYra()
    ikeltiPNG()

def visiTusti():
    laikrodis.configure(text = " ")
    tempIrOrasDabar.configure(text = " ")

    img = ImageTk.PhotoImage(Image.open("C:\\Users\\Stoninis\\Desktop\\Oras ir Laikas\\oras clipart\\empty.png"))
    panel.configure(image = img)
    panel.image = img

def ekranas():
    serialIn = int(usb.readline().decode("utf-8")) #nuskaitom atstumo is arduino #bitai is arduino verciami i sveikuosius skaicius

    if serialIn <= veikimoAtstumas: #jei atstumas iki jutiklio didesnis nei vaikmoAtstumas
       visiIjungti()
        
    elif serialIn > veikimoAtstumas: #jei atstumas iki jutiklio didesnis nei vaikmoAtstumas
        visiTusti()
        
    langas.after(atnaujinimas, ekranas)

ekranas()
langas.mainloop()
