import random
from matplotlib import pyplot

# 乱数の初期化
random.seed()

# 10000個の乱数を作る
r = [random.random() for x in range(10000)]

# ヒストグラムとして30に分類して描画する
pyplot.hist(r, 30)

# UI表示
pyplot.show()