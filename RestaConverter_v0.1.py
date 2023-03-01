import tkinter as tk
from tkinter import filedialog
import numpy as np
import math
dxf = ''
def opnfl():
    global dxf
    with open(filedialog.askopenfilename(), 'r') as dxf:
        dxf = dxf.read() #Сохраняем файл в переменную в формате str
def trnsltFl():
    global dxf
    dxf = dxf[(dxf.find('ENTITIES')):] #Ищем точку начала нужных нам полилиний и обрезаем до этого момента
    dxf = dxf[:(dxf.find('ENDSEC'))] #Ищем точку конца секции полилиний и обрезаем все после.
    dxf = dxf.split('\n')#Создаем лист  с разделителем по новой строке.
    dxf2 = []
    for i in range(0, len(dxf)):
        dxf[i] = dxf[i].lstrip()
        dxf[i] = dxf[i].rstrip()
        dxf2.append(dxf[i])
    dxf = dxf2 #Убираем все пробелы в начале каждой строки и в конце нее.
    dxf2 = []
    for i in range(0, len(dxf)):
        if dxf[i] == '90' and dxf[i+1] == '10':
            pass
        elif dxf[i] == '10' and dxf[i-1] == '90':
            pass
        else:
            dxf2.append(dxf[i])
    dxf = dxf2
    dxf2 = []
    ##########################################################
    def MidArcPoint(a,b,c,d,e):
        p1 = [a,b]
        p1 = np.array(p1)
        p2 = [c,d]
        p2 = np.array(p2)
        b = e
        def sign(b):
            if b == 0:
             b = 0
            elif b < 0:
                b = -1
            else:
                b = 1
            return b
        m = (p1+p2)/2
        p1p2 = p2-p1
        p1m = ((p1p2*0.5)*(-1))
        d2 = ((math.pow(p1m[0],2))+(math.pow(p1m[1],2))) ** 0.5
        d1 = d2 * math.fabs(b)
        Teta = sign(b)*(math.pi/2)
        CosTeta = math.cos(Teta)
        MQx_ = p1m[0]*CosTeta-p1m[1]*math.sin(Teta)
        MQy_ = p1m[0]*math.sin(Teta)+p1m[1]*CosTeta
        MQ_star = np.array([MQx_,MQy_])
        MQ_L = (MQ_star[0]**2 + MQ_star[1]**2) ** 0.5
        MQn = MQ_star / MQ_L
        MQ = d1 * MQn
        M_star = p1 + p2
        M_ = M_star * 0.5
        Q = M_ + MQ
        return f' X{round(float(Q[0]),2)} Y{round(float(Q[1]),2)}'
    ##########################################################
    for i in range(0,len(dxf)):
        if (dxf[i]).isalnum() == True and dxf[i] != '20' and dxf[i] != '10' and dxf[i] != '42':
            dxf2.append(';' + dxf[i])
        else:
            dxf2.append(dxf[i])
    dxf = dxf2
    dxf2 = []
    ##########################################################
    for i in range(0,len(dxf)):
        if dxf[i-2] == ';43':
            dxf2.append(f'T2 X{round(float(dxf[i+1]),2)} Y{round(float(dxf[i+3]),2)}')
        if dxf[i] == '10' and dxf[i+4] != '42' and dxf[i-2] != ';43' and dxf[i-2] != '42':
            dxf2.append(f'T0 X{round(float(dxf[i+1]),2)} Y{round(float(dxf[i+3]),2)}')
        if dxf[i] == '42':
            dxf2.append(f'T4{str(MidArcPoint(float(dxf[i-3]),float(dxf[i-1]),float(dxf[i+3]),float(dxf[i+5]),float(dxf[i+1])))} X{round(float(dxf[i+3]),2)} Y{round(float(dxf[i+5]),2)}')
    ##########################################################
    dxf2.append('T8')
    dxf = '\n'.join(dxf2)
    dxf = dxf.replace('.0 ',' ')
    dxf = dxf.replace('.0\n','\n')
    ##########################################################
    print(dxf)
#######################################################################################################################
def SaveAs_():
    global dxf
    W = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    W.write(dxf)
    W.close()  # `()` was missing.
#######################################################################################################################
if __name__ == '__main__':
    root = tk.Tk()
    root.title('RESTACONV0.1')
    root.geometry('600x600+600+300')
    root.minsize(300,300)
    root.maxsize(900,900)
    root.configure(bg='#B0C4DE',
                   relief='sunken',
                   borderwidth=100)
    OpFileAsk = tk.Button(root,
                          font='gotham 10 bold',
                          activeforeground='#B0C4DE',
                          activebackground='#000080',
                          borderwidth='3',
                          text = 'ВЫБРАТЬ ФАЙЛ',
                          bg='#082567',
                          fg='#B0C4DE',
                          cursor='tcross',
                          relief='raised',
                          overrelief='flat',
                          height='3',
                          width='15',
                          command=opnfl

                          )
    Translate = tk.Button(root,
                          font='gotham 10 bold',
                          activeforeground='#B0C4DE',
                          activebackground='#000080',
                          borderwidth='3',
                          text='ПЕРЕВЕСТИ',
                          bg='#082567',
                          fg='#B0C4DE',
                          cursor='exchange',
                          relief='raised',
                          overrelief='flat',
                          height='3',
                          width='15',
                          command=trnsltFl
                          )
    QuitBtn = tk.Button(root,
                          font='gotham 10 bold',
                          activeforeground='#B0C4DE',
                          activebackground='#000080',
                          borderwidth='3',
                          text = 'ВЫХОД',
                          bg='#082567',
                          fg='#B0C4DE',
                          cursor='x_cursor',
                          relief='raised',
                          overrelief='flat',
                          height='3',
                          width='15',
                          command=root.destroy
                          )
    SvAs = tk.Button(root,
                          font='gotham 10 bold',
                          activeforeground='#B0C4DE',
                          activebackground='#000080',
                          borderwidth='3',
                          text = 'СОХРАНИТЬ',
                          bg='#082567',
                          fg='#B0C4DE',
                          cursor='pencil',
                          relief='raised',
                          overrelief='flat',
                          height='3',
                          width='15',
                          command=SaveAs_
                          )
    OpFileAsk.pack()
    Translate.pack()
    SvAs.pack()
    QuitBtn.pack()
    root.mainloop()