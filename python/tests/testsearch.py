import common
import requests


class Test(common.BaseTest):

    # тест на поиск среди публичных фоников по названию
    def testSearchByTitlePublicFonics(self):
        response = self.client.searchPublicFonics(title = "коммент")
        self.assertStatusCode(response, requests.codes["ok"])
        fonics = response[1]
        self.assertEqual(len(fonics), 3, "3 fonics expected")
        self.assertFonic(fonics[0], "5", "testapi1 testapi1", \
                 "Коммент 1", "про капитана Фила", True)
        self.assertFonic(fonics[1], "5", "testapi1 testapi1", \
                 "Коммент 2", "обсуждение", True)
        self.assertFonic(fonics[2], "1", "testapi3 testapi3", \
                 "Коммент 5", "Тестовый комментарий", True)

    # тест на поиск среди публичных фоников по названию и описанию
    def testSearchByTitleAndDescriptionPublicFonics(self):
        response = self.client.searchPublicFonics(title = "коммент", \
                                                  description = "капитан")
        self.assertStatusCode(response, requests.codes["ok"])
        fonics = response[1]
        self.assertEqual(len(fonics), 1, "1 fonic expected")
        self.assertFonic(fonics[0], "5", "testapi1 testapi1", \
                         "Коммент 1", "про капитана Фила", True)
        
    # тест на поиск среди публичных фоников по описанию
    def testSearchByDesciptionPublicFonics(self):
        response = self.client.searchPublicFonics(description = "капитан")
        self.assertStatusCode(response, requests.codes["ok"])
        fonics = response[1]
        self.assertEqual(len(fonics), 1, "1 fonic expected")
        self.assertFonic(fonics[0], "5", "testapi1 testapi1", \
                         "Коммент 1", "про капитана Фила", True)

    # тест на поиск среди публичных и приватных фоников по названию
    def testSearchByTitlePublicAndPrivateFonics(self):
        response = self.client.searchAllFonics(title = "коммент")
        self.assertStatusCode(response, requests.codes["ok"])
        fonics = response[1]
        self.assertEqual(len(fonics), 5, "5 fonics expected")
        self.assertFonic(fonics[0], "5", "testapi1 testapi1", \
                 "Коммент 3", "про турецкий берег", False)
        self.assertFonic(fonics[1], "5", "testapi1 testapi1", \
                 "Коммент 3", "про турецкий берег", False)
        self.assertFonic(fonics[2], "5", "testapi1 testapi1", \
                 "Коммент 1", "про капитана Фила", True)
        self.assertFonic(fonics[3], "5", "testapi1 testapi1", \
                 "Коммент 2", "обсуждение", True)
        self.assertFonic(fonics[4], "1", "testapi3 testapi3", \
                         "Коммент 5", "Тестовый комментарий", True)