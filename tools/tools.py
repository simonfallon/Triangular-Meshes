def readtxt2list(name):
    content = []
    with open(name, 'r') as file:
        for i in file.readlines():
            content.append(str(i).replace("\n",""))
    return content