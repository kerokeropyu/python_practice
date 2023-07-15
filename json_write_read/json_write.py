import json
items = [
	{"name": "Aoki", "age": 30},
	{"name": "Ishida", "age": 32},
	{"name": "Inoue", "age": 29},
]
# ファイルへ保存
with open('test.json', 'w', encoding='utf-8') as fp:
	json.dump(items, fp, indent=4)
    


	
