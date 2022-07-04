from flask import Flask, request, render_template
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as bs
import datetime
import re, random, os


api = "5131229412:AAEMk2nkxlkG_ZoY9vG91E8ljcmusQqTCwA"
ua = ['Mozilla/5.0 (X11; CrOS x86_64 13310.76.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.108 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 11895.118.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.159 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12239.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.136 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13099.110.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.136 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13099.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.127 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13020.87.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.119 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12499.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.106 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13310.59.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.84 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12739.111.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12607.82.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.123 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13099.85.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.110 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12607.58.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.86 Safari/537.36']
bot = telebot.TeleBot(api, threaded=False)
now = datetime.datetime.now()
ses = requests.Session()
date = now.strftime("%B-%d-%Y, %H:%M")
headers = {
      'User-Agent': random.choice(ua),
      'Cache-Control':'max-age=0'
}
#secret = "DEVOURER789"
#bot.set_webhook("https://alcep.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)

def login(msg):                                                             
    firstnam = msg.chat.first_name;lasnam = msg.chat.last_name
    cet = msg.chat.id;coman = msg.text                                                     
    text_log = (f'command: {coman}, id: {cet} {firstnam} {lasnam} \n')
    log_bot = open('log_bot.txt', 'a')
    log_bot.write(text_log)
    login(msg)
@bot.message_handler(commands=["start"])
def selamat_datang(msg):
    na = msg.chat.first_name
    ma = msg.chat.last_name
    cet = msg.chat.id
    print(f"welcome\nname: {na} {ma}")
    bot.reply_to(msg,f'{date}\nようこそ {na} {ma} id: {cet} i hope you will enjoyed in here\nThie Bot Created with Python\ntype /help for the command\nAuthor: @rup_23\nFB: Rere Kurniawan')

@bot.message_handler(commands=["help"])
def helep(msg):
    cet = msg.chat.id
    bot.reply_to(msg, "Selamat datang!!!\nBot ini mempermudah kalian untuk mendownload anime otakudesu langsung menuju link download :-) Jadi gaperlu mencet kena iklan mulu -_-\nKedepanya admin akan mengupgrade bot download link, menjadi bot streaming Terima Kasih :)\ntype: /cari untuk memulai pencarian anime")

@bot.message_handler(commands=["cari"])
def main(msg):
    types.ReplyKeyboardRemove()
    cet = msg.chat.id
    na = bot.send_message(cet, "Mau cari anime apa?\nexc: Nanatsu Taizai")
    bot.register_next_step_handler(na,two)
    
def two(msg):
    try:
        cet = msg.chat.id
        tek = "".join(msg.text)
        url = "https://otakudesu.watch/?s={}&post_type=anime".format(tek)
        resj = ""
        print("\t\nNAME: {}\nDATE: {}\nTITTLE: {}\n".format(msg.chat.first_name,date,tek))
        res = []
        cek = []
        n=1
        req = ses.get(url, headers=headers)
        #print(end=f"\n\t{headers['User-Agent']}\n")
        bes = bs(req.text, "html.parser")
        nam = bes.find("li", attrs={"style":"list-style:none;"})
        if nam is None:
            bot.reply_to(msg, "Pencarianmu tidak ada hasil\ncoba lain /cari")
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
            resj += "Hasil pencarianmu max 15\n\n"
            nam = bes.find_all("li", attrs={"style":"list-style:none;"})
            for i in nam:
                nam = i.find("a", attrs={"data-wpel-link":"internal"})
                cek.append(nam.string)
                res.append(nam["href"])
            """jvdl = [i.find("a", attrs={"data-wpel-link":"internal"}) for i in nam]
            print(jvdl)"""
            cek.reverse(); res.reverse()
            for i in cek:
                key = types.KeyboardButton(n)
                markup.add(key)
                resj += f"{n}. {i}\n"
                n+=1
            resj += "\nInput pilihanmu berdasarkan nomor:"
            na = bot.send_message(cet, resj, reply_markup=markup)
            bot.register_next_step_handler(na,three,res)
    except Exception as ex:
        bot.reply_to(msg, text="masukan pilihan yang benar\n/cari")
        print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__.tb_lineno,msg.chat.first_name,cet))
        
