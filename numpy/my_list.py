import numpy

a = numpy.array([1, 2, 3, 4, 5])

# インデックスアクセス
print(a[0])

# スライス
print(a[0:2])

# 書き換え
a[1] = 10
print(a)

# forでイテレーション
for x in a:
    print(x)