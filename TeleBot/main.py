from Utils import Form

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from charset_normalizer import md

from config import TOKEN



import logging

from Utils import get_currency


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)
# @dp.message_handler()
# async def echo(message: types.Message):
#     stroka = message.text
#
#     elements = stroka.split()
#
#     result = 0
#
#     a = float(elements[0])
#     b = float(elements[2])
#     sign = elements[1]
#
#     if sign == "+":
#         result = a + b
#     elif sign == "-":
#         result = a - b
#     elif sign == "*":
#         result = a*b
#     elif sign == "/":
#         result = a/b
#     else:
#         await message.answer("Ввод неправильный или я не знаю таких операций")
#
#         await message.answer(str(result))

# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)

@dp.message_handler(commands="start")
async def start_cmd_handler(message: types.Message) :
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=4)

    button_text = ("I'm great!", "I'm tired.")
    keyboard_markup.row(*(types.KeyboardButton(text) for text in button_text))

    more_buttons_text = ("I am Egor.", "Wait, what?", "Wha?")
    keyboard_markup.add(*(types.KeyboardButton(text) for text in more_buttons_text))

    await message.reply("What's up? \n What's your name?", reply_markup=keyboard_markup)

@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)


    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.age.set()
    await message.reply("How old are you?")


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    await message.reply("Age gotta be a number.\nHow old are you? (digits only)")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.gender.set()
    await state.update_data(age=int(message.text))

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Male", "Female")
    markup.add("Other")

    await message.reply("What is your gender?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Male", "Female", "Attack Helicopter"], state=Form.gender)
async def process_gender_invalid(message: types.Message):
    return await message.reply("Bad gender name. Choose your gender from the keyboard.")


@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

        markup = types.ReplyKeyboardRemove()

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Hi! Nice to meet you,', md.bold(data['name'])),
                md.text('Age:', md.code(data['age'])),
                md.text('Gender:', data['gender']),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation
    await state.finish()


@dp.message_handler(commands="cat")
async def cats(message: types.Message):
    with open("cat.jpg", "rb") as photo:
        await message.reply_photo(photo, caption="Кисундрий")


@dp.message_handler(commands="doc")
async def docs(message: types.Message):
    with open("doc.txt", "rb") as doc:
        await message.reply_document(doc, caption="reply_document")


@dp.message_handler(commands="music")
async def music(message: types.Message):
    with open("Rick_Astley_-_Never_Gonna_Give_You_Up_(musmore.com).mp3", "rb") as audio:
        await message.reply_audio(audio, caption="reply_audio")

@dp.message_handler()
async  def all_msg_handler(message: types.Message) :
    global reply_text
    button_text = message.text

    if button_text == "I'm great!":
        reply_text = "Good for you!"
    if button_text == "I'm tired.":
        reply_text = "Sorry to hear that."
    if button_text == "I am Egor.":
        reply_text = "Nice to meet you!"
    if button_text == "Wait, what?":
        reply_text = "Uhm..."
    if button_text == "Wha?":
        reply_text = "Uh..."
    await message.answer(reply_text, reply_markup=types.ReplyKeyboardRemove())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)