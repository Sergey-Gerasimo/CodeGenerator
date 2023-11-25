from show import * 

def get_codes(stat:dict) -> tuple[Tree, ]: 
    stat = list(stat.items())
    stat.sort(key=lambda x: x[1], reverse=True)
    return get_Haffman(stat), get_Hartli(stat)
    

def append_dict(key, item, _dict: dict):
    if key not in _dict:
        _dict[key] = item
    else: 
        _dict[key] += item 

def get_Hartli(chars:list) -> Tree: 
    def get_Fano_Hartli(chars: tuple) -> tuple: 
        if len(chars) == 1: 
            return chars[0][0]
        chars = sorted(chars, key=lambda x: x[1], reverse=True)
        sm1 = 0 # сумма вероятностей слева
        sm2 = 0 # сумма вероятностей спарава
        for i in range(len(chars)): 
            sm1 = sum(map(lambda x: x[1], chars[:i]))
            sm2 = sum(map(lambda x: x[1], chars[i:]))
            if sm1 >= sm2: 
                return get_Fano_Hartli(chars[:((i+1) if i < 1 else i)]), get_Fano_Hartli(chars[((i+1) if i < 1 else i):]), 0
    return Tree(get_Fano_Hartli(chars))

def get_Haffman(chars:list) -> Tree: 
    def get_Haffman_tree(chars:list, code:str='') -> tuple: 
        if len(chars) == 2: return chars
        chars.sort(key=lambda x: x[1], reverse=True)
        chars = chars[:-2] + [((chars[-1][0], chars[-2][0], round(chars[-1][1] + chars[-2][1], 5)), chars[-1][1] + chars[-2][1])]
        return get_Haffman_tree(chars)

    tree = get_Haffman_tree(chars)
    tree = Tree((tree[0][0], tree[1][0]))
    return tree

if __name__ == "__main__": 
    get_codes({'a': 0.02, "b": 0.04, "c": 0.1, "d": 0.1, "e":0.16, "f":0.16, "g":0.2})