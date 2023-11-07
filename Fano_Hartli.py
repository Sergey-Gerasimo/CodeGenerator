from show import * 

def get_codes(stat:dict) -> dict: 
    stat = list(stat.items()) 
    
    stat.sort(key=lambda x: x[1], reverse=True)
    print(get_Haffman(stat))
    print(get_Hartli(stat))

def append_dict(key, item, _dict: dict):
    if key not in _dict:
        _dict[key] = item
    else: 
        _dict[key] += item 

def get_Hartli(chars:list) -> dict: 
    codes = dict() 

    def get_Fano_Hartli(chars: tuple, code:str="") -> list: 
        nonlocal codes
        if len(chars) == 1: return chars[0][0], code

        sm1 = 0 # сумма вероятностей слева
        sm2 = 0 # сумма вероятностей спарава
        
        for i in range(len(chars)): 
            sm1 = sum(map(lambda x: x[1], chars[:i]))
            sm2 = sum(map(lambda x: x[1], chars[i:]))
            if sm1 >= sm2: 
                for key, item in chars[:i]: 
                    append_dict(key, '1', codes)

                for key, item in chars[i:]: 
                    append_dict(key, '0', codes)
                
                return get_Fano_Hartli(chars[:i]), get_Fano_Hartli(chars[i:])
            
    get_Fano_Hartli(chars)
    return codes 

def get_Haffman(chars:list) -> dict: 
    codes = dict() 
    def get_Haffman_tree(chars:list, code:str='') -> tuple: 
        if len(chars) == 2: return chars
        chars.sort(key=lambda x: x[1], reverse=True)
        chars = chars[:-2] + [((chars[-1][0], chars[-2][0]), chars[-1][1] + chars[-2][1])]
        return get_Haffman_tree(chars)

    tree = get_Haffman_tree(chars)
    tree = (tree[0][0], tree[1][0])
    
    def __find_nodes(tree: tuple, code:str='') -> dict: 
        nonlocal codes 
        if len(tree) == 1: return 

        if type(tree[0]) == str: 
            append_dict(tree[0], code+'0', codes)

        if type(tree[1]) == str: 
            append_dict(tree[1], code+'1', codes)

        __find_nodes(tree[0], code=code+'0')
        __find_nodes(tree[1], code=code+'1')

    __find_nodes(tree)
    tree = Tree()
    tree.add(codes)
    tree.show()
    return codes 

if __name__ == "__main__": 
    get_codes({'a': 0.02, "b": 0.04, "c": 0.1, "d": 0.1, "e":0.16, "f":0.16, "g":0.2})