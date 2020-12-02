import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gtts import gTTS
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('This bot converts text to audio try sending a file')

def TexttoAudio(update: Update,context,text=None):
    if(text==None):
        text=update.message.text
    speech = gTTS(text=text, lang="en-us")
    speech.save(str(update.message.chat_id) + ".mp3")
    update.message.reply_audio(audio=open(str(update.message.chat_id) + ".mp3", 'rb'))
def FiletoAudio(update: Update, context: CallbackContext):
    File1=open(update.message.document.get_file().download(custom_path=str(update.message.chat_id)+".txt"))
    string = File1.read()
    TexttoAudio(update,context,string)



def main():
  
    Token="Enter your token here"
    updater = Updater(Token, use_context=True)

   
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler("hi",TexttoAudio(Update,CallbackContext,text="hello")))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,TexttoAudio))
    dispatcher.add_handler(MessageHandler(Filters.document & ~Filters.command, FiletoAudio))
    dispatcher.add_handler(MessageHandler(~Filters.document & ~Filters.command,help_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
