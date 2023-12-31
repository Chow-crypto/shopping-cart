# @Author : 大海
# @File : src.py
from lib import common
import time
from interface import user
from  interface import bank
from  interface import shop
# commin.login_intter
# 二
# 设置一个用户的信息，登录的状态
user_data={'name':None,
           'is_auth':False,}


def login():
    '''
    登录函数，密码输错三次锁定，用户名输错可以一直输入
    :return:
    '''
    if user_data['is_auth']:
        print('你已登录')
        return
    print('请登录')
    # 密码输出错误计数变量
    count = 0
    while True:
        name = input('输入用户名').strip()
        # 九
        # 需要查询是否用户存在
        # 开始省代码
        user_dic = user.get_userinfo_by_name(name)
        if user_dic:
            # 是否锁定
            print(user_dic['locked'])
            # 锁定状态
            if user_dic['locked']:
                # 十三
                # 需要的解锁定 写入 user_dic  locked 变 False  写入 json数据修改
                time.sleep(5)
                user.unlock_user(name)
                count = 0
                continue
            pwd = input('输入密码').strip()
            if user_dic['password'] == pwd and user_dic['locked'] == False:
                user_data['name'] = name
                user_data['is_auth'] = True
                print('登录成功')
                break
            else:
                print('密码错误')
                count += 1
            if count >= 3:
                # 十二。锁定接口
                # 需要的是锁定 写入 user_dic  locked 变 True  写入 json数据修改
                user.lock_user(name)
        else:
            print('用户名不存在')





# 三
def register():
    if user_data['is_auth']:
        print('已登录')
        return
    print('注册')
    while True:
        name = input('输入用户名').strip()
        # 四
        # 查看用户是否已经注册需要用到接口interface  对应的  user
        user_dic = user.get_userinfo_by_name(name)
        print(user_dic)
        if not user_dic:
            pwd = input('输入密码').strip()
            pwd1 = input('确认密码').strip()
            if pwd == pwd1:
                # 八
                # 注册接口
                user.register_user(name, pwd)
                break
            else:
                print('2次密码不一致')
        else:
            print('用户名已经存在')
def loginout():
    user_data['is_auth'] = False
    print('注销')
@common.login_intter
def check_balance():
    # 十四 需要 interface 接口 bank.py 模块 check_balance_interface方法
    # 传入登录名字调用接口加工字典account对应的value余额
    print('查看余额')
    balance = bank.check_balance_interface(user_data['name'])
    print('你的余额为%s' % balance)
@common.login_intter
def transfer():
    print('转账')
    while True:
        # 十六
        # 转账人
        trans_name = input('请输入转入用户名，q返回退出转账').strip()
        if trans_name == user_data['name']:
            print('不能给自己转账')
            continue
        if 'q' == trans_name:
            break
        # 查看转账用户是否存在
        trans_dic = user.get_userinfo_by_name(trans_name)
        if trans_dic:
            trans_money = input('输入转账金额').strip()
            # 纯数字的字符串类型
            if trans_money.isdigit():
                trans_money = int(trans_money)
                # 调用查询余额接口，根据登录名拿到余额
                user_balance = bank.check_balance_interface(user_data['name'])
                # 用户的余额必须大于转入的钱
                if user_balance > trans_money:
                    # 十七
                    # 写转账接口 user_data['name'],trans_name,trans_money
                    bank.transfer_interface(user_data['name'], trans_name, trans_money)
                    break
            else:
                print('请输入数字')



        else:
            print('用户不存在')


@common.login_intter
def repay():
    print('存款')
    while True:

        account=input('请输入存款的金额,输入q退出').strip()
        if account == 'q': break
        if account.isdigit():
            account = int(account)
            # 二十一
            # 调用存款接口执行存款的业务逻辑，传入用户名和存款金额
            bank.repay_interface(user_data['name'], account)
            break
        else:
            print('请输入数字')



