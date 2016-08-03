import logging.config
from recordclass import recordclass

Monster = recordclass('Monster', ['monster_data', 'name', 'hp', 'status', 'attacked'])
Player = recordclass('Player', ['name', 'monsters', 'hp', 'status', 'crystal', 'remained_crystal', 'hand_card', 'stacks', 'oom_turn', 'choice'])
MonsterData = recordclass('MonsterData', ['name', 'cost', 'attack', 'hp', 'bc_funs'])

logging.config.fileConfig('logger.conf')
logger = logging.getLogger()
logger.setLevel("ERROR")
