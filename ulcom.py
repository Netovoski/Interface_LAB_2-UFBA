# # ----------------------------------------------------------------------------------
# # A-17: Mdulo para uso no Python COM-Port LAB2
# # Dev: Pedreira Neto
# # Data: 13/09/2020
# # Referncias: uLab Eletrnica
# # https://github.com/NivaldoMattos/Curso-de-Python-com-Interface-Grafica
# # ----------------------------------------------------------------------------------
 
from asyncio.windows_events import NULL
#from curses import baudrate
from tkinter import *
from tkinter.ttk import LabelFrame
from turtle import width
import winsound
import ulwplace1
import serial 
# Port = "COM5"
# Baud = "256000"
comport = serial.Serial()
Port = "COMx"
Baud = "BAUD"
LED_BuiltInState = False


#terminadores para reconhecer os comandos enviados pelo python
RGB_TERMINATOR = 255
GET_TERMPERATURA_ON = 254
GET_TERMPERATURA_OFF = 253
LED_BUILTIN_ON = 252
LED_BUILTIN_OFF = 251


#Label = NULL
###############
# Classe para controle dos labels do beep
###############
class Message:
    def __init__(self, master):

        self.label_port = Label(master, text="COMx", font="Arial 10 bold", bg="black", fg="yellow")
        self.label_port.place(width=80, height=18, x=52, y=236)

        self.label_baud = Label(master, text="BAUDx", font="Arial 10 bold", bg="black", fg="yellow")
        self.label_baud.place(width=80, height=18, x=164, y=236)

        self.label_RGB = Label(master, text="---.---.---", font="Arial 20", fg="green", bg="black")
        self.label_RGB.place(width=194, height=33, x=571, y=112)

        self.label_temp = Label(master, text="--.--", font="Arial 20", fg="green", bg="black")
        self.label_temp.place(width=120, height=33, x=808, y=112)

        self.label_message = Label(master, text="Status2:", font="Arial 13", fg="yellow", bg="black")
        self.label_message.place(width=907, height=21, x=37, y=574)#rodape
        
    def port(self, color, port):
        global Port #memoriza o valor global
        Port = port
        self.label_port["fg"] = color
        self.label_port["text"] = port
    
    def baud(self, color, baud):
        global Baud
        Baud = baud
        self.label_baud["fg"] = color
        self.label_baud["text"] = baud+"Bps"

    def temper(self, temp):
        temp = temp[2:7] #string que chega formato, fatiamento
        self.label_temp["text"]= temp+"ºC"
    
    def rgb(self, r, g, b):
        self.label_RGB["text"] = str(r) + ',' + str(g) + ',' + str(b)

    def botton(self, message, color, beep): #vai ou não receber mensagem alerta sonora
        self.label_message["text"] = message
        self.label_message["fg"] = color
        if beep:
            frequency = 1200
            duration = 200
            winsound.Beep(frequency, duration)

###############
# Funções para os leds do arduino
###############      
class Leds:
    def __init__(self, master): #metodo construtor
        self.label_LED_RX = Label(master, bg="black")
        self.label_LED_RX.place(width=10, height=7, x =606, y=354)
        
        self.label_LED_TX = Label(master, bg="black")
        self.label_LED_TX.place(width=9, height=6, x=606, y=381)

        self.label_LED_BUILT_IN = Label(master, bg="black") #led embutido da placa arduino
        self.label_LED_BUILT_IN.place(width=9, height=6, x=606, y =406)


        self.label_LED_RGB = Button(master, bg="black")
        self.label_LED_RGB.place(width=19, height=12, x=654, y=251)

    def LED_L(self, state):#led que mostra L na placa do arduino
        global LED_BuiltInState# recebe o estado do LED
        if state:
            self.label_LED_BUILT_IN["background"] = "light green"
            
        else:
            self.label_LED_BUILT_IN["background"] = "black"
        LED_BuiltInState = state

    def LED_TX(self, state):
        if state:
            self.label_LED_TX["background"] = "red"
        else:
            self.label_LED_TX["background"] = "black"
        

    def LED_RX(self, state):
        if state:
            self.label_LED_RX["background"] = "white"
        else:
            self.label_LED_RX["background"] = "black"
    
    def LED_RGB(self, color):
        self.label_LED_RGB["background"] = color


###############
# Funções para acessa porta serial
###############

def open():
    global comport, Baud, Port
    if not comport.is_open:
        try:
            comport = serial.Serial(port=Port, baudrate= Baud)
        except:
            comport.close()
            comport.open()


def close():
    global comport
    comport.close

def is_open():# verifica porta está aberta
    global comport
    return comport.is_open

def write_byte(byte):#escreve na porta
    if comport.is_open:
        comport.write((byte,))

def read_line(): #ler porta serial
    return comport.readline()

def reset_input_buffer(): #limpar o buffer
    if comport.is_open:
        comport.reset_input_buffer()

