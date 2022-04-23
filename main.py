import telebot
from datetime import datetime
from config import token, choose, events_soon, admin_chat_id
from database import BotDB


bot = telebot.TeleBot(token)
botdb = BotDB("database.db")
botdb.create_table_users()
botdb.create_table_records()


@bot.message_handler(commands=["start"])
def get_info(message):
    """Приветственное сообщение при запуске бота (проводится проверка на наличие пользователя в базе)"""
    if (not botdb.user_exists(message.from_user.id)):
        botdb.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)

    markup_inline = telebot.types.InlineKeyboardMarkup()
    item_yes = telebot.types.InlineKeyboardButton(text="Да", callback_data="yes")
    item_no = telebot.types.InlineKeyboardButton(text="Еще нет", callback_data="no")
    markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, f"Приветствуем вас, {message.chat.first_name}! \n"
        f"Мы рады видеть вас в Мята Cyber lounge! 🍃 \n"
        f"Здесь вы можете бронировать столы, видеть анонсы мероприятий и заказывать еду, а так же узнавать о новостях Мяты) \n"
        f"Уже бывали у нас в гостях?", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "yes":
        markup_reply = telebot.types.InlineKeyboardMarkup(row_width=1)
        hookah = telebot.types.InlineKeyboardButton(text="Кальян", callback_data="hookah")
        food_drink = telebot.types.InlineKeyboardButton(text="Еда, напитки", callback_data="food_drink")
        events = telebot.types.InlineKeyboardButton(text="Мероприятия", callback_data="events")
        table_games = telebot.types.InlineKeyboardButton(text="Настольные игры", callback_data="table_games")
        service = telebot.types.InlineKeyboardButton(text="Сервис", callback_data="service")
        video_games = telebot.types.InlineKeyboardButton(text="Компьютеры, Sony PC", callback_data="video_games")
        markup_reply.add(hookah, food_drink, events, table_games, service, video_games)

        bot.send_message(call.message.chat.id, f"Спасибо, что выбираете нас! "
                                               f"Что вам нравится у нас больше всего?", reply_markup=markup_reply)

    elif call.data == "no":
        bot.send_message(call.message.chat.id, f"🍃Ждем вас в гости, наш адрес:\n"
            f"Тюменский ЦУМ, отдельный вход с пересечения улиц Герцена-Орджоникидзе!\n\n"
            f"Слева в нижнем углу есть кнопка МЕНЮ, там вы можете забронировать стол, заказать еду, посмотреть график мероприятий или просто написать нам)\n\n"
            f"До встречи)")

    elif call.data in choose:
        bot.send_message(call.message.chat.id, f"Спасибо за ответ! \n"
            f"Слева в нижнем углу есть кнопка МЕНЮ, там вы можете забронировать стол, заказать еду, посмотреть график мероприятий и просто написать нам)\n\n"
            f"Будем рады видеть вас снова)")

    elif call.data in events_soon.keys():
        markup_reply = telebot.types.InlineKeyboardMarkup(row_width=1)
        event_yes = telebot.types.InlineKeyboardButton(text="Да", callback_data="event_yes")
        event_no = telebot.types.InlineKeyboardButton(text="Нет", callback_data="event_no")
        markup_reply.add(event_yes, event_no)
        bot.send_message(call.message.chat.id, events_soon[call.data])
        bot.send_message(call.message.chat.id, "Забронировать стол?", reply_markup=markup_reply)
        global status, event
        status, event = "event", call.data

    elif call.data == "event_yes":
        markup_reply = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = telebot.types.KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
        markup_reply.add(button_phone)
        bot.send_message(call.message.chat.id, f"Оставьте ваш номер телефона, мы скоро вам перезвоним и подтвердим бронь)\n"
                                               f"(через сообщение, либо воспользовавшись формой ниже)", reply_markup=markup_reply)

    elif call.data == "event_no":
        bot.send_message(call.message.chat.id, f"Если вам интересно что-то другое - нажмите на кнопку Меню в левом нижнем углу.\n"
        f"Всегда рады вам у нас в гостях)")


