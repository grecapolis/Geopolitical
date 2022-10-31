import discord


def sepmess(X):
    Y=[]
    y=""
    for i in X:
        if i != " ":
            y=y+i
        else:
            Y=Y+[y]
            y=""
    Y=Y+[y]
    return Y

def verifpv(X):
    for i in X:
        if i == ";":
            return False
    return True