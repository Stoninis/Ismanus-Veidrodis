from bs4 import BeautifulSoup
from tkinter import *
import requests
import serial
import time

#Puslapis, is kurio traukiama informacija ir mano narsykles agentas
nuoroda = "https://www.accuweather.com/en/lt/silute/228452/current-weather/228452"
agentas = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

res = [1920, 1080] # ekrano raiska

# Kintamieji elementu formatavimui
LangasSpalva = "black"
LangasVisas = True #ar langas uzima visa ekrana

LaikoFormatas = "%H:%M:%S" #"%H:%M:%S"
LaikoVieta = [res[0]/4, res[1]/4]
LaikrodisSpalva = ["white", "black"] #indeksas 0 - fg| 1 - bg
LaikrodisDydis = 44
LaikrodisSriftas = "Courier"

tempDabarVieta = [res[0]/4, res[1]/4+50]
tempDabarSpalva = ["white", "black"] #indeksas 0 - fg| 1 - bg
tempDabarDydis = 12
tempDabarSriftas = "Courier"

veikimoAtstumas = 50 # kokiu atstumu isijungia veidrodis (cm)
atnaujinimas = 500 # po kiek ms is naujo pradedama funkcija

#USB sukurimas, parametrai
usb = serial.Serial() 
usb.baudrate = 9600
usb.port = "COM5"
usb.open()

# Lango sukurimas
langas = Tk()
langas.attributes('-fullscreen', LangasVisas)
langas.configure(bg = LangasSpalva)

# Laikrodzio teksto sukurimas
laikrodis = Label(fg = LaikrodisSpalva[0], bg = LaikrodisSpalva[1])
laikrodis.place( x = LaikoVieta[0] , y = LaikoVieta[1], anchor = "center")
laikrodis.configure(font=(LaikrodisSriftas, LaikrodisDydis))

# Dabartines temperaturos teksto sukurimas
tempDabar = Label(fg = tempDabarSpalva[0], bg = tempDabarSpalva[1])
tempDabar.place( x = tempDabarVieta[0] , y = tempDabarVieta[1], anchor = "center")
tempDabar.configure(font=(tempDabarSriftas, tempDabarDydis))

def tempDabarYra():
    #dabartines temperaturos gavimas
    atsakymas = requests.get(nuoroda, headers=agentas) 
    soup = BeautifulSoup(atsakymas.content, "html.parser")
    temptemp = soup.find(class_ = "display-temp").get_text()
    tempDabar.configure(text = "Šiluma Šilutėje dabar: " + temptemp)

def ekranas():
    serialIn = int(usb.readline().decode("utf-8")) #nuskaitom atstumo is arduino #bitai is arduino verciami i sveikuosius skaicius
    if serialIn <= veikimoAtstumas: #jei atstumas iki jutiklio didesnis nei vaikmoAtstumas
        laikrodis.configure(text = time.strftime(LaikoFormatas, time.localtime()))
        tempDabarYra()
                
    elif serialIn > veikimoAtstumas: #jei atstumas iki jutiklio didesnis nei vaikmoAtstumas
        laikrodis.configure(text = " ")
        tempDabar.configure(text = " ")
    
    langas.after(atnaujinimas, ekranas)

ekranas()

langas.mainloop()
