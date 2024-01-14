import random
from matplotlib import pyplot

# TIOBE Programming Indexの結果
ranking = [
    ('Python', 20.31),
    ('Java', 18.92),
    ('JavaScript', 8.21),
    ('C', 7.71),
    ('C++', 7.12),
    ('C#', 4.81),
    ('Ruby', 2.97),
    ('Swift', 2.45),
    ('Kotlin', 2.15),
    ('PHP', 1.92),
    ('Rust', 1.77),
    ('TypeScript', 1.51),
    ('Scala', 1.28),
    ('Go', 1.18),
    ('Haskell', 0.91),
    ('Other', 13.46)
]

# 割合だけを抜き出す
rates = [x[1] for x in ranking]

# ラベルだけを抜き出す
labels = [x[0] for x in ranking]

# 円グラフを描画する
pyplot.pie(rates, labels=labels)
pyplot.show()