from telegram.ext import Application, CommandHandler, MessageHandler, filters 
from dotenv import load_dotenv
import os
import logging



load_dotenv()

async def start(update,context):
  user = update.effective_user  
  await update.message.reply_text(f"Greetings {user.username}!")
  
async def processed_messages(update, context):
  print('test')
  user = update.effective_user
  mesg = update.message.text
  print(update)
  print(user)
  print(mesg)
  
  
def main():
# Starting Bot
  token = os.getenv("tlgToken")
  application = Application.builder().token(token).build()
  logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  application.add_handler(CommandHandler('start', start))
  application.add_handler(MessageHandler(filters.TEXT, processed_messages ))
  application.add_handler
  print('Starting process')
  application.run_polling()
  
if __name__ == '__main__':
  main()
