import json
import os
import logging
from telegram import InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup, Update # type: ignore
from telegram.ext import ( # type: ignore
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
# 📌 الاستيراد الإضافي لمعالجة الأخطاء
from telegram.error import BadRequest  # type: ignore


# --------------- CONFIG ---------------
TOKEN = "8043416262:AAEfNBPFH-YigKrcwyuVbZeWUJ2d3lc6FJ0"
ADMINS = [6694003250]

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_PATH, "users.json")

# 📌 الصورة الترحيبية: تم استخدام الرابط الذي زودتنا به
WELCOME_IMAGE_URL = "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1jh9qc3591fu891515qs106b19inc.jpg"
DEVELOPER_IMAGE_URL = "https://payhip.com/cdn-cgi/image/format=auto,width=500/https://pe56d.s3.amazonaws.com/o_1jifq1pip1n7flb61sq41qgo75ql.jpg" # يمكنك تغيير الرابط لصورة المطور الخاصة
# الروابط الجديدة للصور
WELCOME_IMAGE_URL = "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1jh9qc3591fu891515qs106b19inc.jpg"
SOCIAL_IMAGE_URL = "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1jh9qc3591fu891515qs106b19inc.jpg"

# --------------- LOGGING ---------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING
)
logger = logging.getLogger(__name__)

# --------------- TRANSLATIONS (قاموس اللغات) ---------------
TEXTS = {
    "en": {
        "welcome": "<b>Welcome to BENTRADE Trading 👨‍💻</b>\n\nBelow you can explore our trading products, including EAs, Indicators, and Professional tools.\n\n<b>Thank you for choosing our tools ❤️</b>",
        "choose_lang": "Please select your language / يرجى اختيار لغتك:",
        "products_btn": "Products 📦",
        "store_btn": "Visit Store 🛒",
        "social_btn": "Social Media 🌐",
        "dev_contact_btn": "Contact Developer 👨‍💻",
        "channel_btn": "Telegram Channel 📢",
        "contact_btn": "Contact the developer 💬",
        "info_btn": "Why BENTRADE Trading ? ℹ️",
        "admin_btn": "Admin Panel 🛠️",
        "close_btn": "Close",
        "back_btn": "🔙 Back",
        "buy_btn": "💵 Buy Now",
        "thank_you": "Thank you for using our bot 😊\nSee you again soon! 👋",
        "social_msg": "<b>Our Social Networks</b>\n\nStay updated with our latest news and offers through our official accounts:",
        "dev_msg": "<b>Direct Contact with Developer</b>\n\nYou can reach out for technical support or custom requests below:",
        "tools_msg": "<b>Why BENTRADE Trading ?</b>\n\n ✔ Market-Specific Trading Systems.\n\n ✔ Built for MT4, MT5 & TradingView.\n\n ✔ Developed with Real Market Data.\n\n ✔ One-Time Payment – No Monthly Fees.\n\n ✔ Lifetime License & Free Updates.\n\n✔ Designed for Precision, Not Over-Trading.",
        #"info_msg": "ℹ️ <b>About This Bot</b>\n\nWelcome to BENALI Trading Tools Bot!\n\nHere you can:\n• Browse EAs and Indicators\n• Access free tools\n• Contact the developer\n\nThank you for using the bot 😊",
        "choose_cat": "📦 Choose a Product Category: \n\n⤵",
        "choose_prod": "📦 Choose a Product: \n\n⤵",
        "click_buy": "\n\n🛒 <i>Start improving your Trading by Clicking tje botton below ✅.</i>",
        "cat_ea": "Expert Advisors 🤖",
        "cat_ind": "Indicators 📊",
        "cat_tools": "Utilities ⚒️",
        "cat_tv": "TradingView 📈",
        "cat_free": "Free Downloads 🎁",
        "admin_users": "User Count 👥",
        "admin_bc": "Send Broadcast 📢",
        "unauth": "❌ You are not authorized.",
        "bc_hint": "Usage: /broadcast Your message here",
        "bc_sent": "✅ Broadcast sent to {} users.",
        "lang_set": "✅ Language set to English.",
        "change_lang_btn": "Change Language 🌐",
        "copy_hint": "📋 Click on the email to copy",
        "buy_1m": "1 Month",
        "buy_3m": "3 Months",
        "buy_6m": "6 Months",
        "buy_life": "",

        "prev_btn": "⬅️ Previous",
        "next_btn": "Next ➡️",
        "back_btn": "🔙 Back",
        "choose_lang": "Please choose your language first",
        "user_reviews": "User Reviews 📝",

        "why_benali": (
            "<b> Why BENTRADE Trading ?</b>\n\n"
            "✔ Market-Specific Trading Systems.\n\n"
            "✔ Built for MT4, MT5 & TradingView.\n\n"
            "✔ Developed with Real Market Data.\n\n"
            "✔ One-Time Payment – No Monthly Fees.\n\n"
            "✔ Lifetime License & Free Updates.\n\n"
            "✔ Designed for Precision, Not Over-Trading."
        ),



        "dev_msg": (
            "<b>👨‍💻 BENALI | Quant Developer</b>\n\n"
            "Expert in (MT4/MT5) development with a Master's in <b>Quantitative Economics</b>. "
            "I build tools that bridge statistical precision with practical market insights.\n\n"
            "📩 <b>Contact me for support or custom projects:</b>"
        ),

        "coming_soon": "Link coming soon! 🚧"
    },
    "ar": {
        "welcome": "<b>مرحباً بك في (BENTRADE Trading ) 👨‍💻</b>\n\nفي الأسفل يمكنك استعراض منتجاتنا، بما في ذلك الاكسبيرتات، المؤشرات، والأدوات الاحترافية.\n\n<b>شكراً لاختيارك أدواتنا ❤️</b>",
        "choose_lang": "يرجى اختيار لغتك / Please select your language:",
        "products_btn": "المنتجات 📦",
        "store_btn": "زيارة المتجر 🛒",
        "social_btn": "مواقع التواصل الاجتماعي 🌐",
        "dev_contact_btn": "التواصل مع المطور 👨‍💻",
        "channel_btn": "قناة التليجرام 📢",
        "contact_btn": "تواصل مع المطور 💬",
        "info_btn": "لماذا أدوات BENTRADE للتداول؟ ℹ️",
        "admin_btn": "لوحة التحكم 🛠️",
        "close_btn": "إغلاق",
        "back_btn": "🔙 رجوع",
        "buy_btn": "💵 شراء الآن",
        "thank_you": "شكراً لاستخدامك البوت 😊\nنراك قريباً! 👋",
        "social_msg": "<b>منصاتنا على التواصل الاجتماعي</b>\n\nتابع آخر الأخبار والعروض عبر حساباتنا الرسمية:",
        "dev_msg": "<b>التواصل المباشر مع المطور</b>\n\nيمكنك التواصل للحصول على الدعم الفني أو الطلبات الخاصة عبر الوسائل أدناه:",
        "tools_msg": "<b>لماذا BENTRADE للتداول؟</b>\n\n✔ أنظمة تداول مخصصة لكل سوق.\n\n✔ متوافقة مع MT4 وMT5 وTradingView.\n\n✔ مطورة باستخدام بيانات السوق الحقيقية.\n\n✔ دفع مرة واحدة فقط – بدون رسوم شهرية.\n\n✔ ترخيص دائم وتحديثات مجانية.\n\n✔ مصممة للدقة، وليس للإفراط في التداول.",
        #"info_msg": "ℹ️ <b>عن هذا البوت</b>\n\nمرحباً بك في بوت BENALI Trading Tools!\n\nهنا يمكنك:\n• تصفح الاكسبيرتات والمؤشرات\n• الوصول لأدوات مجانية\n• التواصل مع المطور\n\nشكراً لاستخدامك البوت 😊",
        "choose_cat": "📦 اختر تصنيف المنتج: \n\n⤵",
        "choose_prod": "📦 اختر المنتج: \n\n⤵",
        "click_buy": "\n\n🛒 <i>ابدا تحسين تداولك بالضغط على الزر أدناه ✅.</i>",
        "cat_ea": "روبوتات تداول (EA) 🤖",
        "cat_ind": "مؤشرات 📊",
        "cat_tools": "أدوات مساعدة ⚒️",
        "cat_tv": "TradingView 📈",
        "cat_free": "تحميلات مجانية 🎁",
        "admin_users": "عدد المشتركين 👥",
        "admin_bc": "إرسال نشرة 📢",
        "unauth": "❌ ليس لديك صلاحية.",
        "bc_hint": "الاستخدام: /broadcast اكتب رسالتك هنا",
        "bc_sent": "✅ تم الإرسال إلى {} مستخدم.",
        "lang_set": "✅ تم تعيين اللغة إلى العربية.",
        "change_lang_btn": "تغيير اللغة 🌐",
        "copy_hint": "📋 اضغط على الإيميل للنسخ",
        "buy_1m": " شهر",
        "buy_3m": " 3 أشهر",
        "buy_6m": " 6 أشهر",
        "buy_life": "",

        "prev_btn": "⬅️ السابق",
        "next_btn": "التالي ➡️",
        "back_btn": "🔙 العودة",
        "choose_lang": "يرجى اختيار اللغة أولاً",
        "user_reviews": "تقييمات المستخدمين 📝",

        "why_benali": (
            "<b>لماذا BENTRADE للتداول؟</b>\n\n"
            "✔ أنظمة تداول مخصصة لكل سوق.\n\n"
            "✔ متوافقة مع MT4 وMT5 وTradingView.\n\n"
            "✔ مطورة باستخدام بيانات السوق الحقيقية.\n\n"
            "✔ دفع مرة واحدة فقط – بدون رسوم شهرية.\n\n"
            "✔ ترخيص دائم وتحديثات مجانية.\n\n"
            "✔ مصممة للدقة، وليس للإفراط في التداول."
        ),


        "dev_msg": (
            "<b>👨‍💻 BENALI  | مطور كمي </b>\n\n"
            "خبير في تطوير أدوات (MT4/MT5) بخلفية أكاديمية في <b>الاقتصاد الكمي</b>. "
            "أقوم ببناء أدوات تجمع بين الدقة الإحصائية والواقع العملي للسوق.\n\n"
            "📩 <b>تواصل معي للدعم الفني أو الطلبات الخاصة:</b>"
        ),

        "coming_soon": "الرابط سيتوفر قريباً! 🚧"
    }
}

