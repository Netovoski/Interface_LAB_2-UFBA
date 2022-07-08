# DEV: Pedreira Neto
# Data: 17/05/2022
# Referencias: uLab Eletronica
# ARQUIVO PRINCIPAL COM-port
#

# -----------------------------------------------------------------------------------
# Importações
# -----------------------------------------------------------------------------------
from tkinter import *
import ulcom
import ulwplace1
import threading
import serial.tools.list_ports
from time import sleep
from tkinter import colorchooser




Master = Tk()
# def constante ON/OFF

ON = True
OFF = False
GetTemperatureFlag = False
SearchingPorts = True



# -----------------------------------------------------------------------------------
# Funções
# -----------------------------------------------------------------------------------

def ask_to_open_port():
    message.botton("Favor, abra a porta serial", "yellow", beep=True)

def send_byte(byte):
    if ulcom.is_open():
        ulcom.write_byte(byte)
        LEDs.LED_TX(ON)
    else:
        ask_to_open_port()

def send_rgb(r, g, b):
    if r > 250:
        r = 250
    if g > 250:
        g = 250
    if b > 250:
        b = 250

    if ulcom.is_open:
        LEDs.LED_TX(ON)
        DadosTx = [int(b), int(g), int(r), ulcom.RGB_TERMINATOR]
        for idx in range(0, len(DadosTx)):
            ulcom.write_byte(DadosTx[idx])
        else:
            ask_to_open_port()



def f_receiving_serial():
    while True:
        sleep(0.3)
        if ulcom.is_open():
            ulcom.reset_input_buffer()
            LEDs.LED_RX(OFF)
            try:
                serial_data = ulcom.read_line()
                message.temper(str(serial_data))
            except IOError:
                message.temper("Erro")
                LEDs.LED_RX(ON)



    
def f_searching_ports():#processo flag
    global SearchingPorts 
    while True:
        sleep(0.3)
        LEDs.LED_TX(OFF)
        if SearchingPorts:
            message.botton('Aguardando, busca COM ports...', "red", beep=False)
            ports = serial.tools.list_ports.comports(include_links=False)
            port_list.delete('0','end')
            idx = 0
            for port in sorted(ports):
                port_list.insert(idx, port.device)
                idx = idx + 1
            port_list["height"] = idx
            SearchingPorts = False
            message.botton('Escolha a porta e COM/BAUD par,'
                            'F6 para conectar...',
                            "yellow",
                            beep= False)
def f1():
    print("F1")
    # message.botton("Obrigado Teste","yellow", beep=False)
    # LEDs.LED_RX(ON)
    if ulcom.is_open():
        message.botton("Selecionar Cor", "yellow", beep=False)
        color= colorchooser.askcolor(title="Select Color")
        if color[1] is not None:
            rgb = color[0]
            print(color)
            send_rgb(rgb[0], rgb[1], rgb[2])
            message.rgb(int(rgb[0]), int(rgb[1]), int(rgb[2]))
            LEDs.LED_RGB(color[1])
        else:
            ask_to_open_port()

def f2():
    print("f2")
    # message.botton("Obrigado ","yellow", beep=False)
    # message.port("yellow", "COM1")
    # message.baud("yellow", "19200")
    # LEDs.LED_TX(ON)
    if ulcom.is_open():
        send_rgb(0,0,0)
        message.botton('Limpar RGB LED...', "yellow", beep=False)
        message.rgb(0,0,0)
        LEDs.LED_RGB("black")
    else:
        ask_to_open_port()
def f3():
    print("f3")
    # message.rgb(128, 64, 92)
    # LEDs.LED_L(ON)
    if ulcom.is_open():
        if ulcom.LED_BuiltInState:
            LEDs.LED_L(OFF)
            send_byte(ulcom.LED_BUILTIN_OFF)
            message.botton("LED_BUILTIN_OFF ", "yellow", beep=False)
        else:
            LEDs.LED_L(ON)
            send_byte(ulcom.LED_BUILTIN_OFF)
            message.botton("LED_BUILTIN_ON","yellow", beep=False)
    else:
        ask_to_open_port()
        
