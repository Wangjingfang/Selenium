
#  UTF-8

import pandas as pd
import os
import numpy as np
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains  #鼠标动作
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
# record_log = pd.read_excel(r"D:\坚果云\我的坚果云\log\投放位置竞价调整记录-未出单0.xlsx")
# length = len(record_log)
# print(length)
# n = 8
# for i in range(2):
#     print('已修改第%d条竞价修改完成，请在Excel中查看' % i)
#     print('提高竞价已修改第{}完成，请在Excel中查看'.format(i+1))

# print('已修改第%d条竞价修改完成，请在Excel中查看'%i)
## 测试实现vlookup 功能

# # import pandas as pd
# path1 = r"C:\Users\Administrator\Desktop\1.xlsx"
# df1 = pd.read_excel(path1)
# # df2 = pd.read_excel(r"C:\Users\Administrator\Desktop\2.xlsx")
# final = df1[['Station','唯一','可用库存','0','1','2']]
# final['Country'] = final['Station'].map(lambda x: x[-2:])


#
# for i in range(3):
#     df1[str(i)] = "monday"

# print(df1)
# print(df2)
# df1.insert(3, 'MAKE', df1['MODEL'].map(df2.set_index('MODEL')['MAKE']))

# print (df1)
#
# df1.to_excel(excel_writer=path1, index=None)

# url = "http://94.74.123.132"
# brower = webdriver.Chrome(ChromeDriverManager().install())
# brower.get(url)

# path = r"C:\Users\Administrator\Desktop\text\changename"
# def changename(path):
#     for root, dirs, files in os.walk(path):
#         for i in range(len(files)):
#
#             filename = files[i]
#             print(filename)
#             if "_SBV" in filename :
#                 new_name = filename[:10] + ".xlsx"
#
#             # new_name = filename[:6] + " 21.04.csv"
#             else:
#                 new_name = filename[:6] + ".xlsx"
#             print(new_name)
#             os.rename(root + "\\" + filename, root + "\\" + new_name)

# from random import randint
#
# money = 1000
# while money > 0:
#     print('你的总资产为:', money)
#     needs_go_on = False
#     while True:
#         debt = int(input('请下注: '))
#         if 0 < debt <= money:
#             break
#     first = randint(1, 6) + randint(1, 6)
#     print('玩家摇出了%d点' % first)
#     if first == 7 or first == 11:
#         print('玩家胜!')
#         money += debt
#     elif first == 2 or first == 3 or first == 12:
#         print('庄家胜!')
#         money -= debt
#     else:
#         needs_go_on = True
#     while needs_go_on:
#         needs_go_on = False
#         current = randint(1, 6) + randint(1, 6)
#         print('玩家摇出了%d点' % current)
#         if current == 7:
#             print('庄家胜')
#             money -= debt
#         elif current == first:
#             print('玩家胜')
#             money += debt
#         else:
#             needs_go_on = True
# print('你破产了, 游戏结束!')
#
#
#
# # 99乘法口诀
# for i in range(1, 10):
#     for j in range(1, i + 1):
#         print('%d*%d=%d' % (i, j, i * j), end='\t')
#     print()
#
#
# # 回文数
# num = int(input('请输入一个正整数: '))
# temp = num
# num2 = 0
# while temp > 0:
#     num2 *= 10
#     num2 += temp % 10
#     print(num2)
#     temp //= 10
# if num == num2:
#     print('%d是回文数' % num)
# else:
#     print('%d不是回文数' % num)

"""
找出1~9999之间的所有完美数
完美数是除自身外其他所有因子的和正好等于这个数本身的数
例如: 6 = 1 + 2 + 3, 28 = 1 + 2 + 4 + 7 + 14
Version: 0.1
Author: 骆昊
Date: 2018-03-02
"""
# import math
#
# for num in range(1, 10000):
#     result = 0
#     for factor in range(1, int(math.sqrt(num)) + 1):
#         if num % factor == 0:
#             result += factor
#             if factor > 1 and num // factor != factor:
#                 result += num // factor
#     if result == num:
#         print(num)


# if __name__ == '__main__':
#
#     # changename(path)

