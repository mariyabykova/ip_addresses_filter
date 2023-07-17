def func() -> bool:
    string = '(()()))'
    bracket_list = []
    for element in string:
        if element == '(':
            bracket_list.append(element)
        elif bracket_list and element == ')' and bracket_list[-1] == '(':
            bracket_list.pop()
        else:
            bracket_list.append(element)
    if bracket_list == []:
        return True
    return False

print(func())