REVIEWS = [
    "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1ji4dj5r116do1ikpo3n16rop1rl.jpg",
    "https://payhip.com/cdn-cgi/image/format=auto,width=750/https://pe56d.s3.amazonaws.com/o_1jifq3d9s96rjuste61turc9u.jpg",
    "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1ji4djm3do8e198q1eot1vj5vmuu.jpg",
    "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1ji97cuu3ur4t7gg8n52l40hc.jpg",
    "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1ji4dh4no1u6cv30imu1ibi1fudc.jpg",
    "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1ji4eeadv52achh4q31c9l1nfac.jpg",
    # أضف كل روابط الصور هنا
    ]

# --------------- USERS & DATA ---------------
def load_users_data():
    if not os.path.exists(USERS_FILE):
        return {"users": {}}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Migration check: if old format (list), convert to dict
            if "users" in data and isinstance(data["users"], list):
                new_users = {str(uid): "en" for uid in data["users"]}
                data["users"] = new_users
                save_users_data(data)
            return data
    except Exception as e:
        logger.error("Error loading users.json: %s", e)
        return {"users": {}}

def save_users_data(data):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error("Error saving users.json: %s", e)

def get_user_lang(chat_id):
    data = load_users_data()
    return data["users"].get(str(chat_id), None)

def set_user_lang(chat_id, lang_code):
    data = load_users_data()
    data["users"][str(chat_id)] = lang_code
    save_users_data(data)

