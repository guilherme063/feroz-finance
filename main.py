from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

import sqlite3
from datetime import datetime

import os

TOKEN = os.getenv("8966773536:AAHN4eLyYBPs9kqm3zrG6fyx9-ralws3LPU")

ADMINS = [
    8943277650,
    8626825035
]

db = sqlite3.connect(
    "finance.db",
    check_same_thread=False
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movimentacoes(
    nome TEXT,
    valor REAL,
    categoria TEXT,
    tipo TEXT,
    data TEXT
)
""")

db.commit()

EMOJIS = {
    "mercado": "🛒",
    "combustivel": "⛽",
    "cartao": "💳",
    "moto": "🏍",
    "internet": "🌐",
    "lanche": "🍔",
    "farmacia": "💊",
    "salario": "💰",
    "extra": "🪙"
}

def pegar_nome(user_id):

    if user_id == 8943277650:
        return "Guilherme"

    elif user_id == 8626825035:
        return "Maiane"

    return "Usuário"

# ================= MENU =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
╔════════════════════╗
║   FEROZ FINANCE    ║
╚════════════════════╝

💰 CONTROLE FINANCEIRO

📌 COMANDOS

/g 50 mercado
/r 1500 salario

/lista
/total
/hoje
/mes
/ranking
/saldo
/menu
"""

    await update.message.reply_text(texto)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
📌 MENU FEROZ

💸 GASTOS
/g 50 mercado

💰 RECEITAS
/r 1500 salario

📊 RELATÓRIOS
/lista
/total
/hoje
/mes
/saldo
/ranking
"""

    await update.message.reply_text(texto)

# ================= GASTO =================

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    if len(context.args) < 2:

        await update.message.reply_text(
            "Use:\n/g 50 mercado"
        )

        return

    valor = float(context.args[0])

    categoria = context.args[1].lower()

    nome = pegar_nome(
        update.effective_user.id
    )

    data = datetime.now().strftime(
        "%d/%m/%Y"
    )

    cursor.execute(
        "INSERT INTO movimentacoes VALUES (?, ?, ?, ?, ?)",
        (
            nome,
            valor,
            categoria,
            "gasto",
            data
        )
    )

    db.commit()

    emoji = EMOJIS.get(categoria, "💸")

    texto = f"""
✅ GASTO SALVO

{emoji} Categoria:
{categoria}

💵 Valor:
R${valor}

👤 Pessoa:
{nome}

📅 Data:
{data}
"""

    await update.message.reply_text(texto)

# ================= RECEITA =================

async def receita(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    if len(context.args) < 2:

        await update.message.reply_text(
            "Use:\n/r 1500 salario"
        )

        return

    valor = float(context.args[0])

    categoria = context.args[1].lower()

    nome = pegar_nome(
        update.effective_user.id
    )

    data = datetime.now().strftime(
        "%d/%m/%Y"
    )

    cursor.execute(
        "INSERT INTO movimentacoes VALUES (?, ?, ?, ?, ?)",
        (
            nome,
            valor,
            categoria,
            "receita",
            data
        )
    )

    db.commit()

    emoji = EMOJIS.get(categoria, "💰")

    texto = f"""
✅ RECEITA SALVA

{emoji} Categoria:
{categoria}

💵 Valor:
R${valor}

👤 Pessoa:
{nome}

📅 Data:
{data}
"""

    await update.message.reply_text(texto)

# ================= LISTA =================

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cursor.execute(
        "SELECT * FROM movimentacoes"
    )

    dados = cursor.fetchall()

    if len(dados) == 0:

        await update.message.reply_text(
            "Nenhuma movimentação"
        )

        return

    texto = "📋 MOVIMENTAÇÕES\n\n"

    for mov in dados:

        nome = mov[0]
        valor = mov[1]
        categoria = mov[2]
        tipo = mov[3]
        data = mov[4]

        emoji = EMOJIS.get(categoria, "💰")

        texto += (
            f"{emoji} {nome} | "
            f"R${valor} | "
            f"{categoria} | "
            f"{tipo} | "
            f"{data}\n"
        )

    await update.message.reply_text(texto)

# ================= TOTAL =================

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cursor.execute(
        "SELECT SUM(valor) FROM movimentacoes WHERE tipo='gasto'"
    )

    gastos = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(valor) FROM movimentacoes WHERE tipo='receita'"
    )

    receitas = cursor.fetchone()[0]

    if gastos is None:
        gastos = 0

    if receitas is None:
        receitas = 0

    saldo = receitas - gastos

    texto = f"""
📊 TOTAL GERAL

💸 Gastos:
R${round(gastos,2)}

💰 Receitas:
R${round(receitas,2)}

🏦 Saldo:
R${round(saldo,2)}
"""

    await update.message.reply_text(texto)

# ================= HOJE =================

async def hoje(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = datetime.now().strftime(
        "%d/%m/%Y"
    )

    cursor.execute(
        "SELECT * FROM movimentacoes WHERE data=?",
        (data,)
    )

    dados = cursor.fetchall()

    if len(dados) == 0:

        await update.message.reply_text(
            "Nenhuma movimentação hoje"
        )

        return

    texto = f"📅 HOJE ({data})\n\n"

    for mov in dados:

        nome = mov[0]
        valor = mov[1]
        categoria = mov[2]

        emoji = EMOJIS.get(categoria, "💰")

        texto += (
            f"{emoji} {nome} - "
            f"R${valor} ({categoria})\n"
        )

    await update.message.reply_text(texto)

# ================= SALDO =================

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cursor.execute(
        "SELECT SUM(valor) FROM movimentacoes WHERE tipo='receita'"
    )

    receitas = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(valor) FROM movimentacoes WHERE tipo='gasto'"
    )

    gastos = cursor.fetchone()[0]

    if receitas is None:
        receitas = 0

    if gastos is None:
        gastos = 0

    saldo_final = receitas - gastos

    await update.message.reply_text(
        f"🏦 SALDO ATUAL\n\nR${round(saldo_final,2)}"
    )

# ================= RANKING =================

async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cursor.execute("""
    SELECT nome, SUM(valor)
    FROM movimentacoes
    WHERE tipo='gasto'
    GROUP BY nome
    ORDER BY SUM(valor) DESC
    """)

    dados = cursor.fetchall()

    texto = "🏆 RANKING DE GASTOS\n\n"

    for pos, item in enumerate(dados, start=1):

        nome = item[0]
        valor = item[1]

        texto += (
            f"{pos}° {nome} - "
            f"R${round(valor,2)}\n"
        )

    await update.message.reply_text(texto)

# ================= APP =================

app = (
    ApplicationBuilder()
    .token(TOKEN)
    .build()
)

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("menu", menu)
)

app.add_handler(
    CommandHandler("g", gasto)
)

app.add_handler(
    CommandHandler("r", receita)
)

app.add_handler(
    CommandHandler("lista", lista)
)

app.add_handler(
    CommandHandler("total", total)
)

app.add_handler(
    CommandHandler("hoje", hoje)
)

app.add_handler(
    CommandHandler("saldo", saldo)
)

app.add_handler(
    CommandHandler("ranking", ranking)
)

print("FEROZ FINANCE ONLINE 😄")

app.run_polling()