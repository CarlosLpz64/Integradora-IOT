# Importamos la paquteria necesaria
import RPi.GPIO as GPIO
from Sensores.ClaseSensor import Sensor as baseSensor


class Sensor(baseSensor):
    def __init__(self, _id, pines, efecto, Zona):
        self.pines = pines
        super().__init__(_id, "humo", pines, efecto, Zona)
        self.DATA = self.boardToBCM(pines[0])
        self.setGPIO()

    def setGPIO(self):
        GPIO.setmode(GPIO.BCM) #Establecemos el modo según el cual nos refiriremos a los GPIO de nuestra RPi            
        GPIO.setup(self.DATA, GPIO.IN) #Configuramos el pin DATA como una salida 
    
    def Cargar(self):
        if GPIO.input(self.DATA):
            valor = "Gas detectado"
        else:
            valor = "No se detecta gas"
            
        res1 = {
                "SensorID": self._id,
                "Sensor": self.nombre,
                "Unidad": "",
                "Valor": valor,
                "Fecha": self.fechaRegistro()
            }
        respuestas = []
        respuestas.append(res1)
        
        return respuestas

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