import random

'''
# 对于号码提前设定：
    狼预言家：0
    真预言家：11
    2狼：1、2
    狼王：3
    4民：4、5、6、7
    女巫：8
    猎人：9
    魔术师：10
# '''

# 定义全局变量
all_players = []
alive_all = [0,1,2,3,4,5,6,7,8,9,10,11]
topic_all = [0,1,2,3,4,5,6,7,8,9,10,11]
wolf_win = 0
good_win = 0
num_epoch = 0

''''定义各种类，进行游戏的模拟'''
# 定义玩家父类
# 拥有初始属性：号码[num]、存活[alive]、站边对象[believe]
class player():
    def __init__(self,num):
        self.num = num
        self.alive = True
        self.believe = -1
    def death(self):
        self.alive = False

# 预言家大类
class eye(player):
    def __init__(self, num):
        super().__init__(num)
        self.diction = {}
    def predict(self,pre_num):
        if pre_num < 4 :
            return False    # 表示是狼
        else :
            return True     # 表示为好人
    def side(self):
        return 0
# 悍跳狼类
class wolf_eye(eye):
    def __init__(self, num):
        super().__init__(num)
        self.believe = 0
        self.diction = {}
        self.predict(random.choice(range(1,11)))
    def predict(self,num):
        pre = random.choice([True,False])
        if pre == False:
            self.vote_target = num
            self.diction[num] = pre
# 真预言家类
class true_eye(eye):
    def __init__(self, num):
        super().__init__(num)
        self.believe = 11
        self.diction = {}
        self.predict(random.choice(range(1,11)))
    def predict(self, num):
        self.diction[num] = super().predict(num)
        return 0



# 没有视角的大类
class noviewer(player):
    def __init__(self, num):
        super().__init__(num)
        self.believe = -1
    def side(self):
        self.believe = random.choice([0,11])
        print(str(self.num)+"已经重新站边")

# 狼人类
class wolf(noviewer):
    def __init__(self, num):
        super().__init__(num)
        self.believe = random.choice([0,11,0]) # 增加一个对于队友的倾向，哈哈哈我是冲锋狼
    def side(self):
        self.believe = random.choice([0,11,0])
        print(str(self.num)+"已经重新站边")
# 狼王类
class wolf_king(noviewer):
    def __init__(self, num):
        super().__init__(num)
        self.believe = random.choice([0,11,0])
    def side(self):
        self.believe = random.choice([0,11,0])
        print(str(self.num)+"已经重新站边")
    def deathKill(self):
        global alive_all
        global topic_all
        global all_players
        # 优先带走拍过身份的猎人
        kill_num = -1
        if (9 not in topic_all) & (9 in alive_all):
            kill_num = 9
            alive_all.remove(9)
            # topic_all.remove(9)
            if(check_end()==False):
                all_players[9].deathKill()
        elif (8 not in topic_all) & (8 in alive_all):
            alive_all.remove(8)
            # topic_all.remove(8)
        elif (10 not in topic_all) & (10 in alive_all):
            alive_all.remove(10)
            # topic_all.remove(10)
        else:
            # 随机开枪带走一名玩家（除狼队）
            kill_num = random.choice(alive_all)
            while(kill_num in [0,1,2,3]):
                kill_num = random.choice(alive_all)
            alive_all.remove(kill_num)
            topic_all.remove(kill_num)
        print('3号开枪带走了：'+str(kill_num))
        print(alive_all)
        return 0

# 平民类
class man(noviewer):
    def __init__(self, num):
        super().__init__(num)
        self.believe = random.choice([0,11])

# 神职人员大类
class toolman(noviewer):
    def __init__(self, num):
        super().__init__(num)
        self.believe = random.choice([0,11])
        self.show = False
