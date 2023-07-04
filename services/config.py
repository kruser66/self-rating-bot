from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
LOGGING_ID = env.list('LOGGING_IDS', [])
DEV = env.bool('DEV', False)