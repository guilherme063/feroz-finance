main.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import sqlite3
from datetime import datetime
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
    tipo TEXT,
    data TEXT
)
""")

db.commit()

# ================= EMOJIS =================

EMOJIS = {
    "mercado": "🛒",
    "combustivel": "⛽",
    "gasolina": "⛽",
    "lanche": "🍔",
    "ifood": "🍕",
    "internet": "🌐",
    "uber": "🚗",
    "farmacia": "💊",
    "cartao": "💳",
    "roupa": "👕",
    "pix": "📲",
    "salario": "💰",
    "extra": "🪙",
    "presente": "🎁"
}

# ================= PEGAR NOME =================

def pegar_nome(user_id):

    if user_id == 8943277650:
        return "Guilherme"

    elif user_id == 8626825035:
        return "Maiane"

    return "Usuário"

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = [
        ["➕ Gasto", "💰 Receita"],
        ["📊 Relatório", "🏦 Saldo"],
        ["📋 Lista", "🏆 Ranking"],
        ["🗑 Apagar"]
    ]

    menu = ReplyKeyboardMarkup(
        teclado,
        resize_keyboard=True
    )

    texto = """
💎 FEROZ FINANCE

━━━━━━━━━━━━━━━━━━
🏦 Sistema Financeiro Premium
━━━━━━━━━━━━━━━━━━

💸 Registrar gasto:
G 50 mercado

💰 Registrar receita:
R 1500 salario

🗑 Apagar movimentação:
APAGAR 3

━━━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(
        texto,
        reply_markup=menu
    )

# ================= GASTO =================

async def registrar_gasto(update):

    texto = update.message.text.lower()

    partes = texto.split()

    if len(partes) < 3:

        await update.message.reply_text(
            "Use:\nG 50 mercado"
        )

        return

    try:
        valor = float(partes[1])

    except:

        await update.message.reply_text(
            "Valor inválido"
        )

        return

    categoria = partes[2]

    nome = pegar_nome(
        update.effective_user.id
    )

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    cursor.execute(
        """
        INSERT INTO movimentacoes
        (nome, valor, categoria, tipo, data)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            nome,
            valor,
            categoria,
            "gasto",
            data
        )
    )

    db.commit()

    emoji = EMOJIS.get(
        categoria,
        "💸"
    )

    await update.message.reply_text(f"""
✅ GASTO SALVO

{emoji} Categoria:
{categoria}

💵 Valor:
R${valor}

👤 Usuário:
{nome}

📅 Data:
{data}
""")

# ================= RECEITA =================

async def registrar_receita(update):

    texto = update.message.text.lower()

    partes = texto.split()

    if len(partes) < 3:

        await update.message.reply_text(
            "Use:\nR 1500 salario"
        )

        return

    try:
        valor = float(partes[1])

    except:

        await update.message.reply_text(
            "Valor inválido"
        )

        return

    categoria = partes[2]

    nome = pegar_nome(
        update.effective_user.id
    )

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    cursor.execute(
        """
        INSERT INTO movimentacoes
        (nome, valor, categoria, tipo, data)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            nome,
            valor,
            categoria,
            "receita",
            data
        )
    )

    db.commit()

    emoji = EMOJIS.get(
        categoria,
        "💰"
    )

    await update.message.reply_text(f"""
✅ RECEITA SALVA

{emoji} Categoria:
{categoria}

💵 Valor:
R${valor}

👤 Usuário:
{nome}

📅 Data:
{data}
""")

# ================= RELATÓRIO =================

async def relatorio(update):

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

    cursor.execute(
        "SELECT * FROM movimentacoes ORDER BY id DESC LIMIT 15"
    )

    dados = cursor.fetchall()

    if len(dados) == 0:

        await update.message.reply_text(
            "Nenhuma movimentação"
        )

        return

    texto = "📋 MOVIMENTAÇÕES\n\n"

    for mov in dados:

        idd = mov[0]
        nome = mov[1]
        valor = mov[2]
        categoria = mov[3]

        emoji = EMOJIS.get(
            categoria,
            "💰"
        )

        texto += (
            f"#{idd} {emoji} {categoria}\n"
            f"💵 R${valor}\n"
            f"👤 {nome}\n\n"
        )

    await update.message.reply_text(texto)

# ================= APAGAR =================

async def apagar(update):

    texto = update.message.text.lower()

    partes = texto.split()

    if len(partes) < 2:

        await update.message.reply_text(
            "Use:\nAPAGAR 3"
        )

        return

    idd = partes[1]

    cursor.execute(
        "DELETE FROM movimentacoes WHERE id=?",
        (idd,)
    )

    db.commit()

    await update.message.reply_text(
        f"🗑 Registro {idd} apagado"
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

        nome = item[0]
        valor = item[1]

        texto += (
            f"{pos}° {nome}\n"
            f"💸 R${round(valor,2)}\n\n"
        )

    await update.message.reply_text(texto)

# ================= MENSAGENS =================

async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    texto = update.message.text

    if texto == "➕ Gasto":

        await update.message.reply_text(
            "💸 Exemplo:\nG 50 mercado"
        )

    elif texto == "💰 Receita":

        await update.message.reply_text(
            "💰 Exemplo:\nR 1500 salario"
        )

    elif texto == "📊 Relatório":

        await relatorio(update)

    elif texto == "🏦 Saldo":

        await relatorio(update)

    elif texto == "📋 Lista":

        await lista(update)

    elif texto == "🏆 Ranking":

        await ranking(update)

    elif texto == "🗑 Apagar":

        await update.message.reply_text(
            "🗑 Exemplo:\nAPAGAR 3"
        )

    elif texto.lower().startswith("g "):

        await registrar_gasto(update)

    elif texto.lower().startswith("r "):

        await registrar_receita(update)

    elif texto.lower().startswith("apagar"):

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

print("💎 FEROZ FINANCE ONLINE")

app.run_polling()

requirements.txt

python-telegram-bot==20.7

PASSO IMPORTANTE

No GitHub:

1. Abra main.py


2. Apague tudo


3. Cole SOMENTE o código de dentro do bloco python


4. Salve em Commit changes


5. Crie também um arquivo chamado:



requirements.txt

6. Cole o texto do requirements nele


7. Commit changes



Depois o Railway vai parar de dar erro.