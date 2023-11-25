import sys

LANGUAGE = 'АВБГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789.,:;- ('


def GetStatistic(path_to_file: str) -> dict: 
    """ Функция для сбора сатистики по файлу"""
    try:
        with open(path_to_file, "r", encoding='utf-8') as file:
            text = ''
            for i in file:
                text += i.upper()
    except: 
        print("Сбор статистики: Ошибка при декодировании текстового файла", file=sys.stderr)
        exit(-1)

    sum_of_chars = 0 
    stat = [] 

    for char in LANGUAGE:
        count = text.count(char)
        if not count: 
            print("Сбор статистики: Текст не содержет всех символов алфавита", file=sys.stderr)
            exit(-1)

        stat += [(char, count)]
        sum_of_chars += stat[-1][1]
    
    else: 
        return dict(stat), sum_of_chars 

    
    
    