@bot.message_handler(commands=["event_schedule"])
def event_schedule(message):
    """Корректировка ближайших мероприятий еженедельно"""
    markup_reply = telebot.types.InlineKeyboardMarkup(row_width=1)
    event_1 = telebot.types.InlineKeyboardButton(text="Мероприятие 1 (20.04.2022)", callback_data="event_1")
    event_2 = telebot.types.InlineKeyboardButton(text="Мероприятие 2 (22.04.2022)", callback_data="event_2")
    event_3 = telebot.types.InlineKeyboardButton(text="Мероприятие 3 (26.04.2022)", callback_data="event_3")
    markup_reply.add(event_1, event_2, event_3)
    bot.send_message(message.chat.id, "Ближайшие мероприятия", reply_markup=markup_reply)


@bot.message_handler(commands=["book_table"])
def book_table(message):
    markup_reply = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = telebot.types.KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    markup_reply.add(button_phone)
    bot.send_message(message.chat.id, f"Оставьте ваш номер телефона, мы скоро вам перезвоним и подтвердим бронь)\n"
                                      f"(через сообщение, либо воспользовавшись формой ниже)", reply_markup=markup_reply)
    global status, event
    status, event = "book_table", None


@bot.message_handler(commands=["delivery"])
def delivery(message):
    """Актуализировать ссылку на Мята Cyber lounge в Delivery Club"""
    bot.send_message(message.chat.id, "[Перейти в Delivery Club](https://www.delivery-club.ru/)", parse_mode="Markdown")


@bot.message_handler(commands=["make_event"])
def make_event(message):
    markup_reply = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = telebot.types.KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    markup_reply.add(button_phone)
    bot.send_message(message.chat.id, f"Оставьте ваш номер телефона, мы свяжемся с вами и уточним все детали \n"
                                      f"(через сообщение, либо воспользовавшись формой ниже)",
                     reply_markup=markup_reply)
    global status, event
    status, event = "make_event", None


@bot.message_handler(commands=["interior"])
def interior(message):
    """При необходимости актуализировать ссылку на Мята Cyber lounge в VK"""
    bot.send_message(message.chat.id, "[Посмотреть интерьер](https://m.vk.com/albums-211038382)", parse_mode="Markdown")


@bot.message_handler(commands=["location"])
def location(message):
    """При необходимости актуализировать ссылку на Мята Cyber lounge в 2gis"""
    bot.send_message(message.chat.id, "[Где мы находимся](https://2gis.ru/tyumen/firm/70000001050825242)", parse_mode="Markdown")


@bot.message_handler(commands=["review"])
def review(message):
    bot.send_message(message.chat.id, "Мы будем рады услышать ваше мнение о любых сторонах нашей работы")
    global status, event
    status, event = "review", None


@bot.message_handler(commands=["other"])
def other(message):
    global status, event
    status, event = "other", None


@bot.message_handler(commands=["getchatid"])
def chatid(message):
    bot.send_message(message.chat.id, f"{message.chat.id}")


@bot.message_handler(content_types=["contact"])
def write_phone(message):
    global status
    botdb.add_data(message.from_user.id, datetime.now(), status, message.contact.phone_number, event)
    bot.send_message(message.chat.id, "Ваш ответ получен, спасибо!")
    bot.send_message(admin_chat_id, f"user {message.from_user.first_name}\n"
                                    f"status {status}\n"
                                    f"phone {message.contact.phone_number}\n"
                                    f"event {event}")
    status = None


@bot.message_handler(content_types=["text"])
def get_text(message):
    try:
        global status
        if "admin" in message.text:
            to_chat_id, mess_text = message.text[6:].split("#")
            bot.send_message(to_chat_id, mess_text)

        if status is None:
            bot.send_message(message.chat.id, "Что Вас интересует? Воспользуйтесь кнопкой Меню")

        else:
            text = message.text
            botdb.add_data(message.from_user.id, datetime.now(), status, text, event)
            bot.send_message(message.chat.id, "Ваш ответ получен, спасибо!")

            bot.send_message(admin_chat_id, f"user {message.from_user.first_name}\n"
                                            # f"user_id {message.from_user.username}\n"
                                            f"chat {message.chat.id}\n"
                                            f"status {status}\n"
                                            f"text {text}\n"
                                            f"event {event}")
            status = None

    except Exception:
        bot.send_message(message.chat.id, "Что Вас интересует? Воспользуйтесь кнопкой Меню")


if __name__ == "__main__":
    bot.polling(none_stop=True)
