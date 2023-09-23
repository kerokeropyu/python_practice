import numpy

a = numpy.array([1, 2, 3], numpy.float64)

# 配列に定数をかける
print(a * 2)

# 配列同士の足し算
b = numpy.array([10, 20, 30])
print(a + b)

# 配列の内積
print(a @ b)