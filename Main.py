import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен из переменных окружения Render
BOT_TOKEN = os.getenv("8722039884:AAGxeOFmja1NADpP9Q7CPDiFuQBPi5yVS1A")

if not BOT_TOKEN:
    raise ValueError("ОШИБКА: Переменная BOT_TOKEN не найдена в Environment Variables!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- Главное меню (Клавиатура) ---
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


# --- Кнопка Назад ---
def back_keyboard():
    kb = [
        [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# --- Команда /start ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    text = (
        f"🐾 **KISA-VPN** | Привет, {message.from_user.first_name}!\n\n"
        "Я — твой кибер-кот KISA 🐱. Я обеспечиваю безопасный, "
        "анонимный и сверхскоростной доступ в интернет.\n\n"
        "Выбери нужное действие в меню ниже 👇"
    )
    await message.answer(text, reply_markup=main_keyboard(), parse_mode="Markdown")


# --- Возврат в главное меню ---
@dp.callback_query(F.data == "main_menu")
async def process_main_menu(callback: types.CallbackQuery):
    text = (
        "🐾 **Главное меню KISA-VPN**\n\n"
        "Выбери нужный раздел ниже:"
    )
    await callback.message.edit_text(text, reply_markup=main_keyboard(), parse_mode="Markdown")
    await callback.answer()


# --- Личный кабинет ---
@dp.callback_query(F.data == "profile")
async def process_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    text = (
        f"👤 **Личный кабинет**\n\n"
        f"🆔 **Ваш ID:** `{user_id}`\n"
        f"📊 **Статус подписки:** 🔴 Не активна\n"
        f"⏳ **Срок действия:** —\n\n"
        "Оформите подписку, чтобы получить свой приватный ключ!"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")
    await callback.answer()


# --- Получить VPN (Тестовый ключ) ---
@dp.callback_query(F.data == "get_vpn")
async def process_get_vpn(callback: types.CallbackQuery):
    text = (
        "🔑 **Ваш тестовый ключ KISA-VPN:**\n\n"
        "`vless://test-key-kisa-vpn-placeholder@127.0.0.1:443?type=tcp&security=reality#KISA-VPN-Test`\n\n"
        "📌 *Нажмите на код выше, чтобы скопировать его.*"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")
    await callback.answer()


# --- Инструкции ---
@dp.callback_query(F.data == "instructions")
async def process_instructions(callback: types.CallbackQuery):
    text = (
        "📖 **Инструкция по подключению KISA-VPN**\n\n"
        "1. Скопируйте ваш ключ из раздела **«Получить VPN»**.\n"
        "2. Скачайте приложение для вашего устройства:\n"
        "   • **Android:** v2rayNG / Happ\n"
        "   • **iOS (iPhone):** Streisand / V2Box / v2rayTUN\n"
        "   • **Windows:** v2rayN\n"
        "3. Вставьте ключ в приложение и нажмите **Подключиться** 🚀"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")
    await callback.answer()


# --- Поддержка ---
@dp.callback_query(F.data == "support")
async def process_support(callback: types.CallbackQuery):
    text = (
        "💬 **Служба поддержки KISA-VPN**\n\n"
        "Если у вас возникли проблемы с подключением или оплатой, "
        "напишите нашему администратору."
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")
    await callback.answer()


# --- Запуск бота ---
async def main():
    print("🚀 KISA-VPN Bot успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
