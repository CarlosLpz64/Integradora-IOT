import requests 
from requests.structures import CaseInsensitiveDict
import json


class APIRestProyecto:
    def __init__(self,domain,prefix):
        self.domain = domain
        self.prefix = prefix
        self.endpoint = self.domain + self.prefix
        self.token = ""
    
    #MÉTODOS

    def metodoGet(self, path):
        try:
            path = self.endpoint + path
            data = {}
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = "Bearer %s" % self.token
            data = requests.get(path, data=data, headers=headers)
            if data.status_code == 401:
                miResponse = {
                    'status': data.status_code,
                    'msg': "Permiso denegado",
                    'data': False
                }
                return miResponse
            elif data.status_code == 404:
                miResponse = {
                    'status': data.status_code,
                    'msg': "URL no encontrada",
                    'data': False
                }
                return miResponse
            else:
                miResponse = {
                    'status': data.status_code,
                    'msg': "Correcto",
                    'data': data.json()
                }
                return miResponse
        except:
            miResponse = {
                    'status': data.status_code,
                    'msg': "Error al cargar",
                    'data': False
            }
            return miResponse

    def metodoPost(self, data, path):
        path = self.endpoint + path
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer %s" % self.token
        resp = requests.post(path, json=data, headers=headers)
        return resp.json()

    def metodoPatch(self, data, path, id):
        path = self.endpoint + path + "/" + str(id)
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer %s" % self.token
        resp = requests.patch(path, data=data, headers=headers)
        return resp.json()

    def metodoDelete(self, path, id):
        path = self.endpoint + path + "/" + str(id)
        headers = CaseInsensitiveDict()
        data = {}
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer %s" % self.token
        resp = requests.delete(path, data=data, headers=headers)
        return resp.json()

        
    #AUTH

    def getToken(self,data):
        path = self.domain+ "auth/v1/login"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        resp = requests.post(path, data, headers)
        return resp.json()

    def miLogin(self, data):
        respuesta = self.getToken(data)
        self.token = respuesta["token"]["token"]
        self.getToken(data) 
