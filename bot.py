import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage


from app.handlers import command, private
# from app.handlers import handlers

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Start working with bot"),
        BotCommand(command="help", description="Get help"),
        BotCommand(command="game", description="Start game"),
        BotCommand(command="profile", description="My profile"),
        BotCommand(command="bag", description="My bag"),
    ]
    await bot.set_my_commands(commands)


async def reset_bot(bot: Bot) -> None:
    # Delete webhook and clear updates queue
    await bot.delete_webhook(drop_pending_updates=True)
    # Delete bot commands
    await bot.delete_my_commands()
    # Clear FSM storage - using close instead of clear
    await storage.close()


async def main() -> None:
    try:
        # dp.include_router(handlers.router)
        dp.include_router(command.router)
        dp.include_router(private.router)
        # setup_logging()

        # First clear old updates
        await bot.delete_webhook(drop_pending_updates=True)

        # Set bot commands
        await set_commands(bot)

        # Start polling with ignored updates
        await dp.start_polling(bot, allowed_updates=[], skip_updates=True)
    finally:
        await reset_bot(bot)
        await storage.close()
        await bot.session.close()
        # setup_logging()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # setup_logging()
        pass