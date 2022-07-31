import re
import json
import math

a0 = 0
a1 = 99
x= 87
n= 3

Xn = (x-a0)/(a1-a0)
Xm = pow(2,n)*Xn
ix = math.floor(Xm)
x = bin(ix)
x = '{:0b}'.format(ix)
m=len(x)
while m != n:
	x = "0" + x
	m=m+1
c=[]	
for t in range(n):
	if x[t] == '1':
		x_c = True
		c.append(x_c)
	elif x[t] == '0':
		x_c = False
		c.append(x_c)
print(c)