# --------------- PRODUCTS DATABASE (Remain Unchanged) ---------------
# Structure: (Name, Links_Dict, Desc_En, Desc_Ar, Image_URL)
# Links_Dict keys: '1m', '3m', '6m', 'life' -> Value: ("URL", "PRICE_TEXT")
PRODUCTS = {
    "ea_list": [
        (
            "GOLDEN Guard Pro EA©",
            {
                #"1m": ("soon", "30$"), 
                #"3m": ("soon", "80$"), 
                #"6m": ("soon", "150$"), 
                "life": ("https://www.mql5.com/en/market/product/160320", "62$")
            },
            "💬 <b>Advanced Expert Advisor for Gold Trading.</b>\n• Designed for precise and safe gold trading\n• Smart entry system with risk control filters\n• Automatic money management system\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
            "💬 <b>إكسبيرت احترافي لتداول الذهب.</b>\n • دخول ذكي مع حماية متقدمة \n• إدارة تلقائية لرأس المال \n• مخصص لزوج XAUUSD \n\n⚙️ المنصة: MT5\n ⭐ التقييم: ★★★★★",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1jermgvk74g813v7p14iobk1h15.png"
        ),
        (
            "GOLDEN ALGO MT5©",
            {
                #"1m": ("soon", "30$"), 
                #"3m": ("soon", "80$"), 
                #"6m": ("soon", "150$"), 
                "life": ("https://www.mql5.com/en/market/product/137973", "125$")
            },
            "💬 <b>Powerful Expert Advisor for XAUUSD.</b>\n• Designed for gold trend trading\n• Smart entries with volatility filters\n• Automatic money management\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
            "💬 <b>اكسبيرت قوي لزوج الذهب XAUUSD.</b>\n• مصمم لتداول اتجاه الذهب (Trend)\n• نقاط دخول ذكية مع فلترة التذبذب\n• إدارة رأس مال تلقائية\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★★",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1jdttgpan1aik1sbu196d1go21b2r15.png"
        ),
        (
            "Gold Strike EA©",
            {
                #"1m": ("soon", "25$"), 
                #"3m": ("soon", "70$"), 
                #"6m": ("soon", "130$"), 
                "life": ("https://www.mql5.com/en/market/product/148798", "99$")
            },
            "💬 <b>Simple and reliable EA for daily gold signals.</b>\n• No martingale / no grid\n• Easy to use for beginners\n• Low-risk entries\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
            "💬 <b>اكسبيرت بسيط وموثوق لإشارات الذهب اليومية.</b>\n• خالٍ من المضاعفات (Martingale) والشبكات (Grid)\n• سهل الاستخدام للمبتدئين\n• صفقات منخفضة المخاطرة\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★★",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1je0buut218jhrvabo37r4123215.png"
        ),
        (
            "Prime Trader EA©",
            {
                #"1m": ("soon", "35$"), 
                #"3m": ("soon", "90$"), 
                #"6m": ("soon", "160$"), 
                "life": ("https://www.mql5.com/en/market/product/147302", "59$")
            },
            "💬 <b>Professional Expert Advisor for accurate trade signals.</b>\n• Trend detection for high-probability entries\n• Adjustable settings: lot size, SL/TP, indicators\n• News Filter\n• Lightweight and fast interface\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
            "💬 <b>اكسبيرت احترافي لإشارات تداول دقيقة.</b>\n• كشف الاتجاه للدخول بفرص عالية الاحتمال\n• إعدادات مرنة: اللوت، الوقف/الهدف، والمؤشرات\n• فلتر للأخبار الاقتصادية\n• واجهة خفيفة وسريعة التنفيذ\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★★",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1jdtt0e6qctc1jha12tl1t5r1fas15.png"
        ),
        (
            "FOREX Strike EA©",
            {
                #"1m": ("soon", "20$"), 
                #"3m": ("soon", "55$"), 
                #"6m": ("soon", "100$"), 
                "life": ("https://www.mql5.com/en/market/product/149611", "65$")
            },
            "💬 <b>Reliable EA for major forex pairs.</b>\n• Stable performance\n• No martingale / no grid\n• Designed for long-term consistency\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★☆",
            "💬 <b>اكسبيرت موثوق لأزواج الفوركس الرئيسية.</b>\n• أداء مستقر وثابت\n• لا يستخدم المضاعفات أو الشبكات\n• مصمم لتحقيق الاستمرارية على المدى الطويل\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★☆",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j54oivp31ofi168117le1autk4m10.png"
        ),
        (
            "BitRocket EA MT5©",
            {
                #"1m": ("soon", "20$"), 
                #"3m": ("soon", "55$"), 
                #"6m": ("soon", "100$"), 
                "life": ("https://www.mql5.com/en/market/product/141569", "65$")
            },
            "💬 <b>High-speed crypto trading EA.</b>\n• Works on BTC & crypto pairs\n• Smart trend detection\n• Low-latency execution\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★☆☆",
            "💬 <b>اكسبيرت عالي السرعة لتداول العملات الرقمية.</b>\n• يعمل على البيتكوين وأزواج الكريبتو\n• كشف ذكي للاتجاه (Trend)\n• تنفيذ فائق السرعة (Low-latency)\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★☆☆",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j2vkdrbf2ol7v8kn359hs4f10.png"
        ),
    ],
    "ind_list": [
        (
            "Deal Tracker Dashboard©",
            {
                #"1m": ("soon", "15$"), 
                #"3m": ("soon", "40$"), 
                #"6m": ("soon", "70$"), 
                "life": ("https://www.mql5.com/en/market/product/158114", "30$")
            },
            "📊 <b>Deal Tracker Dashboard</b>\n• Visual trade performance analyzer\n• Displays each closed trade directly on the chart\n• Instant profit & loss insight with smart color coding\n• Clean statistics panel for better decisions\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
            "📊 <b>لوحة تعقب الصفقات </b>\n• أداة احترافية لتحليل أداء التداول بصريًا\n• عرض الصفقات المغلقة مباشرة على الشارت\n• تمييز الربح والخسارة بالألوان\n• لوحة إحصائيات ذكية لتحسين قراراتك\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★★",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1jcut99fv1vot1gl166n1m781eno1c.png"
        ),
        (
            "Trade Vision Panel©",
            {
                #"1m": ("soon", "15$"), 
                #"3m": ("soon", "40$"), 
                #"6m": ("soon", "70$"), 
                "life": ("https://www.mql5.com/en/market/product/154765", "30$")
            },
            "📊 <b>Complete market dashboard for MT5.</b>\n• Multi-timeframe scanner\n• News Filter and display it according to importance \n• Strength & direction analyzer\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
            "📊 <b>لوحة معلومات السوق الكاملة </b>\n• لوحة احترافية لمتابعة السوق بشكل كامل \n• فاحص متعدد الفريمات \n• فلترة الأخبار حسب الأهمية \n• تحليل قوة العملات واتجاه الترند \n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★★",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j9kluek8anc9q41afo1gua197i1t.png"
        ),
        (
            "RSI Dashboard Pro©",
            {
                #"1m": ("soon", "10$"), 
                #"3m": ("soon", "25$"), 
                #"6m": ("soon", "45$"), 
                "life": ("https://www.mql5.com/en/market/product/152394", "49$")
            },
            "📉 <b>Advanced RSI indicator with alerts.</b>\n• MTF RSI scanner\n• Overbought/oversold alerts\n• Great for reversals\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★☆",
            "📉 <b>مؤشر RSI متطور مع تنبيهات ذكية.</b>\n• ماسح RSI متعدد الفريمات (MTF)\n• تنبيهات عند التشبع الشرائي والبيعي\n• ممتاز لاكتشاف الانعكاسات\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★☆",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1jd5v3ugct837g014du1tfa1phh15.png"
        ),
        (
            "CrossMaster PRO©",
            {
                #"1m": ("soon", "12$"), 
                #"3m": ("soon", "30$"), 
                #"6m": ("soon", "50$"), 
                "life": ("https://www.mql5.com/en/market/product/144048", "49$")
            },
            "⚡ <b>Fast-moving average crossover system.</b>\n• Trend reversals detection\n• MTF signals\n• Simple and effective\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★☆",
            "⚡ <b>نظام تقاطع المتوسطات المتحركة السريع.</b>\n• كشف انعكاسات الاتجاه (Reversals)\n• إشارات متعددة الفريمات\n• بسيط وفعال جداً\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★☆",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j2o3l6vu1tql1j4vefg4ai1db0r.png"
        ),
    ],
    "tools_list": [
        (
            "Smart EA Summary MT5©",
            {
                "life": ("https://www.mql5.com/en/market/product/142115", "59$")
            },
            "🖥️ <b>Monitor all your EAs in one panel.</b>\n• Tracks profit/loss by Magic Number\n• Real-time updates\n• Clean & modern interface\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
            "🖥️ <b>راقب جميع اكسبيرتاتك في لوحة واحدة.</b>\n• تتبع الربح/الخسارة لكل Magic Number\n• تحديث لحظي للبيانات\n• واجهة عصرية ونظيفة\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★★",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j2up103r1a95i8962d1lqk1rvr.png"
        ),
        (
            "Smart Risk Manager©",
            {
                "life": ("https://www.mql5.com/en/market/product/145748", "39$")
            },
            "⚖️ <b>Advanced risk and lot-size calculator.</b>\n• Auto lot calculation\n• SL-based risk management\n• Helps prevent over-risking\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
            "⚖️ <b>حاسبة متقدمة للمخاطرة وحجم العقد.</b>\n• حساب اللوت (Lot) تلقائياً\n• إدارة المخاطر بناءً على وقف الخسارة (SL)\n• يحميك من المخاطرة الزائدة\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★★",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j2nt4hb8ttr1q0d1e5ljp3vsi10.png"
        ),
        (
            "Smart EA Summary MT4©",
            {
                "life": ("https://www.mql5.com/en/market/product/142120", "59$")
            },
            "📊 <b>EA summary panel for MT4 users.</b>\n• Magic-number grouping\n• Full EA monitoring\n• Clean & responsive UI\n\n⚙️ Platform: MT4\n⭐ Rating: ★★★★☆",
            "📊 <b>لوحة ملخص الاكسبيرتات لمستخدمي MT4.</b>\n• تجميع الصفقات حسب الـ Magic Number\n• مراقبة شاملة لأداء الروبوتات\n• واجهة مستخدم سلسة\n\n⚙️ المنصة: MT4\n⭐ التقييم: ★★★★☆",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j2up103r1a95i8962d1lqk1rvr.png"
        ),
    ],
 #   "tv_list": [
  #      (
 #           "TrendGuard PRO",
          #  {
         #       "life": ("https://payhip.com/b/a5b3Q", "137.08$")
         #   },
         #   "🛡️ <b>Advanced alert system for TradingView.</b>\n• Trend detection\n• Smart alerts\n• Multi-asset support\n\n⚙️ Platform: TradingView\n⭐ Rating: ★★★★★",
        #    "🛡️ <b>نظام تنبيهات متطور لمنصة TradingView.</b>\n• كشف دقيق للاتجاه\n• تنبيهات ذكية\n• دعم لعدة أصول مالية\n\n⚙️ المنصة: TradingView\n⭐ التقييم: ★★★★★",
       #     "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j2o0l709h7v19ki16nk1eqc1raor.png"
       # ),
       # (
       #     "ProfitWave Pro",
      #      {
     #           "life": ("https://payhip.com/b/zXuYD", "59.8$")
    #        },
   #         "🌊 <b>Clean and effective signals indicator.</b>\n• Wave-based entries\n• Trend reversals\n• Simple and accurate\n\n⚙️ Platform: TradingView\n⭐ Rating: ★★★★☆",
    #        "🌊 <b>مؤشر إشارات نظيف وفعال.</b>\n• دخول بناءً على الموجات (Waves)\n• كشف انعكاسات الاتجاه\n• بسيط ودقيق\n\n⚙️ المنصة: TradingView\n⭐ التقييم: ★★★★☆",
   #         "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j2nr6kh817sq1meacks1beqb8u15.png"
   #     ),
  #  ],
    "free_list": [
        (
            "Candle Close Timer©",
            {"life": ("https://www.mql5.com/en/market/product/164898", "FREE")},
            "⏳ <b>Real-time candle countdown timer.</b>\n• Displays remaining time until candle close\n• Appears above the active candle\n• Adjustable color & font size\n• Works on all symbols and timeframes\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
            "⏳ <b>مؤقت إغلاق الشمعة بالوقت الحقيقي.</b>\n• يعرض الوقت المتبقي حتى إغلاق الشمعة\n• يظهر فوق الشمعة الحالية مباشرة\n• إمكانية تعديل اللون وحجم الخط\n• يعمل على جميع الأزواج والفريمات\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★★",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1ji6hjtvvqahlqq7u51e5b10be1a.png"
        ),
      #  (
      #      "EMA Cross Over©",
      #      {"life": ("https://payhip.com/b/tqOye", "FREE")},
      #      "📉 <b>Simple and clean EMA crossover system.</b>\n• Fast signals\n• Works on all pairs\n• Great for beginners\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★★",
      #      "📉 <b>نظام تقاطع المتوسطات المتحركة (EMA) البسيط.</b>\n• إشارات سريعة\n• يعمل على جميع الأزواج\n• ممتاز للمبتدئين\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★★",
      #      "https://payhip.com/cdn-cgi/image/format=auto,width=1500/https://pe56d.s3.amazonaws.com/o_1j2nrbkn61v991a9fudi10k0d7ur.png"
      #  ),
        (
            "FX Clock©",
            {"life": ("https://www.mql5.com/en/market/product/148289", "FREE")},
            "⏰ <b>Trading session timer.</b>\n• Shows market sessions\n• Great for timing entries\n• Must-have utility\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★☆",
            "⏰ <b>مؤقت جلسات التداول العالمية.</b>\n• يعرض افتتاح وإغلاق الأسواق\n• ممتاز لتوقيت الدخول بدقة\n• أداة لا غنى عنها\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★☆",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j3m1qfpgate1j441e5b1qcj1a2m10.png"
        ),
        (
            "Trend Vision MT5©",
            {
                #"1m": ("soon", "8$"), 
                #"3m": ("soon", "20$"), 
                #"6m": ("soon", "35$"), 
                "life": ("https://www.mql5.com/en/market/product/143803", "FREE")
            },
            "📈 <b>Powerful trend monitoring indicator.</b>\n• Trend direction visualization\n• MTF confirmation\n• Very easy to use\n\n⚙️ Platform: MT5\n⭐ Rating: ★★★★☆",
            "📈 <b>مؤشر قوي لمراقبة الاتجاه (Trend).</b>\n• تصور مرئي لاتجاه السوق\n• تأكيد الإشارة من فريمات متعددة\n• سهل الاستخدام للغاية\n\n⚙️ المنصة: MT5\n⭐ التقييم: ★★★★☆",
            "https://payhip.com/cdn-cgi/image/format=auto/https://pe56d.s3.amazonaws.com/o_1j2o202tq6e418lvt5r1je918do10.png"
        ),
    ],
}

