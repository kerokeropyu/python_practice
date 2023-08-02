import pprint

x=[]
x.append("spam")
print(x)
x.append("egg")
print(x)

y=["spam","egg"]
y.remove("egg")
print(y)
y.remove("spam")
print(y)

z=["spam","egg"]
z[1]="hogehoge"
print(z)

a=[1,2,3,4,5]
a=a[1:4]
print(a)

b=[1,2,3]
b.reverse()
print(b)

c=[1,0,17,4,1,4,7,3,3]
c.sort()
print(c)

l = [i for i in range(10) if i%2 == 0]
print(l) 

l2 = [str(i) for i in range(10) if i % 2 == 0]
print(l2)