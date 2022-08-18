from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import telebot
from telebot import types

from auth import TOKEN

from time import sleep



def start_bot():
    bot = telebot.TeleBot(token=TOKEN)




    @bot.message_handler(commands=['start'])
    def send_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        schedule_btn = types.KeyboardButton('Узнать расписание 🗒')
        markup.add(schedule_btn)
        bot.send_message(message.chat.id, 'Привет, вот что ты можешь сделать:', reply_markup=markup)


    @bot.message_handler(commands=['/schedule'])
    def get_data(message):
        options = Options()
        options.add_argument('--no-sandbox')
        options.headless = True
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())
                                  , options=options)

        bot.send_message(message.chat.id, 'Звоню в неофит')

        driver.get('https://s.n-fit.ru/?link=')

        sleep(3)
        button_more_timetable = driver.find_element(By.ID, 'show-more-lessons')
        button_more_timetable.click()

        schedule = driver.find_elements(By.CLASS_NAME, 'timetableEntries')

        for i in schedule:
            data = i.text

        bot.send_message(message.chat.id, data)

        driver.close()
        driver.quit()


    @bot.message_handler(content_types=['text'])
    def button(message):
        if (message.text == 'Узнать расписание 🗒'):
            bot.send_message(message.chat.id, 'Хорошо')
        get_data(message)


    bot.polling()
