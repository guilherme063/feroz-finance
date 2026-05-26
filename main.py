from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import sqlite3
import os

# ================= TOKEN =================

TOKEN = os.getenv("8966773536:AAHN4eLyYBPs9kqm3zrG6fyx9-ralws3LPU")

# ================= ADMINS =================

ADMINS = [
    8943277650,
    8626825035
]

# ================= DATABASE =================

db = sqlite3.connect(
    "finance.db",
    check_same_thread=False
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movimentacoes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    valor REAL,
    categoria TEXT,
    tipo TEXT
)
""")

db.commit()

# ================= MENU =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = [

        ["➕ Gasto", "💰 Receita"],

        ["📊 Relatório", "📋 Lista"],

        ["🏆 Ranking", "🗑 Apagar"]

    ]

    menu = ReplyKeyboardMarkup(
        teclado,
        resize_keyboard=True
    )

    texto = """
💎 FEROZ FINANCE

━━━━━━━━━━━━━━━━━━

💸 Gasto:
g 50 mercado

💰 Receita:
r 1500 salario

🗑 Apagar:
apagar 1

━━━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(
        texto,
        reply_markup=menu
    )

# ================= PEGAR NOME =================

def pegar_nome(user_id):

    if user_id == 8943277650:
        return "Guilherme"

    elif user_id == 8626825035:
        return "Maiane"

    return "Usuário"

# ================= GASTO =================

async def registrar_gasto(update):

    partes = update.message.text.split()

    if len(partes) < 3:

        await update.message.reply_text(
            "Use:\ng 50 mercado"
        )

        return

    try:

        valor = float(partes[1])

    except:

        await update.message.reply_text(
            "Valor inválido."
        )

        return

    categoria = partes[2]

    nome = pegar_nome(
        update.effective_user.id
    )

    cursor.execute(
        """
        INSERT INTO movimentacoes
        (nome, valor, categoria, tipo)
        VALUES (?, ?, ?, ?)
        """,
        (
            nome,
            valor,
            categoria,
            "gasto"
        )
    )

    db.commit()

    await update.message.reply_text(f"""
✅ GASTO SALVO

👤 {nome}
💵 R${valor}
📂 {categoria}
""")

# ================= RECEITA =================

async def registrar_receita(update):

    partes = update.message.text.split()

    if len(partes) < 3:

        await update.message.reply_text(
            "Use:\nr 1500 salario"
        )

        return

    try:

        valor = float(partes[1])

    except:

        await update.message.reply_text(
            "Valor inválido."
        )

        return

    categoria = partes[2]

    nome = pegar_nome(
        update.effective_user.id
    )

    cursor.execute(
        """
        INSERT INTO movimentacoes
        (nome, valor, categoria, tipo)
        VALUES (?, ?, ?, ?)
        """,
        (
            nome,
            valor,
            categoria,
            "receita"
        )
    )

    db.commit()

    await update.message.reply_text(f"""
✅ RECEITA SALVA

👤 {nome}
💵 R${valor}
📂 {categoria}
""")

# ================= RELATÓRIO =================

async def relatorio(update):

    cursor.execute("""
    SELECT SUM(valor)
    FROM movimentacoes
    WHERE tipo='gasto'
    """)

    gastos = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUM(valor)
    FROM movimentacoes
    WHERE tipo='receita'
    """)

    receitas = cursor.fetchone()[0]

    if gastos is None:
        gastos = 0

    if receitas is None:
        receitas = 0

    saldo = receitas - gastos

    texto = f"""
📊 RELATÓRIO

💸 Gastos:
R${round(gastos,2)}

💰 Receitas:
R${round(receitas,2)}

🏦 Saldo:
R${round(saldo,2)}
"""

    await update.message.reply_text(texto)

# ================= LISTA =================

async def lista(update):

    cursor.execute("""
    SELECT * FROM movimentacoes
    ORDER BY id DESC
    LIMIT 10
    """)

    dados = cursor.fetchall()

    if len(dados) == 0:

        await update.message.reply_text(
            "Nenhuma movimentação."
        )

        return

    texto = "📋 MOVIMENTAÇÕES\n\n"

    for mov in dados:

        texto += (
            f"#{mov[0]} | "
            f"{mov[1]} | "
            f"R${mov[2]} | "
            f"{mov[3]}\n"
        )

    await update.message.reply_text(texto)

# ================= APAGAR =================

async def apagar(update):

    partes = update.message.text.split()

    if len(partes) < 2:

        await update.message.reply_text(
            "Use:\napagar 1"
        )

        return

    idd = partes[1]

    cursor.execute(
        "DELETE FROM movimentacoes WHERE id=?",
        (idd,)
    )

    db.commit()

    await update.message.reply_text(
        f"🗑 Registro {idd} apagado."
    )

# ================= RANKING =================

async def ranking(update):

    cursor.execute("""
    SELECT nome, SUM(valor)
    FROM movimentacoes
    WHERE tipo='gasto'
    GROUP BY nome
    ORDER BY SUM(valor) DESC
    """)

    dados = cursor.fetchall()

    texto = "🏆 RANKING\n\n"

    for pos, item in enumerate(dados, start=1):

        texto += (
            f"{pos}° {item[0]}\n"
            f"💸 R${round(item[1],2)}\n\n"
        )

    await update.message.reply_text(texto)

# ================= MENU =================

async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    texto = update.message.text.lower()

    if texto == "➕ gasto":

        await update.message.reply_text(
            "Digite:\ng 50 mercado"
        )

    elif texto == "💰 receita":

        await update.message.reply_text(
            "Digite:\nr 1500 salario"
        )

    elif texto == "📊 relatório":

        await relatorio(update)

    elif texto == "📋 lista":

        await lista(update)

    elif texto == "🏆 ranking":

        await ranking(update)

    elif texto == "🗑 apagar":

        await update.message.reply_text(
            "Digite:\napagar 1"
        )

    elif texto.startswith("g "):

        await registrar_gasto(update)

    elif texto.startswith("r "):

        await registrar_receita(update)

    elif texto.startswith("apagar"):

        await apagar(update)

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
    MessageHandler(
        filters.TEXT,
        mensagens
    )
)

print("FEROZ ONLINE ✅")

app.run_polling()