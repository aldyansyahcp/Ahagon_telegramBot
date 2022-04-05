from PIL import Image
from io import BytesIO
import telebot
import requests
from bs4 import BeautifulSoup as bs
import datetime

api = "Your TelegramBot Api"
bot = telebot.TeleBot(api)
now = datetime.datetime.now()
date = now.strftime("%B-%m-%Y, %H:%M")
ses = requests.session()
headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
      'Cache-Control':'max-age=0'
}

def login(message):                                                             
    firstnam = message.chat.first_name
    lasnam = message.chat.last_name
    ttd = datetime.now()                                                        
    ttd = ttd.strftime('%d-%B-%Y %H:%M')            
    ied = message.chat.id
    commands = message.text                                                     
    text_log = (f'{ttd}, id: {ied} {firstnam} {lasnam} ')
    log_bot = open('log_bot.txt', 'a')
    log_bot.write(text_log)                                                     
    log_bot.close()

@bot.message_handler(commands=["start"])
def selamat_datang(msg):
    #login(msg)
    na = msg.chat.first_name
    ma = msg.chat.last_name
    cet = msg.chat.id
    print(na,ma,cet, "text:",cet)
    bot.reply_to(msg,f'{date}\nようこそ {na} {ma} id: {cet} i hope you will enjoyed in here\nThie Bot Created with Python\ntype /help for the command\nAuthor: @rup_23\nFB: Rere Kurniawan')

@bot.message_handler(commands=["help"])
def helep(msg):
    cet = msg.chat.id
    bot.reply_to(msg, "Selamat datang!!!\nBot ini mempermudah kalian untuk mendownload anime otakudesu langsung menuju link download :-) Jadi gaperlu mencet kena iklan mulu -_-\nKedepanya admin akan mengupgrade bot download link, menjadi bot streaming Terima Kasih :)\ntype: /cari untuk memulai pencarian anime")

@bot.message_handler(commands=["cari"])
def main(msg):
    cet = msg.chat.id
    na = bot.send_message(cet, "Mau cari anime apa?")
    bot.register_next_step_handler(na,two)
def two(msg):
    try:
        cet = msg.chat.id
        tek = "".join(msg.text)
        url = "https://otakudesu.live/?s={}&post_type=anime".format(tek)
        resj = ""
        res = []
        n=1
        req = requests.get(url, headers=headers)
        if tek.isalnum() == True:
            bes = bs(req.text, "html.parser")
            resj += "Hasil pencarianmu max 12\n\n"
            for i in bes.find_all("li", attrs={"style":"list-style:none;"}):
                nam = i.find("a", attrs={"data-wpel-link":"internal"})
                lin = nam["href"]
                resj += f"{n}. {nam.string}\n"
                res.append(lin)
                n+=1
            resj += "\nMasukan pilihan angka:"
        else:
            bot.reply_to(cet, "nulis yg bener asw")
        na = bot.send_message(cet, resj)
        bot.register_next_step_handler(na,three,res)
    except:
        bot.send_message(cet, "/cari")
def three(msg,res):
    try:
        cet = msg.chat.id
        fin = res[int(msg.text)-1]
        nam = msg.chat.first_name
        resj = ""
        rez = []
        n=1
        req = requests.get(fin,headers=headers)
        if req.status_code == 200:
            bes = bs(req.text, "html.parser")
            for i in bes.find_all("a", attrs={"data-wpel-link":"internal"}):
                lin = i["href"]
                rez.append(lin)
            for i in bes.find("div", attrs={"class":"fotoanime"}):
                pic = i.get("src")
                rek = requests.get(pic).content
                #bot.send_photo(cet, rek)
            sinopsis = bes.find("div", attrs={"class":"infozingle"})
            for i in sinopsis.find_all("span"):
                sinop = i.get_text()
                resj += f"{sinop}\n"
            sinop = bes.find("div", attrs={"class":"sinopc"})
            for i in sinop.find_all("p"):
                resj += f"\n{i.get_text()}"
        else:
            bot.send_message(cet, req.status_code)
        resj += "\n\n1. Batch\n2. Episode\n\nPilih Download input angka:"
        na = bot.send_message(cet, resj)
        bot.register_next_step_handler(na,four, fin)
    except Exception as ex:
        bot.reply_to(msg, text="masukan pilihan dengan benar\n/cari")
        print("\ntipe salah: {}\nid: {}, nama: {}\n".format(ex,cet,msg.chat.first_name))
        