# s1 = '\'hello,world!\''
# s2 = '\n\\hello,world!\\\n'
# print(s1,s2,end='')
# 'hello,world!'
# \hello,world!\
# s1='\141\142\143\x61\x62\x63'
# s2='\u9a86\u660a'
# print(s1,s2)
# abcabc 骆昊

# 类，私有属性的命名，‘__’两个下滑先标示
# class Test:
#
#     def __init__(self, foo):
#         self.__foo = foo
#
#     def __bar(self):
#         print(self.__foo)
#         print('__bar')
#
#
# def main():
#     test = Test('hello')
#     test._Test__bar()
#     print(test._Test__foo)
#
#
# if __name__ == "__main__":
#     main()
#
from time import sleep

# class Clock(object):
#
#     '''数字时钟'''
#     def __init__(self,hour=0,minute=0,second=0):
#         '''初始化方法
#         :param _second: 秒
#         :param _minute: 分
#         :param _hour: 时
#
#         '''
#
#         self._second = second
#         self._minute = minute
#         self._hour = hour
#
#     def run(self):
#         '''走字'''
#         self._second += 1
#         if self._second == 60 :
#             self._minute += 1
#             self._second = 0
#             if self._minute == 60:
#                 self._hour += 1
#                 self._minute = 0
#                 if self._hour == 24:
#                     self._hour = 0
#
#     def show(self):
#         '''显示时间'''
#         return '%02d:%02d:%02d' % \
#                (self._hour, self._minute, self._second)
#
# def main():
#     clock = Clock(23,59,58)
#     print(1)
#     while True:
#         print(clock.show())
#         sleep(1)
#         clock.run()
#
#
# if __name__ == '__main__':
#     main()


'''
@property装饰器
之前我们讨论过Python中属性和方法访问权限的问题，虽然我们不建议将属性设置为私有的，但是如果直接将属性暴露给外界也是有问题的，比如我们没有办法检查赋给属性的值是否有效。
我们之前的建议是将属性命名以单下划线开头，通过这种方式来暗示属性是受保护的，不建议外界直接访问，那么如果想访问属性可以通过属性的getter（访问器）和setter（修改器）方法进行对应的操作。
如果要做到这点，就可以考虑使用@property包装器来包装getter和setter方法，使得对属性的访问既安全又方便，代码如下所示。
__slots__魔法
我们讲到这里，不知道大家是否已经意识到，Python是一门动态语言。通常，动态语言允许我们在程序运行时给对象绑定新的属性或方法，
当然也可以对已经绑定的属性和方法进行解绑定。但是如果我们需要限定自定义类型的对象只能绑定某些属性，可以通过在类中定义__slots__变量来进行限定。
需要注意的是__slots__的限定只对当前类的对象生效，对子类并不起任何作用。

class Person(object):

    # 需要限定自定义类型的对象只能绑定某些属性，可以通过在类中定义__slots__变量来进行限定。需要注意的是__slots__的限定只对当前类的对象生效，对子类并不起任何作用。


    # 限定Person 只绑定 _name,_age,_gender 这三个属性

    __slots__ =('_name','_age','_gender')

    def __init__(self,name,age):
        self._name = name
        self._age = age


    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    def play(self):
        if self._age <= 16:
            print('%s正在玩飞行棋'%self._name)
        else:
            print('%s正在玩大富翁'%self._name)


def main():
    person = Person('王大锤',12)
    person.play()
    person.age = 22
    person.play()
    person._gender = '男'
    # person._is_gay = True
    # AttributeError: 'Person' object has no attribute '_is_gay'

if __name__ == '__main__':
    main()
'''

'''
静态方法和类方法
之前，我们在类中定义的方法都是对象方法，也就是说这些方法都是发送给对象的消息。实际上，我们写在类中的方法并不需要都是对象方法，例如我们定义一个“三角形”类，
通过传入三条边长来构造三角形，并提供计算周长和面积的方法，但是传入的三条边长未必能构造出三角形对象，因此我们可以先写一个方法来验证三条边长是否可以构成三角形，
这个方法很显然就不是对象方法，因为在调用这个方法时三角形对象尚未创建出来（因为都不知道三条边能不能构成三角形），
所以这个方法是属于三角形类而并不属于三角形对象的。我们可以使用静态方法来解决这类问题，代码如下所示。
'''