def three(msg,res):
    try:
        cet = msg.chat.id
        fin = res[int(msg.text)-1]
        nam = msg.chat.first_name
        resj = ""
        rez = []
        cek = []
        n=1
        req = ses.get(fin,headers=headers)
        if req.status_code == 200:
            bes = bs(req.text, "html.parser")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            for i in bes.find("div", attrs={"class":"fotoanime"}):
                pic = i.get("src")
                rek = ses.get(pic,headers=headers).content
                bot.send_photo(cet, rek)
            _info = bes.find("div", attrs={"class":"infozingle"})
            for k in _info.find_all("span"):
                resj += f"{k.get_text()}\n"
                cek.append(k.get_text())
            sinop = bes.find("div", attrs={"class":"sinopc"})
            for i in sinop.find_all("p"):
                resj += f"\n{i.get_text()}"
        else:
            bot.send_message(cet, req.status_code)
        if "Completed" in str(cek):
            key = types.KeyboardButton("Batch")
            markup.add(key)
        else:
            resj += "\nAnime onGoing batch belum rilis\n"
        key = types.KeyboardButton("Episode")
        markup.add(key)
        resj += "\n\nPilih Download Batch atau Perepisode"
        na = bot.send_message(cet, resj, reply_markup=markup)
        bot.register_next_step_handler(na,four, fin)
    except Exception as ex:
        bot.reply_to(msg, text="masukan pilihan dengan benar\n/cari")
        print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__.tb_lineno,msg.chat.first_name,cet))
        
def four(msg,fin):
    try:
        cet = msg.chat.id
        tek = "".join(msg.text)
        res = []
        ress = []
        judul = []
        judull = []
        resj = ""
        n=1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        req = ses.get(fin, headers=headers)
        bes = bs(req.text, "html.parser")
        name = bes.find_all("a", attrs={"data-wpel-link":"internal"})
        if tek == "batch" or tek == "Batch":
            for i in name:
                lin = i["href"]
                if "batch" in lin or "-batch-" in lin:
                    ress.append(lin)
                    num = f"Batch {n}"
                    key = types.KeyboardButton(num)
                    markup.add(key)
                    judl = i.string
                    resj += f"{n}. {judl}\n"
                    n+=1
                    resj += "\nInput pilihanmu berdasarkan nomor: "
                else:
                    pass
        elif tek == "Episode" or tek == "episode":
            for i in name:
                lin = i["href"]
                if "-ova-" in lin or "-sp-" in lin or "-special-" in lin or "-episode-" in lin:
                    res.append(lin)
                    judul.append(i.string)
            for j in judul:
                judull.insert(0,j)
            for j in judull:
                resj += f"{n}. {j}\n"
                num = f"Episode {n}"
                key = types.KeyboardButton(num)
                markup.add(key)
                n+=1
            for r in res:
                ress.insert(0,r)
            resj += "\nInput pilihanmu berdasarkan nomor: "                
        else:
            bot.send_message(cet,"Pilihanmu tidak ada ")
        if len(resj) > 4500:
            bot.reply_to(msg, "Bot tidak dapat memuat, list episode terlalu banyak\nulangi /cari")
        else:
            na = bot.send_message(cet, resj, reply_markup=markup)
            bot.register_next_step_handler(na,five,ress)
    except Exception as ex:
        bot.reply_to(msg, "masukan pilihan yg benar\n\t/cari")
        print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__.tb_lineno,msg.chat.first_name,cet))
        
