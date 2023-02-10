from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler 
from telegram import  InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
import logging



load_dotenv()
input_state = 0

async def start(update,context):
  user = update.effective_user  
  await update.message.reply_text(f"Greetings {user.username}!")
  
async def processed_messages(update, context):
  print('test')
  # user = update.effective_user
  # mesg = update.message.text
  # print(update)
  # print(user)
  # print(mesg)
  print(update)
  
async def buttons_handler (update, context):
  print(update)
  
async def chatId(update,context):
    """Returns the chat id where the bot responds to"""
    chatId = update.message.chat.id
    await update.message.reply_text(chatId)
  
async def rules_group (update, context):
  print('----entramos a rules---')
  chatId = update.message.chat.id
  userData = update.message.new_chat_members
  for User in userData:
    userFirstName = User.first_name
    userId = User.id
    if(User.username):
      userName = User.username
    else:
      userName = None
    if (User.last_name):
      userLastName = User.last_name
    else:
      userLastName=None
  mention = "["+userFirstName+"](tg://user?id="+str(userId)+")"  
  # button1 = InlineKeyboardButton(
  #   text="probando",
  #   url="google.com"
  # )
  
  await context.bot.send_message (
    chat_id=chatId,
    parse_mode = "Markdown",
    text=f"""Welcome to *Iconicmind* {mention}
    Reglas: 
    1. No spamming""",
    reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton(text="testing", callback_data="test1")],
    ])
    
  )
  return input_state
    
  
  
 
  
def main():
# Starting Bot
  token = os.getenv("tlgToken")
  application = Application.builder().token(token).build()
  logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  application.add_handler(CommandHandler('start', start))
  application.add_handler(CommandHandler('chat_id', chatId))
  application.add_handler(MessageHandler(filters.TEXT, processed_messages ))
  #application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, rules_group ))
  application.add_handler(ConversationHandler(
    entry_points=[
      MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, rules_group),
      CallbackQueryHandler(pattern='test', callback=buttons_handler)
    ],
    states={
      input_state:[MessageHandler(filters.TEXT, processed_messages )]
      },
    fallbacks=[]
  ))
  application.add_handler
  print('Starting process')
  application.run_polling()
  
if __name__ == '__main__':
  main()