# from math import sqrt
#
#
# class Triangle(object):
#
#     def __init__(self, a, b, c):
#         self._a = a
#         self._b = b
#         self._c = c
#
#
#     @staticmethod
#     def is_valid(a, b, c):
#         return a + b > c and b + c > a and a + c > b
#
#     def perimeter(self):
#         return self._a + self._b + self._c
#
#     def area(self):
#         half = self.perimeter() / 2
#         return sqrt(half * (half - self._a) *
#                     (half - self._b) * (half - self._c))
#
#
# def main():
#     a, b, c = 3, 4, 5
#     # 静态方法和类方法都是通过给类发消息来调用的
#     if Triangle.is_valid(a, b, c):
#         t = Triangle(a, b, c)
#         print(t.perimeter())
#         # 也可以通过给类发消息来调用对象方法但是要传入接收消息的对象作为参数
#         # print(Triangle.perimeter(t))
#         print(t.area())
#         # print(Triangle.area(t))
#     else:
#         print('无法构成三角形.')
#
#
# if __name__ == '__main__':
#     main()

'''
类之间的关系
简单的说，类和类之间的关系有三种：is-a、has-a和use-a关系。

is-a关系也叫继承或泛化，比如学生和人的关系、手机和电子产品的关系都属于继承关系。
has-a关系通常称之为关联，比如部门和员工的关系，汽车和引擎的关系都属于关联关系；关联关系如果是整体和部分的关联，那么我们称之为聚合关系；如果整体进一步负责了部分的生命周期（整体和部分是不可分割的，同时同在也同时消亡），
那么这种就是最强的关联关系，我们称之为合成关系。
use-a关系通常称之为依赖，比如司机有一个驾驶的行为（方法），其中（的参数）使用到了汽车，那么司机和汽车的关系就是依赖关系。
我们可以使用一种叫做UML（统一建模语言）的东西来进行面向对象建模，其中一项重要的工作就是把类和类之间的关系用标准化的图形符号描述出来。关于UML我们在这里不做详细的介绍，有兴趣的读者可以自行阅读《UML面向对象设计基础》一书。
'''
'''
继承和多态
刚才我们提到了，可以在已有类的基础上创建新类，这其中的一种做法就是让一个类从另一个类那里将属性和方法直接继承下来，从而减少重复代码的编写。
提供继承信息的我们称之为父类，也叫超类或基类；得到继承信息的我们称之为子类，也叫派生类或衍生类。子类除了继承父类提供的属性和方法，还可以定义自己特有的属性和方法，所以子类比父类拥有的更多的能力，
在实际开发中，我们经常会用子类对象去替换掉一个父类对象，这是面向对象编程中一个常见的行为，对应的原则称之为里氏替换原则。下面我们先看一个继承的例子。
'''
# class Person(object):
#     '''人'''
#
#     def __init__(self, name, age):
#         self._name = name
#         self._age = age
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def age(self):
#         return self._age
#
#     @age.setter
#     def age(self, age):
#         self._age = age
#
#
#     def play(self):
#         print('%s正在愉快的玩耍'%(self._name))
#
#     def watch_av(self):
#         if self._age >= 18:
#             print('%s正在观看动作片.' %(self._name))
#         else:
#             print('%s只能看《熊出没》'%(self._name))
#
#
# class Student(Person):
#     '''学生'''
#
#     def __init__(self, name, age, grade):
#         super().__init__(name, age)
#         self._grade = grade
#
#     @property
#     def grade(self):
#         return self._grade
#
#     @grade.setter
#     def grade(self, grade):
#         self._grade = grade
#
#     def study(self, course):
#         print('%s的%s正在学习%s'% (self._grade,self._name, course))
#
# class Teacher(Person):
#     """老师"""
#
#     def __init__(self, name, age, title):
#         super().__init__(name, age)
#         self._title = title
#
#     @property
#     def title(self):
#         return self._title
#
#     @title.setter
#     def title(self, title):
#         self._title = title
#
#     def teach(self, course):
#         print('%s%s正在讲%s.' % (self._name, self._title, course))
#
#
# def main():
#     stu = Student('王大锤', 15, '初三')
#     stu.study('数学')
#     stu.watch_av()
#     t = Teacher('骆昊', 38, '砖家')
#     t.teach('Python程序设计')
#     t.watch_av()
#
#
# if __name__ == '__main__':
#     main()


