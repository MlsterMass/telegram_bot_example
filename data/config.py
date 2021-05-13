from pathlib import Path

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
PAYMENT_TOKEN = env.str("PAYMENT_TOKEN")
QIWI_WALLET = env.str("QIWI_WALLET")
QIWI_P_KEY = env.str("QIWI_P_KEY")
QIWI_S_KEY = env.str("QIWI_S_KEY")
QIWI_TOKEN = env.str("QIWI_TOKEN")
BLOCKCYPHER_TOKEN = env.str("BLOCKCYPHER_TOKEN")
WALLET_BTC = env.str("WALLET_BTC")
PGPASSWORD = env.str("POSTGRES_PASSWORD")
PGUSER = env.str("PGUSER")
DATABASE = env.str("DATABASE")
POSTGRES_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{IP}/{DATABASE}"
REQUEST_LINK = "bitcoin:{address}?" \
               "amount:{amount}" \
               "&label={message}"
channels = [
    -1001380981384

]
groups = [
    -1001192467974
]

allowed_users = [

]
support_ids = [
    1662877395
]
I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
