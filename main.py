from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8966773536:AAHN4eLyYBPs9kqm3zrG6fyx9-ralws3LPU"

USUARIO1 = 8943277650
USUARIO2 = 8626825035

gastos = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
💰 FEROZ FINANCE ONLINE

Comandos:

/g 50 mercado
/g 20 gasolina
/g 100 salario

/lista
/total
"""

    await update.message.reply_text(texto)

async def g(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in [USUARIO1, USUARIO2]:
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Use: /g 50 mercado"
        )
        return

    valor = float(context.args[0])

    categoria = context.args[1]

    if update.effective_user.id == USUARIO1:
        nome = "Guilherme"
    else:
        nome = "Maiane"

    gastos.append(
        [nome, valor, categoria]
    )

    await update.message.reply_text(
        f"✅ {nome} adicionou R${valor} em {categoria}"
    )

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(gastos) == 0:
        await update.message.reply_text(
            "Nenhum gasto salvo"
        )
        return

    texto = "💰 GASTOS\n\n"

    for item in gastos:

        texto += f"{item[0]} - R${item[1]} ({item[2]})\n"

    await update.message.reply_text(texto)

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):

    soma = 0

    for item in gastos:
        soma += item[1]

    await update.message.reply_text(
        f"💰 TOTAL: R${soma}"
    )

app = (
    ApplicationBuilder()
    .token(TOKEN)
    .build()
)

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("g", g)
)

app.add_handler(
    CommandHandler("lista", lista)
)

app.add_handler(
    CommandHandler("total", total)
)

print("FEROZ FINANCE ONLINE 😄")

app.run_polling()