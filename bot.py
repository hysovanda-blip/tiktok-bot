import telebot, requests, os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bot is running!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = '9217613909:AAHV589DUCO2108DJRuNqNcWA06gvcQDYeA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message): bot.reply_to(message, "សួស្តី! សូមផ្ញើលីង TikTok ដើម្បីដោនឡូត។")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text
    if 'tiktok.com' in url or 'vt.tiktok.com' in url:
        bot.reply_to(message, "កំពុងដំណើរការ... ⏳")
        try:
            res = requests.get(f"https://www.tikwm.com/api/?url={url}").json()
            if res.get('code') == 0: bot.send_video(message.chat.id, res['data']['play'])
            else: bot.reply_to(message, "មិនអាចដោនឡូតបានទេ។")
        except: bot.reply_to(message, "មានបញ្ហាបច្ចេកទេស។")
    else: bot.reply_to(message, "សូមបញ្ជូនលីង TikTok អោយបានត្រឹមត្រូវ។")

if __name__ == "__main__":
    keep_alive()
    bot.polling(non_stop=True)
