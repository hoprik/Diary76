import requests
from bs4 import BeautifulSoup as BS
from colorama import Fore



def getMarks1(school, login, password):
    school = school
    login = login
    password = password
    r = requests.session()
    auth_r = r.get("https://my.dnevnik76.ru/accounts/login/?next=/marks/current/edurng11933/list/")
    stf_bs = BS(auth_r.content, "html.parser")
    crftoken = stf_bs.select("input[name=csrfmiddlewaretoken]")[0]["value"]
    markStr = ""
    send = {
        "csrfmiddlewaretoken": crftoken,
        "next": "/marks/current/edurng11933/list/",
        "username": login + "@" + school,
        "school": school,
        "fake_username": login,
        "password": password
    }
    marks = r.post("https://my.dnevnik76.ru/accounts/login/", data=send, headers={'referer': "https://my.dnevnik76.ru/accounts/login/"})
    marksBs = BS(marks.content, "html.parser")
    for row in marksBs.select(".mark-row"):
        markRow = ""
        markRow += row.select(".mark-label")[0].text + ": "
        for mark in row.select(".mark"):
            if mark.attrs["class"][1] == "avg":
                if mark.attrs["class"][2] == "m5":
                    markRow += "[" +Fore.LIGHTGREEN_EX+ mark.text.replace("\n", "")+Fore.RESET + "] "
                elif mark.attrs["class"][2] == "m4":
                    markRow += "[" + Fore.GREEN + mark.text.replace("\n", "") + Fore.RESET + "] "
                elif mark.attrs["class"][2] == "m3":
                    markRow += "[" + Fore.LIGHTYELLOW_EX + mark.text.replace("\n", "") + Fore.RESET + "] "
                elif mark.attrs["class"][2] == "m2":
                    markRow += "[" + Fore.LIGHTRED_EX + mark.text.replace("\n", "") + Fore.RESET + "] "
                elif mark.attrs["class"][2] == "m1":
                    markRow += "[" + Fore.RED + mark.text.replace("\n", "") + Fore.RESET + "] "
            else:
                if mark.attrs["class"][1] == "m5":
                    markRow += Fore.LIGHTGREEN_EX+ mark.text.replace("\n", "")+Fore.RESET+ " "
                elif mark.attrs["class"][1] == "m4":
                    markRow += Fore.GREEN + mark.text.replace("\n", "") + Fore.RESET+ " "
                elif mark.attrs["class"][1] == "m3":
                    markRow += Fore.LIGHTYELLOW_EX + mark.text.replace("\n", "") + Fore.RESET+ " "
                elif mark.attrs["class"][1] == "m2":
                    markRow += Fore.LIGHTRED_EX + mark.text.replace("\n", "") + Fore.RESET+ " "
                elif mark.attrs["class"][1] == "m1":
                    markRow += Fore.RED + mark.text.replace("\n", "") + Fore.RESET+ " "
                elif mark.attrs["class"][1] == "m-1":
                    markRow += Fore.LIGHTBLACK_EX + mark.text.replace("\n", "") + Fore.RESET+ " "
                #markRow += mark.text.replace("\n", "") + ", "
        markStr+=markRow+"\n"

    return markStr

def getMarks(school, login, password, half, subject):
    school = school
    login = login
    password = password
    r = requests.session()
    auth_r = r.get("https://my.dnevnik76.ru/accounts/login/?next=/marks/current/edurng1193" + str(half) + "/list/")
    stf_bs = BS(auth_r.content, "html.parser")
    crftoken = stf_bs.select("input[name=csrfmiddlewaretoken]")[0]["value"]
    markStr = ""
    send = {
        "csrfmiddlewaretoken": crftoken,
        "next": "/marks/current/edurng1193" + str(half) + "/list/",
        "username": login + "@" + school,
        "school": school,
        "fake_username": login,
        "password": password
    }
    marks = r.post("https://my.dnevnik76.ru/accounts/login/", data=send,
                   headers={'referer': "https://my.dnevnik76.ru/accounts/login/"})
    marksBs = BS(marks.content, "html.parser")

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

    return "Оценки за триместр №" + str(half) + "\n" + markStr