'''
子类在继承了父类的方法后，可以对父类已有的方法给出新的实现版本，这个动作称之为方法重写（override）。
通过方法重写我们可以让父类的同一个行为在子类中拥有不同的实现版本，当我们调用这个经过子类重写的方法时，
不同的子类对象会表现出不同的行为，这个就是多态（poly-morphism）。
'''
# from abc import ABCMeta, abstractmethod
#
#
# class Pet(object, metaclass=ABCMeta):
#     """宠物"""
#
#     def __init__(self, nickname):
#         self._nickname = nickname
#
#     @abstractmethod
#     def make_voice(self):
#         """发出声音"""
#         pass
#
#
# class Dog(Pet):
#     """狗"""
#
#     def make_voice(self):
#         print('%s: 汪汪汪...' % self._nickname)
#
#
# class Cat(Pet):
#     """猫"""
#
#     def make_voice(self):
#         print('%s: 喵...喵...' % self._nickname)
#
#
# def main():
#     pets = [Dog('旺财'), Cat('凯蒂'), Dog('大黄')]
#     for pet in pets:
#         pet.make_voice()
#
#
# if __name__ == '__main__':
#     main()

'''综合案例
案例1：奥特曼打小怪兽。'''
# from abc import ABCMeta, abstractmethod
# from random import randint, randrange
#
#
# class Fighter(object, metaclass=ABCMeta):
#     """战斗者"""
#
#     # 通过__slots__魔法限定对象可以绑定的成员变量
#     __slots__ = ('_name', '_hp')
#
#     def __init__(self, name, hp):
#         """初始化方法
#
#         :param name: 名字
#         :param hp: 生命值
#         """
#         self._name = name
#         self._hp = hp
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def hp(self):
#         return self._hp
#
#     @hp.setter
#     def hp(self, hp):
#         self._hp = hp if hp >= 0 else 0
#
#     @property
#     def alive(self):
#         return self._hp > 0
#
#     @abstractmethod
#     def attack(self, other):
#         """攻击
#
#         :param other: 被攻击的对象
#         """
#         pass
#
#
# class Ultraman(Fighter):
#     """奥特曼"""
#
#     __slots__ = ('_name', '_hp', '_mp')
#
#     def __init__(self, name, hp, mp):
#         """初始化方法
#
#         :param name: 名字
#         :param hp: 生命值
#         :param mp: 魔法值
#         """
#         super().__init__(name, hp)
#         self._mp = mp
#
#     def attack(self, other):
#         other.hp -= randint(15, 25)
#
#     def huge_attack(self, other):
#         """究极必杀技(打掉对方至少50点或四分之三的血)
#
#         :param other: 被攻击的对象
#
#         :return: 使用成功返回True否则返回False
#         """
#         if self._mp >= 50:
#             self._mp -= 50
#             injury = other.hp * 3 // 4
#             injury = injury if injury >= 50 else 50
#             other.hp -= injury
#             return True
#         else:
#             self.attack(other)
#             return False
#
#     def magic_attack(self, others):
#         """魔法攻击
#
#         :param others: 被攻击的群体
#
#         :return: 使用魔法成功返回True否则返回False
#         """
#         if self._mp >= 20:
#             self._mp -= 20
#             for temp in others:
#                 if temp.alive:
#                     temp.hp -= randint(10, 15)
#             return True
#         else:
#             return False
#
#     def resume(self):
#         """恢复魔法值"""
#         incr_point = randint(1, 10)
#         self._mp += incr_point
#         return incr_point
#
#     def __str__(self):
#         return '~~~%s奥特曼~~~\n' % self._name + \
#             '生命值: %d\n' % self._hp + \
#             '魔法值: %d\n' % self._mp
#
#
# class Monster(Fighter):
#     """小怪兽"""
#
#     __slots__ = ('_name', '_hp')
#
#     def attack(self, other):
#         other.hp -= randint(10, 20)
#
#     def __str__(self):
#         return '~~~%s小怪兽~~~\n' % self._name + \
#             '生命值: %d\n' % self._hp
#
#
# def is_any_alive(monsters):
#     """判断有没有小怪兽是活着的"""
#     for monster in monsters:
#         if monster.alive > 0:
#             return True
#     return False
#
#
# def select_alive_one(monsters):
#     """选中一只活着的小怪兽"""
#     monsters_len = len(monsters)
#     while True:
#         index = randrange(monsters_len)
#         monster = monsters[index]
#         if monster.alive > 0:
#             return monster
#
#
# def display_info(ultraman, monsters):
#     """显示奥特曼和小怪兽的信息"""
#     print(ultraman)
#     for monster in monsters:
#         print(monster, end='')
#
#
# def main():
#     u = Ultraman('骆昊', 1000, 120)
#     m1 = Monster('狄仁杰', 250)
#     m2 = Monster('白元芳', 500)
#     m3 = Monster('王大锤', 750)
#     ms = [m1, m2, m3]
#     fight_round = 1
#     while u.alive and is_any_alive(ms):
#         print('========第%02d回合========' % fight_round)
#         m = select_alive_one(ms)  # 选中一只小怪兽
#         skill = randint(1, 10)   # 通过随机数选择使用哪种技能
#         if skill <= 6:  # 60%的概率使用普通攻击
#             print('%s使用普通攻击打了%s.' % (u.name, m.name))
#             u.attack(m)
#             print('%s的魔法值恢复了%d点.' % (u.name, u.resume()))
#         elif skill <= 9:  # 30%的概率使用魔法攻击(可能因魔法值不足而失败)
#             if u.magic_attack(ms):
#                 print('%s使用了魔法攻击.' % u.name)
#             else:
#                 print('%s使用魔法失败.' % u.name)
#         else:  # 10%的概率使用究极必杀技(如果魔法值不足则使用普通攻击)
#             if u.huge_attack(m):
#                 print('%s使用究极必杀技虐了%s.' % (u.name, m.name))
#             else:
#                 print('%s使用普通攻击打了%s.' % (u.name, m.name))
#                 print('%s的魔法值恢复了%d点.' % (u.name, u.resume()))
#         if m.alive > 0:  # 如果选中的小怪兽没有死就回击奥特曼
#             print('%s回击了%s.' % (m.name, u.name))
#             m.attack(u)
#         display_info(u, ms)  # 每个回合结束后显示奥特曼和小怪兽的信息
#         fight_round += 1
#     print('\n========战斗结束!========\n')
#     if u.alive > 0:
#         print('%s奥特曼胜利!' % u.name)
#     else:
#         print('小怪兽胜利!')
#
#
# if __name__ == '__main__':
#     main()
#
# '''案例2：扑克游戏'''
#
# import random
#
#
# class Card(object):
#     """一张牌"""
#
#     def __init__(self, suite, face):
#         self._suite = suite
#         self._face = face
#
#     @property
#     def face(self):
#         return self._face
#
#     @property
#     def suite(self):
#         return self._suite
#
#     def __str__(self):
#         if self._face == 1:
#             face_str = 'A'
#         elif self._face == 11:
#             face_str = 'J'
#         elif self._face == 12:
#             face_str = 'Q'
#         elif self._face == 13:
#             face_str = 'K'
#         else:
#             face_str = str(self._face)
#         return '%s%s' % (self._suite, face_str)
#
#     def __repr__(self):
#         return self.__str__()
#
#
# class Poker(object):
#     """一副牌"""
#
#     def __init__(self):
#         self._cards = [Card(suite, face)
#
#
#                        for suite in '♠♥♣♦'
#                        for face in range(1, 14)]
#         self._current = 0
#
#     @property
#     def cards(self):
#         return self._cards
#
#     def shuffle(self):
#         """洗牌(随机乱序)"""
#         self._current = 0
#         random.shuffle(self._cards)
#
#     @property
#     def next(self):
#         """发牌"""
#         card = self._cards[self._current]
#         self._current += 1
#         return card
#
#     @property
#     def has_next(self):
#         """还有没有牌"""
#         return self._current < len(self._cards)
#
#
# class Player(object):
#     """玩家"""
#
#     def __init__(self, name):
#         self._name = name
#         self._cards_on_hand = []
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def cards_on_hand(self):
#         return self._cards_on_hand
#
#     def get(self, card):
#         """摸牌"""
#         self._cards_on_hand.append(card)
#
#     def arrange(self, card_key):
#         """玩家整理手上的牌"""
#         self._cards_on_hand.sort(key=card_key)
#
#
# # 排序规则-先根据花色再根据点数排序
# def get_key(card):
#     return (card.suite, card.face)
#
#
# def main():
#     p = Poker()
#     p.shuffle()
#     players = [Player('东邪'), Player('西毒'), Player('南帝'), Player('北丐')]
#     for _ in range(13):
#         for player in players:
#             player.get(p.next)
#     for player in players:
#         print(player.name + ':', end=' ')
#         player.arrange(get_key)
#         print(player.cards_on_hand)
#
#
# if __name__ == '__main__':
#     main()

