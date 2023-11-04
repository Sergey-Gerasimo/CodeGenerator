LANGUAGE = 'АВБГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789.,:;- ('


def GetStatistic(path_to_file: str) -> dict: 
    """ Функция для сбора сатистики по файлу"""


    with open(path_to_file, "r", encoding='utf-8') as file:
        text = ''
        for i in file:
            text += i.upper()

    sum_of_chars = 0 
    stat = [] 

    for char in LANGUAGE:
        stat += [(char, text.count(char))]
        sum_of_chars += stat[-1][1]
    
    else: 
        return dict(stat), sum_of_chars 

    
    
    