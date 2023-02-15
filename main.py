from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler 
from telegram import  InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
import logging
import utils



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
  #print(update)
  

  
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
  mention = "["+userFirstName+"](tg://user?id="+str(userId)+")"    
  await context.bot.send_message (
    chat_id=chatId,
    parse_mode = "Markdown",
    text=f"""Welcome to *Iconicmind* {mention}
    Reglas: 
    1. No spamming""",
    reply_markup=InlineKeyboardMarkup([
      [
        InlineKeyboardButton(text="Call Center", callback_data="phones"), 
        InlineKeyboardButton(text="Scans  Proccess", callback_data="scans")
      ],
      [
        InlineKeyboardButton(text="Administration", callback_data="administration"),
        InlineKeyboardButton(text="Other", callback_data="other")
      ],
      
    ])
    
  )
  return input_state
    


async def buttons_handler (update, context):
  
  charge = update.callback_query.data
  user_tlgid = update.callback_query.from_user.id
  user_firstN = update.callback_query.from_user.first_name
  user_lastN = None
  username = None
  if update.callback_query.from_user.last_name:
    user_lastN = update.callback_query.from_user.last_name
  if update.callback_query.from_user.username:
    username = update.callback_query.from_user.username  
  register = utils.register_employe(user_tlgid, user_firstN, username, charge)  
  print(register)
  query = update.callback_query
  if register == None:    
    # query.answer()
    await query.message.edit_text(
      text="thanks you"
    )
  else: 
    await query.message.edit_text(
      text=register
    )
    
  
  return ConversationHandler.END
  
async def remove_user(update, context):
  print("---- estamos en el remove----")
  tlg_id = update.message.left_chat_member.id
  user_name = update.message.left_chat_member.first_name
  mention = "["+user_name+"](tg://user?id="+str(tlg_id)+")"   
  response = utils.remove_user(str(tlg_id))
  print(tlg_id)
  if response == None:
    text = f"I removed {mention} successfully"
    await update.message.reply_text(text, parse_mode = "Markdown",)
  else: 
    text = f"I have a error tried to remove {mention}"
    await update.message.reply_text(text,parse_mode = "Markdown",)
    
  
def main():
# Starting Bot
  token = os.getenv("tlgToken")
  application = Application.builder().token(token).build()
  logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  application.add_handler(CommandHandler('start', start))
  application.add_handler(CommandHandler('chat_id', chatId))
  application.add_handler(MessageHandler(filters.TEXT, processed_messages ))
  application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, rules_group ))
  application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, remove_user ))
  
  application.add_handler(ConversationHandler(
    entry_points=[
      #MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, rules_group),
      CallbackQueryHandler(pattern='phones', callback=buttons_handler),
      CallbackQueryHandler(pattern='scans', callback=buttons_handler),
      CallbackQueryHandler(pattern='administration', callback=buttons_handler),
      CallbackQueryHandler(pattern='other', callback=buttons_handler)
      
    ],
    states={
      input_state:
        [
          # MessageHandler(filters.TEXT, processed_messages ),
          CallbackQueryHandler(pattern='phones', callback=buttons_handler),
          CallbackQueryHandler(pattern='scans', callback=buttons_handler),
          CallbackQueryHandler(pattern='administration', callback=buttons_handler),
          CallbackQueryHandler(pattern='other', callback=buttons_handler)
        ]
      },
    fallbacks=[]
  ))
  
  print('Starting process')
  application.run_polling()
  
if __name__ == '__main__':
  main()