'''
在上面的代码中，我们将Pet类处理成了一个抽象类，所谓抽象类就是不能够创建对象的类，这种类的存在就是专门为了让其他类去继承它。
Python从语法层面并没有像Java或C#那样提供对抽象类的支持，但是我们可以通过abc模块的ABCMeta元类和abstractmethod包装器来达到抽象类的效果，如果一个类中存在抽象方法那么这个类就不能够实例化（创建对象）。
上面的代码中，Dog和Cat两个子类分别对Pet类中的make_voice抽象方法进行了重写并给出了不同的实现版本，当我们在main函数中调用该方法时，这个方法就表现出了多态行为（同样的方法做了不同的事情）。
'''

### 工资结算系统 ###
"""
某公司有三种类型的员工 分别是部门经理、程序员和销售员
需要设计一个工资结算系统 根据提供的员工信息来计算月薪
部门经理的月薪是每月固定15000元
程序员的月薪按本月工作时间计算 每小时150元
销售员的月薪是1200元的底薪加上销售额5%的提成
"""
# from abc import ABCMeta, abstractmethod
#
#
# class Employee(object, metaclass=ABCMeta):
#     """员工"""
#
#     def __init__(self, name):
#         """
#         初始化方法
#
#         :param name: 姓名
#         """
#         self._name = name
#
#     @property
#     def name(self):
#         return self._name
#
#     @abstractmethod
#     def get_salary(self):
#         """
#         获得月薪
#
#         :return: 月薪
#         """
#         pass
#
#
# class Manager(Employee):
#     """部门经理"""
#
#     def get_salary(self):
#         return 15000.0
#
#
# class Programmer(Employee):
#     """程序员"""
#
#     def __init__(self, name, working_hour=0):
#         super().__init__(name)
#         self._working_hour = working_hour
#
#     @property
#     def working_hour(self):
#         return self._working_hour
#
#     @working_hour.setter
#     def working_hour(self, working_hour):
#         self._working_hour = working_hour if working_hour > 0 else 0
#
#     def get_salary(self):
#         return 150.0 * self._working_hour
#
#
# class Salesman(Employee):
#     """销售员"""
#
#     def __init__(self, name, sales=0):
#         super().__init__(name)
#         self._sales = sales
#
#     @property
#     def sales(self):
#         return self._sales
#
#     @sales.setter
#     def sales(self, sales):
#         self._sales = sales if sales > 0 else 0
#
#     def get_salary(self):
#         return 1200.0 + self._sales * 0.05
#
#
# def main():
#     emps = [
#         Manager('刘备'), Programmer('诸葛亮'),
#         Manager('曹操'), Salesman('荀彧'),
#         Salesman('吕布'), Programmer('张辽'),
#         Programmer('赵云')
#     ]
#     for emp in emps:
#         if isinstance(emp, Programmer):
#             emp.working_hour = int(input('请输入%s本月工作时间: ' % emp.name))
#         elif isinstance(emp, Salesman):
#             emp.sales = float(input('请输入%s本月销售额: ' % emp.name))
#         # 同样是接收get_salary这个消息但是不同的员工表现出了不同的行为(多态)
#         print('%s本月工资为: ￥%s元' %
#               (emp.name, emp.get_salary()))
#
#
# if __name__ == '__main__':
#     main()


