from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import json
from datetime import datetime

TOKEN = "8746573661:AAGB6164g19ls49PobR29aTBKyuV00c5dVA"


def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}


def save_users(users):
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команды:\n"
        "/check ник\n"
        "/add ник причина\n"
        "/remove ник\n"
        "/list"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Используй: /check ник или часть ника")
        return

    search = context.args[0].lower()
    users = load_users()

    # ищем всех совпадающих
    matches = [username for username in users.keys() if search in username]

    if not matches:
        await update.message.reply_text("✅ Ничего не найдено")
        return

    # если найден 1 человек — показываем полную инфу
    if len(matches) == 1:
        username = matches[0]
        user = users[username]

        text = (
            f"❌ Есть в списке\n\n"
            f"👤 Ник: {username}\n"
            f"📌 Причина: {user['reason']}\n"
            f"➕ Добавил: {user['added_by']}\n"
            f"📅 Дата: {user['date']}"
        )

        await update.message.reply_text(text)
        return

    # если найдено несколько — список
    text = "🔎 Найдено несколько совпадений:\n\n"
    text += "\n".join([f"• {m}" for m in matches])

    await update.message.reply_text(text)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Используй: /add ник причина")
        return

    username = context.args[0].lower()
    reason = " ".join(context.args[1:])

    users = load_users()

    users[username] = {
        "reason": reason,
        "added_by": update.effective_user.username,
        "date": datetime.now().strftime("%d.%m.%Y"),
    }

    save_users(users)

    await update.message.reply_text(f"✅ {username} добавлен")


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Используй: /remove ник")
        return

    username = context.args[0].lower()
    users = load_users()

    if username in users:
        del users[username]
        save_users(users)
        await update.message.reply_text(f"🗑 {username} удалён")
    else:
        await update.message.reply_text("Такого пользователя нет")


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()

    if not users:
        await update.message.reply_text("Список пуст")
        return

    text = "\n".join(users.keys())
    await update.message.reply_text(text)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("remove", remove))
app.add_handler(CommandHandler("list", list_users))

print("Бот запущен...")
app.run_polling()