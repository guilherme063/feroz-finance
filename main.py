from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

import sqlite3
from datetime import datetime
import os

# ================= TOKEN =================

TOKEN = os.getenv("TOKEN")

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
    "gasolina": "⛽",
    "combustivel": "⛽",
    "cartao": "💳",
    "moto": "🏍",
    "internet": "🌐",
    "lanche": "🍔",
    "farmacia": "💊",
    "salario": "💰",
    "extra": "🪙",
    "pix": "📲",
    "ifood": "🍕",
    "uber": "🚗",
    "roupa": "👕",
    "presente": "🎁"

}

# ================= NOME =================

def pegar_nome(user_id):

    if user_id == 8943277650:
        return "Guilherme"

    elif user_id == 8626825035:
        return "Maiane"

    return "Usuário"

# ================= MENU =================

def teclado_menu():

    teclado = [

        [
            InlineKeyboardButton(
                "💸 Registrar Gasto",
                callback_data="ajuda_gasto"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 Registrar Receita",
                callback_data="ajuda_receita"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 Ver Relatório",
                callback_data="ajuda_total"
            ),

            InlineKeyboardButton(
                "🏦 Ver Saldo",
                callback_data="ajuda_saldo"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 Movimentações",
                callback_data="ajuda_lista"
            ),

            InlineKeyboardButton(
                "🏆 Ranking",
                callback_data="ajuda_ranking"
            )
        ]

    ]

    return InlineKeyboardMarkup(teclado)

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
💎 <b>FEROZ FINANCE</b>

━━━━━━━━━━━━━━━━━━━
🏦 Painel Financeiro Inteligente
━━━━━━━━━━━━━━━━━━━

💸 Controle de gastos
💰 Controle de receitas
📊 Relatórios automáticos
🏆 Ranking financeiro
📅 Histórico diário

━━━━━━━━━━━━━━━━━━━
👑 Usuários autorizados

• Guilherme
• Maiane
━━━━━━━━━━━━━━━━━━━

👇 Escolha uma opção abaixo
"""

    await update.message.reply_text(
        texto,
        parse_mode="HTML",
        reply_markup=teclado_menu()
    )

# ================= MENU =================

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await start(update, context)

# ================= BOTÕES =================

async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    respostas = {

        "ajuda_gasto":
        "💸 Para registrar um gasto:\n\n/g 50 mercado",

        "ajuda_receita":
        "💰 Para registrar uma receita:\n\n/r 1500 salario",

        "ajuda_total":
        "📊 Ver relatório:\n\n/total",

        "ajuda_saldo":
        "🏦 Ver saldo:\n\n/saldo",

        "ajuda_lista":
        "📋 Ver movimentações:\n\n/lista",

        "ajuda_ranking":
        "🏆 Ver ranking:\n\n/ranking"

    }

    await query.message.reply_text(
        respostas.get(query.data)
    )

# ================= GASTO =================

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    try:

        valor = float(context.args[0])

        categoria = context.args[1].lower()

    except:

        await update.message.reply_text(
            "❌ Use:\n/g 50 mercado"
        )

        return

    nome = pegar_nome(
        update.effective_user.id
    )

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
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

    emoji = EMOJIS.get(
        categoria,
        "💸"
    )

    texto = f"""
✅ <b>GASTO REGISTRADO</b>

{emoji} Categoria:
<b>{categoria}</b>

💵 Valor:
<b>R${valor}</b>

👤 Responsável:
<b>{nome}</b>

📅 Data:
<b>{data}</b>
"""

    await update.message.reply_text(
        texto,
        parse_mode="HTML"
    )

# ================= RECEITA =================

async def receita(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    try:

        valor = float(context.args[0])

        categoria = context.args[1].lower()

    except:

        await update.message.reply_text(
            "❌ Use:\n/r 1500 salario"
        )

        return

    nome = pegar_nome(
        update