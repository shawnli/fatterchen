import copy
import logging
from functools import partial
from lushi import attack, get_possible_action, take_action
from action import summon, attack

class Choice(object):
    name = "DefaultChoice"
    def __init__(self):
        self.name = self.__class__.__name__

    def choose(self, user, enemy, possible_actions):
        return NotImplementedError()

    def train(self, status):
        pass

    def update_weights(self):
        pass

import random

##random = random.Random(1)

class RandomChoice(Choice):

    def choose(self, user, enemy, possible_actions):
        return random.choice(possible_actions)

class FaceChoice(Choice):
    def __init__(self):
        super(FaceChoice, self).__init__()
    def choose(self, user, enemy, possible_actions):
        for action in possible_actions:
            if action.func is attack and action.args[1](enemy) is enemy:
                return action
        return random.choice(possible_actions)

class ScoreChoice(Choice):

    def statPlus(attackList, maxnum):
        attackList[len(attackList)-1]+=1

        i=1
        while attackList[len(attackList)-i]== maxnum :
            attackList[len(attackList)-i]=0
            i+=1
            attackList[len(attackList)-i]+=1

    def getScore(attackList,myMoinsters,enomyMonsters,enomyhp):
        hpStat=[enomyhp]
        hpStat.extend([monster.hp for monster in enomyMonsters])
        for i in range(len(myMoinsters)):
            hpStat[attackList[i]] -= myMoinsters[i].attack
        score=2*(enomyhp-hpStat[0])

        for i in  range(1,len(hpStat)):
            if hpStat[i]<=0:
                score+=enomyMonsters[i].attack

    def choose(self, user, enemy, possible_actions):
        bestAttackScore = -1000

        bestAttack = []
        attackList = [0] * len(user.monsters)

        if enemy.hp <= sum([monster.monster_data.attack for monster in user.monsters ]):
            return partial(attack, lambda x : x.monsters[0], lambda x: x)
        
        ##for i in range(math.pow(len(enemy.monsters) + 1, len(user.monsters))):
        for action in possible_actions  :
            if action.func.__name__ != 'attack':
                continue
        
            resultScore=0
            target = action.args[1](enemy)
            source = action.args[0](user)
            if target != enemy:
                if source.monster_data.attack>=target.hp:
                    resultScore+=target.monster_data.attack
                if source.hp<=target.monster_data.attack:
                    resultScore-=source.monster_data.attack
            else:
                resultScore +=0.002*source.monster_data.attack
                
            if resultScore > bestAttackScore:
                bestAttackScore = resultScore
                bestAttack = action
           ## for i in range(len(attackList)):
           ##     if attackList[i] == 0:
           ##         yield partial(attack, user.monsters[i], enemy)
           ##    else:
           ##         yield partial(attack, user.monsters[i], enemy.monsters[attackList[i] - 1])
        for action in possible_actions  :
            if action.func.__name__!='summon':
                continue
            data = action.args[0](user)
            resultScore=0
            resultScore+=data.attack
            if resultScore > bestAttackScore:
                bestAttackScore = resultScore
                bestAttack = action
        return bestAttack

class LinearChoice(Choice):
    trainning = []
    weights = {}
    weights1 = {}

    def __init__(self):
        super(LinearChoice, self).__init__()
        self.trainning = []
        self.weights = {}
        self.weights1 = {}
    def get_score1(self, player):
        if len(self.weights1) == 0:
            return self.get_score0(player)
        cnt = self.weights1.get(player.hp, 0.0) * 2
        for monster in player.monsters:
            key = (monster.monster_data.attack, monster.hp)
            cnt += self.weights1.get(key, 0.0)
        return cnt


    def get_score0(self, player):
        cnt = player.hp * 2
        for monster in player.monsters:
            cnt += max(monster.monster_data.attack - monster.hp, 0) + monster.monster_data.attack
        return cnt
    def get_score(self, user, enemy):
        return self.get_score1(user) - self.get_score1(enemy)

    def choose(self, raw_user, raw_enemy, possible_actions):
        possible_actions = get_possible_action(raw_user, raw_enemy)
        value_actions = []
        cnt = 0
        for monster in raw_user.monsters:
            if not monster.attacked:
               cnt += monster.monster_data.attack
        if cnt >= raw_enemy.hp:
            for action in possible_actions:
                if (action.func is attack) and (action.args[1](raw_enemy) is raw_enemy):
                    return action

        for action in possible_actions:
            result = take_action(raw_user, raw_enemy, action)
            if isinstance(result, str):
                return action
            user,enemy = result
            value_actions = [(self.get_score(user, enemy, self.get_score1), action, user, enemy)]
        choosed, user, enemy = max(value_actions)[1:4]
        self.trainning.append((choosed, user, enemy))
        return choosed

    def train(self, status):
        cnt = 0
        last_score = 2.0 if status =='win' else -2.0
        for choose, user, enemy in self.trainning[::-1]:
            if user.status != 'normal' and enemy.status != 'normal':
                continue
            score = self.get_score(user, enemy, self.get_score2)
            step = (last_score - score) / 100.0 * (0.8 ** cnt)
            cnt += 1
            each_step = step /(len(user.monsters) + len(enemy.monsters) + 2)
            self.weights[user.hp] += each_step
            self.weights[enemy.hp] -= each_step
            for monster in user.monsters:
                key = (monster.monster_data.attack, monster.hp)
                self.weights[key] += each_step
            for monster in enemy.monsters:
                key = (monster.monster_data.attack, monster.hp)
                self.weights[key] -= each_step
        self.trainning = []


    def update_weights(self):
        self.weights1 = copy.copy(self.weights)