# --------------- KEYBOARDS ---------------
def language_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("English 🇺🇸", callback_data='set_lang_en')],
        [InlineKeyboardButton("العربية 🇸🇦", callback_data='set_lang_ar')]
    ])

def main_menu_keyboard(user_id, lang):
    t = TEXTS[lang]
    buttons = [
        [InlineKeyboardButton(t["products_btn"], callback_data='products')],
        #[InlineKeyboardButton(t["channel_btn"], url="https://t.me/BENALI_Trading_Tools")],
        [InlineKeyboardButton(t["user_reviews"], callback_data='show_reviews')],
        [InlineKeyboardButton(t["store_btn"], url="https://www.mql5.com/en/users/dahmi_benali/seller")],
        [InlineKeyboardButton(t["social_btn"], callback_data='social_links')],
        [InlineKeyboardButton(t["dev_contact_btn"], callback_data='dev_contact')],
        #[InlineKeyboardButton(t["contact_btn"], callback_data='contact')],
        [InlineKeyboardButton(t["info_btn"], callback_data='info')],
        [InlineKeyboardButton(t["change_lang_btn"], callback_data='change_lang')],
    ]

    if user_id in ADMINS:
        buttons.append([InlineKeyboardButton(t["admin_btn"], callback_data='admin_panel')])

    buttons.append([InlineKeyboardButton(t["close_btn"], callback_data='close_msg')])
    return InlineKeyboardMarkup(buttons)

