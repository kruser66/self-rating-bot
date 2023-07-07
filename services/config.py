from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
LOGGING_ID = env.str('LOGGING_ID', [])
DEV = env.bool('DEV', False)

HOST = env.str('HOST', '127.0.0.1')
PORT = env.int('PORT', 5001)

URL_WEBHOOK = f'{HOST}/{BOT_TOKEN}'