# def getname(path):
#     for root, dirs, files in os.walk(path):
#         for i in range(len(files)):
#
#             filename = files[i]
#             print(filename)

# if __name__ == '__main__':
#     getname("D:\data\F-SBV-Data\F部广告活动07.09-08.07")

### 将各个文件夹下的文件复制到新文件夹中
# import os
# import shutil
#
# #目标文件夹
# determination = r"C:\Users\wangjingfang\Desktop\ceshi"
# if not os.path.exists(determination):
#     os.mkdir(determination)
#
# # 源文件夹路径
# path = r"C:\Users\wangjingfang\Desktop\新建文件夹"
#
# def movefile(path,determination):
#
#     folders_list = os.listdir(path)
#     # print(folders_list)
#     for folder in folders_list:
#         dir = path + "\\" + str(folder)
#         # print(dir)
#         files = os.listdir(dir)
#
#         for file in files:
#             print(file)
#             # 移动文件
#             shutil.copyfile(dir + "\\"+ file, determination + "\\" + file)
#         else:
#             continue
#
# if __name__ == '__main__':
#
#     movefile(path,determination)

### 对路径下的文件进行复制 ###
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# import os
# import shutil
#
# # 对象文件的类型指定
# file_type_list = ['pdf', 'txt', 'xls', 'xlsx', 'pptx', 'doc']
# src_folder = r"C:\Users\wangjingfang\Desktop\新建文件夹"
#
#
# # 取得文件夹下面的所有指定类型的文件全名（路径+文件名）
# # os.walk() 方法用于通过在目录树中游走输出在目录中的文件名，向上或者向下。
# # for dirpath,dirnames,filenames in os.walk(folder):
# #     print(dirnames)
# def get_file_list(folder):
#     filelist = []  # 存储要copy的文件全名
#     for dirpath, dirnames, filenames in os.walk(folder):
#         for file in filenames:
#             file_type = file.split('.')[-1]
#             if (file_type in file_type_list):
#                 file_fullname = os.path.join(dirpath, file)  # 文件全名
#                 filelist.append(file_fullname)
#     return filelist
#
#
# # 将文件list里面的文件拷贝到指定目录下
# def copy_file(src_file_list, dst_folder):
#     print('===========copy start===========')
#     for file in src_file_list:
#         shutil.copy(file, dst_folder)
#     print('===========copy end!===========')
#
#
# # filelist = get_file_list(src_folder)
#
# if __name__ == "__main__":
#     # copy源所在目录
#     src_folder = r"C:\Users\wangjingfang\Desktop\新建文件夹"  # 路径最后不要加\
#     # copy到的指定目录
#     dst_folder = r"C:\Users\wangjingfang\Desktop\ceshi"  # 路径最后不要加\
#
#     # 取得文件夹下所有指定类型的文件全名
#
#     filelist = get_file_list(src_folder)
#     copy_file(filelist, dst_folder)

