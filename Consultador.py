#import adafruit_dht
#52.23.247.230
# ----- LIBRERÍAS ----- #
from ApiRequests import APIRestProyecto as ARP
miApi = ARP("http://52.23.247.230:3333/","api/v1/")

from remoteController import Controlador as C
controlador = C()

import time
import json

#temporales
import random
import datetime



class Consultador():
    def __init__(self):
        self.logged = False
        self.intervalo = 2
        self.listaRegistros = []
        self.login()
        self.cargarSensores()
        self.cargarRegistros()

    #ARRANQUE

    def login(self):
        try:
            dataLogin = {
                "email": "soporte@scdam.com",
                "password": "Soporte1."
            }
            miApi.miLogin(dataLogin)
            self.startIsLogged()

        except:
            self.startNotLogged()
        
    def startNotLogged(self):
        self.logged = False
        print("Error al iniciar sesión")

    def startIsLogged(self):
        self.logged = True
        print("Inicio de sesión correcto")
        self.subirRegistros()
        #self.descargarSensores()

    #PROCESO
        # -------- | CICLO | -------- #
    def ciclo(self):
        print("MSG cada " + str(self.intervalo) + " Seg")
        while True:
            #Solicitar información
            #data = self.msgAux()
            data = controlador.consultarTodos()

            #DIRECTO A BD
            if (self.logged):
                self.descargarSensores()
                for d in data:
                    self.listaRegistros.append(d)
                    print(d)
                respuesta = self.enviarInfo(data)

            #DIRECTO A JSON
            else:
                for d in data:
                    self.listaRegistros.append(d)
                    print(d)

            #INTERVALO
            time.sleep(self.intervalo)


    def enviarInfo(self, data):
        return miApi.metodoPost(data, 'configuracion')

    # -------- | FINAL | -------- #

    #REGISTROS
    def guardarRegistros(self):
        f = open("jsonLocal/registros.json", "w")
        f.write(json.dumps(self.listaRegistros, indent=4))
        f.close()

    def cargarRegistros(self):
            try:
                f = open("jsonLocal/registros.json", "r")
                aux=json.loads(f.read())
                f.close()
                self.listaRegistros = aux
            except:
                f = open("jsonLocal/registros.json", "x")
                f.close()

    def subirRegistros(self):
        respuesta = miApi.metodoPost(self.listaRegistros, 'configuracion')
        self.listaRegistros = []
        self.guardarRegistros()

    #SENSORES

    def cargarSensores(self):
        controlador.cargarSensores()
        
    def descargarSensores(self):
        respuesta = miApi.metodoGet('indexP')

        data = respuesta['data']['data']

        f = open("jsonLocal/config.json", "r")
        dataOld=json.loads(f.read())
        f.close()

        if (data != dataOld):
            print("Descargando sensores...")
            controlador.actualizarSensores(data)

    #AUXILIARES
    def getFecha(self):
        x = datetime.datetime.now()
        y = x.strftime("%Y %b %d %X")
        return y

    def msgAux(self):
            res = {
                    "SensorID": 0,
                    "Sensor": 'prueba',
                    "Unidad": "Sensor desactivado",
                    "Valor": random.randint(30, 60),
                    "Fecha": self.getFecha()
                }
            respuestas = []
            respuestas.append(res)
            return respuestas


if __name__ == '__main__':
    MainConsultador = Consultador()
    try:
        MainConsultador.ciclo()
    except KeyboardInterrupt:
        if (MainConsultador.logged):
            print()
        else:
            MainConsultador.guardarRegistros()
        controlador.guardarSensores()
        controlador.LimpiarGPIO()
        print ('Fin del programa manual')