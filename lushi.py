from functools import partial

from action import summon, attack, charge
from base import Player, MonsterData, logger

monster_datas = []

def load_data():
    for st in open('monster_data.txt'):
        splits = st.strip().split(',')
        if len(splits) < 3:
            continue
        cost = int(splits[0])
        attack = int(splits[1])
        hp = int(splits[2])
        bc_funs = []
        if 'charge' in splits:
            bc_funs.append(charge)
        monster_data = MonsterData(cost, attack, hp)
        monster_datas.append(monster_data)


def get_possible_action(user, enemy):
    actions = []
    for i in range(len(user.monsters)):
        source = user.monsters[i]
        if not source.attacked:
            for j in range(len(enemy.monsters)):
                action = partial(attack, lambda x, i=i: x.monsters[i], lambda x, j=j: x.monsters[j])
                actions.append(action)
            actions.append(partial(attack, lambda x, i=i: x.monsters[i], lambda x: x))
    for i in range(len(user.hand_card)):
        data = user.hand_card[i]
        if (user.remained_crystal >= data.cost) and (len(user.monsters) < 7):
            action = partial(summon, lambda x, i=i: x.hand_card[i])
            actions.append(action)
    return actions


import random

##random = random.Random(1)


def take_action(user, enemy, action):
    user, enemy = action(user, enemy)
    if (user.status == 'dead') and (enemy.status == 'dead'):
        return 'draw'
    if (user.status == 'dead'):
        return enemy.name + " win"
    if (enemy.status == 'dead'):
        return user.name + " win"
    return user, enemy

def take_round(players):
    user = players[0]
    enemy = players[1]
    if (user.crystal < 10):
        user.crystal += 1
        user.remained_crystal = user.crystal
    if len(user.stacks) > 1:
        user.hand_card.append(user.stacks[0])
        user.stacks = user.stacks[1:]
    else:
        user.oom_turn += 1
        user.hp -= user.oom_turn
    if user.hp <= 0:
        user.status = 'dead'
        return enemy.name + " win"
    for source in user.monsters:
        source.attacked = False
    while True:
        possible_action = get_possible_action(user, enemy)
        if not possible_action:
            break
        action = user.choice.choose(user, enemy, possible_action)
        if action is None:
            break
        result = take_action(user, enemy, action)
        if isinstance(result, str):
            return result
        else:
            user,enemy = result
    players[0] = user
    players[1] = enemy

import math


def gen_random_data():
    for cost in range(0, 11):
        sum = 2 * cost + 1
        for hp in range(int(math.floor(sum / 3.0) + 1), int(math.floor(sum * 3.0 / 4) + 1)):
            for loop in range(0, 10 * (10 - hp)):
                attack = sum - hp
                fun = []
                if random.randint(0, 10) < 1:
                    fun.append(charge)
                data = MonsterData('a%sh%sc%s_%s' % (attack, hp, cost, loop), cost, attack, hp, fun)
                monster_datas.append(data)


def get_stacks():
    statcks = []
    if monster_datas < 15:
        raise Exception("monster type nums < 15.")
    while (len(statcks) < 30):
        choice = random.choice(monster_datas)
        if statcks.count(choice) >= 2:
            continue
        statcks.append(choice)
    return statcks


def get_face_stacks():
    statcks = []
    if monster_datas < 15:
        raise Exception("monster type nums < 15.")
    while (len(statcks) < 30):
        choice = random.choice(monster_datas)
        if statcks.count(choice) >= 2 or choice.cost>=4:
            continue
        statcks.append(choice)
    return statcks


def play_game(choice1, choice2):
    stacks = get_stacks()
    for t in range(0, 2):
        results = {}
        for j in range(0, 5000):
            stacks1 = get_face_stacks()
            
            stacks2 = get_face_stacks();
            if j%2 == 0:
                stacks = get_stacks()
                player1 = Player("a1%s"%choice1.name, [], 30, 'normal', 0, 0, stacks1[:3], stacks[4:], 0, choice1)
                stacks = get_stacks()
                player2 = Player("a2%s"%choice2.name, [], 30, 'normal', 0, 0, stacks2[:4], stacks[5:], 0, choice2)
                players = [player1, player2]
            else:
                stacks = get_stacks()
                player1 = Player("a1%s"%choice1.name, [], 30, 'normal', 0, 0, stacks1[:4], stacks[5:], 0, choice1)
                stacks = get_stacks()
                player2 = Player("a2%s"%choice2.name, [], 30, 'normal', 0, 0, stacks2[:3], stacks[4:], 0, choice2)
                players = [player2, player1]
            for i in range(0, 100):
                logger.info('round %s %s' % (i + 1, players[0].name))
               
                result = take_round(players)
                if result:
                    # logger.error('TERM %s' % result)
                    results.setdefault(result[0], 0)
                    results[result[0]] += 1
                    winner = result[1]
                    ##for player in players:
                        ##player.choice.train('win' if player.name == winner.name else 'fail')

                    break
                players.reverse()
        print results
        choice1.update_weights()
        choice2.update_weights()