def products_menu(lang):
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["cat_ea"], callback_data='ea_list')],
        [InlineKeyboardButton(t["cat_ind"], callback_data='ind_list')],
        [InlineKeyboardButton(t["cat_tools"], callback_data='tools_list')],
        #[InlineKeyboardButton(t["cat_tv"], callback_data='tv_list')],
        [InlineKeyboardButton(t["cat_free"], callback_data='free_list')],
        [InlineKeyboardButton(t["back_btn"], callback_data='back')]
    ])

def admin_panel_keyboard(lang):
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["admin_users"], callback_data='admin_users')],
        [InlineKeyboardButton(t["admin_bc"], callback_data='admin_broadcast')],
        [InlineKeyboardButton(t["back_btn"], callback_data='back')]
    ])

def generate_product_list(category, lang):
    t = TEXTS[lang]
    # item[0] is Name
    buttons = [[InlineKeyboardButton(item[0], callback_data=f"prd__{item[0]}")] for item in PRODUCTS[category]]
    buttons.append([InlineKeyboardButton(t["back_btn"], callback_data='products')])
    return InlineKeyboardMarkup(buttons)

# Updated Product Keyboard (Supports Link + Price Tuple)
def product_keyboard(links, lang):
    t = TEXTS[lang]
    buttons = []
    
    # Define keys and mapping to text keys
    options = [
        ("1m", "buy_1m"),
        ("3m", "buy_3m"),
        ("6m", "buy_6m"),
        ("life", "buy_life")
    ]
    
    row = []
    for key, text_key in options:
        # Check if product has this link key
        if key in links:
            # Unpack the tuple: (url, price_text)
            val = links[key]
            if isinstance(val, tuple) or isinstance(val, list):
                link = val[0]
                price = val[1]
            else:
                link = val
                price = ""

            label_duration = t[text_key] # e.g., "1 Month" or "لمدة شهر"
            
            # --- START MODIFICATION: Display price clearly in the button label ---
            # New format: [Price] | [Duration]
            if price:
                # This ensures the price is prominent.
                label = f"{price}  {label_duration}"
            else:
                label = label_duration
            # --- END MODIFICATION ---
            
            # If link is valid URL -> URL Button
            # If link is 'soon' or None -> Callback Button for Alert
            if link and link.startswith("http"):
                btn = InlineKeyboardButton(label, url=link)
            else:
                btn = InlineKeyboardButton(label, callback_data="coming_soon")
            
            row.append(btn)
            
            # 2 buttons per row
            if len(row) == 2:
                buttons.append(row)
                row = []
    
    # Append any remaining buttons
    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton(t["back_btn"], callback_data='back_products_section')])
    return InlineKeyboardMarkup(buttons)

