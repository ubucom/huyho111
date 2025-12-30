import requests
import pandas as pd
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHEET_CSV_URL = os.getenv("SHEET_CSV_URL")

df = pd.read_csv(SHEET_CSV_URL)

df["Số ngày trễ"] = df["Số ngày trễ"].fillna(0)
df["Số tiền nợ"] = df["Số tiền nợ"].fillna(0)

df["Điểm rủi ro"] = df["Số ngày trễ"] * 2 + df["Số tiền nợ"] / 100000

top15 = (
    df[df["Số ngày trễ"] >= 10]
    .sort_values("Điểm rủi ro", ascending=False)
    .head(15)
)

message = "🚨 *CẢNH BÁO NGUY CƠ CẮT DỊCH VỤ*\n\n"

for _, row in top15.iterrows():
    message += (
        f"👤 {row['Tên KH']}\n"
        f"📞 {row['SĐT']}\n"
        f"💰 Nợ: {int(row['Số tiền nợ']):,}đ\n"
        f"⏰ Trễ: {int(row['Số ngày trễ'])} ngày\n\n"
    )

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
})
