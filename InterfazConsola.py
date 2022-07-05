from MainController import Controlador as C
controlador = C()
controlador.cargarConfig()
import time


def imprimirPines():
    pines = controlador.getPinesLibres()
    for x in pines:
        print("Board: " + str(x["board"]) + " | BCM: " + x["BCM"])

def verZonas():
    zonas = controlador.getZonas()
    for x in zonas:
        print("ID: " + str(x["id"]) + " | ZONA: " + x["nombre"])

def consultar():
    respuesta = controlador.consultarTodos()
    print("REGISTROS:")
    print()
    for x in respuesta:
        for y in x:
            print("Sensor: " + y["Sensor"] + 
                " | SensorID: " + str(y["SensorID"]) + 
                "| Unidad: " + str(y["Unidad"]) +
                "| Valor: " + str(y["Valor"]) +
                "| Fecha: " + y["Fecha"])

#---------------| MENÚ |----------------#
opc = ""
while opc != "z" and opc != "Z":
    print("BIENVENIDO A LA INTERFAZ DE CONTROLADOR. SELECCIONE UNA OPCIÓN")
    print()
    print("a) Configurar sensores")
    print("b) Manipular mis sensores")
    print("c) Ver opciones de Raspberry")
    print("d) Configurar zonas")
    print("z) Salir")
    print()

    opc = input("Seleccione opción: ")

    # ********* | CONFIGURAR SENSORES | ********* #
    while opc == "a" or opc == "A":
        print()
        print("1) Alta ultrasónico")
        print("2) Alta temperatura")
        print("3) Alta presencia")
        print("4) Alta humo")
        print("5) Alta nfc")
        print("6) Alta infrarrojo")
        print("9) Regresar")
        print()
        opc2 = input("Seleccione opción: ")

        #Sensor ultrasónico
        if opc2 == '1':
            imprimirPines()
            Trig = int(input("Inserte el pin 'TRIG': "))
            Echo = int(input("Inserte el pin 'ECHO': "))
            verZonas()
            ZonaID = int(input("Inserte ID de la zona: "))
            #Zona = controlador.getZonaPorID(ZonaID)
            controlador.AltaSensorUltrasonico(Trig, Echo, ZonaID)

        if opc2 == '2':
            imprimirPines()
            Data = int(input("Inserte el pin 'DATA': "))
            verZonas()
            ZonaID = int(input("Inserte ID de la zona: "))
            #Zona = controlador.getZonaPorID(ZonaID)
            controlador.AltaSensorTemperatura(Data, ZonaID)

        if opc2 == '3':
            imprimirPines()
            Data = int(input("Inserte el pin 'DATA': "))
            verZonas()
            ZonaID = int(input("Inserte ID de la zona: "))
            #Zona = controlador.getZonaPorID(ZonaID)
            controlador.AltaSensorPresencia(Data, ZonaID)

        if opc2 == '4':
            imprimirPines()
            Data = int(input("Inserte el pin 'DATA': "))
            verZonas()
            ZonaID = int(input("Inserte ID de la zona: "))
            #Zona = controlador.getZonaPorID(ZonaID)
            controlador.AltaSensorHumo(Data, ZonaID)

        if opc2 == '5':
            imprimirPines()
            Data = int(input("Inserte el pin 'DATA': "))
            verZonas()
            ZonaID = int(input("Inserte ID de la zona: "))
            #Zona = controlador.getZonaPorID(ZonaID)
            controlador.AltaSensorNFC(Data, ZonaID)

        if opc2 == '6':
            imprimirPines()
            Data = int(input("Inserte el pin 'DATA': "))
            verZonas()
            ZonaID = int(input("Inserte ID de la zona: "))
            #Zona = controlador.getZonaPorID(ZonaID)
            controlador.AltaSensorInfrarrojo(Data, ZonaID)

        #Regresar
        elif opc2 == '9':
            opc = ""
    
    # ********* | MIS SENSORES | ********* #
    while opc == "b" or opc == "B":
        print()
        print("1) Ver sensores configurados")
        print("2) Consultar mis sensores")
        print("3) Consultar varias veces")
        print("9) Regresar")
        print()
        opc2 = input("Seleccione opción: ")

        if opc2 == '1':
            sensores = controlador.getSensores()
            i=0
            print("SENSORES:")
            print()
            for x in sensores:
                i += 1 
                print("#" + str(i) +  " | Sensor: " + x.nombre + " | Pines: " + str(x.pines) + " | Zona: " + str(x.zona))

        if opc2 == '2':
            consultar()

        if opc2 == '3':
            x = 0
            while x < 100:
                consultar()
                time.sleep(1)
                x= x + 1

        #Regresar
        elif opc2 == '9':
            opc = ""

    # ********* | RASPBERRY | ********* #
    while opc == "c" or opc == "C":
        print()
        print("1) Ver pines")
        print("2) Resetear configuración")
        print("9) Regresar")
        print()
        opc2 = input("Seleccione opción: ")

        #Pines disponibles
        if opc2 == '1':
            imprimirPines()

        if opc2 == '2':
            controlador.bajaReset()
            print("Configuración reiniciada")

        #Regresar
        elif opc2 == '9':
            opc = ""

    # ********* | ZONAS | ********* #
    while opc == "d" or opc == "D":
        print()
        print("1) Alta zona")
        print("2) Ver zonas")
        print("9) Regresar")
        print()
        opc2 = input("Seleccione opción: ")

        #Pines disponibles
        if opc2 == '1':
            nombre = input("Inserte el nombre de la zona: ")
            controlador.agregarZona(nombre)

        if opc2 == '2':
            print()
            verZonas()

        #Regresar
        elif opc2 == '9':
            opc = ""

controlador.guardarConfig()
controlador.LimpiarGPIO()
print("Programa finalizado")
