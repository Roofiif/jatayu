import asyncio
import pandas as pd
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message
from aiogram.filters import Command
from rapidfuzz import process
import os
from dotenv import load_dotenv

load_dotenv()

# Masukkan TOKEN dari BotFather
TOKEN = os.getenv("TOKEN")

# Inisialisasi bot dan dispatcher
bot = Bot(token=TOKEN, parse_mode="Markdown")
dp = Dispatcher()
router = Router()  # Router untuk handler

# Load data perusahaan dari CSV
df = pd.read_csv("companies.csv")
company_names = df["Name"].tolist()

@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Halo! Kirimkan nama perusahaan yang ingin Anda cari.")

@router.message()
async def search_company(message: Message):
    query = message.text.strip()

    # Cari kecocokan dengan RapidFuzz
    matches = process.extract(query, company_names, limit=10, score_cutoff=60)

    if not matches:
        await message.answer("Perusahaan tidak ditemukan. Coba nama lain.")
    else:
        response = "**Hasil Pencarian:**\n\n"
        for match in matches:
            response += f"✅ {match[0]} (Skor: {match[1]}%)\n"

        await message.answer(response)

async def main():
    dp.include_router(router)  # Tambahkan router ke dispatcher
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())  # Gunakan asyncio.run untuk menjalankan bot
