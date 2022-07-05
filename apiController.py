from ApiRequests import APIRestProyecto as ARP

print("ola")

miApi = ARP("http://localhost:3333/","api/v1/")

opc = ""

def login():
    #LOGIN
    dataLogin = {
        "email": "miadmin@gmail.com",
        "password": "adminSegura!654"
    }
    miApi.miLogin(dataLogin)

def crearUsuario():
    #CREAR USUARIO
    username = input("Username: ")
    email = input("Correo: ")
    password = input("Contraseña: ")
    age = int(input("Edad: "))
    curp = input("Curp: ")
    
    dataRegister = {
        "username": username,
        "email": email,
        "password": password,
        "age": age,
        "curp": curp
    }

    resp = miApi.metodoPost(dataRegister, 'usuarios/registro')
    
    print(resp)

def verUsuarios():
    #VER USUARIOS
    resp = miApi.metodoGet('usuarios/inde')
    if (resp['data']):
        for user in resp['data']:
            print("******************")
            print("ID: " + str(user["id"]))
            print("Username: " + str(user["username"]))
            print("Edad: " + str(user["age"]))
            print("Curp: " + str(user["curp"]))
    else:
        print(resp['msg'])

def verUsuariosID():
    resp = miApi.metodoGet('usuarios/index')

    for user in resp:
        print("******************")
        print("ID: " + str(user["id"]) + " | " + "Username: " + str(user["username"]))

def eliminarUsuario():
    verUsuariosID()
    print()
    print("-------------")
    print()
    idUser = input("Inserte id: ")
    resp = miApi.metodoDelete('usuarios/delete', idUser)
    print(resp)

def actualizarUsuario():

    verUsuariosID()
    print()
    print("-------------")
    print()
    idUser = input("Inserte id: ")

    age = int(input("Edad: "))
    
    dataRegister = {
        "age": age
    }

    resp = miApi.metodoPatch(dataRegister, 'usuarios/update', idUser)
    
    print(resp)

while opc != "z":
    print("| ----- MENÚ ----- |")
    print("a) Login")
    print("b) Crear usuario")
    print("c) Ver usuarios")
    print("d) Eliminar usuarios")
    print("e) Actualizar usuarios")
    print("z) Salir")
    print()
    opc = input("Seleccione opción: ")

    if (opc == 'a'):
        login()

    elif (opc == 'b'):
        crearUsuario()

    elif (opc == 'c'):
        verUsuarios()

    elif (opc == 'd'):
        eliminarUsuario()

    elif (opc == 'e'):
        actualizarUsuario()

print("Adiós!")