'''
基于tkinter模块的GUI
GUI是图形用户界面的缩写，图形化的用户界面对使用过计算机的人来说应该都不陌生，在此也无需进行赘述。Python默认的GUI开发模块是tkinter（在Python 3以前的版本中名为Tkinter），从这个名字就可以看出它是基于Tk的，Tk是一个工具包，最初是为Tcl设计的，后来被移植到很多其他的脚本语言中，它提供了跨平台的GUI控件。当然Tk并不是最新和最好的选择，也没有功能特别强大的GUI控件，事实上，开发GUI应用并不是Python最擅长的工作，如果真的需要使用Python开发GUI应用，wxPython、PyQt、PyGTK等模块都是不错的选择。

基本上使用tkinter来开发GUI应用需要以下5个步骤：

导入tkinter模块中我们需要的东西。
创建一个顶层窗口对象并用它来承载整个GUI应用。
在顶层窗口对象上添加GUI组件。
通过代码将这些GUI组件的功能组织起来。
进入主事件循环(main loop)。
下面的代码演示了如何使用tkinter做一个简单的GUI应用。
'''
# import tkinter
# import tkinter.messagebox
#
#
# def main():
#     flag = True
#
#     # 修改标签上的文字
#     def change_label_text():
#         # nonlocal 定义经常在嵌套函数中
#         nonlocal flag
#         flag = not flag
#         color, msg = ('red', 'Hello, world!')\
#             if flag else ('blue', 'Goodbye, world!')
#         label.config(text=msg, fg=color)
#
#     # 确认退出
#     def confirm_to_quit():
#         if tkinter.messagebox.askokcancel('温馨提示', '确定要退出吗?'):
#             top.quit()
#
#     # 创建顶层窗口
#     top = tkinter.Tk()
#     # 设置窗口大小
#     top.geometry('240x160')
#     # 设置窗口标题
#     top.title('小游戏')
#     # 创建标签对象并添加到顶层窗口
#     label = tkinter.Label(top, text='Hello, world!', font='Arial -32', fg='red')
#     label.pack(expand=1)
#     # 创建一个装按钮的容器
#     panel = tkinter.Frame(top)
#     # 创建按钮对象 指定添加到哪个容器中 通过command参数绑定事件回调函数
#     button1 = tkinter.Button(panel, text='修改', command=change_label_text)
#     button1.pack(side='left')
#     button2 = tkinter.Button(panel, text='退出', command=confirm_to_quit)
#     button2.pack(side='right')
#     panel.pack(side='bottom')
#     # 开启主事件循环
#     tkinter.mainloop()
#
#
# if __name__ == '__main__':
#     main()

