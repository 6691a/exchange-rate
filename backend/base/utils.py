def destructuring(dict:dict, *args:str):
    """
    ex) foo, blah = pluck(things, 'foo', 'blah')
    https://stackoverflow.com/a/17074606/15126990
    lambda dict, *args: (dict[arg] for arg in args)
    """
    return (dict[arg] for arg in args)
