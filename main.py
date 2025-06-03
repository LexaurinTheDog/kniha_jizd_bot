from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from export_pdf import export_to_pdf
import zipfile
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
jizdy = {}  # {user_id: [záznamy]}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Vítej v Knize jízd!\nPoužij:\n"
        "/nova_jizda Říčany; Brno; 200; Služební jednání\n"
        "/prehled\n/export_pdf\n/export_zip"
    )

async def nova_jizda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        data = " ".join(context.args)
        odkud, kam, km, ucel = data.split(";")
        if user_id not in jizdy:
            jizdy[user_id] = []
        jizdy[user_id].append({
            "odkud": odkud.strip(),
            "kam": kam.strip(),
            "km": float(km.strip()),
            "ucel": ucel.strip()
        })
        await update.message.reply_text("Jízda uložena.")
    except Exception:
        await update.message.reply_text("Zadej ve formátu: /nova_jizda Říčany; Brno; 200; Služební jednání")

async def prehled(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    zaznamy = jizdy.get(user_id, [])
    if not zaznamy:
        await update.message.reply_text("Zatím nejsou žádné jízdy.")
        return
    text = "\n\n".join(
        [f"{j['odkud']} ➝ {j['kam']} ({j['km']} km) – {j['ucel']}" for j in zaznamy]
    )
    await update.message.reply_text(f"Přehled jízd:\n\n{text}")

async def export_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    filename = f"jizdy_export_{user_id}.pdf"
    export_to_pdf(jizdy.get(user_id, []), filename=filename)
    with open(filename, "rb") as f:
        await update.message.reply_document(document=f, filename="kniha_jizd.pdf")

async def export_zip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    pdf_filename = f"jizdy_export_{user_id}.pdf"
    export_to_pdf(jizdy.get(user_id, []), filename=pdf_filename)
    zip_filename = f"kniha_jizd_export_{user_id}.zip"
    with zipfile.ZipFile(zip_filename, "w") as zf:
        zf.write(pdf_filename)
    with open(zip_filename, "rb") as f:
        await update.message.reply_document(document=f, filename="kniha_jizd_export.zip")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("nova_jizda", nova_jizda))
app.add_handler(CommandHandler("prehled", prehled))
app.add_handler(CommandHandler("export_pdf", export_pdf))
app.add_handler(CommandHandler("export_zip", export_zip))

app.run_polling()
