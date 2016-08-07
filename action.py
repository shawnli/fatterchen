import copy

from base import Monster, Player, logger


def bc_fun(monster, user, enemy):
    pass
def charge(monster, user, enemy):#上随从，默认随从不能进行攻击
    monster.attacked = False
    return monster, user, enemy

def summon(data_fun, user, enemy):
    data = data_fun(user)
    player = copy.copy(user)
    player.hand_card = copy.copy(player.hand_card)
    logger.info("%s summon %s)" % (player.name, data.name))
    player.hand_card.remove(data)
    player.remained_crystal -= data.cost
    monster = Monster(data, data.name, data.hp, 'normal', True)
    for fun in data.bc_funs:
        monster, player, enemy = fun(monster, player, enemy)

    player.monsters = copy.copy(player.monsters)
    player.monsters.append(monster)
    return player, enemy

def attack(source_fun, target_fun, user, enemy):

    source = source_fun(user)
    target = target_fun(enemy)
    if not (isinstance(source, Monster) and isinstance(target, (Monster, Player))):
        raise NotImplementedError("%s %s", type(source), type(target))

    if (source.status != 'normal') or (target.status != 'normal'):
        raise NotImplementedError("%s %s", source.status, target.status)

    new_source = copy.copy(source)
    if (hasattr(target, 'monster_data')):
        new_source.hp -= target.monster_data.attack
        if (new_source.hp <= 0):
            new_source.status = 'dead'
            logger.info(source.name+"  dead")
    new_source.attacked = True
    new_user = copy.copy(user)
    new_user.monsters = [monster if monster is not source else new_source for monster in user.monsters if (monster is not source) or (new_source.status != 'dead')]

    new_target = copy.copy(target)
    new_target.hp -= source.monster_data.attack

    if (new_target.hp <= 0):
        new_target.status = 'dead'
        logger.info(new_target.name+"  dead")

    if isinstance(new_target, Player):
        new_enempy = new_target
    else:
        new_enempy = copy.copy(enemy)
        new_enempy.monsters = [monster if monster is not target else new_target for monster in enemy.monsters if (monster is not target) or (new_target.status != 'dead')]
    logger.info("%s attack %s  ,%s blood is %s, %s blood is %s" % (source.name, target.name,source.name,new_source.hp, target.name,new_target.hp))

    return new_user, new_enempy