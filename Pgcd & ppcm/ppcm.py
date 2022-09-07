from pgcd import *
def ppcm(a,b):
    if a == 0 or b == 0:
        return 0
    else :
        return (a*b)//pgcd(a,b)
