import telebot
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from newsapi import NewsApiClient
env_path = Path('.', 'API.env')
load_dotenv(dotenv_path=env_path)
telegram_key=os.getenv("PRIVATE_KEY")
NewsApiKey=os.getenv("NEWSAPIKEY")
newsapi = NewsApiClient(api_key=NewsApiKey)
bot=telebot.TeleBot(telegram_key)

def get_top_news(country):
    try:
        top_headlines = newsapi.get_top_headlines(page_size=5 ,country=country)
        articles=top_headlines.get('articles',[])
        if not articles:
            return ["No News for This country"]
        news=[]
        for article in articles:
            title=article.get('title','No title')
            url=article.get('url','')
            news.append(f"{title}\n{url}\n")
        return news
    except Exception as e:
        return[f"An error occured{str(e)}"]
@bot.message_handler(commands=['start','hello'])
def send_welcome(message):
    bot.reply_to(message,"Hi , i'm Hriday\n To get the latest news type a country code")
@bot.message_handler(func=lambda message:True)
def handle_message(message):
    country_code=message.text.strip().lower()
    news=get_top_news(country_code)
    bot.reply_to(message,"\n".join(news))
bot.infinity_polling(none_stop=True)