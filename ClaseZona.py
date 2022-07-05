
class Zona:
    def __init__(self):
        self.listaZonas = []

    def agregarZona(self, nombre):
        zona = {
            "id": len(self.listaZonas) + 1,
            "nombre": nombre
        }
        self.listaZonas.append(zona)

    def getZonaPorID(self, id):
        for x in self.listaZonas:
            if (id == x["id"]):
                return x["nombre"]
        return ""

    def cargarZonas(self, zonas):
        self.listaZonas = zonas
