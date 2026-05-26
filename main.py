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

# ================= CONFIG =================

TOKEN = os.getenv("8966773536:AAHN4eLyYBPs9kqm3zrG6fyx9-ralws3LPU")

ADMINS = [
    8943277650,  # Guilherme
    8626825035   # Maiane
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
    "combustivel": "⛽",
    "gasolina": "⛽",
    "cartao": "💳",
    "moto": "🏍",
    "internet": "🌐",
    "lanche": "🍔",
    "farmacia": "💊",
    "salario": "💰",
    "extra": "🪙",
    "pix": "📲",
    "almoço": "🍽",
    "ifood": "🍕",
    "roupa": "👕",
    "uber": "🚗",
    "presente": "🎁"

}

# ================= FUNÇÕES =================

def pegar_nome(user_id):

    if user_id == 8943277650:
        return "Guilherme"

    elif user_id == 8626825035:
        return "Maiane"

    return "Usuário"

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = [

        [
            InlineKeyboardButton(
                "💸 Adicionar Gasto",
                callback_data="gasto"
            ),

            InlineKeyboardButton(
                "💰 Adicionar Receita",
                callback_data="receita"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 Relatórios",
                callback_data="relatorios"
            ),

            InlineKeyboardButton(
                "🏦 Saldo",
                callback_data="saldo"
            )
        ],

        [
            InlineKeyboardButton(
                "📅 Hoje",
                callback_data="hoje"
            ),

            InlineKeyboardButton(
                "📆 Mês",
                callback_data="mes"
            )
        ],

        [
            InlineKeyboardButton(
                "🏆 Ranking",
                callback_data="ranking"
            ),

            InlineKeyboardButton(
                "📋 Lista",
                callback_data="lista"
            )
        ]

    ]

    painel = InlineKeyboardMarkup(teclado)

    texto = """
╔══════════════════════╗
      💎 FEROZ FINANCE
╚══════════════════════╝

🏦 SISTEMA FINANCEIRO

👤 Guilherme
👤 Maiane

━━━━━━━━━━━━━━━━━━━
💸 Controle de gastos
💰 Controle de ganhos
📊 Relatórios automáticos
🏆 Ranking financeiro
━━━━━━━━━━━━━━━━━━━

Escolha uma opção abaixo 👇
"""

    await update.message.reply_text(
        texto,
        reply_markup=painel
    )

# ================= MENU =================

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await start(update, context)

# ================= BOTÕES =================

async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    opcao = query.data

    respostas = {

        "gasto":
        "💸 Exemplo:\n/g 50 mercado",

        "receita":
        "💰 Exemplo:\n/r 1500 salario",

        "relatorios":
        "📊 Use:\n/total",

        "saldo":
        "🏦 Use:\n/saldo",

        "hoje":
        "📅 Use:\n/hoje",

        "mes":
        "📆 Use:\n/mes",

        "ranking":
        "🏆 Use:\n/ranking",

        "lista":
        "📋 Use:\n/lista"

    }

    await query.message.reply_text(
        respostas.get(opcao)
    )

# ================= GASTO =================

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

    emoji = EMOJIS.get(
        categoria,
        "💸"
    )

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

        await update.message.reply_text(
            "❌ Sem permissão"
        )

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

    emoji = EMOJIS.get(
        categoria,
        "💰"
    )

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
        "SELECT * FROM movimentacoes ORDER BY rowid DESC"
    )

    dados = cursor.fetchall()

    if len(dados) == 0:

        await update.message.reply_text(
            "📭 Nenhuma movimentação"
        )

        return

    texto = "📋 MOVIMENTAÇÕES\n\n"

    for mov in dados:

        nome = mov[0]
        valor = mov[1]
        categoria = mov[2]
        tipo = mov[3]
        data = mov[4]

        emoji = EMOJIS.get(
            categoria,
            "💰"
        )

        if tipo == "gasto":
            tipo_emoji = "💸"
        else:
            tipo_emoji = "💰"

        texto += (
            f"{emoji} {nome}\n"
            f"{tipo_emoji} R${valor}\n"
            f"📂 {categoria}\n"
            f"📅 {data}\n\n"
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
📊 RELATÓRIO GERAL

💸 Gastos:
R${round(gastos, 2)}

💰 Receitas:
R${round(receitas, 2)}

🏦 Saldo:
R${round(saldo, 2)}
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
            "📭 Nenhuma movimentação hoje"
        )

        return

    texto = f"📅 MOVIMENTAÇÕES DE HOJE\n\n"

    for mov in dados:

        nome = mov[0]
        valor = mov[1]
        categoria = mov[2]

        emoji = EMOJIS.get(
            categoria,
            "💰"
        )

        texto += (
            f"{emoji} {nome} - "
            f"R${valor} ({categoria})\n"
        )

    await update.message.reply_text(texto)

# ================= MÊS =================

async def mes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mes_atual = datetime.now().strftime("%m/%Y")

    cursor.execute(
        "SELECT * FROM movimentacoes"
    )

    dados = cursor.fetchall()

    texto = f"📆 RELATÓRIO DO MÊS\n\n"

    total = 0

    for mov in dados:

        data = mov[4]

        if mes_atual in data:

            nome = mov[0]
            valor = mov[1]
            categoria = mov[2]

            emoji = EMOJIS.get(
                categoria,
                "💰"
            )

            texto += (
                f"{emoji} {nome} - "
                f"R${valor} ({categoria})\n"
            )

            total += valor

    texto += f"\n🏦 Total movimentado:\nR${round(total,2)}"

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
            f"{pos}° {nome}\n"
            f"💸 R${round(valor,2)}\n\n"
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
    CommandHandler("mes", mes)
)

app.add_handler(
    CommandHandler("saldo", saldo)
)

app.add_handler(
    CommandHandler("ranking", ranking)
)

app.add_handler(
    CallbackQueryHandler(botoes)
)

print("💎 FEROZ FINANCE ONLINE")

app.run_polling()