# -------- REQUERIMIENTOS --------- #
#sudo pip3 install adafruit-circuitpython-dht
#sudo apt-get install -y libgpiod-dev
#https://www.internetdelascosas.cl/2017/05/19/raspberry-pi-conectando-un-sensor-de-temperatura-y-humedad-dht11/


# Importamos la paquteria necesaria
import RPi.GPIO as GPIO
import adafruit_dht
#import board
from Sensores.ClaseSensor import Sensor as baseSensor


class Sensor(baseSensor):
    def __init__(self, _id, pines, efecto, Zona):
        self.pines = pines
        super().__init__(_id, "temperatura", pines, efecto, Zona)
        self.DATA = self.boardToBCM(pines[0])
        self.setGPIO()

    def setGPIO(self):
        #GPIO.setmode(GPIO.BOARD) #Establecemos el modo según el cual nos refiriremos a los GPIO de nuestra RPi            
        #GPIO.setup(self.DATA, GPIO.OUT) #Configuramos el pin DATA como una salida
        self.sensor = adafruit_dht.DHT11(self.DATA)
 
    
    def Cargar(self):

        correcto = False

# Intenta ejecutar las siguientes instrucciones, si falla va a la instruccion except
        try:
    		# Obtiene la humedad y la temperatura desde el sensor
            humedad = self.sensor.humidity
            temperatura = self.sensor.temperature
            correcto = True

    		# Imprime en la consola las variables temperatura y humedad con un decimal
            #print('Temperatura={0:0.1f} C  Humedad={1:0.1f}%'.format(temperatura, humedad))

        # Se ejecuta en caso de que falle alguna instruccion dentro del try
        except RuntimeError as error:
            # Imprime en pantalla el error
            #print(error.args[0])
            correcto = False

        if (correcto):

            res1 = {
                    "SensorID": self._id,
                    "Sensor": self.nombre,
                    "Unidad": "°C",
                    "Valor": temperatura,
                    "Fecha": self.fechaRegistro()
                }
            res2 = {
                    "SensorID": self._id,
                    "Sensor": "humedad",
                    "Unidad": "%",
                    "Valor": humedad,
                    "Fecha": self.fechaRegistro()
                }
            respuestas = []
            respuestas.append(res1)
            respuestas.append(res2)
            
            return respuestas

        else:
            return self.msgError()

    def msgError(self):
        res1 = {
                "SensorID": self._id,
                "Sensor": self.nombre,
                "Unidad": "Sensor desactivado",
                "Valor": 0,
                "Fecha": self.fechaRegistro()
            }
        respuestas = []
        respuestas.append(res1)
        return respuestas