from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    '''Стартовая inline клавиатура'''
    return  InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Начать', callback_data='ask_questions_0'),
                InlineKeyboardButton('Не хочу', callback_data='cancel')
            ],
        ]
    )


def cancel_keyboard():
    '''inline клавиатура при окончании работы'''
    return  InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('До свидания', callback_data='cancel')],
        ]
    )

def answers_keyboard():
    '''Основая inline клавиатера для ответов '''
    return InlineKeyboardMarkup(
        row_width=2,
        keyboard=[
            [
                InlineKeyboardButton('1️⃣', callback_data='ask_questions_0'),
                InlineKeyboardButton('2️⃣', callback_data='ask_questions_1'),
                InlineKeyboardButton('3️⃣', callback_data='ask_questions_2'),
                InlineKeyboardButton('4️⃣', callback_data='ask_questions_3'),
                InlineKeyboardButton('5️⃣', callback_data='ask_questions_4'),
            ],
            [InlineKeyboardButton('Закончить', callback_data='cancel')],

        ]
    )
    