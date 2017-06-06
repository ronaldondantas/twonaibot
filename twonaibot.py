#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbhelper import DBHelper
import json 
import requests
import time
import sys
import urllib

TOKEN = "381560116:AAEc-eX08p3NpCFSdNeCVMgnu79tyfddp9A"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

db = DBHelper()
cur_cmd = ""

def build_keyboard(members):
    keyboard = [[member.name] for member in members]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)

def handle_updates(updates):
    global cur_cmd
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            members = db.get_members_delay()
            if str(text).startswith("/help"):
                cur_cmd = "hp"
                send_message("Fala, *twospleik*! Eu rankeio os membros Twonai pelos atrasos em reuniões " + 
                    "que eles cometem no setor de dev da Polibrás.\n\n Esses são meus comandos: \n\n" + 
                    " /rank - Ranking dos atrasados \n" + 
                    " /adddelay - Adicionar atraso para um membro\n" +
                    " /addpending - Adicionar pendência para um membro\n" +
                    " /addmember - Adicionar membro \n" + 
                    " /deletemember - Deletar um membro \n" + 
                    " /deleteallmembers - Deletar todos os membros \n" + 
                    " /deleteallpendencies - Zerar as pendências de todos os membros \n" + 
                    " /decreasependingfrom - Diminuir uma pendência de um membro " +
                    " /deletependenciesfrom - Zerar as pendências de um membro \n" + 
                    " /deletealldelays - Zerar os atrasos de todos os membros \n" + 
                    " /deletedelaysfrom - Zerar os atrasos de um membro \n" + 
                    " /decreasedelayfrom - Diminuir um atraso de um membro ", chat)
            elif text.startswith("/addmember"):
                cur_cmd = "am"
                send_message("Digite o nome do novo membro Twonai", chat)
            elif text.startswith("/adddelay"):
                if members:
                    cur_cmd = "ad"
                    keyboard = build_keyboard(members)
                    send_message("Quem foi o Twonai que se atrasou?", chat, keyboard)
                else:
                    send_message("Não existe membro Twonai cadastrado :(", chat)
            elif text.startswith("/addpending"):
                if members:
                    cur_cmd = "ap"
                    keyboard = build_keyboard(members)
                    send_message("Adicionar pendência para quem?", chat, keyboard)
                else:
                    send_message("Não existe membro Twonai cadastrado :(", chat)
            elif text.startswith("/rank"):
                cur_cmd = "rk"
                msg = "Não existe membro Twonai cadastrado :("
                if members:
                    msg = "*RANKING TWONAI ATRASADOS :D* \n\n" 
                    for member in members:
                        msgPart = " atrasos"
                        if member.delay_number == 1:
                            msgPart = " atraso"
                        msg += member.name + ": " + str(member.delay_number) + msgPart + "\n"
                send_message(msg, chat)
            elif text.startswith("/deleteallmembers"):
                db.deleteAll()
                send_message("Todos os membros Twonai foram deletados :(", chat)
            elif text.startswith("/deletependenciesfrom"):
                cur_cmd = "delpdfm"
                keyboard = build_keyboard(members)
                send_message("Quem é o membro que terá suas pendências zeradas?", chat, keyboard)
            elif text.startswith("/decreasependingfrom"):
                cur_cmd = "decpdfm"
                keyboard = build_keyboard(members)
                send_message("Quem é o membro que devo retirar uma pendência? :D", chat, keyboard)
            elif text.startswith("/deleteallpendencies"):
                cur_cmd = "delallpnd"
                db.deleteAllPendencies()
                send_message("Pendências zeradas! :P", chat)
            elif text.startswith("/deletedelaysfrom"):
                cur_cmd = "deldf"
                keyboard = build_keyboard(members)
                send_message("Quem é o membro que terá seus atrasos zerados? :D", chat, keyboard)
            elif text.startswith("/decreasedelayfrom"):
                cur_cmd = "decdf"
                keyboard = build_keyboard(members)
                send_message("Quem é o membro que devo retirar um atraso? :D", chat, keyboard)
            elif text.startswith("/deletealldelays"):
                cur_cmd = "delalld"
                db.deleteAllDelays()
                send_message("Atrasos zerados. UI DIDI! :D", chat)
            elif text.startswith("/deletemember"):
                cur_cmd = "delmb"
                keyboard = build_keyboard(members)
                send_message("Quem é o membro que devo dar um chute na bunda? >D", chat, keyboard)
            elif text.startswith("/"):
                cur_cmd = ""
                send_message("Não existe esse comando, twonai!", chat)
            else:
                if cur_cmd ==  "am":
                    db.add_member(text)
                    send_message(text + " incluido com sucesso!\n", chat)
                elif cur_cmd ==  "delpdfm":
                    db.deletePendenciesFrom(text)
                    send_message(text + " esta sem pendencias, papai!\n", chat)
                elif cur_cmd ==  "decpdfm":
                    db.decreasePendingFrom(text)
                    send_message("UAU! " + text + " deu uma reduzida nas pendencias... ;)\n", chat)
                elif cur_cmd ==  "deldf":
                    db.deleteDelaysFrom(text)
                    send_message(text + " esta sem atrasos, papai!\n", chat)
                elif cur_cmd ==  "decdf":
                    db.decreaseDelaysFrom(text)
                    send_message("UAU! " + text + " deu uma reduzida nos atrasos... ;)\n", chat)
                elif cur_cmd == "delmb":
                    db.delete_member(text)
                    send_message("Ja vai tarde, " + text + "! Flw", chat)
                elif cur_cmd ==  "ad":
                    if (db.exists(text) == True):
                        db.add_delay(text)
                        db.add_pending(text)
                        send_message("IEEEEEI! " + text + " se lascou, papaai!", chat)
                    else:
                        cur_cmd = ""
                        send_message("Oh o Douglas! Esse membro Twonai não existe.\n", chat)
                elif cur_cmd ==  "ap":
                    if (db.exists(text) == True):
                        db.add_pending(text)
                        send_message("Pois toma essa pendência, " + text + "!", chat)
                    else:
                        cur_cmd = ""
                        send_message("Oh o Douglas! Esse membro Twonai não existe.\n", chat)
        except Exception as e:
            print(e)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def main():
    db.setup()
    
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    print "TwonaiBot Running"
    main()
