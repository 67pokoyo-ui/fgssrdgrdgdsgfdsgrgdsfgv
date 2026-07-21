import telebot, os, re
from telebot.types import InlineKeyboardMarkup as KM, InlineKeyboardButton as KB

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
orders = {}

def get_start_markup():
    m = KM(row_width=2)
    b1 = KB("🛍️ Купить Звёзды или Premium", callback_data="buy")
    b2 = KB("🚀 Приложение", web_app=telebot.types.WebAppInfo(url="https://67pokoyo-ui.github.io/fgssrdgrdgdsgfdsgrgdsfgv/"))
    b3 = KB("🧾 Мои чеки", callback_data="c_cl")
    b4 = KB("👥 Поддержка", url="https://t.me/TonPuresSupportBot")
    b5 = KB("🇬🇧 English", callback_data="l_cl")
    return m.add(b1).row(b2, b3).row(b4, b5)

def get_products_markup():
    m = KM(row_width=2)
    m.row(KB("Звёзды ⭐", callback_data="p_stars"), KB("Премиум 💎", callback_data="p_prem"))
    return m.add(KB("Прокси 🌐", callback_data="p_prox"), KB("🔙 Назад", callback_data="to_st"))

def get_pay_m(c):
    return KM().add(KB("Карты (RU)", callback_data=f"sbp_{c}"), KB("🔙 Назад", callback_data="buy"))

def get_gate_m(c):
    return KM().add(KB("RUB (СБП) #1", callback_data=f"g_1_{c}"), KB("RUB (СБП) #2", callback_data=f"g_2_{c}"), KB("🔙 Назад", callback_data=f"p_{c}"))

def get_items_markup(c):
    m = KM(row_width=2)
    if c == "stars":
        m.row(KB("100 ⭐", callback_data="i_stars_100_175"), KB("500 ⭐", callback_data="i_stars_500_875")).row(KB("1000 ⭐", callback_data="i_stars_1000_1750"), KB("5000 ⭐", callback_data="i_stars_5000_8750"))
    elif c == "premium":
        m.add(KB("3 мес. 💎", callback_data="i_prem_3_1290"), KB("6 мес. 💎", callback_data="i_prem_6_1690"), KB("12 мес. 💎", callback_data="i_prem_12_2990"))
    elif c == "proxy":
        m.add(KB("1 нед. 🌐", callback_data="i_prox_1н_50"), KB("2 нед. 🌐", callback_data="i_prox_2н_90"), KB("1 мес. 🌐", callback_data="i_prox_1м_190"), KB("2 мес. 🌐", callback_data="i_prox_2м_350"), KB("3 мес. 🌐", callback_data="i_prox_3м_490"))
    return m.add(KB("🔙 Назад", callback_data="buy"))

