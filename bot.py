from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery
)
# from aiogram import F
from config import (
    BOT_TOKEN,
    FIRST_VIDEO,
    LAST_VIDEO,
    COURSE_VIDEO,
    START_IMG,
)

import asyncio
# import os


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: Message):
    await bot.send_photo(message.chat.id, 
                         photo=START_IMG ,
                         caption="""Я рада тебя приветствовать, моя прекрасная подписчица!""")
    
    await asyncio.sleep(2)
    await bot.send_message(message.chat.id,
                            text="Ты замечала, как тело начинает само двигаться в такт той музыке, что находит в нас отклик?",
                            disable_web_page_preview=True)

    await asyncio.sleep(4)
    await bot.send_message(message.chat.id,
                            text="Я подготовила атмосферную <b>музыкальную подборку</b>, передающую дух трайбла.\nЕсли ты ощутишь, что тебе откликнулась эта музыка, то приглашаю вместе продолжить погружение в мир танца",
                            disable_web_page_preview=True)
    def ease_link_kb():
        inline_kb_list = [
            [InlineKeyboardButton(text="Продолжить знакомство с трайблом", callback_data="continue_tribal")],
                          ]
        return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

    await asyncio.sleep(3)
    await message.answer(
        '<a href="https://music.yandex.ru/users/yanakrem/playlists/1002?utm_medium=copy_link">'
        "Музыкальная подборка Я.Музыки из 20 треков</a>",
        disable_web_page_preview=True,
        reply_markup=ease_link_kb()
    )

# all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
# video_1_file = os.path.join(all_media_dir, 'video_nub_1.mp4')

# @dp.message(F.video)
# async def handle_files(message: types.Message):
#     file_id = bot.get_file(message.video.file_id)
#     print(file_id)
#     video_id = message.video.file_id
#     await message.answer(f"ID вашего видео: {video_id}")

# @dp.message(Command('send_video'))
# async def cmd_start(message: types.Message, state: FSMContext):
#     video_file = FSInputFile(path=os.path.join(all_media_dir, 'video_nub_3.mp4'))
#     msg = await message.answer_video(video=video_file,
#                                      caption='Моя отформатированная подпись к файлу')
#     await asyncio.sleep(2)
#     print(msg.video.file_id)

# @dp.message(Command('send_photo'))
# async def cmd_start(message: Message, state: FSMContext):
#     photo_file = FSInputFile(path=os.path.join(all_media_dir, 'start_img.jpg'))
#     msg_id = await message.answer_photo(photo=photo_file,
#                                         caption='Моя <u>отформатированная</u> подпись к <b>фото</b>')
#     print(msg_id.photo[-1].file_id)

@dp.callback_query(lambda c: c.data == "continue_tribal")
async def send_video_1(callback_query: CallbackQuery):
    # video_file = FSInputFile(path=os.path.join(all_media_dir, 'video_nub_1.mp4'))
    await bot.send_video(callback_query.message.chat.id, video=FIRST_VIDEO)
    def link_course():
        inline_kb_list = [
            [InlineKeyboardButton(text="Посмотреть урок", callback_data="view_lesson")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    await asyncio.sleep(3)

    await bot.send_message(callback_query.message.chat.id, text="Продолжаем погружение в мир трайбла?", reply_markup=link_course())


@dp.callback_query(lambda c: c.data == "view_lesson")
async def send_lesson_video(callback_query: types.CallbackQuery):
    await bot.send_video(callback_query.message.chat.id, video=COURSE_VIDEO, caption="Учимся делать волны")

    await asyncio.sleep(4)
    def newYearPromo():
        inline_kb_list = [
            [InlineKeyboardButton(text="Получить промокод к Новому году", callback_data="get_promocode")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    # video_file = FSInputFile(path=os.path.join(all_media_dir, 'video_nub_3.mp4'))
    await bot.send_video(callback_query.message.chat.id, video=LAST_VIDEO)

    await asyncio.sleep(3)
    await bot.send_message(callback_query.message.chat.id, text="С наступающим Новым 2025 годом!", reply_markup=newYearPromo())

@dp.callback_query(lambda c: c.data == "get_promocode")
async def send_promocode(callback_query: CallbackQuery):
    await bot.send_message(
        callback_query.message.chat.id, 
        text="""
Промокод <b>New</b> даёт скидку 50% при приобретении любого онлайн-курса Кремушки до 31.12.24.\n
<a href="https://kremushka.com/kombo">Ссылка на онлайн-курсы</a>\n
По всем вопросам, связанным с онлайн-курсами, пожалуйста, обращайтесь @krema_support
""")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