def f4():
    print("f4")
    # message.botton("Boa noite","yellow", beep=False)
    # LEDs.LED_RGB("blue")
    global GetTemperatureFlag
    if ulcom.is_open():
        if GetTemperatureFlag:
            send_byte(ulcom.GET_TERMPERATURA_ON)
            message.botton("Get_Temperature_on", "yellow", beep=False)
            GetTemperatureFlag = Flag
        else:
            send_byte(ulcom.GET_TERMPERATURA_OFF)
            message.botton("GET_TEMPERATURE OFF", "yellow", beep = False)
            GetTemperatureFlag= True
    else:
        ask_to_open_port()

def f5():
    # print("f5")
    # message.botton("ateé","white", beep=True)
    # LEDs.LED_RX(OFF)
    global SearchingPorts
    SearchingPorts = True

def f6():
    print("f6")
    # LEDs.LED_RX(OFF)
    # LEDs.LED_L(OFF)
    # LEDs.LED_TX(OFF)
    # LEDs.LED_RGB("black")
    # message.botton('TODOS OS LEDs OFF', "white", beep= True)
    global GetTemperatureFlag
    if ulcom.Port == 'COMx' or ulcom.Baud == '0':
        
        message.botton('Escolha a porta e COM/BAUD par',
                                'F6 para conectar...',
                                "yellow",
                                beep= False)    
        return None
    if not ulcom.os_open():
        
        message.botton(message= 'Connected!', color='green', beep=False)
        bt_f6 ["imagem "] = btf6_close_img
        GetTemperatureFlag = True
        if not receiving_serial.is_alive():
            receiving_serial.start()
    else:
        ulcom.close()
        message.botton('Unconnected', "red", beep=False)
        bt_f6["imagem"]=btf6_open_img



#############################    
#widgets
#############################


back_img = PhotoImage(file="images/bg_inicial1.png")
btf1_img = PhotoImage(file="images/btf1.png")
btf2_img = PhotoImage(file="images/btf2.png")
btf3_img = PhotoImage(file="images/btf3.png")
btf4_img = PhotoImage(file="images/btf4.png")
btf5_img = PhotoImage(file="images/btf5.png")
btf6_close_img = PhotoImage(file="images/btf6_close.png")
btf6_open_img = PhotoImage(file="images/btf6_open.png")

label_fundo = Label(Master, image=back_img)
label_fundo.place(x=0, y=0)

bt_f1 = Button(Master, image=btf1_img, bd=0, command=f1)
bt_f1.place(width=121, height=70, x=23, y=80)

bt_f2 = Button(Master, image=btf2_img, bd=0, command=f2)
bt_f2.place(width=121, height=70, x=151, y=80)

bt_f3 = Button(Master, image=btf3_img, bd=0, command=f3)
bt_f3.place(width=121, height=70, x=279, y=80)

bt_f4 = Button(Master, image=btf4_img, bd=0, command=f4)
bt_f4.place(width=121, height=70, x=407, y=80)

bt_f5 = Button(Master, image=btf5_img, bd=0, command=f5)
bt_f5.place(width=94, height=50, x=45, y=484)

bt_f6 = Button(Master, image=btf6_open_img, bd=0, command=f6)
bt_f6.place(width=94, height=50, x=158, y=484)

port_list = Listbox(Master, height=1, width=7, bd=10, font="Arial 10", bg="black",
                    fg="#008000",
                    highlightcolor="black",
                    highlightthickness=0,
                    selectbackground="black",
                    )

port_list.place(width=83, height=175, x=51, y=285)
port_list.insert(END, "COM5")
port_list.bind('<Double-Button>', lambda e: message.port("green", port_list.get(ANCHOR)))

baud_list = Listbox(Master, height=1, width=7, bd=10, font="Arial 10", bg="black",
                    fg="#008000",
                    highlightcolor="black",
                    highlightthickness=0,
                    selectbackground="black",
                    )

baud_list.place(width=82, height=175, x=163, y=285)
baud_list.insert(END, "9600", "19200", "38400", "57200", "128000", "256000")
baud_list.bind('<Double-Button>', lambda e: message.baud("green", baud_list.get(ANCHOR)))

# Threads para a busca das p ortas
searching_ports = threading.Thread(target=f_searching_ports)
searching_ports.daemon = True
searching_ports.start()

# Thread para a recepcao serial
receiving_serial = threading.Thread(target=f_receiving_serial)
receiving_serial.daemon = True

# # Comandos do mouse para o posicionador de Widgets
# # ativamento botoes
#Master.bind('<Button-1>', lambda e: ulwplace1.m_btn1(e, Master))
#Master.bind('<Button-3>', lambda e: ulwplace1.m_btn3(e, Master))
#Master.bind('<ButtonRelease-1>', lambda e: ulwplace1.m_btn1_release(e, Master))