# 女巫类
class woman(toolman):
    def __init__(self, num):
        super().__init__(num)
    def drag(self): # 完全参照猎人的技能整的
        # 随机开枪带走一名玩家
        kill_num = -1
        # 确保另外两个拍过身份的神职不会被他崩走
        he_think_good = [8]
        if 3 not in topic_all:
            he_think_good.append(3)
        if 9 not in topic_all:
            he_think_good.append(9)
        if 10 not in topic_all:
            he_think_good.append(10)
        # 考虑他的站边情况, 在0和11中选择
        if self.believe == 0:
            # 站边狼警
            he_think_good.append(0)
            # 读取狼警的验人信息
            test = all_players[0].diction
            # 如果里面有查杀，那么就直接开枪带走查杀
            for each in test.keys():
                if test[each] == False:
                    kill_num = each
                if test[each] == True:
                    he_think_good.append(each)
            # 如果没有查杀，就直接带走对面预言家
            if kill_num == -1:
                if 11 in alive_all:
                    # 开枪带走对面的预言家
                    kill_num = 11
            # 不然就结合自己认为的好人随便开一枪
            bad = []
            for i in alive_all:
                if i not in he_think_good:
                    bad.append(i)
            kill_num = random.choice(bad)
        if self.believe == 11:
            # 站边狼警
            he_think_good.append(11)
            # 读取狼警的验人信息
            test = all_players[11].diction
            # 如果里面有查杀，那么就直接开枪带走查杀
            for each in test.keys():
                if test[each] == False:
                    kill_num = each
                if test[each] == True:
                    he_think_good.append(each)
            # 如果没有查杀，就直接带走对面预言家
            if kill_num == -1:
                if 11 in alive_all:
                    # 开枪带走对面的预言家
                    kill_num = 0
            # 不然就结合自己认为的好人随便开一枪
            bad = []
            for i in alive_all:
                if i not in he_think_good:
                    bad.append(i)
            try:
                kill_num = random.choice(bad)
            except:
                print('女巫：找不到人撒毒啊~')
                kill_num = -1

        return kill_num

# 猎人类
class trueman(toolman):
    def __init__(self, num):
        super().__init__(num)
    def deathKill(self):
        global alive_all
        global topic_all
        global all_players
        kill_num = -1
        # 优先带走拍过身份的狼王
        if (3 not in topic_all) & (3 in alive_all):
            kill_num = 3
            alive_all.remove(3)
            # topic_all.remove(3)
            if(check_end()==False):
                all_players[3].deathKill()
        else:
            # 随机开枪带走一名玩家
            # 确保另外两个拍过身份的神职不会被他崩走
            he_think_good = [3]
            if 8 not in topic_all:
                he_think_good.append(8)
            if 10 not in topic_all:
                he_think_good.append(10)
            # 考虑他的站边情况, 在0和11中选择
            if self.believe == 0:
                # 站边狼警
                he_think_good.append(0)
                # 读取狼警的验人信息
                test = all_players[0].diction
                print(type(test))
                # 如果里面有查杀，那么就直接开枪带走查杀
                for each in test.keys():
                    if test[each] == False:
                        kill_num = each
                    if test[each] == True:
                        he_think_good.append(each)
                # 如果没有查杀，就直接带走对面预言家
                if kill_num == -1:
                    if 11 in alive_all:
                        # 开枪带走对面的预言家
                        kill_num = 11
                # 不然就结合自己认为的好人随便开一枪
                bad = []
                for i in alive_all:
                    if i not in he_think_good:
                        bad.append(i)
                kill_num = random.choice(bad)
            if self.believe == 11:
                # 站边狼警
                he_think_good.append(11)
                # 读取狼警的验人信息
                test = all_players[11].diction
                print(type(test))
                # 如果里面有查杀，那么就直接开枪带走查杀
                for each in test.keys():
                    if test[each] == False:
                        kill_num = each
                    if test[each] == True:
                        he_think_good.append(each)
                # 如果没有查杀，就直接带走对面预言家
                if kill_num == -1:
                    if 11 in alive_all:
                        # 开枪带走对面的预言家
                        kill_num = 0
                # 不然就结合自己认为的好人随便开一枪
                bad = []
                for i in alive_all:
                    if i not in he_think_good:
                        bad.append(i)
                if len(bad) < 1:
                    kill_num = -1
                else:
                    kill_num = random.choice(bad)
            if kill_num != -1:
                # 不吞枪
                alive_all.remove(kill_num)
                topic_all.remove(kill_num)
                # 开枪打中狼王，进行再度判断
                if kill_num == 3:
                    while(check_end()==False):
                        all_players[3].deathKill()
        print('9号带走了：'+str(kill_num))
        print(alive_all)
        return 0

        return kill_num
# 魔术师类
class magic(toolman):
    def __init__(self, num):
        super().__init__(num)
        self.changed_num = []
    def change(self):
        global alive_all
        no_one_to_exchange = True
        for each in alive_all:
            if each not in self.changed_num:
                no_one_to_exchange = False
        if not no_one_to_exchange:
            num1 = random.choice(alive_all)
            while(num1 in self.changed_num):
                num1 = random.choice(alive_all)
            num2 = random.choice(alive_all)
            while(num2 in self.changed_num):
                num2 = random.choice(alive_all)
            self.changed_num.append(num1)
            self.changed_num.append(num2)
            return [num1,num2]
        else:
            return [-2,-2]



