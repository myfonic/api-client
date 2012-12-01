import common
import requests


class FonicsTest(common.BaseTest):
    def setUp(self):
        super().setUp()
        self.validFonicId = 396
        self.notFoundFonicId = 662345

    # тест на получение фоника по идентификатору
    def testGetFonic(self):
        response = self.client.getFonicById(self.validFonicId)
        self.assertStatusOk(response)
        fonic = response[1]
        self.assertFonic(fonic, "5", "testapi1 testapi1", "голодный и трезвый", \
                         "голодный и трезвый", True)
        
    # тест на получение медиа-файла публичного фоника по идентификатору
    def testGetPublicFonicFile(self):
        response = self.client.getFonicFile(438)
        self.assertTrue(response.ok, "Response failed")
        self.assertEqual(response.headers["content-length"], "3890496")
    
    # тест на получение медиа-файла приватного фоника по идентификатору
    def testGetPrivateFonicFile(self):
        response = self.client.getFonicFile(428)
        self.assertTrue(response.ok, "Response failed")
        self.assertEqual(response.headers["content-length"], "460290")
        
    # тест на получение фоника, принадлежащего другому пользователю
    def testGetFonicUsingNotOwnerApiKey(self):
        self.client.apiKey = "ca6e543f23a754a0ae09f4f9daba96ee63890c87" #testapi2 api key
        response = self.client.getFonicById(self.validFonicId)
        self.assertStatusCode(response, requests.codes["not_found"])
        
    # тест на получение фоника по несуществующему идентификатору
    def testFonicNotFound(self):
        response = self.client.getFonicById(self.notFoundFonicId)
        self.assertStatusCode(response, requests.codes["not_found"])
        
    # тест на публикацию фоника в хранилище
    def testPushNewFonic(self):
        response = self.client.uploadFonicFile("third.mp3")
        self.assertStatusOk(response)
        fid = response[1]
        
        album = { "nid" : "385" }
        fonic = {
            "album" : album,
            "type" : "5",
            "title" : "New fonic from python",
            "visibility" : "1",
            "fonic_audio_file" : fid,
            "fonic_description" : "Monthy Python",
            "fonic_type_cmnt_text" : "Описание коммента"
        }
        response = self.client.postFonic(fonic)
        self.assertStatusOk(response)
        
        createdFonicId = int(response[1]["nid"])
        response = self.client.getFonicById(createdFonicId)
        self.assertStatusOk(response)
        fonic = response[1]
        self.assertFonic(fonic, "5", "testapi1 testapi1", "New fonic from python", \
                         "Monthy Python", True)