@bot.message_handler(commands=['start'])
def start_cmd(msg):
    bot.clear_step_handler_by_chat_id(msg.chat.id)
    orders[msg.chat.id] = {}
    txt = f"Добро пожаловать, **{msg.from_user.first_name}**!\n\nЭто официальный бот **TonPures** 🌟\n\nЗдесь можно купить **Telegram Stars** ⭐, **Premium** 💎\nА также **Proxy** 🌐 по самой выгодной цене на рынке.\n\n• Нужен только username\n• Оплата по СБП\n• Без скрытых комиссий"
    bot.send_message(msg.chat.id, txt, reply_markup=get_start_markup(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    cid, mid = call.message.chat.id, call.message.id
    if cid not in orders: orders[cid] = {}
    bot.answer_callback_query(call.id)
    
    if call.data == "buy":
        bot.clear_step_handler_by_chat_id(cid)
        bot.edit_message_text("Выберите товар:", cid, mid, reply_markup=get_products_markup())
    elif call.data == "to_st":
        bot.clear_step_handler_by_chat_id(cid)
        txt = f"Добро пожаловать, **{call.from_user.first_name}**!\n\nЭто официальный бот **TonPures** 🌟"
        bot.edit_message_text(txt, cid, mid, reply_markup=get_start_markup(), parse_mode='Markdown')
    elif call.data.startswith("p_"):
        c = call.data.split("_")[1]
        orders[cid]["cat"] = c
        n = {"stars": "Звёзды ⭐", "prem": "Премиум 💎", "prox": "Прокси 🌐"}[c]
        msg = bot.edit_message_text(f"Товар: {n}\n\nВведите Telegram username получателя (без @) вручную в чат:", cid, mid, reply_markup=KM().row(KB("🔙 Назад", callback_data="buy")))
        bot.register_next_step_handler(msg, pr_user, c, mid)
    elif call.data.startswith("sbp_"):
        c = call.data.split("_")[1]
        bot.edit_message_text(f"Товар: {c}\nПолучатель: {orders[cid].get('user', '@User')}\n\nВыберите оплату:", cid, mid, reply_markup=get_gate_m(c))
    elif call.data.startswith("g_"):
        pts = call.data.split("_")
        g, c = f"RUB (СБП) #{pts[1]}", pts[2]
        orders[cid]["gate"] = g
        t = f"Товар: {c}\nПолучатель: {orders[cid].get('user', '@User')}\nСпособ оплаты: {g}\n\nВыберите пак:"
        msg = bot.edit_message_text(t, cid, mid, reply_markup=get_items_markup(c))
        if c == "stars": bot.register_next_step_handler(msg, pr_stars, mid)
    elif call.data.startswith("i_"):
        pts = call.data.split("_")
        orders[cid]["amt"], orders[cid]["price"] = pts[2], pts[3]
        show_inv(cid, mid, pts[1])
    elif call.data == "pay_f":
        pr = orders[cid].get("price", "150")
        u = orders[cid].get("user", "@User")
        my_phone = "79123456789"
        lnk = f"https://nspk.ru{my_phone}&sum={pr}&desc=TonPures_{u.replace('@','')}"
        txt = f"🔒 **Анонимный счёт СБП успешно сформирован!**\n\nСумма: **{pr} ₽**\nПолучатель товара: `{u}`\n\n👇 **Инструкция по оплате через СБП:**\n1. Нажмите синюю кнопку ниже.\n2. Сумма **{pr} ₽** подставится сама. Твой телефон скрыт на 100%.\n3. После перевода нажмите «Я оплатил» и пришлите чек! 🚀"
        m = KM().add(KB("📱 Открыть приложение банка (СБП)", url=lnk)).add(KB("✅ Я оплатил (Отправить чек)", callback_data="c_sent")).add(KB("🏡 В меню", callback_data="to_st"))
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode='Markdown')
    elif call.data == "c_sent":
        bot.send_message(cid, "📥 Отлично! Пришлите скриншот чека об оплате прямо в этот чат.")

def pr_user(message, c, old_mid):
    cid = message.chat.id
    try: bot.delete_message(cid, message.message_id)
    except: pass
    if message.text and message.text.startswith('/'): return
    t = message.text.strip().replace('@', '')
    if not re.match(r"^[a-zA-Z0-9_]{4,32}$", t):
        msg = bot.send_message(cid, "❌ Неверный формат! Введите юзернейм ещё раз:")
        bot.register_next_step_handler(msg, pr_user, c, old_mid)
        return
    orders[cid]["user"] = f"@{t}"
    try: bot.edit_message_text(f"Товар: {c}\nПолучатель: @{t}\n\nВыберите способ оплаты:", cid, old_mid, reply_markup=get_pay_m(c))
    except: bot.send_message(cid, f"Товар: {c}\nПолучатель: @{t}\n\nВыберите способ оплаты:", reply_markup=get_pay_m(c))

def pr_stars(message, old_mid):
    cid = message.chat.id
    try: bot.delete_message(cid, message.message_id)
    except: pass
    if message.text and message.text.startswith('/'): return
    try:
        count = int(message.text.strip())
        if count < 50 or count > 20000: raise ValueError
    except:
        msg = bot.send_message(cid, "❌ От 50 до 20 000 звёзд! Введите заново:")
        bot.register_next_step_handler(msg, pr_stars, old_mid)
        return
    pr = str(round(count * 1.75))
    orders[cid]["amt"], orders[cid]["price"] = str(count), pr
    show_inv(cid, old_mid, "stars")

def show_inv(cid, mid, cat):
    u, g, a, pr = orders[cid].get("user", "@User"), orders[cid].get("gate", "СБП #1"), orders[cid].get("amt", "100"), orders[cid].get("price", "150")
    lnk = f"[{u}](https://t.me{u.replace('@', '')})"
    txt = f"🛍️ Пополнение для {lnk}\n\n**Telegram TONPURES**\n\nПолучатель: {u}\nСпособ оплаты: {g}\nПак: {a} (~{pr}₽)\n\nНажмите кнопку ниже, чтобы создать платёж"
    m = KM().row(KB(f"🚀 Заплатить {pr}₽", callback_data="pay_f"), KB("🏡 В меню", callback_data="to_st"))
    bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == "__main__":
    bot.infinity_polling()
