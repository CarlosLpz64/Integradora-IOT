# ----- LIBRERÍAS ----- #
from ApiRequests import APIRestProyecto as ARP
miApi = ARP("http://52.23.247.230:3333/","api/v1/")
#miApi = ARP("http://52.91.233.31:3333/","api/v1/")

import time
import RPi.GPIO as GPIO
import datetime

from pirc522 import RFID


class NFC_Controller():
    def __init__(self):
        self.logged = False
        self.retryInterval = 5
        self.Trigger = 40
        self.configGPIO()
        self.login()

    #ARRANQUE

    def configGPIO(self):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.Trigger, GPIO.OUT) 
            self.rc522 = RFID() #On instancie la lib

    def login(self):
        while self.logged == False:
            print("Iniciando sesión...")
            try:
                dataLogin = {
                    "email": "soporte@scdam.com",
                    "password": "Soporte1."
                }
                miApi.miLogin(dataLogin)
                self.logged = True
                print("Inicio de sesión correcto")

            except:
                print("Error al iniciar sesión. Reintentando en " + str(self.retryInterval) + " segundos.")
                time.sleep(self.retryInterval)
                self.retryInterval += 5
        

    #PROCESO
        # -------- | CICLO | -------- #
    def ciclo(self):
        print("Esperando tarjeta NFC...")
        while True:
            self.rc522.wait_for_tag()
            (error, tag_type) = self.rc522.request() 

            #TARJETA DETECTADA
            if not error : 
                (error, uid) = self.rc522.anticoll() 

            #TARJETA DETECTADA
            if not error :
                clave = self.TraductorNFC(uid)
                print("CÓDIGO: " + clave)
                self.subirNFC(clave)
                time.sleep(1)


    def subirNFC(self, clave):
        data = {
                "llave": clave,
                "f_reg": self.getFecha()
            }
        respuesta = miApi.metodoPost(data, 'nfc')

        if (respuesta['caso'] == 3):
            self.abrirPuertas()
        print(respuesta)


    def getFecha(self):
        x = datetime.datetime.now()
        y = x.strftime("%Y %b %d %X")
        return y


    def abrirPuertas(self):
        print("puertas abiertas")
        GPIO.output(self.Trigger, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(self.Trigger, GPIO.LOW)

    #EXTRAS
    def TraductorNFC(self, uid):
        aux = ""
        for x in uid:
            aux = aux + str(x)
        return aux


if __name__ == '__main__':
    MainConsultador = NFC_Controller()
    try:
        MainConsultador.ciclo()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print ('Fin del programa manual')