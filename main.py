from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

import sqlite3

# ========= TOKEN =========

TOKEN = "8966773536:AAHN4eLyYBPs9kqm3zrG6fyx9-ralws3LPU"

# ========= ADMINS =========

ADMINS = [
    8943277650,
    8626825035
]

# ========= BANCO =========

db = sqlite3.connect(
    "finance.db",
    check_same_thread=False
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS gastos(
    nome TEXT,
    valor REAL,
    categoria TEXT
)
""")

db.commit()

# ========= EMOJIS =========

EMOJIS = {
    "mercado": "🛒",
    "comb": "⛽",
    "cartao": "💳",
    "moto": "🏍",
    "internet": "🌐",
    "lanche": "🍔"
}

# ========= PEGAR NOME =========

def pegar_nome(user_id):

    if user_id == 8943277650:
        return "Guilherme"

    elif user_id == 8626825035:
        return "Maiane"

    return "Usuário"

# ========= START =========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
╔════════════════════╗
║   FEROZ FINANCE    ║
╚════════════════════╝

💰 BOT FINANCEIRO

Comandos:

/g 50 mercado
/lista
/total
"""

    await update.message.reply_text(texto)

# ========= GASTOS =========

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:

        await update.message.reply_text(
            "❌ Sem permissão"
        )

        return

    if len(context.args) < 2:

        await update.message.reply_text(
            "Use:\n/g 50 mercado"
        )

        return

    try:

        valor = float(context.args[0])

    except:

        await update.message.reply_text(
            "Valor inválido"
        )

        return

    categoria = context.args[1].lower()

    nome = pegar_nome(
        update.effective_user.id
    )

    cursor.execute(
        "INSERT INTO gastos VALUES (?, ?, ?)",
        (nome, valor, categoria)
    )

    db.commit()

    emoji = EMOJIS.get(categoria, "💰")

    texto = f"""
✅ GASTO SALVO

{emoji} Categoria:
{categoria}

💵 Valor:
R${valor}

👤 Pessoa:
{nome}
"""

    await update.message.reply_text(texto)

# ========= LISTA =========

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cursor.execute(
        "SELECT * FROM gastos"
    )

    dados = cursor.fetchall()

    if len(dados) == 0:

        await update.message.reply_text(
            "Nenhum gasto salvo"
        )

        return

    texto = "💰 GASTOS\n\n"

    for gasto in dados:

        nome = gasto[0]
        valor = gasto[1]
        categoria = gasto[2]

        emoji = EMOJIS.get(categoria, "💰")

        texto += (
            f"{emoji} {nome} - "
            f"R${valor} "
            f"({categoria})\n"
        )

    await update.message.reply_text(texto)

# ========= TOTAL =========

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cursor.execute(
        "SELECT SUM(valor) FROM gastos"
    )

    resultado = cursor.fetchone()[0]

    if resultado is None:
        resultado = 0

    texto = f"""
💰 TOTAL GERAL

R${round(resultado, 2)}
"""

    await update.message.reply_text(texto)

# ========= APP =========

app = (
    ApplicationBuilder()
    .token(TOKEN)
    .build()
)

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("g", gasto)
)

app.add_handler(
    CommandHandler("lista", lista)
)

app.add_handler(
    CommandHandler("total", total)
)

print("FEROZ FINANCE ONLINE 😄")

app.run_polling()
