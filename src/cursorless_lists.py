from dragonfly import DictList, DictListRef, Choice, Impossible
        
lists = {}

def get_dict(name) -> dict:
    for key in lists:
        if key == name:
            return lists[key]
    dictionary = {}
    # append_list(name, dictionary)
    return dictionary
    # return {}

def append_list(name, dictionary):
    found = False
    for key in lists:
        if key == name:
            lists[key].update(dictionary)
            found = True
    if not found:
        lists.update({name: dictionary})
        
def get_ref(name):
    dictionary = get_dict(name)
    if dictionary == {}:
        return Impossible(name)
    return Choice(name, dictionary)
    
# lists = []  
    
# def get_dict(name) -> DictList:
#     for dictionary in lists:
#         if dictionary.name == name:
#             return dictionary
#     empty_dict = DictList(name, {})
#     append_list(name, empty_dict)
#     return empty_dict

# def append_list(name, dictionary):
#     found = False
#         #does double for loop if got called from get_dict
#     for item in lists:
#         if item.name == name:
#             item.update(dictionary)
#             found = True
#     if not found:
#         if isinstance(dictionary, DictList):
#             lists.append(dictionary)
#         else:
#             lists.append(DictList(name, dictionary))
        
# def get_ref(name):
#     return DictListRef(name, get_dict(name))