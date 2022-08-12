s = input()
a = int(s)%10
b = int(s)%100 //10
c = int(s)%1000 //100
d = int(s)%10000 //1000
e = int(s)%100000 //10000
f = int(s)%1000000 //100000
if a+b+c==e+d+f:
    print("YES")
else:
    print("NO")