''''游戏过程的定义'''
#
def magic_change(num_list,num1):
    index = num_list.index(num1)
    num = num_list[0] if (index == 1) else num_list[1]
    return num


# 初始化 ,这里初始化的时候，暂时没有考虑验人信息
def initialization():
    players = []
    # 狼预言家
    players.append(wolf_eye(0))
    # 3狼的定义
    players.append(wolf(1))
    players.append(wolf(2))
    players.append(wolf_king(3))
    # 4民的定义
    players.append(man(4))
    players.append(man(5))
    players.append(man(6))
    players.append(man(7))
    # 神职的定义
    players.append(woman(8))
    players.append(trueman(9))
    players.append(magic(10))
    # 真预言家
    players.append(true_eye(11))

    # # 狼预言家验人信息
    # wolf_dict = players[0].dict
    # # 真预言家验人信息
    # true_dict = players[-1].dict

    return players

# 检查游戏是否结束
def check_end():
    global alive_all
    print(alive_all)
    # 检验狼人全死
    bo1 = True
    for item in alive_all:
        if item < 4:
            bo1 = False
    # 检验神职全死
    bo2 = True
    for item in alive_all:
        if item > 7:
            bo2 = False
    # 检验平民全死
    bo3 = True
    for item in alive_all:
        if (item > 3) & (item < 8):
            bo3 = False

    # 进行结果输出：
    global wolf_win
    global good_win
    global num_epoch
    if bo2:
        print('Wolf win')
        wolf_win += 1
        wolf_win -= num_epoch
        num_epoch = 1
        return True
    elif bo3:
        print('Wolf win')
        wolf_win += 1
        wolf_win -= num_epoch
        num_epoch = 1
        return True
    elif bo1:
        print('Good win')
        good_win += 1
        good_win -= num_epoch
        num_epoch = 1
        return True
    else:
        return False

# 站边过程
def reside():
    global all_players
    for player in all_players:
        player.side()
    return 0

# 白天投票环节
def day_vote():
    global all_players
    global alive_all

    # 汇集每个人的信任数值
    num_vote = -1
    dict_side = {}
    dict_side[0] = 0
    dict_side[11] = 0
    for player_num in alive_all:
        temp = all_players[player_num]
        # print(temp.believe)
        dict_side[temp.believe] += 1

    # 比较谁占据大多数票
    wolf_b = dict_side[0]
    true_b = dict_side[11]

    # 调用他们中的票多的人的验人信息
    dict_truth = all_players[0].diction if (wolf_b > true_b) else all_players[11].diction # 这里已经考虑了第一轮警长拿到了警徽

    # 判断其中有没有查杀
    for each in dict_truth.keys():
        if (dict_truth[each] == False) & (each in alive_all):
            num_vote = each

    global topic_all
    # 如果没有查杀，那么就随机出现两张焦点牌
    if num_vote == -1:
        topic_num1 = random.choice(topic_all)
        topic_num2 = random.choice(topic_all)
        # while (topic_num2 == topic_num1):
        #     topic_num2 = random.choice(topic_all)
        # 若焦点牌中有神或者狼王，则拍身份，则出另一张
        if (topic_num1 in [3,8,9,10]) ^ (topic_num2 in [3,8,9,10]):
            num_vote = topic_num1 if (topic_num2 in [3,8,9,10]) else topic_num2
        # 若两张均为神或者狼王，则均拍身份，并从中随意走一张
        # 若两张均无身份，随机走一张
        else:
            num_vote = random.choice([topic_num1,topic_num2])

        # 处理拍身份的牌
        if topic_num1 in [3,8,9,10]:
            # 拍身份
            topic_all.remove(topic_num1)
        if topic_num2 in [3,8,9,10]:
            # 拍身份
            try:
                topic_all.remove(topic_num2)
            except:
                print(topic_all)

    # 被票选的玩家出局，相应开技能
    # print(num_vote)
    alive_all.remove(num_vote)
    try:
        topic_all.remove(num_vote)
    except:
        print('它拍身份了，还是要被抗推，可惜可惜')
    print('本轮出局：'+str(num_vote)+'号玩家')
    # 猎人狼王开死亡技能
    if num_vote in [3,9]:
        all_players[num_vote].deathKill()

    return 0
