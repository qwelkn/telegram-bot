import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    if message.chat.type != "private":
        await message.answer("Ця команда використовується лише у чаті з ботом")
        return
    await message.answer("Вітаю у мафії!")

@router.message(Command("profile"))
async def profile(message: Message):
    user_name = message.from_user.full_name

    text = (
        f"👤 {user_name} \n"
        "Зіграно ігор: 10\n" 
        "Переможено ігор: 7\n"
        "Виконано завдань: \n"
        "Нагороди: \n"
        "Ранг: початківець\n"
    )
    await message.answer(text, reply_markup=InlineKeyboardMarkup(
        inline_keyboard = [
        [
            InlineKeyboardButton(text="Завдання", callback_data="task")     
        ]
        ]
    )
    )

@router.callback_query(lambda c: c.data == "task")
async def task(query: CallbackQuery):
    text= (
        "Твоє завдання сьогодні: \n"
        "Виграти за мафію два рази"
    )
    await query.answer(text, show_alert=True)

@router.message(Command("bag"))
async def bag(message: Message):
    user_name = message.from_user.full_name
    if message.chat.type != "private":
        await message.answer("Ця команда використовується лише у чаті з ботом")
        return
    
    text = (
        f"👤 {user_name} \n"
        "Гроші: 700\n"
        "Діаманти: 2\n"
        "Захист: 1\n"
        "Документи: 3\n"
        "Міна: 0\n"
        "Таксі: 0"
    )

    await message.answer(text, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="Купити діаманти", callback_data="buy_diamants"),
            InlineKeyboardButton(text="Магазин", callback_data="shop"),
            ]
        ]
    )
    )

@router.message(Command("buy_diamants"))
async def buy_diamants(message: Message):
    pass

@router.message(Command("shop"))
async def shop(message: Message):
    pass
