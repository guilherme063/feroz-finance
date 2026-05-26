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

# ================= FUNÇÕES =================

def pegar_nome(user_id):

    if user_id == 8943277650:
        return "Guilherme"

    elif user_id == 8626825035:
        return "Maiane"

    return "Usuário"

# ================= MENU =================

def menu_markup():

    teclado = [