def five(msg,ress):
    try:
        cet = msg.chat.id
        rez = []
        rek = []
        resj = ""
        n=1
        tek = re.findall("\d", msg.text); num = "".join(tek)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        url = ress[int(num)-1]
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            if "-batch" in url or "batch" in url:
                bes = bs(req.text, "html.parser")
                batc = bes.find("div", "batchlink")
                lili = batc.find_all("li");n=1
                resj += "Pilih Resolusi Download\n"
                for i,k in enumerate(lili):
                    rez.append(k)
                    markup.add(str(n))
                    resj += f"{n}. {k.find('strong').string}\n";n+=1
                na = bot.send_message(cet, resj, reply_markup=markup)
                bot.register_next_step_handler(na, batch, rez)
            elif "-episode-" in url or "-ova-" in url or "-special-" in url or "-sp-" in url:
                bes = bs(req.text, "html.parser")
                link = bes.find("div", "download")
                res = link.find_all("li");n=1
                resj += "Pilih Resolusi Download\n\n"
                for i,k in enumerate(res):
                    rek.append(k)
                    markup.add(str(n))
                    resj += f"{n}. {k.find('strong').string}\n";n+=1
                na = bot.send_message(cet, resj, reply_markup=markup)
                bot.register_next_step_handler(na, pisode, rek)
        else:
            print(req)
    except Exception as ex:
        bot.reply_to(msg, "masukan pilihan yg benar\n/cari")
        print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__.tb_lineno,msg.chat.first_name,cet))
        
def pisode(msg, rek):
    try:
        cet = msg.chat.id
        tek = int(msg.text)-1
        isi = rek[tek]
        lin = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        if tek > len(rek):
            bot.send_message(cet, "Out of range\n/cari")
        else:
            n=1
            _res = "Pilih Download dari/Streaming\nBila streaming rekomen zippyshare/filesim\n\n"
            for i in isi.find_all("a", attrs={"data-wpel-link":"external"}):
                _res += f"{n}. {i.string}\n"
                link = i["href"]
                key = types.KeyboardButton(n)
                markup.add(key)
                lin.append(link)
                n+=1
            na = bot.send_message(cet,_res, reply_markup=markup)
            bot.register_next_step_handler(na, dlepisode, lin)
    except Exception as ex:
        bot.reply_to(msg, "Masukan pilihan dengan benar\n/cari")
        print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__.tb_lineno,msg.chat.first_name,cet))
        
def dlepisode(msg, lin):
    cet = msg.chat.id
    fin = lin[int(msg.text)-1]
    res = "Here your link download\n\n"
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(text="open link", url=fin))
    bot.reply_to(msg, res,reply_markup=markup)
    
def batch(msg, rez):
    try:
        cet = msg.chat.id
        tek = int(msg.text)-1
        isi = rez[tek]
        lin = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        if tek > len(rez):
            bot.send_message(cet, "Out of range\n/cari")
        else:
            n=1
            _res = "Pilih download dari\n"
            for i in isi.find_all("a", attrs={"data-wpel-link":"external"}):
                _res += f"{n}. {i.string}\n"
                link = i["href"]
                key = types.KeyboardButton(n)
                markup.add(key)
                lin.append(link)
                n+=1
            na = bot.send_message(cet,_res, reply_markup=markup)
            bot.register_next_step_handler(na, dlbatch, lin)
    except Exception as ex:
        bot.reply_to(msg, "Masukan pilihan dengan benar\n/cari")
        print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__.tb_lineno,msg.chat.first_name,cet))
        
def dlbatch(msg, lin):
    try:
        cet = msg.chat.id
        fin = lin[int(msg.text)-1]
        res = "=====Here your download link=====\n\n"
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton(text="open link", url=fin))
        bot.reply_to(msg, res,reply_markup=markup)
    except Exception as ex:
            bot.reply_to(msg, "Masukan pilihan dengan benar\n/cari")
            print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__,tb_lineno,msg.chat.first_name,cet))

@app.route("/"+api, methods=["POST", "GET"])
def getmew():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
       
@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ahagontele-test.herokuapp.com/' + api)
    return "!", 200
    
if __name__ == "__main__":
    print("\n\tBOT.STARTED",date)
    print(bot.get_me(),"\n")
    #bot.get_updates()
    #bot.infinity_polling(interval=0, timeout=20)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
