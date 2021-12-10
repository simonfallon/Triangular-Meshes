def readtxt2list(name):
    content=[]
    with open(name, 'r') as file:
        for i in file.readlines():
            content.append(str(i))#.replace("\n",""))
    return content

def writetxt(name,contenido):
    with open(name, 'w+') as file:
        file.writelines(contenido)
        file.close()