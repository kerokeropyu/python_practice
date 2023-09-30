import csv
import matplotlib.pyplot as plt
from datetime import datetime

filename = 'data/sitka_weather_07-2018_simple.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # print(header_row)

    # for index, column_header in enumerate(header_row):
    #     print(index, column_header)

    # ファイルから最高気温を取得する
    # highs = []
    # for row in reader:
    #     high = int(row[5])
    #     highs.append(high)

    # ファイルから日付と最高気温を取得する
    dates, highs = [], []
    for row in reader:
        current_date = datetime.strptime(row[2], '%Y-%m-%d')
        high = int(row[5])
        dates.append(current_date)
        highs.append(high)

    # 最高気温のグラフを描画する
    # plt.style.use('whitegrid')
    fig, ax = plt.subplots()
    ax.plot(highs, c='red')

    # グラフにフォーマットを指定する
    plt.title("Daily high temperatures - 2018", fontsize=24)
    plt.xlabel('', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel("Temperature (F)", fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.show()
print(highs)



