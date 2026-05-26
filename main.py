from telegram import (
    Update,
    ReplyKeyboardMarkup
)

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

# ==================================================
# 🔐 TOKEN
# ==================================================

TOKEN = os.getenv("8966773536:AAHN4eLyYBPs9kqm3zrG6fyx9-ralws3LPU")

# ==================================================
# 👤 ADMINS
# ==================================================

ADMINS = [
    8943277650,
    8626825035
]

# ==================================================
# 💾 DATABASE
# ==================================================

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

# ==================================================
# 🎨 EMOJIS
# ==================================================

EMOJIS = {

    "mercado": "🛒",
    "gasolina": "⛽",
    "combustivel": "⛽",
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

# ==================================================
# 👤 NOME
# ==================================================

def pegar_nome(user_id):

    if user_id == 8943277650:
        return "Guilherme"

    elif user_id == 8626825035:
        return "Maiane"

    return "Usuário"

# ==================================================
# 🏠 MENU
# ==================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = [

        ["➕ Gasto", "💰 Receita"],

        ["📊 Relatório", "🏦 Saldo"],

        ["📅 Hoje", "📆 Mês"],

        ["📋 Lista", "🗑 Apagar"],

        ["🏆 Ranking"]

    ]

    menu = ReplyKeyboardMarkup(
        teclado,
        resize_keyboard=True
    )

    texto = f"""
╔══════════════════════╗
      💎 FEROZ FINANCE
╚══════════════════════╝

🏦 SISTEMA FINANCEIRO PREMIUM

━━━━━━━━━━━━━━━━━━

💸 Controle de gastos
💰 Controle de receitas
📊 Relatórios automáticos
🏆 Ranking financeiro
🗑 Exclusão rápida
📆 Histórico mensal

━━━━━━━━━━━━━━━━━━

🔥 COMO USAR

💸 Adicionar gasto:
g 50 mercado

💰 Adicionar receita:
r 1500 salario

🗑 Apagar:
apagar 3

━━━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(
        texto,
        reply_markup=menu
    )

# ==================================================
# 💸 GASTO
# ==================================================

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text.lower()

    partes = texto.split()

    if len(partes) < 3:
        return

    valor = float(partes[1])

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
╔════════════════╗
   ✅ GASTO SALVO
╚════════════════╝

{emoji} Categoria:
{categoria}

💵 Valor:
R${valor}

👤 Usuário:
{nome}

📅 Data:
{data}
""")

# ==================================================
# 💰 RECEITA
# ==================================================