# --------------- HANDLERS ---------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = get_user_lang(chat_id)

    # If new user or lang not set -> Force select lang
    if not lang:
        await update.message.reply_text(TEXTS['en']['choose_lang'], reply_markup=language_keyboard())
        return

    # 📌 إرسال الصورة الترحيبية بدلاً من نص فقط
    # If lang exists, show menu with PHOTO
    welcome_text = TEXTS[lang]["welcome"]
    keyboard = main_menu_keyboard(chat_id, lang)
    
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=WELCOME_IMAGE_URL,
        caption=welcome_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def products_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = get_user_lang(chat_id)

    # إذا كان مستخدم جديد ولم يحدد اللغة بعد
    if not lang:
        await update.message.reply_text(
            "Please choose your language first / يرجى اختيار اللغة أولاً:", 
            reply_markup=language_keyboard()
        )
        return

    t = TEXTS[lang]
    
    # إرسال قائمة الأقسام مباشرة
    await context.bot.send_message(
        chat_id=chat_id,
        text=t["choose_cat"],
        reply_markup=products_menu(lang),
        parse_mode="HTML"
    )

async def dev_contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = get_user_lang(chat_id)

    if not lang:
        await update.message.reply_text(TEXTS['en']['choose_lang'], reply_markup=language_keyboard())
        return

    t = TEXTS[lang]
    
    # تعريف أزرار التواصل (نفس الموجودة في قسم Callback)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Telegram (Direct) 💬", url="https://t.me/BenTrade_Trading")],
        [InlineKeyboardButton("Show Email 📧", callback_data='show_email')],
        [InlineKeyboardButton(t["back_btn"], callback_data='back')]
    ])

    # إرسال صورة المطور مع النص والأزرار
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=DEVELOPER_IMAGE_URL,
        caption=t["dev_msg"],
        reply_markup=kb,
        parse_mode="HTML"
    )


async def why_benali_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = get_user_lang(chat_id)

    # إذا كان مستخدم جديد ولم يحدد اللغة بعد
    if not lang:
        await update.message.reply_text(
            "Please choose your language first / يرجى اختيار اللغة أولاً:", 
            reply_markup=language_keyboard()
        )
        return

    t = TEXTS[lang]

    # إنشاء زر الرجوع
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t["back_btn"], callback_data='back')]
    ])

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=WELCOME_IMAGE_URL,
        caption=t["why_benali"],
        reply_markup=kb,
        parse_mode="HTML"
    )

async def show_review(update, context, index=0):
    query = update.callback_query
    chat_id = query.message.chat.id
    lang = get_user_lang(chat_id)

    if not lang:
        await query.message.reply_text(TEXTS['en']['choose_lang'], reply_markup=language_keyboard())
        return

    t = TEXTS[lang]

    total = len(REVIEWS)
    index = index % total  # يجعل الصور تدور في حلقة

    review = REVIEWS[index]

    # دعم captions متعددة اللغات
    if isinstance(review, dict):
        photo_path = review["path"]
        caption_dict = review.get("caption", {})
        # استخدم اللغة المحددة، أو النص الإنجليزي كافتراضي
        caption = caption_dict.get(lang, caption_dict.get("en", ""))
    else:
        photo_path = review
        caption = ""

    # إضافة عنوان ثابت أعلى الصورة (اختياري)
    #full_caption = f"{t['user_reviews']}\n\n{caption}" if caption else t['user_reviews']

    # إنشاء لوحة أزرار مترجمة
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t["prev_btn"], callback_data=f"review_{(index-1)%total}"),
            InlineKeyboardButton(t["next_btn"], callback_data=f"review_{(index+1)%total}")
        ],
        [
            InlineKeyboardButton(t["back_btn"], callback_data="back")
        ]
    ])

    # تعديل الرسالة الحالية بدل إرسال رسالة جديدة
    try:
        await query.edit_message_media(
            media=InputMediaPhoto(media=photo_path, parse_mode="HTML"),
            reply_markup=kb
        )
    except:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo_path,
            #caption=full_caption,
            reply_markup=kb,
            parse_mode="HTML"
        )

    # تحديث index عند الضغط على زر
    data_btn = query.data
    if data_btn.startswith('review_'):
        new_index = int(data_btn.split('_')[1])
        if new_index != index:
            await show_review(update, context, new_index)



