import datetime

#CLASE ELEMENTO
class Sensor:
    def __init__(self, _id, nombre, pines, efecto, zona):
        self._id = _id
        self.nombre = nombre
        self.pines = pines
        self.efecto = efecto
        self.zona = zona

    def fechaRegistro(self):
        x = datetime.datetime.now()
        y = x.strftime("%Y %b %d %X")
        return y

    def boardToBCM(self, pin):
        if (pin == 7):
            return 4
        elif (pin == 11):
            return 17
        elif (pin == 12):
            return 18
        elif (pin == 13):
            return 27
        elif (pin == 15):
            return 22
        elif (pin == 16):
            return 23
        elif (pin == 18):
            return 24
        elif (pin == 22):
            return 25
        elif (pin == 29):
            return 5
        elif (pin == 31):
            return 6
        elif (pin == 32):
            return 12
        elif (pin == 33):
            return 13
        elif (pin == 35):
            return 19
        elif (pin == 36):
            return 16
        elif (pin == 37):
            return 26
        elif (pin == 38):
            return 20
        elif (pin == 40):
            return 21