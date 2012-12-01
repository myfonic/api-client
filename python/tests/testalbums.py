import requests
import common

class AlbumsTests(common.BaseTest):
    
    def setUp(self):
        super().setUp()
        self.validAlbumId = 395
        self.notFoundAlbumId = 63242
    
    # тест на получение списка альбомов пользователя
    def testNotEmptyList(self):
        response = self.client.listOwnAlbums()
        self.assertStatusOk(response)
        self.assertTrue(len(response[1]) > 0, "Expected non-empty list")
    
    # тест на получение пустого списка альбомов пользователя
    def testEmptyList(self):
        self.client.apiKey = "ca6e543f23a754a0ae09f4f9daba96ee63890c87" # testapi2
        response = self.client.listOwnAlbums()
        self.assertStatusOk(response)
        self.assertListEqual(response[1], [], "Expected empty result")
    
    # тест на получение фоников заданного альбома
    def testGetApiKeyOwnerAlbumFonics(self):
        response = self.client.listFonicsFromAlbum(self.validAlbumId)
        self.assertStatusOk(response)
        fonics = response[1]
        self.assertEqual(len(fonics), 8)
        self.assertFonic(fonics[0], "5", "testapi1 testapi1", \
                         "голодный и трезвый", "голодный и трезвый", True)
        self.assertFonic(fonics[7], "1", "testapi1 testapi1", \
                         "At vero eos et", "Ut enim ad minim", True)

    # тест на получение фоников заданного альбома, принадлежащего другому пользователю
    def testGetNotApiKeyOwnerAlbumFonics(self):
        self.client.apiKey = "ca6e543f23a754a0ae09f4f9daba96ee63890c87" #testapi2 api-key
        result = self.client.listFonicsFromAlbum(self.validAlbumId)
        self.assertStatusCode(result, requests.codes["not_found"])
        
    # тест на получение фоников из неизвестного альбома
    def testGetFonicsAlbumNotFound(self):
        result = self.client.listFonicsFromAlbum(self.notFoundAlbumId)
        self.assertStatusCode(result, requests.codes["not_found"])