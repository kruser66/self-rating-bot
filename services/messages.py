import yaml
from textwrap import dedent
from telebot.formatting import format_text, hitalic, hbold


def fetch_questions(filename='files/self-rating.txt'):
    '''Получаем список вопросов из файла txt'''    
    with open(filename, 'r', encoding='utf-8') as f:
        questions = f.readlines()
        
    return questions


def fetch_data_from_yaml(filename):
    '''Получаем список вопросов с ответами из файла yaml'''
    with open(filename, 'r', encoding='utf-8') as f:
        questions = f.read()
        
    return list(yaml.load_all(questions, Loader=yaml.Loader))
 


def welcome_message():
    return  dedent(
            """        
            Привет, хочешь узнать свою самооценку?
            
            * 15 вопросов и 4 варианта ответов.
            
            * Будьте максимально честны с собой.
            
            -----
            Разработано 
            для Центра нестандартной психологии
            "Сомагенез"
            
            PS: Ищите и читайте нас в социальных сетях.            
            """
        )


def formatted_question(question):
    '''Для вопосов с однотипными ответами'''
    return format_text(
        hitalic('Выберите один из вариантов ответов:'),
        '1️⃣ - Никогда',
        '2️⃣ - Редкo',
        '3️⃣ - Иногда',
        '4️⃣ - Часто',
        '5️⃣ - Очень часто',
        '\n',        
        hitalic('Вопрос:'),
        question,
    )


def formatted_question_with_answers(question, answers):
    
    emodji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
    
    answers_with_emodji = ''
    for emodji, answer in zip(emodji_numbers, answers):
        answers_with_emodji += f'{emodji} - {answer}\n'
    
    return format_text(            
        hitalic('Вопрос:'),
        question,
        '\n',
        hitalic('Варианты ответов:'),
        answers_with_emodji,
        '\n'
    )


def bye_message():
    
    return format_text(
        'До скорых встреч и всего наилучшего!',
        '\n',
        'Чтобы повторно пройти тест нажмите /start',
        'Ищите и читайте нас в социальных сетях:',
        )


def crash_message():
    
    return format_text(
        'Что-то пощло не так ☹️',
        '\n',
        'Попробуйте начать сначала /start',
        '\n',
        'Ищите и читайте нас в социальных сетях:'
        )


def result_message(total_point):

    rating_results = fetch_data_from_yaml(filename='files/self-rating-total.yaml')
    
    for rating in rating_results:
        min_rate, max_rate = rating['rating']
        if total_point in range(min_rate, max_rate + 1):
            
            return format_text(
                'Спасибо, что прошли опросник до конца!',
                '\n'
                f'Ваш результат: {total_point}',
                '\n',
                hbold(rating['result']),
                '\n',
                rating['description']
            )