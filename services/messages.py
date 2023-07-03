from textwrap import dedent
from telebot.formatting import format_text


def fetch_questions():
    
    with open('files/self-rating.txt', 'r', encoding='utf-8') as f:
        questions = f.readlines()
        
    return questions


def welcome_message():
    return  dedent(
            """        
            Привет, хочешь узнать свою самооценку?
            
            * 32 вопроса и 5 вариантов ответа.
            
            * Будьте максимально честны с собой.
            
            (разработано по методике С.В. Ковалёва)
             
            """
        )


def formatted_question(question):
    return dedent(
        f'''
        Выберите один из вариантов ответов:
        1️⃣ - Никогда
        2️⃣ - Редкo
        3️⃣ - Иногда
        4️⃣ - Часто
        5️⃣ - Очень часто
                
        Вопрос:
        {question}
         
        '''
    )


def bye_message():
    return 'До скорых встреч и всего наилучшего'


def result_message(total_point):
    
    if total_point <= 25:
        total_description = '''
        У Вас высокий уровень самооценки.
        
        Вас не гложат сомнения в себе и своих поступках.
        Вы адекватно реагируете на замечания других и трезво оцениваете свои действия.
        '''
    elif 25 < total_point <= 45:
        total_description = '''
        У Вас средний уровень самооценки.
        
        Вы иногда можете ощущать необъяснимую неловкость в общении с другими людьми.
        Нередко недооцениваете себя и свои способности, хотя веских оснований для этого нет.
        '''
    elif 45 < total_point:
        total_description = '''
        У Вас низкий уровень самооценки.
            
        Вы часто болезненно переносите критику в свой адрес.
        Стараетесь подстроиться под других людей.
        Страдаете от избыточной застенчивости.
        '''

    return dedent(
        f'''
        Спасибо, что прошли опросник до конца!
        
        Ваш результат: {total_point}
        
        Расшифровка:
        {total_description}
        '''
    )