async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id
    data_btn = query.data
    
    if data_btn.startswith('review_'):
        index = int(data_btn.split('_')[1])
        await show_review(update, context, index)
        return

    if data_btn == 'show_reviews':
        await show_review(update, context, 0)
        return


    if data_btn == 'show_email':
        await query.answer()

        t = TEXTS[get_user_lang(chat_id)]

        await query.edit_message_caption(
            caption=(
                "📧 <b>Email</b>\n\n"
                "<code>benali.tools@gmail.com</code>\n\n"
                f"{t['copy_hint']}"
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t["back_btn"], callback_data="back")]
            ])
        )
        return
    
    # 1. Handle Language Selection First (Before getting user lang for other actions)
    if data_btn == 'set_lang_en':
        set_user_lang(chat_id, 'en')
        await query.answer("Language set to English 🇬🇧")
        # 📌 حذف رسالة اختيار اللغة وإرسال الصورة الترحيبية الجديدة
        await query.message.delete()
        await context.bot.send_photo(
            chat_id,
            photo=WELCOME_IMAGE_URL, 
            caption=TEXTS['en']["welcome"], 
            reply_markup=main_menu_keyboard(chat_id, 'en'), 
            parse_mode="HTML"
        )
        return
    if data_btn == 'set_lang_ar':
        set_user_lang(chat_id, 'ar')
        await query.answer("تم اختيار اللغة العربية 🇩🇿")
        # 📌 حذف رسالة اختيار اللغة وإرسال الصورة الترحيبية الجديدة
        await query.message.delete()
        await context.bot.send_photo(
            chat_id,
            photo=WELCOME_IMAGE_URL, 
            caption=TEXTS['ar']["welcome"], 
            reply_markup=main_menu_keyboard(chat_id, 'ar'), 
            parse_mode="HTML"
        )
        return
    
    # 2. Get Lang for other buttons
    lang = get_user_lang(chat_id)
    if not lang:
        lang = 'en'
        set_user_lang(chat_id, 'en')

    t = TEXTS[lang]
    
    # Handle "Coming Soon" Alert
    if data_btn == 'coming_soon':
        await query.answer(t["coming_soon"], show_alert=True)
        return

    await query.answer()

    # General navigation
    if data_btn == 'close_msg':
            # 📌 التعديل لضمان إزالة الصورة: حذف الرسالة الحالية (صورة/نص) وإرسال رسالة نصية بسيطة جديدة.
            try:
                # 1. حذف الرسالة الحالية (الصورة أو النص مع الأزرار)
                await query.message.delete()
            except Exception:
                # نتجاوز أي خطأ في الحذف ونتابع (قد تكون الرسالة قد حُذفت مسبقًا)
                pass
                
            # 2. إرسال رسالة نصية جديدة للإغلاق
            await context.bot.send_message(
                chat_id=chat_id, 
                text=t["thank_you"]
            )
            return
    
    if data_btn == 'change_lang':
        # تحرير الرسالة الحالية إلى نص اختيار اللغة
        try:
             await query.edit_message_caption(TEXTS[lang]['choose_lang'], reply_markup=language_keyboard())
        except BadRequest:
             await query.edit_message_text(TEXTS[lang]['choose_lang'], reply_markup=language_keyboard())
        return

    if data_btn == 'back':
            # التحقق مما إذا كانت الرسالة الحالية تحتوي على صورة (مثل صفحة المطور أو التواصل)
            if query.message.photo:
                try:
                    # إذا كانت صورة، نقوم بتعديل الوسائط (Media) لتعود لصورة الترحيب الأصلية
                    await query.edit_message_media(
                        media=InputMediaPhoto(
                            media=WELCOME_IMAGE_URL,
                            caption=t["welcome"],
                            parse_mode="HTML"
                        ),
                        reply_markup=main_menu_keyboard(chat_id, lang)
                    )
                except Exception:
                    # كخطة بديلة إذا فشل التعديل، نحذف ونرسل من جديد
                    try:
                        await query.message.delete()
                    except: pass
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=WELCOME_IMAGE_URL,
                        caption=t["welcome"],
                        reply_markup=main_menu_keyboard(chat_id, lang),
                        parse_mode="HTML"
                    )
            else:
                # إذا كانت الرسالة نصية فقط، نحذفها ونرسل الصورة الترحيبية
                try:
                    await query.message.delete()
                except: pass
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=WELCOME_IMAGE_URL,
                    caption=t["welcome"],
                    reply_markup=main_menu_keyboard(chat_id, lang),
                    parse_mode="HTML"
                )
            return

    if data_btn == 'products':
            # 📌 REFINEMENT: Ensure the message is edited as TEXT, not photo caption.
            # This removes the image and replaces it with text and buttons.
            try:
                # Try to edit the current message (which could be a photo caption 
                # or a simple text message) into a pure text message.
                await query.edit_message_text(t["choose_cat"], reply_markup=products_menu(lang), parse_mode="HTML")
            except BadRequest:
                # If editing fails (e.g., trying to edit text into a photo caption 
                # or vice-versa, or due to message type mismatch), we fall back 
                # to deleting the existing message and sending a new text message.
                try:
                    await query.message.delete()
                except Exception:
                    pass
                
                # Send a brand new text message with the product categories
                await context.bot.send_message(
                    chat_id,
                    text=t["choose_cat"],
                    reply_markup=products_menu(lang),
                    parse_mode="HTML"
                )
            return
    
