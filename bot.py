import logging

from telebot import TeleBot, custom_filters, types
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

import services.config as config
from services.tg_logging_handler import TelegramgLoggingHandler
from services.keyboards import start_keyboard, answers_keyboard, cancel_keyboard
from services.messages import (
    welcome_message,
    fetch_data_from_yaml,
    bye_message,
    result_message,
    formatted_question_with_answers,
    crash_message
)


logger = logging.getLogger('self-rating-bot')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
tg_log = logger.addHandler(
    TelegramgLoggingHandler(config.BOT_TOKEN, config.LOGGING_ID)
)
tg_log.setLevel(logging.INFO)

logger.info('Запущен чат-бот "Самооценка"')

bot = TeleBot(
    token=config.BOT_TOKEN,
    parse_mode='HTML',
    skip_pending=True
)

# Initial working with States
state_storage = StateMemoryStorage()
class QuestionStates(StatesGroup):
    start = State()
    finish = State()

bot.add_custom_filter(custom_filters.StateFilter(bot))


def display_user(from_user):

    return f'{from_user.username} ({from_user.first_name})'


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):  

    logging.debug(f'Пользователь: {display_user(message.from_user)} открыл бот.')

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
        questions=iter(fetch_data_from_yaml(filename='files/self-rating-qa.yaml')),
        total_points=0
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('ask_questions'))
def ask_questions(call):

    point = int(call.data.split('_')[-1])

    with bot.retrieve_data(call.from_user.id, call.from_user.id) as data:
        
        if data['state'] == 'start':
            logging.debug(f'Пользователь: {display_user(call.from_user)} - начал тест')
            data['state'] = 'process'
        
        data['total_points'] += point

        try:
            bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.id,
                text=formatted_question_with_answers(**next(data['questions'])), 
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
            logging.info(f'Результат: {display_user(call.from_user)} - {total_points}')
            bot.delete_state(call.from_user.id, call.from_user.id)     

   
@bot.callback_query_handler(func=lambda call: call.data=='cancel')
def cancel(call):

    bot.send_message(
        chat_id=call.from_user.id,
        text=bye_message(),
        reply_markup=cancel_keyboard() 
    )
    bot.delete_message(call.from_user.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data=='make_appointment')
def make_appointment(call):

    bot.answer_callback_query(call.id, 'Ваша заявка принята. Администратор с Вами свяжется в ближайшее время.')
    logging.info(f'Пользователь: {display_user(call.from_user)} - заявка на консультацию')


if config.DEV:
    bot.infinity_polling()

else:
    
    import fastapi
    import uvicorn
    app = fastapi.FastAPI(docs=None, redoc_url=None)


    @app.post(f'/{config.BOT_TOKEN}/')
    def process_webhook(update: dict):
        if update:
            update = types.Update.de_json(update)
            bot.process_new_updates([update])
        else:
            return 

    bot.remove_webhook()

    bot.set_webhook(
        url=f'https://kruser.site/{config.BOT_TOKEN}',
    )

    uvicorn.run(
        app,
        host='127.0.0.1',
        port=5050,
    ) 

