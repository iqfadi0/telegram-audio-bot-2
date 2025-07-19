from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8098179665:AAHQRbxn4zW745olQvMvIZjLeIWxSjCbdeY"

prayers = {
    "الصلاة": """أبانا الّذي في السّماوات، ليتقدّس اسمك، ليأتِ ملكوتك، لتكن مشيئتك كما في السّماء كذلك على الأرض. أعطنا خبزنا كفاف يومنا، واغفر لنا ذنوبنا وخطايانا كما نحن نغفر  لِمَن أخطأ إلينا، ولا تُدخلنا في التجربة، لكن نجّنا من الشّرّير امين .

السلام عليك يا مريم يا ممتلئة نعمة، الرب معك، مباركة أنت في النساء، و مباركة ثمرة بطنك، سيدنا يسوع المسيح. يا قديسة مريم، يا والدة الله، صلّي لأجلنا نحن الخطأة، الآن وفي ساعة موتنا امين .""",

    "نص الايمان": """نؤمن بإله واحد، آب ضابط الكل خالق السماء والأرض كلّ ما يُرى وما لا يُرى وبربٍّ واحد يسوع المسيح أبن الله الوحيد المولود من الآب قبلَ كل الدهور إله من إله، نور من نور، إله حق من إله حق، مولود غير مخلوق، مساوٍ للآب في الجوهر، الذي به كان كلّ شيء الذي من أجلنا نحنُ البشر ومن أجلِ خلاصنا 
نزل من السماء وتجسّد من الروح القدس ومن مريم العذراء وصارَ إنساناً وصُلبَ عنّا على عهدِ بيلاطس البنطي تألّم ومات وقُبِرَ وقام في اليوم الثالث كما جاء في الكتب وصعِدَ إلى السماء وجلس عن يمين الله الآب وأيضًا يأتي بمجدٍ عظيم ليدينَ الأحياء والأموات الذي لا فناء لمُلكه. 
ونؤمن بالروح القدس الرّبّ المُحيي، المنبثق من الآب والإبن الذي هوَ مع الآب والإبن يُسجَد لهُ ويُمَجّد، الناطق بالأنبياء والرُسل وبكنيسة واحدة، جامِعة، مقّدَسة، رَسوليّة ونعترف بمعموديّة واحدة لمغفرة الخَطايا 
ونترَجّى قيامَة الموتى والحياة في الدهرِ الآتي، آمين.""",

    "صلاة قبل النوم": """اني أختُم، يا ربّ نهاري بشكركَ، كما افتتحتُهُ بتسبيحِكَ
فاختم بالخير كلّ أعمال حياتي
لتكن يا ربّ، خدمتُنا لرضاك
وصلاتُنا لحمدك
وحياتُنا لمجدك
أحِلَّ، يا ربّ،
حُبك في نفوسنا ونورَك في ضمائرنا
وسلامَك في قلوبنا
ومع غياب شمسِ هذا النهار كُنْ لنا شمساً لا تغيب
وعند رقادنا في هذا الليل أرمقنا بعين لا تنام
ولا تحسب علينا، يا ربّ، هفواتِنا
أعطنا ليلاً هادئاً ونوماً هنيئاً ويقظة نشيطة
وصباحاً يبشرُ بالأفراح
بشفاعة أمك مريم، فرح البيعة وأمِّ المحبة
ونُصعد لك المجد الآن والى الأبد. آمين.""",

    "صلاة الصبح": """مباركٌ أنت، أيّها المسيح، يا من بك طلع النهار وزالت ظلمةُ الليل يا نور الحقّ وشمس البر يا من حللتَ في البيعة فاستنارتْ وفي الأرض فابتهجتْ يا من دنا منك الخطأة فتبرّروا والضالونَ فاهتدَوا والعميانُ فأبصروا يا من ايقظتنا في هذا الصباح ووهبتنا نهاراً نفرح به نسألك أن تنير عقولَنا وقلوبَنا بنور محبتك وليكن لنا مطلعُ صباحِكَ فاتحةَ كلِّ خير فسدّد خطانا على سنّة مشوراتِكَ ولا تسمح للخطيئة بأن تستعبدَنا بل حرِّرنا من ظلمة الأميال وثبتنا في مقاصدنا وأنرنا في تصرفاتنا اليومَ وفي كلّ أيّام حياتِنا فنرتل مبتهجين، لك أيها المسيح ولأبيك وروحِك القدوس الآن والى الأبد، آمين."""
}

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("الصلاة", callback_data="الصلاة"),
         InlineKeyboardButton("نص الايمان", callback_data="نص الايمان")],
        [InlineKeyboardButton("صلاة قبل النوم", callback_data="صلاة قبل النوم"),
         InlineKeyboardButton("صلاة الصبح", callback_data="صلاة الصبح")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("✞", callback_data="back")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✞", reply_markup=get_main_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back":
        await query.message.reply_text("✞", reply_markup=get_main_keyboard())
        return

    text = prayers.get(data, "هذه الصلاة غير موجودة")
    display_text = f"**{data}**\n\n{text}"
    await query.message.reply_text(display_text, reply_markup=get_back_keyboard(), parse_mode="Markdown")

# Flask server for keeping Replit awake
app = Flask('')

@app.route('/')
def home():
    return "Bot is running."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    from threading import Thread
    thread = Thread(target=run)
    thread.start()

def main():
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    print("البوت شغال...")
    application.run_polling()

if __name__ == "__main__":
    main()
Add main.py