from enum import Enum, unique
from math import sqrt
from random import randint

import pygame


@unique
class Color(Enum):
    """颜色"""

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (242, 242, 242)

    @staticmethod
    def random_color():
        """获得随机颜色"""
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)


class Ball(object):
    """球"""

    def __init__(self, x, y, radius, sx, sy, color=Color.RED):
        """初始化方法"""
        self.x = x
        self.y = y
        self.radius = radius
        self.sx = sx
        self.sy = sy
        self.color = color
        self.alive = True

    def move(self, screen):
        """移动"""
        self.x += self.sx
        self.y += self.sy
        if self.x - self.radius <= 0 or \
                self.x + self.radius >= screen.get_width():
            self.sx = -self.sx
        if self.y - self.radius <= 0 or \
                self.y + self.radius >= screen.get_height():
            self.sy = -self.sy

    def eat(self, other):
        """吃其他球"""
        if self.alive and other.alive and self != other:
            dx, dy = self.x - other.x, self.y - other.y
            distance = sqrt(dx ** 2 + dy ** 2)
            if distance < self.radius + other.radius \
                    and self.radius > other.radius:
                other.alive = False
                self.radius = self.radius + int(other.radius * 0.146)

    def draw(self, screen):
        """在窗口上绘制球"""
        pygame.draw.circle(screen, self.color,
                           (self.x, self.y), self.radius, 0)

def main():
    # 定义用来装所有球的容器
    balls = []
    # 初始化导入的pygame中的模块
    pygame.init()
    # 初始化用于显示的窗口并设置窗口尺寸
    screen = pygame.display.set_mode((800, 600))
    # 设置当前窗口的标题
    pygame.display.set_caption('大球吃小球')
    running = True
    # 开启一个事件循环处理发生的事件
    while running:
        # 从消息队列中获取事件并对事件进行处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 处理鼠标事件的代码
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 获得点击鼠标的位置
                x, y = event.pos
                radius = randint(10, 100)
                sx, sy = randint(-10, 10), randint(-10, 10)
                color = Color.random_color()
                # 在点击鼠标的位置创建一个球(大小、速度和颜色随机)
                ball = Ball(x, y, radius, sx, sy, color)
                # 将球添加到列表容器中
                balls.append(ball)
        screen.fill((255, 255, 255))
        # 取出容器中的球 如果没被吃掉就绘制 被吃掉了就移除
        for ball in balls:
            if ball.alive:
                ball.draw(screen)
            else:
                balls.remove(ball)
        pygame.display.flip()
        # 每隔50毫秒就改变球的位置再刷新窗口
        pygame.time.delay(50)
        for ball in balls:
            ball.move(screen)
            # 检查球有没有吃到其他的球
            for other in balls:
                ball.eat(other)


if __name__ == '__main__':
    main()

