from flask import Flask, request, render_template
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as bs
import datetime
from pytz import timezone
import re, random, os, base64

api = '==QQ3NEVxF1c112YqxGOFFTOHZXOZ9mWfd0ash3auJzaNVUQBpjMxQTOyITMzETN'[::-1].encode("ascii")
apik = base64.b64decode(api).decode("ascii")
ua = ['Mozilla/5.0 (X11; CrOS x86_64 13310.76.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.108 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 11895.118.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.159 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12239.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.136 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13099.110.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.136 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13099.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.127 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13020.87.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.119 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12499.66.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.106 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13310.59.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.84 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12739.111.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12607.82.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.123 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 13099.85.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.110 Safari/537.36','Mozilla/5.0 (X11; CrOS x86_64 12607.58.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.86 Safari/537.36']
bot = telebot.TeleBot(apik, threaded=False)
idn = timezone("Asia/Jakarta")
now = datetime.datetime.now(idn)
global inbut 
inbut= types.InlineKeyboardMarkup()
inbut.add(types.InlineKeyboardButton(text="Cari lagi", callback_data="again"))
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
    log_bot = open('log_bot.txt', 'wb')
    log_bot.write(text_log)
    log_bot.close()
    
@bot.message_handler(commands=["start"])
def selamat_datang(msg):
    na = msg.chat.first_name
    ma = msg.chat.last_name
    cet = msg.chat.id
    print(f"welcome\nname: {na} {ma}")
    bot.reply_to(msg,f'{date}\nSelamat datang!!.\nNama: {na} {ma}, ID: {cet}\nSemoga bot ini bisa membantumu\ntipe /help untuk perintahnya\nAuthor: @rup_23\nFB: AC Putranto ')

@bot.message_handler(commands=["help"])
def helep(msg):
    cet = msg.chat.id
    bot.reply_to(msg, "Selamat datang!!!\nBot ini mempermudah kalian untuk mendownload anime otakudesu langsung menuju link download :-) Jadi gaperlu mencet kena iklan mulu -_-\nKedepanya admin akan mengupgrade bot download link, menjadi bot streaming Terima Kasih :)\ntype: /cari untuk memulai pencarian anime")

@bot.message_handler(commands=["cari"])
def main(msg):
    types.ReplyKeyboardRemove()
    cet = msg.chat.id
    na = bot.send_message(cet, "Mau cari anime apa? Tulis saja judulnya.\nexc: Nanatsu Taizai")
    #na = bot.send_photo(cet, open("beliau-ini.jpg", "rb"))
    bot.register_next_step_handler(na,two)
    
def two(msg):
    try:
        cet = msg.chat.id
        tek = "".join(msg.text)
        fname = msg.chat.first_name; lname = msg.chat.last_name
        teklog = f"NAMA = {fname} {lname}, ID = {cet}, cari_anime = {tek}\n"
        f = open('log_bot.txt', 'a')
        f.writelines(teklog)
        f.close()
        url = "https://otakudesu.video/?s={}&post_type=anime".format(tek)
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
            bot.reply_to(msg, "Pencarianmu tidak ada hasil", reply_markup=inbut)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=False)
            resj += "Hasil pencarianmu max 15\n"
            nam = bes.find_all("li", attrs={"style":"list-style:none;"})
            for i in nam:
                nam = i.find("a", attrs={"data-wpel-link":"internal"})
                cek.append(nam.string)
                res.append(nam["href"])
            res.reverse(), cek.reverse()
            for i in cek:
                key = types.KeyboardButton(f"{n}. {i}")
                markup.add(key)
                n+=1
            resj += "Pilih anime yg mana? atau ketik yg no brp:"
            na = bot.send_message(cet, resj, reply_markup=markup)
            bot.register_next_step_handler(na,three,res)
    except Exception as ex:
        bot.reply_to(msg, text="masukan pilihan yang benar", reply_markup=inbut)
        print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__.tb_lineno,msg.chat.first_name,cet))
        
def three(msg,res):
    try:
        cet = msg.chat.id
        c = re.search("\d+|$", msg.text)[0]
        fin = res[int(c)-1]
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
        bot.reply_to(msg, text="masukan pilihan dengan benar", reply_markup=inbut)
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
                    resj += f"{judl}\n"
                    n+=1
                    resj += "\nInput pilihanmu berdasarkan nomor: "
        elif tek == "Episode" or tek == "episode":
            for i in name:
                lin = i["href"]
                if "episode" in lin or "-ova-" in lin or "-sp-" in lin or "-special-" in lin or "-episode-" in lin:
                    res.append(lin)
                    judul.append(i.string)
            for j in judul:
                judull.insert(0,j)
            for j in judull:
                num = f"Episode {n}"
                key = types.KeyboardButton(num)
                markup.add(key)
                n+=1
            for r in res:
                ress.insert(0,r)
            resj += "\nPilih episode Berapa? atau ketik nomor eps: "                
        if len(resj) > 4500:
            bot.reply_to(msg, "Bot tidak dapat memuat, list episode terlalu banyak\nulangi /cari")
        else:
            na = bot.send_message(cet, resj, reply_markup=markup)
            bot.register_next_step_handler(na,five,ress)
    except Exception as ex:
        bot.reply_to(msg, "masukan pilihan yg benar", reply_markup=inbut)
        print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__.tb_lineno,msg.chat.first_name,cet))
        
