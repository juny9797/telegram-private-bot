from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from html import escape

ADMIN_ID = 7695731166  # 관리자 텔레그램 ID

# /start 명령어 처리
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = escape(user.first_name or "사용자")

    welcome_message = (
        f"<b>{user_name}님 안녕하세요</b>\n"
        "프라이빗 CS bot입니다.\n\n"
        "<b><u>프라이빗 입장은 업무 인증을 받고있습니다.\n"
        "본계정으로 말씀 부탁드리며,</u></b>\n\n"
        "프라이빗 방에서는 불법적인 마약거래, 인신매매, 계좌 매입, 통협, 피싱 등 관련 내용은 절대적 금지이며 추천인 및 주변인 모두 영구적 차단됩니다.\n\n"
        "<b>프라이빗 그룹에서는 무단 홍보 광고를 먹튀사기 예방 차원에서 금지합니다.\n"
        "(1차적인 검증 시스템을 통과한 \"추천\" 제도를 사용합니다.)</b>\n\n"
        "➖➖➖➖➖➖➖➖➖➖➖\n\n"
        "프라이빗은 텔레그램과 전속 연동되어 독자적인 시스템으로 장기간 사업 중인 업자를 엄선하여 \"추천\"합니다.\n"
        "<u>또한 독자적인 시스템으로 주관하여 확실한 데이터, 오래되고 실력있는 업자만을 입장 받고있습니다.</u>\n\n"
        "➖➖➖➖➖➖➖➖➖➖➖\n\n"
        "<b>private은</b> 제휴라는 단어로 유저들을 거짓 현혹하지 않고 무책임한 거짓 약속은 절대 하지 않습니다.\n"
        "<b><u>단, 장기간 정상적으로 운영 중인 업자를 엄선하여 '추천'합니다.\n"
        "이 또한 각종 사고에 휘말릴 경우 피해자와 최대한 정보를 공유하며 업계에서 완전한 폐기 조치합니다.</u></b>"
    )

    keyboard = [
        [InlineKeyboardButton("🔒 private입장", callback_data="private_entry")],
        [InlineKeyboardButton("📩 private추천등록", callback_data="private_recommend")],
        [InlineKeyboardButton("💰 보증거래신청", callback_data="guaranteed_trade")],
        [InlineKeyboardButton("📘 private운영안내", callback_data="private_info")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='HTML')


# 버튼 클릭 응답
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    button_texts = {
        "private_entry": "프라이빗 입장을 원하시면 인증 절차를 위해 닉네임과 사용자명을 남겨주세요.",
        "private_recommend": "추천 등록을 위해 추천인과 업력 정보, 활동 내역 등을 보내주세요.",
        "guaranteed_trade": "보증 거래 신청을 원하시면 거래 내용을 입력해주세요.",
        "private_info": "프라이빗 운영안내는 별도 PDF 안내서를 통해 전달드릴 예정입니다.",
    }

    await query.message.reply_text(button_texts.get(query.data, "알 수 없는 요청입니다."))


# 일반 메시지를 관리자에게 전달
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    forward_text = (
        f"[문의 도착]\nFrom: {user.first_name} (@{user.username})\nUserID: {user.id}\n\n{message}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)
    await update.message.reply_text("문의가 접수되었습니다. 담당자가 확인 후 순차적으로 답변드릴 예정입니다.")


# 관리자 답변 기능 (/reply USERID 내용)
async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        _, user_id, *reply_text = update.message.text.split()
        reply_text = ' '.join(reply_text)
        await context.bot.send_message(chat_id=int(user_id), text=f"[관리자 답변]\n{reply_text}")
        await update.message.reply_text("답변 전송 완료 ✅")
    except Exception:
        await update.message.reply_text("답변 형식 오류입니다.\n예: /reply 123456789 안녕하세요. 문의 주신 건은...")


# 앱 실행
app = ApplicationBuilder().token("7310597734:AAElXF8USSHGUoKmatSSSgujn5WJKkH357c").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler("reply", reply_to_user))  # <-- 영어 명령어만 가능
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_to_admin))
app.run_polling()
