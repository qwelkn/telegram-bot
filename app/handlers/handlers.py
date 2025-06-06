from aiogram import Router 
from aiogram.filters import CommandStart, Command
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton, 
                           CallbackQuery,
                           Message)
from app.keyboards.keyboards import menu_profile, mafia_buttons

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")

@router.message(Command("profile"))
async def menu(message: Message):
    text = (
        "💵 Гривні: 7340 \n" 
        "💰 Золото Полуботка: 0"
    )
    await message.answer("text", reply_markup=menu_profile)

@router.message(Command("test"))
async def test(message: Message):
    await message.answer("text",reply_markup=mafia_buttons)

@router.message(Command("game"))
async def join_game(message: Message):
    await message.answer("Набір у гру триває\n "
    "Гравці: ", 
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Приєднатися", callback_data="join_game")
                                 ]
                             ]
                         )
                         )
    
@router.callback_query(lambda c: c.data == "join_game")
async def process_join(callback: CallbackQuery):
    user_name = callback.from_user.first_name  # Отримуємо ім'я гравця
    
    active_players = []

    # Додаємо ім'я в список, якщо його ще немає
    if user_name not in active_players:
        active_players.append(user_name)

    # Формуємо новий текст з гравцями
    new_text = "Набір у гру триває\n\nГравці:\n" + "\n".join(active_players)

    # Редагуємо попереднє повідомлення
    await callback.message.edit_text(new_text, reply_markup=callback.message.reply_markup)

    # Відповідаємо на callback (щоб кнопка не "зависала")
    await callback.answer("Ви приєднались до гри!")