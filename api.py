import requests
from bs4 import BeautifulSoup as BS


class Diary:
    season = None
    login = ""
    password = ""
    # school id
    region = ""
    city = ""
    school = ""

    def __init__(self):
        self.season = requests.Session()

    def FindSchool(self, region, city, school):
        cityRegionR = self.season.get("https://my.dnevnik76.ru/ajax/kladr/frontend/")
        cityRegionB = BS(cityRegionR.content, "html.parser")
        for regionF in cityRegionB.select(".custom-select__item"):
            if regionF.text == region:
                cityR = self.season.get(
                    "https://my.dnevnik76.ru/ajax/kladr/frontend/" + regionF.attrs.get("data-value"))
                cityB = BS(cityR.content, "html.parser")
                for cityF in cityB.select(".custom-select__item"):
                    if cityF.text == city:
                        schoolR = self.season.get(
                            "https://my.dnevnik76.ru/ajax/school/frontend/" + cityF.attrs.get("data-value"))
                        schoolB = BS(schoolR.content, "html.parser")
                        for schoolF in schoolB.select(".custom-select__item"):
                            if schoolF.text == school:
                                return schoolF.attrs.get("data-value")

    def FindSchoolByRegion(self, region, school):
        cityRegionR = self.season.get("https://my.dnevnik76.ru/ajax/kladr/frontend/")
        cityRegionB = BS(cityRegionR.content, "html.parser")
        for regionF in cityRegionB.select(".custom-select__item"):
            if regionF.text == region:
                schoolR = self.season.get(
                    "https://my.dnevnik76.ru/ajax/school/frontend/" + cityRegionB.attrs.get("data-value"))
                schoolB = BS(schoolR.content, "html.parser")
                for schoolF in schoolB.select(".custom-select__item"):
                    if schoolF.text == school:
                        return schoolF.attrs.get("data-value")

    def Auth(self, school, login, password):
        auth_r = self.season.get("https://my.dnevnik76.ru/accounts/login/")
        stf_bs = BS(auth_r.content, "html.parser")
        crftoken = stf_bs.select("input[name=csrfmiddlewaretoken]")[0]["value"]
        send = {
            "csrfmiddlewaretoken": crftoken,
            "username": login + "@" + school,
            "school": school,
            "fake_username": login,
            "password": password
        }
        authP = self.season.post("https://my.dnevnik76.ru/accounts/login/", data=send,
                                 headers={'referer': "https://my.dnevnik76.ru/accounts/login/"})
        errorLogin = BS(authP.content, "html.parser")
        if errorLogin.select(".errorlist"):
            errorList = ""
            for error in errorLogin.select(".errorlist"):
                errorList += error.text.replace("\n", "") + "\n"
            return errorList
        else:
            self.login = login
            self.password = password
            self.school = school
            return True

    def Marks(self, subject, half):
        if int(half) >= 7:
            return "Ошибка оценки не найдены"
        marksReq = self.season.get("https://my.dnevnik76.ru/marks/current/edurng1193" + str(half) + "/list/")
        marksBs = BS(marksReq.content, "html.parser")
        markStr = ""
        for row in marksBs.select(".mark-row"):
            if subject == "all":
                markRow = ""
                markRow += row.select(".mark-label")[0].text + ": "
                for mark in row.select(".mark"):
                    if mark.attrs["class"][1] == "avg":
                        markRow += "[" + mark.text.replace("\n", "") + "] "
                    else:
                        markRow += mark.text.replace("\n", "") + " "
                markStr += markRow + "\n"
            else:
                if row.select(".mark-label")[0].text == subject:
                    markRow = ""
                    markRow += row.select(".mark-label")[0].text + ": "
                    for mark in row.select(".mark"):
                        if mark.attrs["class"][1] == "avg":
                            markRow += "[" + mark.text.replace("\n", "") + "] "
                        else:
                            markRow += mark.text.replace("\n", "") + " "
                    markStr += markRow + "\n"
        if int(half) <= 3:
            return "Оценки за триместр №" + str(half) + "\n" + markStr
        elif int(half) == 4 or int(half) == 5:
            return "Оценки за полугодие №" + str(int(half) - 3) + "\n" + markStr
        elif int(half) == 6:
            return "Оценки за учебный год\n" + markStr

    # getter and setters
    def GetCityRegionId(self):
        cityRegionR = self.season.get("https://my.dnevnik76.ru/ajax/kladr/frontend/")
        cityRegionB = BS(cityRegionR.content, "html.parser")
        list = []
        for regionF in cityRegionB.select(".custom-select__item"):
            list.append(regionF.text)
        return list

    def GetCityId(self, cityRegionid):
        cityRegionR = self.season.get("https://my.dnevnik76.ru/ajax/kladr/frontend/")
        cityRegionB = BS(cityRegionR.content, "html.parser")
        list = []
        for regionF in cityRegionB.select(".custom-select__item"):
            if regionF.text == cityRegionid:
                cityR = self.season.get(
                    "https://my.dnevnik76.ru/ajax/kladr/frontend/" + regionF.attrs.get("data-value"))
                cityB = BS(cityR.content, "html.parser")
                for cityF in cityB.select(".custom-select__item"):
                    list.append(cityF.text)
        return list

    def GetSchoolId(self, regionId, nameCity):
        cityR = self.season.get("https://my.dnevnik76.ru/ajax/kladr/frontend/" + regionId)
        cityB = BS(cityR.content, "html.parser")
        list = []
        for cityF in cityB.select(".custom-select__item"):
            if cityF.text == nameCity:
                schoolR = self.season.get(
                    "https://my.dnevnik76.ru/ajax/school/frontend/" + cityF.attrs.get("data-value"))
                schoolB = BS(schoolR.content, "html.parser")
                for schoolF in schoolB.select(".custom-select__item"):
                    list.append(schoolF.text)
        return list

    def SetLogin(self, login):
        self.login = login

    def SetPassword(self, password):
        self.password = password

    def SetRegion(self, region):
        self.region = region

    def SetCity(self, city):
        self.city = city

    def SetSchool(self, school):
        self.school = school

    def GetRegion(self):
        return self.region

    def GetCity(self):
        return self.city

    def GetSchool(self):
        return self.school

    def GetLogin(self):
        return self.login

    def GetPassword(self):
        return self.password