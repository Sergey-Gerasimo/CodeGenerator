from docx import Document
import math 
from collections.abc import Iterable


def GetTable(stat: dict, sum_of_chars, *args, **kwargs) -> Iterable[tuple]: 
    id = 1
    table = [("№ п/п", "Символ", "Код символа", "Число вхождений символа в текст", "Вероятность вхождения символа (рi)", "Ii")]
    pv = 0 
    Isr = 0 
    for key in stat: 
        table += [tuple(map(str, (id, 
                                  key, 
                                  ord(key), 
                                  stat[key], 
                                  round(stat[key]/sum_of_chars, 5), 
                                  round(-math.log2(stat[key]/sum_of_chars),5))))]
        
        pv += stat[key]/sum_of_chars
        Isr += -math.log2(stat[key]/sum_of_chars) * stat[key]/sum_of_chars
        id += 1 

    table += [("", "", "Всего символов в тексте (K)", f"{sum_of_chars}", "", "")]
    table += [("", "", "", "Полная вероятность(Р)", f"{pv:.5f}", "")]
    table += [("", "", "", "", "Энтропия источника (Iср)", f"{Isr:.5f}")]
    
    return table

def CreateWordTable(table: Iterable[tuple], *args, **kwargs) -> Document: 
    doc = Document()
    WordTable = doc.add_table(0, len(table[0]))

    for row in table: 
        cell = WordTable.add_row().cells
        for i, item in enumerate(row):
            cell[i].text = item

    return doc 