@common.login_intter
def withdraw():
    print('取款')
    while True:
        qukuan_money = input('请输入取款金额').strip()
        if 'q' == qukuan_money: break
        if qukuan_money.isdigit():
            qukuan_money = int(qukuan_money)
            # 调用查询余额接口，根据登录名拿到余额
            user_account = bank.check_balance_interface(user_data['name'])  # 读文件然后索引用户钱
            # 取款
            if user_account >= qukuan_money:
                # 二十四
                # 调用取款接口执行取款的业务逻辑，传入用户名和取款金额
                bank.withdraw_interface(user_data['name'], qukuan_money)
                print('取款%s元成功' % qukuan_money)
                break



            else:
                print('钱不够')



        else:
            print('输入数字')






@common.login_intter
def check_record():
    print('查看流水')
    # 二十八
    # 调用查看流水接口执行查看流水的业务逻辑，传入用户名
    bankflow = bank.check_bankflow_interface(user_data['name'])
    # print(bankflow)
    for record in bankflow:
        print(record)
@common.login_intter
def shopping():
    print('购物')
    goods_list = [
        ['coffe', 30],
        ['chicken', 20],
        ['iPhone', 8000],
        ['macBook', 12000],
        ['car', 100000]
    ]
    shopping_cart = {}
    # 二十九
    # 调用查询余额接口，根据登录名拿到余额
    user_money = bank.check_balance_interface(user_data['name'])
    cost_money = 0
    while True:
        for i, item in enumerate(goods_list):
            print(i, item)
        choice = input('请输入购物编号').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice < 0 or choice >= len(goods_list): continue
            goods_name = goods_list[choice][0]
            goods_price = goods_list[choice][1]
            if user_money >= goods_price:
                if goods_name in shopping_cart:  # 原来已经购买过
                    shopping_cart[goods_name]['count'] += 1
                    shopping_cart[goods_name]['price'] = shopping_cart[goods_name]['count'] * goods_price
                else:
                    shopping_cart[goods_name] = {'price': goods_price, 'count': 1}
                user_money -= goods_price
                cost_money += goods_price
                print('%s 新的购物商品' % goods_name)
            else:
                print('钱不够')
                continue
        elif choice == 'q':
            print(shopping_cart)
            buy = input('卖不卖 (y/n)>>:').strip()
            if buy == 'y':
                # 正常需要加密码验证
                if cost_money == 0: break
                # 三十
                # 调用购物接口，传入用户数据，购物车，花费金额
                if shop.shopping_interface(user_data['name'], shopping_cart, cost_money):
                    print('购买成功 ')
                    break
                else:
                    print('钱不够')
                    break
            else:
                print('不卖')
                break
        else:
            print('非法输入')
            continue








@common.login_intter
def look_shoppingcart():
    print('查看购物车')
    # 三十五
    # 调用查看购物车接口，传入用户名
    shopping_s=shop.check_shoppingcart(user_data['name'])
    print(shopping_s)


# 思考一下，
'''
'3':check_balance,
'4':transfer,
'5':repay,
'6':withdraw,
'7':check_record,
'8':shopping,
'9':look_shoppingcart,
'10':loginout,
都要在登录的情况下才能执行
全部都写一个登录装饰器 
公用的在commin里面写
'''

fun_dic={'1':login,
         '2':register,
         '3':check_balance,
         '4':transfer,
         '5':repay,
         '6':withdraw,
         '7':check_record,
         '8':shopping,
         '9':look_shoppingcart,
         '10':loginout,

         }




def run():
    while True:
        print("""
    "1":登录
    "2":注册
    "3":查看余额
    "4":转账
    "5":存款
    "6":取款
    "7":查看流水
    "8":购物
    "9":查看购买商品
    "10":注销

        """)
        choice = input('输入商品编号').strip()
        if choice not in fun_dic:continue
        # print(choice)
        # print(fun_dic[choice])
        fun_dic[choice]()