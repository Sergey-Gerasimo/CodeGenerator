import tkinter as tk 
import sys 
import math 
sys.setrecursionlimit(10000)


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
        self.degrees = (math.sin(math.pi/3), math.sin(math.pi/5))
        self.width = width
        self.height = height
        self.lenght = 200
        self.canvas = tk.Canvas(width=width, height=height, bg="white")
        self.ovalsize = (120, 60)
        self.canvas.pack()

    def __get_xy(self, center:tuple) -> tuple: 
        x1 = center[0] - self.ovalsize[0]//2
        x2 = center[0] + self.ovalsize[0]//2
        y1 = center[1] - self.ovalsize[1]//2
        y2 = center[1] + self.ovalsize[1]//2
        return Point(x1, y1), Point(x2, y2)

    def calc_lenght(self, a:float, deep:int) -> float: 
        return a*self.degrees[deep%2]

    def add_tree(self, tree:Node, center:tuple, deep:int=0) -> None:
        
        if tree.left is not None: 
            self.canvas.create_line(center[0], center[1], 
                                    center[0] - self.calc_lenght(self.lenght, deep), center[1]+self.calc_lenght(self.lenght, deep),arrow=tk.LAST, fill='black')
            
            self.add_tree(tree.left, center=(center[0]-self.calc_lenght(self.lenght, deep), 
                                             center[1]+self.calc_lenght(self.lenght, deep)), 
                                             deep=deep+1)

        if tree.right is not None: 
            self.canvas.create_line(center[0], center[1], center[0] + self.calc_lenght(self.lenght, deep), 
                                    center[1]+self.calc_lenght(self.lenght, deep),
                                    arrow=tk.LAST, fill='black')
            
            self.add_tree(tree.right, center=(center[0]+self.calc_lenght(self.lenght, deep), 
                                              center[1]+self.calc_lenght(self.lenght, deep)), 
                                              deep=deep+1)

        p1, p2 = self.__get_xy(center)
        self.canvas.create_oval(p1.x, p1.y, p2.x, p2.y, fill='grey70', outline='white')
        self.canvas.create_text(center[0], center[1], text=tree.data, justify=tk.CENTER, font="Verdana 14")

        if (tree.left is None) and (tree.right is None): 
            return 

        

class Tree: 
    def __init__(self, *args, **kwargs) -> None: 
        self.root = Node()
        self.root.data ="main"


    def add(self, codes:tuple):
        self.root.data = "main"
        self.root.left = Node(data=f'0\n{codes[0][2]}')
        self.root.right = Node(data=f'1\n{codes[1][2]}')
        self._add(codes[0], self.root.left)
        self._add(codes[1], self.root.right)

        
    def _add(self, codes:tuple, root:Node): 
        if type(codes) == str : 
            root.data = codes
            root.left = None
            root.right = None
            return 
        
        if root.left is None:
            root.left = Node(data=f'0\n{codes[2]}')
        self._add(codes[0], root.left)
        
        if root.right is None:
            root.right = Node(data=f'1\n{codes[2]}')
        self._add(codes[1], root.right)



    def show(self) -> None: 
        win = tkTree()
        center = (450, 50)
        win.add_tree(self.root, center)
        win.mainloop()