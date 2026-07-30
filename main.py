import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import web

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Получение токена из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("ОШИБКА: Переменная BOT_TOKEN не найдена!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ВЕБ-СЕРВЕР ДЛЯ РЕНДЕРА (чтобы не просил карту) ---
async def handle_healthcheck(request):
    return web.Response(text="KISA-VPN Bot is alive 🐾")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_healthcheck)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- КЛАВИАТУРЫ ---
def main_keyboard():
    kb = [
        [
            InlineKeyboardButton(text="🔑 Получить VPN", callback_data="get_vpn"),
            InlineKeyboardButton(text="👤 Личный кабинет", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="📖 Инструкция", callback_data="instructions"),
            InlineKeyboardButton(text="💬 Поддержка", callback_data="support")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ В главное меню", callback_data="main_menu")]])

# --- ОБРАБОТЧИКИ (HANDLERS) ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    text = (
        f"🐾 **KISA-VPN** | Привет, {message.from_user.first_name}!\n\n"
        "Я — твой кибер-кот KISA 🐱. Я обеспечиваю безопасный, "
        "анонимный и сверхскоростной доступ в интернет.\n\n"
        "Выбери нужное действие в меню ниже 👇"
    )
    await message.answer(text, reply_markup=main_keyboard(), parse_mode="Markdown")

@dp.callback_query(F.data == "main_menu")
async def process_main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("🐾 **Главное меню KISA-VPN**\n\nВыбери нужный раздел ниже:", reply_markup=main_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "profile")
async def process_profile(callback: types.CallbackQuery):
    text = (
        f"👤 **Личный кабинет**\n\n"
        f"🆔 **Ваш ID:** `{callback.from_user.id}`\n"
        f"📊 **Статус подписки:** 🔴 Не активна\n\n"
        "Оформите подписку, чтобы получить свой приватный ключ!"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "get_vpn")
async def process_get_vpn(callback: types.CallbackQuery):
    text = (
        "🔑 **Ваш тестовый ключ KISA-VPN:**\n\n"
        "`vless://test-key-kisa-vpn-placeholder@127.0.0.1:443?type=tcp&security=reality#KISA-VPN-Test`\n\n"
        "📌 *Нажмите на код выше, чтобы скопировать его.*"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "instructions")
async def process_instructions(callback: types.CallbackQuery):
    text = (
        "📖 **Инструкция по подключению KISA-VPN**\n\n"
        "1. Скопируйте ваш ключ.\n"
        "2. Скачайте **v2rayNG** (Android) или **Streisand / V2Box** (iOS).\n"
        "3. Вставьте ключ и нажмите **Подключиться** 🚀"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "support")
async def process_support(callback: types.CallbackQuery):
    await callback.message.edit_text("💬 **Служба поддержки KISA-VPN**\n\nНапишите нашему администратору.", reply_markup=back_keyboard(), parse_mode="Markdown")
    await callback.answer()

# --- ЗАПУСК ---
async def main():
    await start_web_server()
    print("🚀 KISA-VPN Bot успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

