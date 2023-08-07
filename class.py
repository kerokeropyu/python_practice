class Spam:
    ham = 200
spam=Spam()
print(spam.ham)
# del spam.ham
# print(spam.ham)

class Spam1:
    def ham(self):
        self.egg("メソッド呼び出し")

    def egg(self, msg):
        print(msg)
spam1 = Spam1()
spam1.egg("123")

# コンストラクタ、デストラクタ
class Spam2:
    def __init__(self, ham, egg):
        self.ham = ham
        self.egg = egg
    def __del__(self):
        print("spamが削除されました。")
spam2 = Spam2(5, 10)
print(spam2.ham, spam2.egg)

# プライベートメンバー
class Spam3:
    def __init__(self):
        self.__attr = 999
    def method(self):
        self.__method()
    def __method(self):
        print(self.__attr)

spam3 = Spam3()
spam3.method() # メソッド内では呼び出せる
# spam3.__method() # 外部からは呼び出せない

# ディスクリプタ
class MyDescriptor:
    def __init__(self, value):
        self.value = value
    def __get__(self, instanze, owner):
        return self.value
    def __set__(self, instanze, value):
        self.value = value
    def __delete__(self, instance):
        del self.value

class MyClass:
    descr = MyDescriptor(9999)

obj = MyClass()
print(obj.descr)        

test: int = 1
print(test)