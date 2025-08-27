import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

# הכנס כאן את הטוקן שקיבלת מ-BotFather
BOT_TOKEN = "8388838263:AAFbVAx1rTOLJ4JiHXLCkS4h5eOWAbpfPhc"

# כתובת ה-API של Google Sheets שהפעלת
GOOGLE_SHEETS_API_URL = "https://script.google.com/macros/s/AKfycbwe0TmNVfaZxYJBAw6UPQLpEXKUpqVK6jGbxkQKGBTiXLYuOgDuUE2z6Oublid_l01Ing/exec"

# הגדרת לוגים – עוזר לזהות תקלות
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "שלום! שלח לי את שם המנה ואני אחזור אליך עם המרכיבים והאלרגנים."
    )

# הודעות רגילות
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    meal_name = update.message.text.strip()
    params = {'q': meal_name}
    
    try:
        response = requests.get(GOOGLE_SHEETS_API_URL, params=params)
        data = response.json()
        
        if "error" in data:
            await update.message.reply_text("מצטער, לא מצאתי את המנה ששלחת.")
        else:
            ingredients = data.get("מרכיבים", "אין מידע")
            allergens = data.get("אלרגנים", "אין מידע")
            reply = f"📋 *{meal_name}*\n\n*מרכיבים:*\n{ingredients}\n\n*אלרגנים:*\n{allergens}"
            await update.message.reply_text(reply, parse_mode='Markdown')
            
    except Exception as e:
        await update.message.reply_text("אירעה שגיאה בחיפוש המידע, אנא נסה שוב מאוחר יותר.")
        logging.error(f"שגיאה: {e}")

# פונקציית הפעלה
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("הבוט רץ... לחץ Ctrl+C כדי לעצור.")
    app.run_polling()

# נקודת התחלה
if __name__ == '__main__':
    main()
