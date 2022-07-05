# Importamos la paquteria necesaria
import RPi.GPIO as GPIO
import time
from Sensores.ClaseSensor import Sensor as baseSensor


class Sensor(baseSensor):
    def __init__(self, _id, pines, efecto, Zona):
        self.pines = pines
        super().__init__(_id, "ultrasonico", pines, efecto, Zona)
        self.TRIG = self.boardToBCM(pines[0])
        self.ECHO = self.boardToBCM(pines[1])
        self.setGPIO()

    def setGPIO(self):
        GPIO.setmode(GPIO.BCM)     #Establecemos el modo según el cual nos refiriremos a los GPIO de nuestra RPi            
        GPIO.setup(self.TRIG, GPIO.OUT) #Configuramos el pin TRIG como una salida 
        GPIO.setup(self.ECHO, GPIO.IN)  #Configuramos el pin ECHO como una salida 
        GPIO.output(self.TRIG, GPIO.LOW)
        time.sleep(0.5)
    
    def Cargar(self):

            #Ponemos en alto el pin TRIG esperamos 10 uS antes de ponerlo en bajo
            GPIO.output(self.TRIG, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(self.TRIG, GPIO.LOW)

            # En este momento el sensor envía 8 pulsos ultrasónicos de 40kHz y coloca su pin ECHO en alto
            # Debemos detectar dicho evento para iniciar la medición del tiempo
            
            while True:
                pulso_inicio = time.time()
                if GPIO.input(self.ECHO) == GPIO.HIGH:
                    break

            # El pin ECHO se mantendrá en HIGH hasta recibir el eco rebotado por el obstáculo. 
            # En ese momento el sensor pondrá el pin ECHO en bajo.
        # Prodedemos a detectar dicho evento para terminar la medición del tiempo
            
            while True:
                pulso_fin = time.time()
                if GPIO.input(self.ECHO) == GPIO.LOW:
                    break

            # Tiempo medido en segundos
            duracion = pulso_fin - pulso_inicio

            #Obtenemos la distancia considerando que la señal recorre dos veces la distancia a medir y que la velocidad del sonido es 343m/s
            distancia = (34300 * duracion) / 2 #cm/s

            res1 = {
                "SensorID": self._id,
                "Sensor": self.nombre,
                "Unidad": "cm",
                "Valor": distancia,
                "Fecha": self.fechaRegistro()
            }
            respuestas = []
            respuestas.append(res1)

            #return "Distancia: %.2f cm" % distancia
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
        #return "Sensor ultrasonico desactivado"

