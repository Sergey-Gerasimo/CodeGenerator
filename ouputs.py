
import math 
from openpyxl import Workbook
from Fano_Hartli import *
from openpyxl.styles import (
                        PatternFill, Border, Side, 
                        Alignment, Font, GradientFill
                        )


class Table(Workbook): 
    LANG = sorted('QWERTYUIOPLKJHGFDSAZXCVBNM')
    def __init__(self,stat:dict, sum_of_chars:int,*args, title:str='', **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ws1 = self.active
        self.ws1.title = "Часть1"
        self.ws2 = self.create_sheet("Часть2")
        self.ws3 = self.create_sheet("Часть3.1")
        self.ws3_2 = self.create_sheet("Часть3.2")
        self.setws1(stat, ["ID", "Символ", "Код символа", "Число вхождений символа в текст", "Вероятность вхождения символа (рi)", "Ii"], sum_of_chars)
        self.setws2(stat, ["ID", "Символ", "Вероятность", "Код"], sum_of_chars)
        self.setws3_1(stat, ["ID", "Символ", "Вероятность", "Код"], sum_of_chars)
        self.setws3_2(stat, ["ID", "Символы", "Вероятности"], sum_of_chars)
        

    @staticmethod
    def nfloat(a:float) -> str:
        return str(a).replace('.', ',')


    def setws1(self, stat:dict, header:list, sum_of_chars:int): 
        stat_ = list(stat.items())
        stat_.sort(key=lambda x: x[1])
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
                                  self.nfloat(count/sum_of_chars), 
                                  self.nfloat(-math.log2(count/sum_of_chars))))))
            pv += count/sum_of_chars
            Isr += -math.log2(count/sum_of_chars) * count/sum_of_chars
            
        else: 
            self.ws1[f"C{i+3}"] = "Всего символов в тексте (K)"
            self.ws1[f"D{i+3}"] = sum_of_chars
            self.ws1[f"D{i+4}"] = "Полная вероятность(Р)"
            self.ws1[f"E{i+4}"] = self.nfloat(pv)
            self.ws1[f"E{i+5}"] = "Энтропия источника (Iср)"
            self.ws1[f"F{i+5}"] = self.nfloat(Isr)

    def __set_underlines(self, deep:int) -> None: 
        ...
        

    def setws2(self, stat:dict, header:list, sum_of_chars:int) -> None: 
        self.ws2.append(header)
        stat = list(stat.items())
        stat.sort(key=lambda x: x[1], reverse=True)
        
        codes = get_Hartli(stat).dict
        Isr = 0 
        stat = list(map(lambda x: (x[0], x[1]/sum_of_chars), stat))
        for i in range(len(stat)):
            char = stat[i][0]
            probab = stat[i][1]
            self.ws2.append([i+1, char, self.nfloat(probab), codes[char]])
            Isr += -math.log2(probab) * probab

        else: 
            self.ws2[f"A{i+3}"] = "Значение средней информации в битах"
            self.ws2[f"B{i+3}"] = self.nfloat(Isr)

    def setws3_1(self, stat:dict, header:list, sum_of_chars:int) -> None: 
        self.ws3.append(header)
        stat = list(stat.items())
        stat.sort(key=lambda x: x[1], reverse=True)

        codes = get_Haffman(stat).dict
        stat = list(map(lambda x: (x[0], x[1]/sum_of_chars), stat))

        Isr = 0 
        for i in range(len(stat)):
            char = stat[i][0]
            probab = stat[i][1]
            self.ws3.append([i+1, char, probab, codes[char]])
            Isr += -math.log2(probab) * probab
        else: 
            self.ws2[f"A{i+3}"] = "Значение средней информации в битах"
            self.ws2[f"B{i+3}"] = Isr

    def setws3_2(self, stat:dict, header:list, sum_of_chars:int) -> None:
        self.ws3_2.append(header)
        self.ws3_2.merge_cells('A1:A2')
        self.ws3_2.merge_cells('B1:B2')
        
        stat = list(stat.items())
        stat = list(map(lambda x: (x[0], x[1]/sum_of_chars), stat))
        stat.sort(key=lambda x: x[1], reverse=True)
        self.ws3_2.append([])
        for i in range(len(stat)):
            char = stat[i][0]
            probab = stat[i][1]
            self.ws3_2.append([i+1, char, self.nfloat(probab)])
    
