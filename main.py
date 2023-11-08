import argparse
import statFunc as sf
from ouputs import  *
import sys 
import re 
import os 

InputPattern = re.compile(r"[a-zA-Z0-9_.+-//\\]{1,}.txt")
OutputPattern = re.compile(r"[a-zA-Z0-9_.+-//\\]{1,}.xlsx")

parser = argparse.ArgumentParser(
    prog="Генератор кода", 
    description="Эта программа создана для лабараторной работы 7 по иформатике на исследование кодирования и декодирования", 
    epilog="""" """)


parser.add_argument("TxtFile", help="Путь до txt файла")
parser.add_argument("-fn", '--FileName', help="Путь до сохраняемого файла документа excel(должен быть xlsx)")

args = parser.parse_args()

def exam() -> None:

    if args.FileName: 
        SavePath = args.FileName
    else: 
        SavePath = 'out.xlsx'

    if InputPattern.match(args.TxtFile) is None: 
        print("Файл с текстом должен быть в формате txt", file=sys.stderr)
        return -1 
    
    if OutputPattern.match(SavePath) is None:
        print("Файл должен быть в формате xlsx", file=sys.stderr)


if __name__ == "__main__":
    exam()
    try: 
        stat, sm = sf.GetStatistic(args.TxtFile)

    except: 
        print("Ошибка при декодировании текстового файла", file=sys.stderr)
        exit()

    
    table = Table(stat, sm)
    table.save(args.FileName)
    

