import telebot
import whisper
import string
import random
model = whisper.load_model("medium")
bot = telebot.TeleBot('Токен Бота')

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.username}\n\nЯ умею преобразовать аудио, видео и голосовое сообщение в текст!\nПоделитесь аудио/видео/голосовым сообщением и ждите текста :)")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.from_user.id, f"Чтобы получить текст, необходимо переслать видео/аудио/голосовое сообщение этому боту и ждите!")

@bot.message_handler(content_types=['video', 'audio', 'voice'])
def handle_audio(message):
    if(message.content_type == 'audio'):
        file_info = bot.get_file(message.audio.file_id)
        message.audio.file_name = generate_random_string(8) + '.mp3'
        namef = message.audio.file_name
    elif(message.content_type == 'video'):
        file_info = bot.get_file(message.video.file_id)
        message.video.file_name = generate_random_string(8) + '.mp4'
        namef = message.video.file_name
    elif (message.content_type == 'voice'):
        file_info = bot.get_file(message.voice.file_id)
        message.voice.file_name = generate_random_string(8) + '.ogg'
        namef = message.voice.file_name

    bot.send_message(message.from_user.id, f'Преобразуем, подождите!')
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'C:/temp/' + namef
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    result = model.transcribe(namef)
    bot.send_message(message.from_user.id, f'Готово!\n\n{result["text"]}')

bot.polling(none_stop=True)