from docx import Document
import math 
from collections.abc import Any, Iterable
from openpyxl import Workbook
from Fano_Hartli import *

class Table(Workbook): 
    LANG = sorted('QWERTYUIOPLKJHGFDSAZXCVBNM')
    def __init__(self,stat:dict, sum_of_chars:int,*args, title:str='', **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ws1 = self.create_sheet("Часть1")
        self.ws2 = self.create_sheet("Часть2")
        self.ws3 = self.create_sheet("Часть3.1")
        self.ws3_2 = self.create_sheet("Часть3.2")
        self.title = title 
        self.setws1(stat, ["ID", "Символ", "Код символа", "Число вхождений символа в текст", "Вероятность вхождения символа (рi)", "Ii"], sum_of_chars)
        self.setws2(stat, ["ID", "Символ", "Вероятность", "Код"], sum_of_chars)
        self.setws3_1(stat, ["ID", "Символ", "Вероятность", "Код"], sum_of_chars)
        self.setws3_2(stat, ["Символы", "Вероятности"], sum_of_chars)


    def setws1(self, stat:dict, header:list, sum_of_chars:int): 
        stat_ = list(stat.items())
        stat_.sort(key=lambda x: x[1]/sum_of_chars)
        pv = 0 
        Isr = 0 
        self.ws1.append(header)
        for i in range(len(stat_)):
            char = stat_[i][0]
            count = stat_[i][1]
            self.ws1.append(list(map(str, (i+1, 
                                  char, 
                                  ord(char), 
                                  count, 
                                  count/sum_of_chars, 
                                  -math.log2(count/sum_of_chars)))))
            pv += count/sum_of_chars
            Isr += -math.log2(count/sum_of_chars) * count/sum_of_chars
            
        else: 
            self.ws1[f"C{i+2}"] = "Всего символов в тексте (K)"
            self.ws1[f"D{i+2}"] = sum_of_chars
            self.ws1[f"D{i+3}"] = "Полная вероятность(Р)"
            self.ws1[f"E{i+3}"] = pv
            self.ws1[f"E{i+4}"] = "Энтропия источника (Iср)"
            self.ws1[f"F{i+4}"] = Isr

    def setws2(self, stat:dict, header:list, sum_of_chars:int) -> None: 
        self.ws2.append(header)
        stat = list(stat.items())
        stat = list(map(lambda x: (x[0], x[1]/sum_of_chars), stat))
        stat.sort(key=lambda x: x[1], reverse=True)

        codes = get_Hartli(stat).dict
        Isr = 0 
        for i in range(len(stat)):
            char = stat[i][0]
            probab = stat[i][1]
            self.ws2.append([i+1, char, probab, codes[char]])
            Isr += -math.log2(probab) * probab

        else: 
            self.ws2[f"A{i+2}"] = "Значение средней информации в битах"
            self.ws2[f"B{i+2}"] = Isr

    def setws3_1(self, stat:dict, header:list, sum_of_chars:int) -> None: 
        self.ws3.append(header)
        stat = list(stat.items())
        stat = list(map(lambda x: (x[0], x[1]/sum_of_chars), stat))
        stat.sort(key=lambda x: x[1], reverse=True)

        codes = get_Haffman(stat).dict
        Isr = 0 
        for i in range(len(stat)):
            char = stat[i][0]
            probab = stat[i][1]
            self.ws3.append([i+1, char, probab, codes[char]])
            Isr += -math.log2(probab) * probab
        else: 
            self.ws2[f"A{i+2}"] = "Значение средней информации в битах"
            self.ws2[f"B{i+2}"] = Isr

    def setws3_1(self, stat:dict, header:list, sum_of_chars:int) -> None:
        self.ws3_2.append(header)
        self.ws3_2.merge_cells('A1:A2')
        self.ws3_2.merge_cells('B1:B2')
        
        stat = list(stat.items())
        stat = list(map(lambda x: (x[0], x[1]/sum_of_chars), stat))
        stat.sort(key=lambda x: x[1], reverse=True)

        for i in range(len(stat)):
            char = stat[i][0]
            probab = stat[i][1]
            self.ws3.append([i+1, char, probab])
    
