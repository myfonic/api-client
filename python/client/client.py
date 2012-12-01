import requests
import json
from requests.auth import HTTPBasicAuth
import base64

# тестовый класс клиент к API myfonic
# демонстрирует использование API myfonic
# в боевой версии, возможно стоит подумать 
# над настройкой пула http-соединений
# сейчас используется управление соединениями по умолчанию
class RestApiClient:
    def __init__(self, url = "http://myfonic.develop.web.drucode.com/", \
                 user = "drucode", password = "thooTh6xoiF7ooWi", apiKey = ""):
        self.__url = url
        self.user = user
        self.password = password
        self.apiKey = apiKey
        
    # получить все фоники, которыми владеет пользователь
    def listOwnFonics(self):
        return self.__post("api/fonic/getfonicslist.json", self.__defaultParams())
    
    # получить все альбомы, которыми владеет пользователь
    def listOwnAlbums(self):
        return self.__post("api/album/getalbumslist.json", self.__defaultParams())
    
    # получить список фоников в заданном альбоме 
    def listFonicsFromAlbum(self, albumNid):
        path = "api/album/getfonicsinalbum.json"
        params = self.__defaultParams()
        params["nid"] = repr(albumNid)
        return self.__post(path, params)
    
    # получить мета-информацию о заданном фонике
    def getFonicById(self, fonicNid):
        path = "api/fonic/getfonic.json"
        params = self.__defaultParams()
        params["nid"] = repr(fonicNid)
        return self.__post(path, params)
    
    # получить медиа-файл фоника
    def getFonicFile(self, fileNid):
        path = "api/fonic/getfile/"
        return self.__get(path + repr(fileNid), params = None)
    
    # загрузить медиа-файл на сервер
    def uploadFonicFile(self, path):
        bytesRead = open(path, "rb").read()
        params = self.__defaultParams()
        params["filename"] = path
        params["file"] = base64.b64encode(bytesRead).decode("utf-8")
        return self.__post("api/fonic/uploadfile.json", params)
    
    # опубликовать фоник, для которого уже загружен медиа-файл
    def postFonic(self, fonic):
        params = self.__defaultParams()
        params["node_data"] = fonic
        return self.__post("api/fonic/createfonic.json", params)
    
    # поиск среди всех публичных фоников
    def searchPublicFonics(self, title = None, fonicType = None, description = None):
        params = {}
        if (title != None):
            params["title"] = title
        if (fonicType != None):
            params["type"] = fonicType
        if (description != None):
            params["description"] = description
        
        return self.__doSearch(params)
    
    # поиск среди всех публичных фоников и закрытых фоников указанного пользователя
    def searchAllFonics(self, title = None, fonicType = None, description = None):
        params = self.__defaultParams()
        if (title != None):
            params["title"] = title
        if (fonicType != None):
            params["type"] = fonicType
        if (description != None):
            params["description"] = description
    
        return self.__doSearch(params)
    
    def __doSearch(self, params):
        return self.__post("api/fonic/search.json", params)
    
    # метод возвращает http-response в чистом виде
    def __get(self, path, params):
        return requests.get(self.__url + path, params=params, \
                            auth=HTTPBasicAuth(self.user, self.password))
    
    # метод возвращает кортеж (http код ответа, json-ответ)
    def __post(self, path, params):
        response = self.__getPostResponse(path, params)
        if (response.status_code == requests.codes["ok"]):
            return (response.status_code, response.json)
        else:
            return (response.status_code, None)
        
    def __defaultParams(self):
        return {"api_key": self.apiKey}
        
    def __getPostResponse(self, path, params):
        data = json.dumps(params)
        headers = {'Content-Type': 'application/json'}
        
        return requests.post(self.__url + path, data=data, \
                             config={"max_retries":10}, headers=headers, \
                             auth=HTTPBasicAuth(self.user, self.password))
