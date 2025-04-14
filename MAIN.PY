import random
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "7566352440:AAFpJHdWSZyc96xqkZKO6fx1sMnZG-U4kL0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "¡Hola! Soy un bot de dados. Estos son mis comandos:\n"
        "/moneda - Lanza una moneda\n"
        "/3c a /20c - Lanza un dado con ese número de caras\n"
        "/dado <número> - Lanza un dado con caras personalizadas"
    )
    await update.message.reply_text(mensaje)

async def moneda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado = random.choice(['Cara', 'Cruz'])
    await update.message.reply_text(f"🪙 La moneda muestra: {resultado}")

async def dado_especifico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comando = update.message.text
    match = re.match(r'^/(\d+)c$', comando)
    
    if not match:
        return
    
    try:
        caras = int(match.group(1))
    except ValueError:
        await update.message.reply_text("Formato inválido")
        return
    
    if 3 <= caras <= 20:
        resultado = random.randint(1, caras)
        await update.message.reply_text(f"🎲 Dado de {caras} caras: {resultado}")
    else:
        await update.message.reply_text("⚠️ Usa un número entre 3 y 20 para este comando")

async def dado_personalizado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        caras = int(context.args[0])
        if caras < 1:
            raise ValueError
    except (IndexError, ValueError):
        await update.message.reply_text("✏️ Indica un número válido de caras\nEjemplo: /dado 15")
        return
    
    resultado = random.randint(1, caras)
    await update.message.reply_text(f"🎲 Dado de {caras} caras: {resultado}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("moneda", moneda))
    app.add_handler(CommandHandler("dado", dado_personalizado))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/\d+c$'), dado_especifico))

    print("✅ Bot iniciado")
    app.run_polling()

if __name__ == '__main__':
    main()
