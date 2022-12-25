import logging
from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN, FILES, AUDIOS
from  pdf import ReadPDF
from voice import Voice
from translator import Translate

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

global document

# Start / Help
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
        await message.reply("Salom! Bu bot orqali siz audio kitoblar yasashingiz mumkin. Foydalanish uchun: PDF fayl jo'nating")

# Any Message except PDF
@dp.message_handler(content_types=types.message.ContentTypes.DOCUMENT)
async def get_file(message: types.file.File):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Audio olish", "Tarjima qilish")

    global document
    document = message.document  
    await message.answer("Amal:", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "Audio olish")
async def convertEn(message: types.Message):
    # Download file
    await message.reply("Processing...", reply_markup=types.ReplyKeyboardRemove())
    await bot.download_file_by_id(document.file_id, FILES + document.file_name) 

    # PDF to TXT
    pdf = ReadPDF(FILES + document.file_name)
    await pdf.read()

    # Create audio
    voice = Voice()
    await voice.toEng(pdf.txt, AUDIOS + document.file_name[:-3] + "mp3")

    # Upload audio
    await message.reply_audio(audio=open(AUDIOS + document.file_name[:-3] + "mp3", "rb"))


@dp.message_handler(lambda message: message.text == "Tarjima qilish")
async def convertUz(message: types.Message):
    # Download file
    await message.reply("Processing...", reply_markup=types.ReplyKeyboardRemove())
    await bot.download_file_by_id(document.file_id, FILES + document.file_name)

    # Read and translate
    tr = Translate()
    uzFile = await tr.to_Uz(FILES + document.file_name)

    # Upload file
    await message.reply_document(document=open( uzFile, "rb"))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

