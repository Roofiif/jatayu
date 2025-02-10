import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from rapidfuzz import process
import os

# Masukkan TOKEN dari BotFather
TOKEN = os.getenv("TOKEN")

# Inisialisasi bot dan dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Load data perusahaan dari CSV
df = pd.read_csv("companies.csv")
company_names = df["Name"].tolist()

@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    await message.reply("Halo! Kirimkan nama perusahaan yang ingin Anda cari.")

@dp.message_handler()
async def search_company(message: Message):
    query = message.text.strip()

    # Cari kecocokan dengan RapidFuzz
    matches = process.extract(query, company_names, limit=10, score_cutoff=60)

    if not matches:
        await message.reply("Perusahaan tidak ditemukan. Coba nama lain.")
    else:
        response = "**Hasil Pencarian:**\n\n"
        for match in matches:
            response += f"✅ {match[0]} (Skor: {match[1]}%)\n"

        await message.reply(response, parse_mode="Markdown")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)