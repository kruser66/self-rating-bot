import logging

from telebot import TeleBot, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

import services.config as config
from services.keyboards import start_keyboard, answers_keyboard, cancel_keyboard
from services.messages import (
    welcome_message,
    fetch_questions,
    bye_message,
    result_message,
    formatted_question
)


logger = logging.getLogger('self-rating-bot')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger.info('Запущен чат-бот "Самооценка"')

bot = TeleBot(config.BOT_TOKEN)

# Initial working with States
state_storage = StateMemoryStorage()
class QuestionStates(StatesGroup):
    start = State()
    finish = State()

bot.add_custom_filter(custom_filters.StateFilter(bot))


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):  
    
    logging.info(f'Пользователь: {message.chat.id} открыл бот.')

    bot.send_message(
        chat_id=message.chat.id,
        text=welcome_message(), 
        reply_markup=start_keyboard()
    )
    bot.set_state(message.chat.id, QuestionStates.start)
    bot.add_data(
        user_id=message.chat.id,
        chat_id=message.chat.id,
        state='start',
        questions=iter(fetch_questions()),
        total_points=0
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('ask_questions'))
def ask_questions(call):

    point = int(call.data.split('_')[-1])

    with bot.retrieve_data(call.from_user.id, call.from_user.id) as data:
        if data['state'] == 'start':
            logging.info(f'Пользователь: {call.from_user.id} - начал тест')
            data['state'] = 'process'
        
        data['total_points'] += point

        try:
            bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.id,
                text=formatted_question(next(data['questions'])), 
                reply_markup=answers_keyboard()
            )
        except StopIteration:
            total_points = data['total_points']     
            bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.id,
                text=result_message(total_points),
                reply_markup=cancel_keyboard()
            )
            logging.info(f'Пользователь: {call.from_user.id} - завершил тест')

    
@bot.callback_query_handler(func=lambda call: call.data=='cancel')
def cancel(call):

    bot.send_message(
        chat_id=call.from_user.id,
        text=bye_message(), 
    )

bot.infinity_polling()