# --- Social Media Section ---
    if data_btn == 'social_links':
        kb = InlineKeyboardMarkup([
            #[InlineKeyboardButton("Telegram Channel", url="https://t.me/BENALI_Trading_Tools")],
            [InlineKeyboardButton("MQL5", url="https://www.mql5.com/en/users/dahmi_benali/news")],
            [InlineKeyboardButton("Instagram", url="https://www.instagram.com/bentrade_trading/?__pwa=1")],
            [InlineKeyboardButton("Facebook", url="https://www.facebook.com/profile.php?id=61579917181259")],
            [InlineKeyboardButton("YouTube", url="https://www.youtube.com/channel/UCb4hdzflJXyL4y9oYAcqihA")],
            [InlineKeyboardButton(t["back_btn"], callback_data='back')]
        ])
        await query.message.delete()
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=SOCIAL_IMAGE_URL, # الآن سيجد المتغير ولن يظهر الخطأ
            caption=t["social_msg"], # الآن سيجد المفتاح ولن يظهر الخطأ
            reply_markup=kb,
            parse_mode="HTML"
        )
        return

    # --- Developer Contact Section ---
    if data_btn == 'dev_contact':
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Telegram (Direct) 💬", url="https://t.me/BenTrade_Trading")],
            [InlineKeyboardButton("Show Email 📧", callback_data='show_email')],
            [InlineKeyboardButton(t["back_btn"], callback_data='back')]
        ])
        await query.message.delete()
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=DEVELOPER_IMAGE_URL,
            caption=t["dev_msg"],
            reply_markup=kb,
            parse_mode="HTML"
        )
        return

    if data_btn in PRODUCTS.keys():
        # نحذف الرسالة الحالية (الصورة أو النص المحرر) ونرسل رسالة نصية جديدة لقائمة المنتجات
        try:
            await query.message.delete()
        except Exception:
            pass # Ignore if delete fails
            
        context.user_data["last_category"] = data_btn
        await context.bot.send_message(chat_id, t["choose_prod"], reply_markup=generate_product_list(data_btn, lang))
        return

    # Product Selection (already sends a photo, which is fine)
    if data_btn.startswith("prd__"):
        sel_name = data_btn.replace("prd__", "")
        
        for cat_key in PRODUCTS:
            for item in PRODUCTS[cat_key]:
                # item structure: (Name, Links_Dict, Desc_En, Desc_Ar, Img)
                if item[0] == sel_name:
                    name = item[0]
                    links = item[1]  # Now a dictionary
                    desc = item[2] if lang == 'en' else item[3]
                    img = item[4]

                    caption = f"📌 <b>{name}</b>\n\n{desc}{t['click_buy']}"
                    kb = product_keyboard(links, lang)
                    
                    if img:
                        try:
                            # Try editing the current message to a new photo/caption
                            await query.edit_message_media(
                                media=InputMediaPhoto(media=img, caption=caption, parse_mode="HTML"),
                                reply_markup=kb
                            )
                        except:
                            # Fallback: Delete current message (text or photo) and send new photo message
                            try:
                                await query.message.delete()
                            except Exception:
                                pass
                            await context.bot.send_photo(chat_id, photo=img, caption=caption, parse_mode="HTML", reply_markup=kb)
                    else:
                        await query.edit_message_text(caption, parse_mode="HTML", reply_markup=kb)
                    return

    if data_btn == "back_products_section":
        # العودة من تفاصيل المنتج (صورة) إلى قائمة المنتجات (رسالة نصية)
        last = context.user_data.get("last_category", "ea_list")
        # نحذف الرسالة الحالية (الصورة) ونرسل قائمة المنتجات كرسالة نصية جديدة
        try:
            await query.message.delete()
        except Exception:
            pass
            
        await context.bot.send_message(chat_id, t["choose_prod"], reply_markup=generate_product_list(last, lang))
        return

    if data_btn == 'contact':
        contact_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Telegram", url="https://t.me/BenTrade_Trading")],
            [InlineKeyboardButton("Instagram", url="https://www.instagram.com/bentrade_trading/?__pwa=1")],
            [InlineKeyboardButton("Facebook", url="https://www.facebook.com/profile.php?id=61579917181259")],
            [InlineKeyboardButton(t["back_btn"], callback_data='back')]
        ])
        # تحرير إلى رسالة نصية عادية
        try:
            await query.edit_message_caption(t["contact_msg"], reply_markup=contact_keyboard)
        except BadRequest:
            await query.edit_message_text(t["contact_msg"], reply_markup=contact_keyboard)
        return

    if data_btn == 'info':
        # تحرير إلى رسالة نصية عادية
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(t["back_btn"], callback_data='back')]])
        try:
            await query.edit_message_caption(t["tools_msg"], parse_mode="HTML", reply_markup=keyboard)
        except BadRequest:
            await query.edit_message_text(t["tools_msg"], parse_mode="HTML", reply_markup=keyboard)
        return

    # Admin Panel (Text Messages)
    if data_btn == 'admin_panel':
        if chat_id not in ADMINS:
            await query.answer(t["unauth"], show_alert=True)
            return
        
        # 📌 التعديل: تحرير الرسالة باستخدام caption إذا كانت رسالة صورة أو text إذا كانت نصية
        text = f"{t['admin_btn']}"
        try:
            await query.edit_message_caption(text, reply_markup=admin_panel_keyboard(lang))
        except BadRequest:
            await query.edit_message_text(text, reply_markup=admin_panel_keyboard(lang))
        return

    if data_btn == "admin_users":
        data = load_users_data()
        count = len(data.get("users", {}))
        text = f"👥 Users: {count}"

        # 📌 التعديل: تحرير الرسالة باستخدام caption إذا كانت رسالة صورة أو text إذا كانت نصية
        try:
            await query.edit_message_caption(text, reply_markup=admin_panel_keyboard(lang))
        except BadRequest:
            await query.edit_message_text(text, reply_markup=admin_panel_keyboard(lang))
        return

    if data_btn == "admin_broadcast":
        text = t["bc_hint"]
        
        # 📌 التعديل: تحرير الرسالة باستخدام caption إذا كانت رسالة صورة أو text إذا كانت نصية
        try:
            await query.edit_message_caption(text, reply_markup=admin_panel_keyboard(lang))
        except BadRequest:
            await query.edit_message_text(text, reply_markup=admin_panel_keyboard(lang))
        return

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /broadcast Message")
        return

    msg = " ".join(context.args)
    data = load_users_data()
    users_dict = data.get("users", {}) # Dict {id: lang}
    
    count = 0
    for uid in users_dict.keys():
        try:
            await context.bot.send_message(chat_id=int(uid), text=msg, parse_mode="HTML")
            count += 1
        except Exception as e:
            logger.warning("Broadcast failed for %s: %s", uid, e)
            
    await update.message.reply_text(f"✅ Broadcast sent to {count} users.")

# Save user if they just type something (default EN if not set)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = get_user_lang(chat_id)
    if not lang:
        pass

if __name__ == "__main__":
    logger.info("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("product", products_command)) # الأمر الجديد
    app.add_handler(CommandHandler("products", products_command)) # إضافة النسخة بالجمع أيضاً

# --- الأوامر الجديدة للتواصل مع المطور ---
    app.add_handler(CommandHandler("dev", dev_contact_command))
    app.add_handler(CommandHandler("developer", dev_contact_command))
    # ---------------------------------------

    # --- الأمر الجديد لعرض Why BENALI Trading Tools ---
    app.add_handler(CommandHandler("why", why_benali_command))

# ---------------------------------------------------

    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()