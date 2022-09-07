def pgcd(a,b):
	if b == 0:
		return a
	else :
		r = a%b
		return pgcd(b,r)
