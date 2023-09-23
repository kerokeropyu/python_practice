import numpy

# 第一引数は配列の中身
# 第二引数は型。省略すると、第一引数の内容から選ばれる
ar = numpy.array([[1, 2, 3],
                  [11, 12, 13]],
                  numpy.int32)
print(ar)

# 配列の型を表示
print(ar.dtype)

# 浮動小数点のリストで初期化してみる
b = numpy.array([[1.1, 2.2, 3.3],
                 [1.2, 2.3, 3.4]])

# 浮動小数点の配列ができる
print(b)
# 配列の型のintではなくfloatになる
print(b.dtype)

# 整数と浮動小数点を混在させてみる
c = numpy.array([[1, 2, 3],
                 [1, 2, 3.3]])
# 結果的に浮動小数点型になる
print(c)
print(b.dtype)
