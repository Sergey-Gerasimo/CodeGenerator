import tkinter as tk 
import sys 
import math 
from PIL import Image, ImageDraw
sys.setrecursionlimit(10000000)

class Node: 
    def __init__(self, *args, data:any=None, right=None, left=None, **kwargs) -> None: 
        self.data = data
        self.right = right
        self.left = left 


class Point: 
    def __init__(self, x, y) -> None: 
        self.x = x 
        self.y = y

class tkTree(tk.Tk): 
    def __init__(self, *args, width:int=2000, height:int=1200,**kwargs) -> None: 
        tk.Tk.__init__(self)
        self.width = width
        self.height = height
        self.ungle = math.pi
        self.lenght = 375
        self.canvas = tk.Canvas(width=width, height=height, bg="white")
        self.ovalsize = (40, 20)
        self.canvas.pack()

    def __get_xy(self, center:tuple) -> tuple: 
        x1 = center[0] - self.ovalsize[0]//2
        x2 = center[0] + self.ovalsize[0]//2
        y1 = center[1] - self.ovalsize[1]//2
        y2 = center[1] + self.ovalsize[1]//2
        return Point(x1, y1), Point(x2, y2)

    def calc_unlg(self, a:float, deep:int) -> float: 
        return a/(deep+2)
    
    def save(self, fileName:str) -> None:
        self.canvas.update()
        self.canvas.postscript(file = fileName + '.eps')
        img = Image.open(fileName + '.eps') 
        img.save(fileName + '.png', 'png')


    def add_tree(self, tree:Node, center:tuple, deep:int=0) -> None:
        a, b = self.lenght*math.sin(self.calc_unlg(self.ungle, deep))/(deep+1), self.lenght*math.cos(self.calc_unlg(self.ungle, deep))/(deep+1)
        if tree.left is not None: 
            self.canvas.create_line(center[0], center[1], 
                                    center[0] - a, center[1]+b,arrow=tk.LAST, fill='black')
            
            self.add_tree(tree.left, center=(center[0]-a, 
                                             center[1]+b), 
                                             deep=deep+1)

        if tree.right is not None: 
            self.canvas.create_line(center[0], center[1], center[0] + a, 
                                    center[1]+b,
                                    arrow=tk.LAST, fill='black')
            
            self.add_tree(tree.right, center=(center[0]+a, 
                                              center[1]+b), 
                                              deep=deep+1)

        p1, p2 = self.__get_xy(center)
        self.canvas.create_oval(p1.x, p1.y, p2.x, p2.y, fill='grey70', outline='white')
        self.canvas.create_text(center[0], center[1], text=tree.data[0], justify=tk.CENTER, font="Verdana 14", fill="black")

        if (tree.left is None) and (tree.right is None): 
            return 
        
class Tree: 
    def __init__(self, *args, **kwargs) -> None: 
        self.root = Node()
        self.root.data ="main"
        if len(args) > 0: 
            self.add(args[0])
            self.dict = self.get_dict()

    def add(self, codes:tuple):
        self.root = Node(data='main')
        self.root.left = Node(data=f'0\n{codes[0][2]}')
        self.root.right = Node(data=f'1\n{codes[1][2]}')
        self.__add(codes[0], self.root.left)
        self.__add(codes[1], self.root.right)
        self.dict = self.get_dict()

        
    def __add(self, codes:tuple, root:Node): 
        if type(codes) == str : 
            root.data = codes
            root.left = None
            root.right = None
            return 
        
        if root.left is None:
            root.left = Node(data=f'0\n{codes[2]}')
        self.__add(codes[0], root.left)
        
        if root.right is None:
            root.right = Node(data=f'1\n{codes[2]}')
        self.__add(codes[1], root.right)

    def show(self) -> None: 
        win = tkTree()
        center = (1024*2, 400)
        win.add_tree(self.root, center)
        win.mainloop()
    

    def save(self, filename:str="out.jpeg", size:tuple=(4*1024, 4*720), bg="#FFFFFF") -> None: 
        im = Image.new("RGB",size, bg)
        draw = ImageDraw.Draw(im)
        
        elipseSize:tuple=(50, 20)
        elipseColor:str="#FFAA00"
        lineColor:str="#000000"
        textColor = "#000000"

        
        def _calcPos(xy:tuple, deep:int, maxAngle:float=math.pi/2, lenght:float=550) -> tuple: 
            if deep < 3: 
                return (xy[0] + math.sin(maxAngle/(deep+1))*lenght/(math.log2(deep+1)+1)*2, xy[1] + math.cos(maxAngle/(deep+1))*lenght/(math.log2(deep+1)+1)*2)
            else: 
                return (xy[0] + math.sin(maxAngle/((math.log2(deep+1)+1)))*lenght/(math.log2(deep+1)), xy[1] + math.cos(maxAngle/(math.log2(deep+1)+1))*lenght/(math.log2(deep+1)+1))

        def __save(tree: Node, *args, deep:int=0, xy:tuple=(size[0]//2, 10),**wargs) -> None: 
            nonlocal draw, elipseColor, elipseSize, lineColor, textColor

            if tree.left is not None: 
                nextPoint = _calcPos(xy, deep, maxAngle=-math.pi/2)
                draw.line((xy, nextPoint), lineColor)
                __save(tree.left, deep=deep+1, xy=nextPoint)

            if tree.right is not None: 
                nextPoint = _calcPos(xy, deep, maxAngle=math.pi/2)
                draw.line((xy, nextPoint), lineColor)
                __save(tree.right, deep=deep+1, xy=nextPoint)

            draw.ellipse(((xy[0]-elipseSize[0], xy[1] - elipseSize[1]), (xy[0]+elipseSize[0], xy[1] + elipseSize[1])), elipseColor)
            draw.text((xy[0]-elipseSize[0]/2, xy[1] - elipseSize[1]/2), tree.data,align='center', fill=textColor, size=50)

        __save(self.root, (size[0]//2, 10))
        im.save(filename)


    def get_dict(self) -> dict: 
        out = dict() 

        def __get_items(nd:Node, code:str=''): 
            if nd.left is None and nd.right is None: 
                out[nd.data[-1]] = code
                return 
            
            __get_items(nd.right, code=code+'1')
            __get_items(nd.left, code=code+'0')

        __get_items(self.root)
        return out 