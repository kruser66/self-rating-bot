from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
LOGGING_ID = env.str('LOGGING_ID', [])
DEV = env.bool('DEV', False)