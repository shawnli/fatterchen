import logging.config #标准日志模块.配置函数
from recordclass import recordclass #没百度到recordclass模块

Monster = recordclass('Monster', ['monster_data', 'name', 'hp', 'status', 'attacked'])#定义怪这个类
Player = recordclass('Player', ['name', 'monsters', 'hp', 'status', 'crystal', 'remained_crystal', 'hand_card', 'stacks', 'oom_turn', 'choice'])#定义玩家类
MonsterData = recordclass('MonsterData', ['name', 'cost', 'attack', 'hp', 'bc_funs'])

logging.config.fileConfig('logger.conf')
logger = logging.getLogger()
logger.setLevel("ERROR")#大约是配置错误的意思吧
