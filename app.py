import os
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_CSV_URL = os.getenv("SHEET_CSV_URL")

def get_top15():
    df = pd.read_csv(SHEET_CSV_URL)

    df["Số ngày trễ"] = df["Số ngày trễ"].fillna(0)
    df["Số tiền nợ"] = df["Số tiền nợ"].fillna(0)

    df["Điểm"] = df["Số ngày trễ"] * 2 + df["Số tiền nợ"] / 100000

    top = df.sort_values("Điểm", ascending=False).head(15)

    msg = "🚨 *TOP 15 NGUY CƠ CẮT*\n\n"
    for _, r in top.iterrows():
        msg += (
            f"👤 {r['Tên KH']}\n"
            f"📞 {r['SĐT']}\n"
            f"💰 {int(r['Số tiền nợ']):,}đ\n"
            f"⏰ {int(r['Số ngày trễ'])} ngày\n\n"
        )
    return msg

async def canhbao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_top15(), parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("canhbao", canhbao))

app.run_polling()
