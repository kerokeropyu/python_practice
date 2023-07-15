import json, japanize_matplotlib
import matplotlib.pyplot as plt

# jsonを読み込む
data = json.load(open('pi_goo.json', encoding = 'utf-8'))

# 描画のために値をラベルを分ける
values = [i[0] for i in data]
labels = [i[1] for i in data]
# 円グラフを描画
plt.pie(values, labels = labels)
plt.show()