from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import re
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

        ### Открываем страницу NEO-FIT
        driver.get('https://s.n-fit.ru/?link=')
        sleep(2)

        ### Выбираем только групповые занятия
        button_group = driver.find_element(By.CLASS_NAME, 'groupClass')
        button_group.click()

        ### Выбираем только занятия для взрослых
        button_adult_timetable = driver.find_element(By.XPATH, '//*[@id="timetable"]/div/header/div[1]/a[1]')
        button_adult_timetable.click()

        ### Раскрываем всё расписание для парсинга
        button_more_timetable = driver.find_element(By.ID, 'show-more-lessons')
        button_more_timetable.click()

        ### Запаковывакм расписание в переменную в переменную
        schedule = driver.find_elements(By.CLASS_NAME, 'timetableEntries')

        ### Проходимся по ней итератором
        for i in schedule:
            data = i.text
            ### Удаляем ненужные слова
            first_result = re.sub('Групповой зал,  ', '', data)
            second_result = re.sub('Бойцовский зал,  ','',first_result)
        ### Отправляем сообщение с расписанием
        bot.send_message(message.chat.id, second_result)

        driver.close()
        driver.quit()


    @bot.message_handler(content_types=['text'])
    def button(message):
        if (message.text == 'Узнать расписание 🗒'):
            bot.send_message(message.chat.id, 'Хорошо')
        get_data(message)


    bot.infinity_polling(timeout=10, long_polling_timeout = 5)


