#Generales
import RPi.GPIO as GPIO
import json
from EstadoRaspberry import Raspberry as MiRasp
miRasp = MiRasp()
from Sensores.ClaseUltrasonico import Sensor as Ultrasonico
from Sensores.ClaseTemperatura import Sensor as Temperatura
from Sensores.ClasePresencia import Sensor as Presencia
from Sensores.ClaseHumo import Sensor as Humo
from Sensores.ClaseNFC import Sensor as NFC
from Sensores.ClaseInfrarrojo import Sensor as Infrarrojo
from ClaseZona import Zona as ZC
miZona = ZC()
import time


class Controlador:
    def __init__(self):
        self.listaSensores = []
        self.listaIDs = []
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(37, GPIO.OUT)
        #GPIO.setwarnings(False)

    #Sensores
        #Altas
    def AltaSensorUltrasonico(self, Trig, Echo, Zona):
        pines = []
        pines.append(Trig)
        pines.append(Echo)
        ultrasonico = Ultrasonico(self.asignarID(), pines, Zona)
        self.listaSensores.append(ultrasonico)
        miRasp.ocuparPin(Trig)
        miRasp.ocuparPin(Echo)

    def AltaSensorTemperatura(self, Data, Zona):
        pines = []
        pines.append(Data)
        temperatura = Temperatura(self.asignarID(), pines, Zona)
        self.listaSensores.append(temperatura)
        miRasp.ocuparPin(Data)

    def AltaSensorPresencia(self, Data, Zona):
        pines = []
        pines.append(Data)
        presencia = Presencia(self.asignarID(), pines, Zona)
        self.listaSensores.append(presencia)
        miRasp.ocuparPin(Data)

    def AltaSensorHumo(self, Data, Zona):
        pines = []
        pines.append(Data)
        humo = Humo(self.asignarID(), pines, Zona)
        self.listaSensores.append(humo)
        miRasp.ocuparPin(Data)

    def AltaSensorNFC(self, Data, Zona):
        pines = []
        pines.append(Data)
        nfc = NFC(self.asignarID(), pines, Zona)
        self.listaSensores.append(nfc)
        miRasp.ocuparPin(Data)

    def AltaSensorInfrarrojo(self, Data, Zona):
        pines = []
        pines.append(Data)
        infrarrojo = Infrarrojo(self.asignarID(), pines, Zona)
        self.listaSensores.append(infrarrojo)
        miRasp.ocuparPin(Data)

    def consultarTodos(self):
        respuesta = []
        for x in self.listaSensores:
            try:
                resultado = x.Cargar()
            except:
                resultado = x.msgError()
            respuesta.append(resultado)
        self.encenderBuzzer()
        return respuesta

    def encenderBuzzer(self):
        GPIO.output(37, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(37, GPIO.LOW)
        time.sleep(0.1)
            

    def getSensores(self):
        return self.listaSensores

    #Raspberry
    def ocuparPin(self, pin):
        miRasp.ocuparPin(pin)

    def getPinesLibres(self):
        return miRasp.getPinesLibres()

    def LimpiarGPIO(self):
        try:
            GPIO.cleanup()
        except:
            return

    #Extras
    def asignarID(self):
        id = len(self.listaIDs) + 1001
        self.listaIDs.append(id)
        return id

    #Almacen de informacion
    def bajaReset(self):
        self.listaSensores=[]
        self.listaIDs = []
        miZona.listaZonas = []
        miRasp.listaPines = []
        miRasp.cargarPines([])

    def guardarConfig(self):
        self.guardarSensores()
        self.guardarZonas()
        self.guardarPines()

    def guardarZonas(self):
        f = open("jsonLocal/zonas.json", "w")
        f.write(json.dumps(miZona.listaZonas, indent=4))
        f.close()

    def guardarPines(self):
        f = open("jsonLocal/pines.json", "w")
        f.write(json.dumps(miRasp.listaPines, indent=4))
        f.close()

    def guardarSensores(self):
        aux = []
        for x in self.listaSensores:
            dict = {
                "id": x.id,
                "nombre": x.nombre,
                "pines": x.pines,
                "zona": x.zona
            }
            aux.append(dict)
        f = open("jsonLocal/config.json", "w")
        f.write(json.dumps(aux, indent=4))
        f.close()

    def cargarConfig(self):
        self.cargarSensores()
        self.cargarZonas()
        self.cargarPines()

    def cargarZonas(self):
        try:
            f = open("jsonLocal/zonas.json", "r")
            aux=json.loads(f.read())
            f.close()
            miZona.cargarZonas(aux)
        except:
            f = open("jsonLocal/zonas.json", "x")
            f.close()

    def cargarPines(self):
        try:
            f = open("jsonLocal/pines.json", "r")
            aux=json.loads(f.read())
            f.close()
        except:
            f = open("jsonLocal/pines.json", "x")
            f.close()
            aux = []
        miRasp.cargarPines(aux)


    def cargarSensores(self):
        try:
            f = open("jsonLocal/config.json", "r")
            aux=json.loads(f.read())
            f.close()

            for x in aux:
                if (x["nombre"] == "ultrasonico"):
                    sensor = Ultrasonico(x["id"], x["pines"], x["zona"])
                elif (x["nombre"] == "temperatura"):
                    sensor = Temperatura(x["id"], x["pines"], x["zona"])
                elif (x["nombre"] == "presencia"):
                    sensor = Presencia(x["id"], x["pines"], x["zona"])
                elif (x["nombre"] == "humo"):
                    sensor = Humo(x["id"], x["pines"], x["zona"])
                elif (x["nombre"] == "nfc"):
                    sensor = NFC(x["id"], x["pines"], x["zona"])
                elif (x["nombre"] == "infrarrojo"):
                    sensor = Infrarrojo(x["id"], x["pines"], x["zona"])
                self.listaIDs.append(x["id"])
                self.listaSensores.append(sensor)
                    
        except:
            f = open("jsonLocal/config.json", "x")
            f.close()

    #Zonas
    def agregarZona(self, nombre):
        miZona.agregarZona(nombre)

    def getZonas(self):
        return miZona.listaZonas

    def getZonaPorID(self, id):
        return miZona.getZonaPorID(id)