def night():
    global all_players
    global alive_all
    global topic_all

    change_num = []
    # 魔术师先行动
    if 10 in alive_all:
        change_num = all_players[10].change()
        print('魔术师交换了:', change_num)

    # 两个预言家验人，这样就可以验死人，但是必然不会查验自己验过的人对吧
    wolf_eye_num = -1
    if 0 in alive_all:
        wolf_predicted = all_players[0].diction.keys()
        wolf_target = alive_all.copy()
        for wolf_p in wolf_predicted:
            if wolf_p in wolf_target:
                wolf_target.remove(wolf_p)
        print("狼警可验对象："+str(wolf_target))
        try:
            wolf_eye_num = random.choice(wolf_target)
            print("狼警查验对象为："+str(wolf_eye_num))
        except:
            print("请相信我的查杀啊")

    true_eye_num = -1
    if 11 in alive_all:
        true_predicted = all_players[11].diction.keys()
        true_target = alive_all.copy()
        for true_p in true_predicted:
            if true_p in true_target:
                true_target.remove(true_p)
        print("真警可验对象："+str(true_target))
        try:
            true_eye_num = random.choice(true_target)
            print("真警查验对象："+str(true_eye_num))
        except:
            print("请相信我的查杀啊")


    # 狼人杀人
    # 优先击杀拍过身份的神职
    w_kill_num = -1
    kill_target = alive_all.copy()
    # 排除自己的队友123，可能自刀狼警和预言家
    if 1 in alive_all:
        kill_target.remove(1)
    if 2 in alive_all:
        kill_target.remove(2)
    if 3 in alive_all:
        kill_target.remove(3)
    # 优先击杀拍过身份的神职
    for w_k_num in kill_target:
        if w_k_num not in topic_all:
            w_kill_num = w_k_num
    # 否则对剩下的目标中随机选取一个进行击杀
    while(w_kill_num == -1):
        w_kill_num = random.choice(kill_target)
    print('狼人选择击杀的目标为：'+str(w_kill_num))

    # 女巫毒人
    drag_num = -1
    # 如果拍过身份，就撒毒
    if (8 not in topic_all) & (8 in alive_all):
        # 毒人
        # 结合自己的believe进行撒毒，这部分类似与猎人
        drag_num = all_players[8].drag()
        print('女巫选择毒杀：'+str(drag_num))

    # 判断
    # 这部分总共获得的num数如下，都没有进行判断操作
    # 判断预言家验人
    if true_eye_num != -1:
        # 可以进行验人
        if true_eye_num in change_num:
            # 验人在魔术师交换的对象中
            if len(change_num) == 2:
                true_eye_num = magic_change(change_num, true_eye_num)
        print('预言家实际验人为:'+str(true_eye_num))
        all_players[11].predict(true_eye_num)
    # 判断狼人预言家验人
    if wolf_eye_num != -1:
        # 可以进行换人
        if wolf_eye_num in change_num:
            # 验人在魔术师交换对象中：
            wolf_eye_num = magic_change(change_num, wolf_eye_num)
        print('狼警实际验人为：'+str(wolf_eye_num))
    # 判断狼人对进行刀人
    if w_kill_num != -1:
        if w_kill_num in change_num:
            w_kill_num = magic_change(change_num, w_kill_num)
        print('今晚死亡的是：'+str(w_kill_num))
        alive_all.remove(w_kill_num)
        try:
            topic_all.remove(w_kill_num)
        # 考虑枪牌和狼王牌
        except:
            print('狼人刀神了，害')
        if w_kill_num in [3,9]:
            all_players[w_kill_num].deathKill()

    # 判断女巫可以撒毒
    if drag_num != -1:
        if drag_num in change_num:
            drag_num = magic_change(change_num, drag_num)
            try:
                alive_all.remove(drag_num)
                print('今晚死亡的是：'+str(drag_num))
                topic_all.remove(drag_num)
            except:
                print('毒在刀口上，血亏')
    return 0


def balanceStrategy():      # 进行初始化
    global all_players
    all_players = initialization()
    global alive_all
    global topic_all
    alive_all = [0,1,2,3,4,5,6,7,8,9,10,11]
    topic_all = [0,1,2,3,4,5,6,7,8,9,10,11]
    global num_epoch
    num_epoch = 0
    # 进行循环
    while(check_end()==False):
        # 站边
        reside()
        day_vote()
        if (check_end() == True):
            break
        else:
            night()
    return 0

if __name__ == '__main__':
    win_num = 0
    for i in range(1000):
        balanceStrategy()

    print(wolf_win)
    print(good_win)