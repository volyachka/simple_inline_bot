import telebot
from telebot import types

TOKEN = ''

bot = telebot.TeleBot(TOKEN)  # инициализируем нашего бота

user_id_and_user_name = dict()
chat_id = str()


@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    first_name = message.new_chat_members[0].first_name
    bot.send_message(message.chat.id, "Добро пожаловать, как дела {0}!".format(first_name))
    user_id_and_user_name[message.new_chat_members[0].username] = message.new_chat_members[0].id
    global chat_id
    chat_id = message.chat.id


@bot.message_handler(content_types=["text"])
def first(message):
    username = message.from_user.username
    print(username)
    print(user_id_and_user_name)

    if username not in user_id_and_user_name.keys():
        first_name = message.from_user.first_name
        bot.send_message(message.chat.id, "Добро пожаловать, {0}!".format(first_name))
        user_id_and_user_name[username] = message.from_user.id
        global chat_id
        chat_id = message.chat.id

    if message.text[:3] == 'ban':
        ban_user(message.text[4:])
        return

    if message.text[:5] == 'unban':
        unban_user(message.text[6:])
        return

    if message.text[:8] == 'do_admin':
        do_admin(message.text[9:])
        return

    if message.text[:14] == 'get_statistics':
        get_statistics(message.text[15:])
        return
    if message.text[:8] == 'quit_bot':
        quit_bot(message.text[9:])
        return


def ban_user(username):
    try:
        bot.ban_chat_member(chat_id=chat_id, user_id=user_id_and_user_name[username])
        bot.send_message(chat_id=chat_id, text="Пользователь " + str(username) + " Забанен")
    except Exception as e:
        bot.send_message(chat_id=chat_id, text='can not ban ' + str(username))
        bot.send_message(chat_id=chat_id, text='no rights or invalid nick, please check')
    return


def unban_user(username):
    try:
        bot.unban_chat_member(chat_id=chat_id, user_id=user_id_and_user_name[username])
        bot.send_message(chat_id=chat_id, text="Пользователь " + str(username) + " Разбанен")
    except Exception as e:
        bot.send_message(chat_id=chat_id, text='can not unban ' + str(username))
        bot.send_message(chat_id=chat_id, text='no rights or invalid nick, please check')
    return


def do_admin(username):
    try:
        is_admin = bot.promote_chat_member(chat_id, user_id_and_user_name[username], True, True, True)
        if (is_admin):
            bot.send_message(chat_id=chat_id, text="Пользователь " + str(username) + "  администратор")
        else:
            bot.send_message(chat_id=chat_id, text="Пользователь " + str(username) + "  не смог стать администратором")
            bot.send_message(chat_id=chat_id, text='no rights or invalid nick, please check')
        print(is_admin)
    except Exception as e:
        bot.send_message(chat_id=chat_id, text="Пользователь " + str(username) + "  не смог стать администратором")
        bot.send_message(chat_id=chat_id, text='no rights or invalid nick, please check')


def get_statistics(username):
    try:
        number_of_people = bot.get_chat_member_count(chat_id)
        bot.send_message(chat_id, 'Количество людей в чате: ' + str(number_of_people))
        bot.send_message(chat_id, 'Администраторы чата: ')
        chat_admins = bot.get_chat_administrators(chat_id)
        for admins in chat_admins:
            userName = admins.user.username
            bot.send_message(chat_id, str(userName))
    except Exception as e:
        bot.send_message(chat_id=chat_id, text='Произошла ошибка')
    return


def quit_bot(username):
    try:
        bot.leave_chat(chat_id)
    except Exception as e:
        bot.send_message(chat_id=chat_id, text='Бот не смог выйти, откройте дверь :(')


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    r_ban = types.InlineQueryResultArticle(
        id='1', title="Забанить",
        description="Введите ник пользователя",
        input_message_content=types.InputTextMessageContent(
            message_text='ban ' + query.query),
    )

    r_unban = types.InlineQueryResultArticle(
        id='2', title="Разбанить",
        description="Введите ник пользователя",
        input_message_content=types.InputTextMessageContent(
            message_text='unban ' + query.query),
    )

    r_admin = types.InlineQueryResultArticle(
        id='3', title="Сделать админом",
        description="Введите ник пользователя",
        input_message_content=types.InputTextMessageContent(
            message_text='do_admin ' + query.query),
    )

    r_statistics = types.InlineQueryResultArticle(
        id='4', title="Посмотреть статистику по каналу",
        description="Введите ник пользователя",
        input_message_content=types.InputTextMessageContent(
            message_text='get_statistics ' + query.query),
    )

    r_quit = types.InlineQueryResultArticle(
        id='5', title="Прогнать бота из канала",
        description="Введите ник пользователя",
        input_message_content=types.InputTextMessageContent(
            message_text='quit_bot ' + query.query),
    )

    bot.answer_inline_query(query.id, [r_ban, r_unban, r_admin, r_statistics, r_quit], cache_time=2147483646)


bot.polling(none_stop=True, interval=0)  # запускаем нашего бота
