import tkinter as tk 
import sys 
sys.setrecursionlimit(10000)

class Node: 
    def __init__(self, *args, **kwargs) -> None: 
        self.data = None
        self.right = None
        self.left = None


class Point: 
    def __init__(self, x, y) -> None: 
        self.x = x 
        self.y = y

class tkTree(tk.Tk): 
    def __init__(self, *args, width:int=600, height:int=600,**kwargs) -> None: 
        super(*args, **kwargs)
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(width=width, height=height)
        self.ovalsize = (120, 60)

    def __get_xy(self, center:tuple) -> tuple: 
        x1 = center[0] - self.ovalsize[0]//2
        x2 = center[0] + self.ovalsize[0]//2
        y1 = center[1] - self.ovalsize[1]//2
        y2 = center[1] + self.ovalsize[1]//2
        return Point(x1, y1), Point(x2, y2)

    def add_tree(self, tree:Node, center:tuple) -> None:
        if (tree.left is None) and (tree.right is None): 
            return 

        p1, p2 = self.__get_xy(center)
        if tree.left is not None: 
            self.canvas.create_line(center[0], center[1], center[0] - 100, center[1]+100 ,arrow=tk.LAST, fill='black')
        if tree.right is not None: 
            self.canvas.create_line(center[0], center[1], center[0] + 100, center[1]+100 ,arrow=tk.LAST, fill='black')

        self.canvas.create_oval(p1.x, p1.y, p2.x, p2.y, fill='grey70', outline='white')

        if not (tree.left is None): 
            self.add_tree(tree.left, center=(center[0]-150, center[1]+150))
        
        if not (tree.right is None):
            self.add_tree(tree.right, center=(center[0]+150, center[1]+150))

class Tree: 
    def __init__(self, *args, **kwargs) -> None: 
        self.root = Node()
        self.root.data ="main"

    def add(self, codes: dict) -> None: 
        for i in codes: 
            self.__add(codes[i], i, self.root)
    
    def __add(self, code:str, char:str, root:Node) -> None:
        if not len(code):
            root.data += f'\n{char}'
            return 
        
        if code[0] == '0': 
            if root.left is None:
                node = Node()
                node.data = code[0]
                root.left = node
            
            self.__add(code[1:], char, root.left)

        if code[0] == '1': 
            if root.right is None:
                node = Node()
                node.data = code[0]
                root.right = node
                
            self.__add(code[1:], char, root.right)

    def show(self) -> None: 
        win = tkTree()
        center = (300, 50)
        win.add_tree(self.root, center)
        win.mainloop()