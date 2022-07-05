#Generales

import RPi.GPIO as GPIO
import json

from Sensores.ClaseUltrasonico import Sensor as Ultrasonico
from Sensores.ClaseTemperatura import Sensor as Temperatura
from Sensores.ClasePresencia import Sensor as Presencia
from Sensores.ClaseHumo import Sensor as Humo
from Sensores.ClaseInfrarrojo import Sensor as Infrarrojo


class Controlador:
    def __init__(self):
        self.listaSensores = []

    def consultarTodos(self):
        respuesta = []
        for x in self.listaSensores:

            resultado = x.Cargar()

            '''
            try:
                resultado = x.Cargar()
            except:
                resultado = x.msgError()
                '''
            for y in resultado:
                respuesta.append(y)
        return respuesta

    def getSensores(self):
        return self.listaSensores

    #Raspberry
    def LimpiarGPIO(self):
        try:
            GPIO.cleanup()
        except:
            return

    def guardarSensores(self):
        aux = []
        for x in self.listaSensores:
            dict = {
                "_id": x._id,
                "nombre": x.nombre,
                "pines": x.pines,
                "efecto": x.efecto,
                "zona": x.zona,
                "__v": 0
            }
            aux.append(dict)
        f = open("jsonLocal/config.json", "w")
        f.write(json.dumps(aux, indent=4))
        f.close()

    def actualizarSensores(self, sensores):
        self.listaSensores = []
        for x in sensores:
                if (x["nombre"] == "ultrasonico"):
                    sensor = Ultrasonico(x["_id"], x["pines"], x["efecto"], x["zona"])
                elif (x["nombre"] == "temperatura"):
                    sensor = Temperatura(x["_id"], x["pines"], x["efecto"], x["zona"])
                elif (x["nombre"] == "presencia"):
                    sensor = Presencia(x["_id"], x["pines"], x["efecto"], x["zona"])
                elif (x["nombre"] == "humo"):
                    sensor = Humo(x["_id"], x["pines"], x["efecto"], x["zona"])
                elif (x["nombre"] == "infrarrojo"):
                    sensor = Infrarrojo(x["_id"], x["pines"], x["efecto"], x["zona"])
                self.listaSensores.append(sensor)
        self.guardarSensores()

    def cargarSensores(self):
        #try:
            f = open("jsonLocal/config.json", "r")
            aux=json.loads(f.read())
            f.close()

            for x in aux:
                if (x["nombre"] == "ultrasonico"):
                    sensor = Ultrasonico(x["_id"], x["pines"], x["efecto"], x["zona"])
                elif (x["nombre"] == "temperatura"):
                    sensor = Temperatura(x["_id"], x["pines"], x["efecto"], x["zona"])
                elif (x["nombre"] == "presencia"):
                    sensor = Presencia(x["_id"], x["pines"], x["efecto"], x["zona"])
                elif (x["nombre"] == "humo"):
                    sensor = Humo(x["_id"], x["pines"], x["efecto"], x["zona"])
                elif (x["nombre"] == "infrarrojo"):
                    sensor = Infrarrojo(x["_id"], x["pines"], x["efecto"], x["zona"])
                self.listaSensores.append(sensor)
                    
"""         except:
            f = open("jsonLocal/config.json", "x")
            f.close() """