def five(msg,ress):
    try:
        cet = msg.chat.id
        rez = []
        rek = []
        resj = ""
        n=1
        tek = re.findall("\d", msg.text); num = "".join(tek)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        url = ress[int(num)-1]
        req = ses.get(url, headers=headers)
        print(req.status_code)
        if req.status_code == 200:
            if "-batch" in url or "batch" in url:
                bes = bs(req.text, "html.parser")
                batc = bes.find("div", "batchlink")
                lili = batc.find_all("li");n=1
                resj += "Pilih Resolusi Download\n"
                for i,k in enumerate(lili):
                    rez.append(k)
                    markup.add(str(f"{n}. {k.find('strong').string}"));n+=1
                    #resj += f"{n}. {k.find('strong').string}\n";n+=1
                na = bot.send_message(cet, resj, reply_markup=markup)
                bot.register_next_step_handler(na, batch, rez)
            elif "episode" in url or"-episode-" in url or "-ova-" in url or "-special-" in url or "-sp-" in url:
                bes = bs(req.text, "html.parser")
                link = bes.find("div", "download")
                res = link.find_all("li");n=1
                resj += "Pilih Resolusi Download\n"
                for i,k in enumerate(res):
                    rek.append(k)
                    markup.add(str(f"{n}. {k.find('strong').string}"));n+=1
                na = bot.send_message(cet, resj, reply_markup=markup)
                bot.register_next_step_handler(na, pisode, rek)
        else:
            print(req)
            print("kobisa yhak asw")
            print(req.status_code)
    except Exception as ex:
        bot.reply_to(msg, "masukan pilihan yg benar", reply_markup=inbut)
        print("tipe salah: {}\ninline: {}\nnama: {}, id: {}".format(ex,ex.__traceback__.tb_lineno,msg.chat.first_name,cet))
        
def pisode(msg, rek):
    try:
        cet = msg.chat.id
        c = re.search("\d+|$", msg.text)[0]
        tek = int(c)-1
        isi = rek[tek]
        lin = []
        jdl = []
        #markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        if tek > len(rek):
            bot.send_message(cet, "Out of range\n/cari")
        else:
            n=1
            _res = "Pilih Download dari/Streaming\nBila streaming rekomen zippyshare/filesim\n\n"
            for i in isi.find_all("a", attrs={"data-wpel-link":"external"}):
                lin.append(i["href"]); jdl.append(i.string)
            key = types.InlineKeyboardMarkup()
            key.width=len(lin)
            [key.add(types.InlineKeyboardButton(text=i, url=x)) for i,x in zip(jdl,lin)]
            key.add(
                types.InlineKeyboardButton(text="Done", callback_data="done"),
                types.InlineKeyboardButton(text="Again", callback_data="again")
            )
            bot.send_message(cet,"Here Your download link\nMau streaming dari Mega juga bisa.",reply_markup=key)
                #_res += f"{n}. {i.string}\n"
                #link = i["href"]
                #key = types.KeyboardButton(n)
                #markup.add(key)
                #lin.append(link)
                #n+=1
            #na = bot.send_message(cet,_res, reply_markup=markup)
            #bot.register_next_step_handler(na, dlepisode, lin)
    except Exception as ex:
        bot.reply_to(msg, "Masukan pilihan dengan benar",reply_markup=inbut)
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
        c = re.search("\d+|$", msg.text)[0]
        tek = int(c)-1
        isi = rez[tek]
        lin = []
        jdl = []
        rem = types.ReplyKeyboardRemove()
        if tek > len(rez):
            bot.send_message(cet, "Out of range\n/cari")
        else:
            n=1
            _res = "Pilih download dari\n"
            for i in isi.find_all("a", attrs={"data-wpel-link":"external"}):
                lin.append(i["href"])
                jdl.append(i.string)
            key = types.InlineKeyboardMarkup()
            key.width=len(lin)
            [key.add(types.InlineKeyboardButton(text=i,url=x)) for i,x in zip(jdl,lin)]
            key.add(
                types.InlineKeyboardButton(text="Done", callback_data="done"),
                types.InlineKeyboardButton(text="Again", callback_data="again"),
            )
            bot.send_message(cet,"Here Your download link",reply_markup=key)
                #key = types.KeyboardButton(n)
                #markup.add(key)
                #lin.append(link)
                #n+=1
            #na = bot.send_message(cet,_res, reply_markup=markup)
            #bot.register_next_step_handler(na, dlbatch, jdl, lin)
    except Exception as ex:
        bot.reply_to(msg, "Masukan pilihan dengan benar", reply_markup=inbut)
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


@bot.callback_query_handler(func=lambda call:True)
def kolbek(msg):
    if msg.message:
        rem = types.ReplyKeyboardRemove()
        cid = msg.message.chat.id
        firstnam = msg.message.chat.first_name;lasnam = msg.message.chat.last_name
        if msg.data == "again":
            main(msg.message)
            pass
        elif msg.data == "done":
            isi = f"<b>Thank You for using this bot! {firstnam} {lasnam}</b>\n<b>See source code <a href='https://github.com/aldyansyahcp/Ahagon_telegramBot'>Here</a></b>"
            bot.send_message(cid, text=isi, reply_markup=rem, parse_mode="HTML")
        else:
            pass

@app.route("/"+apik, methods=["POST", "GET"])
def getmew():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
       
@app.route("/", methods=["POST", "GET"])
def webhook():
    try:
        bot.remove_webhook()
        bot.set_webhook(url='https://ahagonbot-tele.herokuapp.com/' + apik)
        res = "<h1><center><b>BOT STARTED</b></center></h1>", 200
    except Exception as e:
        res = "<h1>False</h1><br>{}".format(e), 404
    return res
    
if __name__ == "__main__":
    print("\n\tBOT.STARTED",date)
    print(bot.get_me(),"\n")
    #bot.remove_webhook()
    #bot.infinity_polling(interval=0, timeout=20)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