async def receita(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text.lower()

    partes = texto.split()

    if len(partes) < 3:
        return

    valor = float(partes[1])

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
╔══════════════════╗
   ✅ RECEITA SALVA
╚══════════════════╝

{emoji} Categoria:
{categoria}

💵 Valor:
R${valor}

👤 Usuário:
{nome}

📅 Data:
{data}
""")

# ==================================================
# 📋 LISTA
# ==================================================

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cursor.execute("""
    SELECT * FROM movimentacoes
    ORDER BY id DESC
    LIMIT 15
    """)

    dados = cursor.fetchall()

    if not dados:

        await update.message.reply_text(
            "📭 Nenhuma movimentação"
        )

        return

    texto = "📋 ÚLTIMAS MOVIMENTAÇÕES\n\n"

    for mov in dados:

        idd = mov[0]
        nome = mov[1]
        valor = mov[2]
        categoria = mov[3]
        tipo = mov[4]

        emoji = EMOJIS.get(
            categoria,
            "💰"
        )

        if tipo == "gasto":
            icone = "💸"
        else:
            icone = "💰"

        texto += (
            f"#{idd} {emoji} {categoria}\n"
            f"{icone} R${valor}\n"
            f"👤 {nome}\n\n"
        )

    await update.message.reply_text(texto)

# ==================================================
# 🗑 APAGAR
# ==================================================

async def apagar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text.lower()

    partes = texto.split()

    if len(partes) < 2:

        await update.message.reply_text(
            "Use:\napagar 3"
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

# ==================================================
# 📊 TOTAL
# ==================================================

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
╔══════════════════╗
     📊 RELATÓRIO
╚══════════════════╝

💸 Gastos:
R${round(gastos,2)}

💰 Receitas:
R${round(receitas,2)}

🏦 Saldo:
R${round(saldo,2)}
"""

    await update.message.reply_text(texto)

# ==================================================
# 🏦 SALDO
# ==================================================

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cursor.execute("""
    SELECT SUM(valor)
    FROM movimentacoes
    WHERE tipo='receita'
    """)

    receitas = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUM(valor)
    FROM movimentacoes
    WHERE tipo='gasto'
    """)

    gastos = cursor.fetchone()[0]

    if receitas is None:
        receitas = 0

    if gastos is None:
        gastos = 0

    saldo_final = receitas - gastos

    await update.message.reply_text(f"""
🏦 SALDO ATUAL

💵 R${round(saldo_final,2)}
""")

# ==================================================
# 📅 HOJE
# ==================================================

async def hoje(update: Update, context: ContextTypes.DEFAULT_TYPE):

    hoje = datetime.now().strftime(
        "%d/%m/%Y"
    )

    cursor.execute("""
    SELECT * FROM movimentacoes
    ORDER BY id DESC
    """)

    dados = cursor.fetchall()

    texto = "📅 MOVIMENTAÇÕES DE HOJE\n\n"

    encontrou = False

    for mov in dados:

        data = mov[5]

        if hoje in data:

            encontrou = True

            categoria = mov[3]
            valor = mov[2]
            nome = mov[1]

            emoji = EMOJIS.get(
                categoria,
                "💰"
            )

            texto += (
                f"{emoji} {categoria}\n"
                f"💵 R${valor}\n"
                f"👤 {nome}\n\n"
            )

    if not encontrou:

        texto = "📭 Nenhuma movimentação hoje"

    await update.message.reply_text(texto)

# ==================================================
# 📆 MÊS
# ==================================================

async def mes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mes_atual = datetime.now().strftime(
        "%m/%Y"
    )

    cursor.execute("""
    SELECT * FROM movimentacoes
    ORDER BY id DESC
    """)

    dados = cursor.fetchall()

    total_mes = 0

    texto = "📆 RELATÓRIO DO MÊS\n\n"

    for mov in dados:

        data = mov[5]

        if mes_atual in data:

            categoria = mov[3]
            valor = mov[2]

            emoji = EMOJIS.get(
                categoria,
                "💰"
            )

            texto += (
                f"{emoji} {categoria} - "
                f"R${valor}\n"
            )

            total_mes += valor

    texto += (
        f"\n🏦 Total movimentado:\n"
        f"R${round(total_mes,2)}"
    )

    await update.message.reply_text(texto)

# ==================================================
# 🏆 RANKING
# ==================================================

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
            f"{pos}° {nome}\n"
            f"💸 R${round(valor,2)}\n\n"
        )

    await update.message.reply_text(texto)

# ==================================================
# 🎛 MENU BOTÕES
# ==================================================

async def menu_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text

    if texto == "➕ Gasto":

        await update.message.reply_text(
            "💸 Digite:\n\ng 50 mercado"
        )

    elif texto == "💰 Receita":

        await update.message.reply_text(
            "💰 Digite:\n\nr 1500 salario"
        )

    elif texto == "📊 Relatório":

        await total(update, context)

    elif texto == "🏦 Saldo":

        await saldo(update, context)

    elif texto == "📅 Hoje":

        await hoje(update, context)

    elif texto == "📆 Mês":

        await mes(update, context)

    elif texto == "📋 Lista":

        await lista(update, context)

    elif texto == "🏆 Ranking":

        await ranking(update, context)

    elif texto == "🗑 Apagar":

        await update.message.reply_text(
            "🗑 Digite:\n\napagar 3"
        )

    elif texto.startswith("g "):

        await gasto(update, context)

    elif texto.startswith("r "):

        await receita(update, context)

    elif texto.startswith("apagar"):

        await apagar(update, context)

# ==================================================
# 🚀 APP
# ==================================================

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
        menu_texto
    )
)

print("💎 FEROZ FINANCE ONLINE")

app.run_polling()