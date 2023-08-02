d = {
    'key1': 'Value1',
    'key2': 'Value2',
    'key3': 'Value3',
}

print(d['key1'])
# key1が辞書に含まれているか
print('key1' in d)
print('key4' in d)
d.get('key1')
d.get('key4')
d.get('key4', 'default')

for key in d:
    print(key)

for value in d.values():
    print(value)

for key, value in d.items():
    print(key, value)

d['key1'] = 'NewValue1'
print(d['key1'])

d['newkey'] = 'NewValue'
print(d)

del d['newkey']
print(d)
d.pop('key2')
print(d)