import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from app.config.logging import logger
from app.models.game import Game
from app.models.players import Player

router = Router()

GAME_START = 60

games = {}
players = []
id


@router.message(Command("game"))
async def join_game(message: Message):
    chat_id = message.chat.id
    id = message.from_user.id
    user_name = message.from_user.full_name

    if id not in players:
        players.append(Player(id, user_name))
    else:
        await message.answer("Ви вже у грі!", show_alert=True)

    if chat_id not in games:
        games.setdefault(chat_id, Game(chat_id, []))

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Приєднатися", callback_data="join_game")],
            [InlineKeyboardButton(text="Вийти з гри", callback_data="leave")],
        ]
    )

    game_message = await message.answer(
        "⏳ Збір гравців розпочато!\n"
        "Залишився час: 60 секунд\n\n"
        "Список гравців:\nПоки що ніхто не приєднався",
        reply_markup=keyboard,
    )

    try:
        # Запускаємо таймер
        for remaining_time in range(GAME_START, 0, -1):
            try:
                # current_players = games[chat_id].players
                current_players = [player.name for player in games[chat_id].players]
                players_text = (
                    ",".join(
                        [
                            f"[{player.name}](tg://user?id={player.user_id})"
                            for player in games[chat_id].players
                        ]
                    )
                    if games[chat_id].players
                    else "Поки що ніхто не приєднався"
                )
                emoji = "⏳" if remaining_time % 2 == 0 else "⌛️"

                # Оновлюємо клавіатуру залежно від статусу поточного користувача
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text=(
                                    "Покинути гру"
                                    if message.from_user.full_name in current_players
                                    else "Приєднатися"
                                ),
                                callback_data=(
                                    "leave"
                                    if message.from_user.full_name in current_players
                                    else "join"
                                ),
                            )
                        ],
                    ]
                )

                await game_message.edit_text(
                    f"{emoji} Збір гравців розпочато!\n"
                    f"Залишився час: {remaining_time} секунд\n\n"
                    f"Список гравців:\n{players_text}",
                    reply_markup=keyboard,
                    parse_mode="Markdown",
                )
                await asyncio.sleep(1)
            except Exception as edit_error:
                if "message is not modified" not in str(edit_error):
                    raise edit_error
                await asyncio.sleep(1)

        # Таймер завершено
        players_count = len(games[chat_id].players)

        keyboard_role = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Отримати роль", callback_data="random_role"
                    )
                ],
            ]
        )

        if players_count < 4:
            await message.answer(
                "Недостатньо гравців для початку гри.\n Гру скасовано."
            )
            games.pop(chat_id, None)
        else:
            await message.answer(
                f"Час збору завершено!\n"
                f"Усього гравців: {players_count}\n\n"
                f"Список гравців:\n{players_text}",
                reply_markup=keyboard_role,
                parse_mode="Markdown",
            )

    except Exception as e:
        logger.error(f"Помилка при створенні гри: {e}")
        await message.answer("Сталася помилка при створенні гри!")
        games.pop(chat_id, None)


@router.callback_query(F.data == "join" or F.data == "leave")
async def join_or_leave_game(query: CallbackQuery):
    chat_id = query.message.chat.id
    # user = query.from_user
    user_name = query.from_user.full_name
    user_id = query.from_user.id

    if chat_id not in games:
        await query.answer("Гру не знайдено!", show_alert=True)
        return

    try:
        game_players = games[chat_id].players

        is_join = any(player.user_id == user_id for player in game_players)

        if query.data == "join":
            if not is_join:
                game_players.append(Player(user_id, user_name))
                await query.answer("Ви приєдналися до гри!", show_alert=True)
                logger.info(f"Гравець {user_name} приєднався до гри в чаті {chat_id}")
            else:
                await query.answer("Ви вже у грі!", show_alert=True)

        elif query.data == "leave":
            if is_join:
                games[chat_id].players = [
                    player for player in game_players if player.user_id != user_id
                ]
                await query.answer("Ви покинули гру!", show_alert=True)
            else:
                await query.answer("Вас немає у грі!", show_alert=True)

    except Exception as e:
        logger.error(f"Помилка при обробці дії гравця: {e}")
        await query.answer("Сталася помилка!", show_alert=True)


@router.callback_query(F.data == "random_role")
async def get_role(query: CallbackQuery):
    chat_id = query.message.chat.id
    # user_id = query.from_user.id

    game = games.get(chat_id)

    for player in game.players:
        # if player.user_id == user_id:
        role = game.random_role()
        player.role = role
        await query.answer(f"Твоя роль: {role}", show_alert=True)
        # elif player.user_id != user_id:
        #     await query.answer("Ти не є учасником гри", show_alert=True)