message = ulcom.Message(Master)

LEDs = ulcom.Leds(Master)

# Configuraes da tela Master
Master.title("Python COM-Port Explorer")
Master.iconbitmap(default='images/ulab.ico')
Master.resizable(width=FALSE, height=FALSE)#bloqueia o redimensionamento tela
Master.geometry("986x615+5+5")
#Master.geometry("986x615+-995+3")
Master.mainloop()
# ----------------------------------------------------------------------------------
#  EOF
# ----------------------------------------------------------------------------------


# back_img = PhotoImage(file = 'imagens/bg_inicial.png')
# btf1_img = PhotoImage(file = 'imagens/btf1.png')
# btf2_img = PhotoImage(file = 'imagens/btf2.png')
# btf3_img = PhotoImage(file = 'imagens/btf3.png')
# btf4_img = PhotoImage(file = 'imagens/btf4.png')
# btf5_img = PhotoImage(file = 'imagens/btf5.png')
# btf6_close_img = PhotoImage(file = 'imagens/btf6_close.png')
# btf6_open_img = PhotoImage(file = 'imagens/btf6_open.png')



# label_fundo = Label(Master, image=back_img)
# label_fundo.place(x=0, y=0)

# bt_f1 = Button(Master, image=btf1_img, bd=0, command=f1)
# bt_f1.place(width=121, height=70, x=23, y=80)

# bt_f2 = Button(Master, image=btf2_img, bd=0, command=f2)
# bt_f2.place(width=121, height=70, x=151, y=80)

# bt_f3 = Button(Master, image=btf3_img, bd=0, command=f3)
# bt_f3.place(width=121, height=70, x=279, y=80)

# bt_f4 = Button(Master, image=btf4_img, bd=0, command=f4)
# bt_f4.place(width=121, height=70, x=407, y=80)

# bt_f5 = Button(Master, image=btf5_img, bd=0, command=f5)
# bt_f5.place(width=94, height=50, x=45, y=484)

# bt_f6 = Button(Master, image=btf6_open_img, bd=0, command=f6)
# bt_f6.place(width=94, height=50, x=158, y=484)

# port_list = Listbox(Master, height=1, width=7, bd =10, font="Arial 10", bg= "black",
#                     fg ="#008000",
#                     highlightcolor="black",
#                     highlightthickness= "8", #espessura
#                     selectbackground="black",
#                     )#height tamanho quantidade linhas windht comprimento quantidade letras

# port_list.place(width=83, height=175, x=51, y=285)
# port_list.insert(END, "COM5")
# port_list.bind('<Double-Button>', lambda e: message.port("green", port_list.get(ANCHOR)))#ANCHOR Listar porta

# baud_list = Listbox(Master, height=1, width=7, bd=10, font= "Arial 10", bg = "black",
#                     fg= "#008000",
#                     highlightcolor="black",
#                     highlightthickness= "8", #espessura
#                     selectbackground="black",
#                     )
# baud_list.place(width=82, height=175, x=163, y=285)

# baud_list.insert(END, "9600", "19200", "38400", "57200", "128000", "256000")
# baud_list.bind('<Double-Button>', lambda e: message.baud("green", baud_list.get(ANCHOR)))




# #Threads para buscar portas de conexão

# searching_ports = threading.Thread(target= f_searching_ports)#chama e verifica as portas
# searching_ports.daemon =True
# searching_ports.start()


# #thread para recepcao serial

# receiving_serial = threading.Thread(target=f_receveing_serial)
# receiving_serial.daemon = True







# # Master.bind('<Button-1>', lambda e: ulwplace1.m_btn1(e, Master))
# # Master.bind('<Button-3>', lambda e: ulwplace1.m_btn3(e, Master))
# # Master.bind('<ButtonRelease-1>', lambda e: ulwplace1.m_btn1_release(e, Master))

# message = ulcom.Message(Master)

# LEDs = ulcom.Leds(Master)

# #configuracoes de tela master
# Master.title("Python COM-port LAB2")
# Master.iconbitmap(default='imagens/favicon.ico')
# #Master.resizable(width=False, height=False)
# Master.geometry("986x612+1454+4")
# Master.resizable(width=False, height=False) #bloqueia o redimensionamento tela
# Master.mainloop()

