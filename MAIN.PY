import random
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
    ContextTypes
)
from uuid import uuid4

TOKEN = "7566352440:AAFpJHdWSZyc96xqkZKO6fx1sMnZG-U4kL0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "¡Hola! Soy un bot que tira dados y monedas, estos son mis comandos:\n\n"
        "/moneda - 🪙 Tiras una moneda (cara o cruz)\n"
        "/dado - 🎲 Tiras un dado de 6 caras\n"
        "/dado <número> - 🎲 Tiras un dado con el número de caras que quieras\n\n"
        "También puedes usarme desde cualquier chat escribiendo: @TuNombreDeBot"
    )
    await update.message.reply_text(mensaje)

async def moneda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numero = random.randint(1, 8222)
    if numero == 1:
        resultado = "😱 ¡La moneda cayó PARADA! como os gusta 🥵..."
    else:
        resultado = f"🪙 La moneda cayó: {random.choice(['Cara', 'Cruz'])}"
    await update.message.reply_text(resultado)

async def dado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        caras = int(context.args[0]) if context.args else 6
        if caras == 1:
            await update.message.reply_text("🚫 Como que un dado de 1 cara que eres, ¿Pendejo?")
            return
        if caras == 2:
            await update.message.reply_text("🪙 Para eso tira una moneda, Cara Almeja")
            return
        if caras == 6 and context.args:
            await update.message.reply_text("🤣 Por personas como tú el shampoo trae instrucciones")
            return
    except (IndexError, ValueError):
        await update.message.reply_text("✏️ Usa un número válido.")
        return

    resultado = random.randint(1, caras)
    await update.message.reply_text(f"🎲 Dado de {caras} caras: {resultado}")

async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip().lower()
    results = []

    if "moneda" in query:
        numero = random.randint(1, 8222)
        if numero == 1:
            resultado = "😱 ¡La moneda cayó PARADA!"
        else:
            resultado = f"🪙 La moneda cayó: {random.choice(['Cara', 'Cruz'])}"

        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="🪙 Lanzar moneda",
                input_message_content=InputTextMessageContent(resultado),
                description="Cara, cruz... o parada 👀",
            )
        )
    else:
        try:
            caras = int(query) if query else 6
            if caras < 1:
                raise ValueError
        except ValueError:
            caras = 6

        resultado = random.randint(1, caras)
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"🎲 Dado de {caras} caras",
                input_message_content=InputTextMessageContent(
                    f"🎲 Resultado del dado de ({caras} caras):   {resultado}"
                ),
                description="Haz clic para enviar el resultado",
            )
        )

    await update.inline_query.answer(results, cache_time=1)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("moneda", moneda))
    app.add_handler(CommandHandler("dado", dado))
    app.add_handler(InlineQueryHandler(inline))

    print("✅ Bot iniciado con modo inline")
    app.run_polling()

if __name__ == '__main__':
    main()
