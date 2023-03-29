import api
from aiogram import Bot, Dispatcher, types, executor

TOKEN = "6284457092:AAEN5JticOikI0-5sgx13JH2je9m5zuRF00"

bot = Bot(TOKEN)
dp = Dispatcher(bot)

Accounts = {}

state = {}

messageInfoBot = "Привет! Это бот который видет ваши оценки в электроном дневнике\n"
"Для того что с ним работать с ботом нужна авторизация электроного дневника!\n"
"Вы можете ввести для авторизации /login и бот вам скажет что дальше делать\nИли"
" login ваш_логин ваш_пороль.\n"
"Для работы с оценками напиши в чат marks и тебе выйдут все оценки 1 триместра.\n"
"marks номер триместра,marks Все номер триместра, выведут все оценки триместра которого указали\n"
"marks Алгебра выведет оценки первого триместра, а marks Алгебра 2 выведет оценки второго триместра"


async def help(message: types.Message):
    if message.text == "помощь":
        await message.reply(messageInfoBot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(text=messageInfoBot, chat_id=message.chat.id)


def algorithmAuth(state, message, account):
    if state == "login":
        state[message.from_user.id] = "password"
        account.SetLogin(message.text)
        await message.reply("Введите пароль")
    elif state == "password":
        state[message.from_user.id] = "region"
        account.SetPassword(message.text)
        await message.reply("Выбрите из списка ваш район")
    elif state == "region":
        state[message.from_user.id] = "city"
        account.SetRegion(message.text)
        await message.reply("Выбрите из списка ваш район")
    elif state == "region":
        state[message.from_user.id] = "city"
        account.SetRegion(message.text)
        await message.reply("Выбрите из списка ваш район")


@dp.message_handler()
async def auth(message: types.Message):
    text = message.text.split(" ")
    if text[0] == "login":
        Accounts[message.from_user.id] = api.Diary()
        ac = Accounts[message.from_user.id]
        if len(text) == 1:
            state[message.from_user.id] = "Login"
            Accounts[message.from_user.id] = api.Diary()
            await message.reply("Введите логин")
        elif len(text) == 2:
            state[message.from_user.id] = "Password"
            ac.setLogin(message.text)
            await message.reply("Введите пароль")
        elif len(text) == 3:
            if ac.Auth("760502", text[1], text[2]):
                await message.reply("Вы авторизованны!")
                state[message.from_user.id] = "auth"
                Accounts[message.from_user.id] = ac
            else:
                await message.reply("Ошибка не правильный логин или пароль!")

    account = Accounts[message.from_user.id]

    if state[message.from_user.id] == "Login":
        if len(text) == 3:
            if account.Auth("760502", text[1], text[2]):
                await message.reply("Вы авторизованны!")
                state[message.from_user.id] = "auth"
            else:
                await message.reply("Ошибка не правильный логин или пароль!")
        state[message.from_user.id] = "Password"
        account.setLogin(message.text)
        await message.reply("Введите пароль")

    elif state[message.from_user.id] == "Password":
        account.setPassword(message.text)
        if account.Auth("760502", account.getLogin(), account.getPassword()):
            await message.reply("Вы авторизованны!")
            state[message.from_user.id] = "auth"
            Accounts[message.from_user.id] = account
        else:
            await message.reply("Ошибка не правильный логин или пароль!")
            state[message.from_user.id] = "Login"
            await message.reply("Введите логин")


def marks():
    pass


if __name__ == '__main__':
    executor.start_polling(dp)
