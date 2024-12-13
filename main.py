import logging
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

#logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Funzione per ottenere gli issues da GitHub
def fetch_issues():
    url = f"https://api.github.com/repos/Rustastic/Drone/issues"
    response = requests.get(url)
    
    if response.status_code == 200:
        issues = response.json()
        if not issues:
            return "No issues found in the repository."
        # Format the issues
        formatted_issues = "\n\n".join(
            [f"🔹 *#{issue['number']}*: {issue['title']}\n{issue['html_url']}" for issue in issues]
        )
        return formatted_issues
    else:
        return f"Error fetching issues: {response.status_code}"

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE): #change the name of the dependecy
    start_message = """\
    Rustastic: it's fantastic 🦀
    In order to use our fantastic drone add it to the dependencies of your project
    {here there will be a link to our crate}
    more info here: https://github.com/Rustastic/Drone/blob/main/README.md
    
    if there are any problems you can create an issue in the /repo or contact one of us more info if you use the command /contacts
    
    if you want to see all the open issues of our repo you can use the command /issues
    
    Hope this was helpful, good luck with your project🦀🦀\
    """
    await context.bot.send_message(chat_id= update.effective_chat.id,text= start_message)
    
async def repo(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id= update.effective_chat.id, text= "https://github.com/Rustastic/Drone")

async def issues(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id= update.effective_chat.id, text= "Fecthing Issues from https://github/Rustastic/Drone")
    issues = fetch_issues()
    await context.bot.send_message(chat_id= update.effective_chat.id, text= issues)

async def contacts(update: Update, context:ContextTypes.DEFAULT_TYPE):
    contacts_message = "Our telegram handles:\n@Pierpieroprepuzi\n@desossiri_bosio\n@ndrdnn\n@ilBuso\nFeel free to contact us if you have any doubts or problems"
    await context.bot.send_message(chat_id= update.effective_chat.id, text= contacts_message)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id= update.effective_chat.id, text= "Sorry, I didn't understand the command")
    

def main():
    
    load_dotenv()
    
    token = os.getenv("BOT_TOKEN")
    
    if not token:
        raise ValueError("No BOT_TOKEN found in environment variables.")
    
    application = Application.builder().token(token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()
    
    print("Telegram Bot started!", flush=True)

    application.add_handler(CommandHandler("start",start))
    
    application.add_handler(CommandHandler("repo",repo))
    
    application.add_handler(CommandHandler("issues",issues))
    
    application.add_handler(CommandHandler("contacts",contacts))
    
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(MessageHandler(filters.TEXT,unknown))
   
    #application.run_polling()
    
    PORT = int(os.environ.get('PORT', '443'))
    HOOK_URL = f"https://YOUR-CODECAPSULES-URL-HERE/{token}" #change when deployed
    
    application.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=HOOK_URL,
    url_path=token
    )


if __name__ == '__main__':
    main()