def four(msg,fin):
    try:
        cet = msg.chat.id
        tek = "".join(msg.text)
        res = []
        resj = ""
        n=1
        req = requests.get(fin, headers=headers)
        bes = bs(req.text, "html.parser")
        name = bes.find_all("a", attrs={"data-wpel-link":"internal"})
        if tek == "1":
            for i in name:
                lin = i["href"]
                if "-batch" in lin or "batch" in lin:
                    res.append(lin)
                    judl = i.string
                    resj += f"{n}. {judl}\n"
                    n+=1
            resj += "\nMasukan pilihan angka: "
        if tek == "2":
            for i in name:
                lin = i["href"]
                if "-ova-" in lin or "-sp-" in lin or "-special-" in lin or "-episode-" in lin:
                    res.append(lin)
                    judl = i.string
                    resj += f"{n}. {judl}\n"
                    n+=1
            resj += "\nMasukan pilihan angka: "
        else:
            pass
        na = bot.send_message(cet, resj)
        bot.register_next_step_handler(na,five,res)
    except Exception as ex:
        bot.reply_to(msg, "masukan pilihan yg benar\n\t/cari")
        print("tipe salah: {}\nid: {}, nama: {}\n".format(ex,cet,msg.chat.first_name))
def five(msg,res):
    try:
        cet = msg.chat.id
        rez = []
        rek = []
        resj = ""
        n=1
        url = res[int(msg.text)-1]
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            if "-batch" in url or "batch" in url:
                bes = bs(req.text, "html.parser")
                batc = bes.find("div", "batchlink")
                lili = batc.find("ul")
                for i in lili.find_all("li"):
                    link = i.find_all("a", attrs={"data-wpel-link":"external"})
                    for i in link:
                        lin = i["href"]
                        rez.append(lin)
                resj += "Pilih Download dari \n1. Acefile\n2. Racaty\n3. Mega\n4. Uptobox\n5. DesuDrive\n Input pilihan angka"
                na = bot.send_message(cet, resj)
                bot.register_next_step_handler(na, batch, rez)
            elif "-episode-" in url or "-ova-" in url or "-special-" in url or "-sp-" in url:
                bes = bs(req.text, "html.parser")
                link = bes.find("div", "download")
                li = link.find("ul")
                for i in li.find_all("li"):
                    name = i.find_all("a", attrs={"data-wpel-link":"external"})
                    for k in name:
                        lin = k["href"]
                        rek.append(lin)
                resj += "Pilih Download dari\n1. Zippyshare\n2. Racaty\n3. Acefile\n4. Mega\n5. Filesim\nBila mau streaming pilih zippyshare/mega\n Input pilihan angka "
                na = bot.send_message(cet, resj)
                bot.register_next_step_handler(na, pisode, rek)
        else:
            pass
    except Exception as ex:
        bot.reply_to(msg, "masukan pilihan yg benar\n/cari")
        print("tipe salah: {},\nid: {}, nama: {}\n".format(ex,cet,msg.chat.first_name))
def pisode(msg, rek):
    try:
        cet = msg.chat.id
        tek = int(msg.text)
        nam = []
        if tek > 5:
            bot.send_message(cet, "Out of range\n/cari")
        else:
            bot.reply_to(msg, "Here your link download\n")
            for i in rek:
                if tek == 1 and "zippyshare" in i:
                    nam.append(i)
                    bot.send_message(cet,i)
                elif tek == 2 and "racaty" in i:
                    nam.append(i)
                    bot.send_message(cet, i)
                elif tek == 3 and "acefile" in i:
                    nam.append(i)
                    bot.send_message(cet, i)
                elif tek == 4 and "mega.nz" in i:
                    nam.append(i)
                    bot.send_message(cet, i)
                elif tek == 5 and "filesim" in i:
                    nam.append(i)
                    bot.send_message(cet,i)
            if len(nam) == 0:
                bot.send_message(cet, "null\n ")
    except Exception as ex:
        bot.reply_to(msg, "Masukan pilihan dengan benar\n/cari")
        print("tipe salah: {}\nid: {}, nama: {}".format(ex,cet,msg.chat.first_name))
def batch(msg, rez):
    try:
        cet = msg.chat.id
        tek = int(msg.text)
        nam = []
        if tek > 5:
            bot.send_message(cet, "out of range\n/cari")
        else:
            bot.reply_to(msg, "Here your download link\n")
            for i in rez:
                if tek == 1 and "acefile" in i:
                    nam.append(i)
                    bot.send_message(cet, i)
                elif tek == 2 and "racaty" in i:
                    nam.append(i)
                    bot.send_message(cet, i)
                elif tek == 3 and "mega.nz" in i:
                    nam.append(i)
                    bot.send_message(cet, i)
                elif tek == 4 and "uptobox" in i:
                    nam.append(i)
                    bot.send_message(cet, i)
                elif tek == 5 and "desudrive" in i:
                    nam.append(i)
                    bot.send_message(cet, i)
            if len(nam) == 0:
                bot.send_message(cet,"null")
    except Exception as ex:
        bot.reply_to(msg, "Masukan pilihan dengan benar")
        print("tipe salah: {}\nid: {}, nama: {}".format(ex,cet,msg.chat.first_name))
if __name__ == "__main__":
    print("\n\tBOT.STARTED",date)
    print(bot.get_me())
    bot.get_updates()
    bot.infinity_polling(interval=0, timeout=20)
    #bot.polling()
    
