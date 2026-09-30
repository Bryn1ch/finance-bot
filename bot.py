# ---------- FSM ----------
class AddOp(StatesGroup):
    entering_amount = State()
    choosing_account = State()

class AdjustBalance(StatesGroup):
    entering_amount = State()
    choosing_account = State()
    confirming = State()

class NewCategory(StatesGroup):
    entering_name = State()

class NewDebt(StatesGroup):
    entering_person = State()
    entering_amount = State()
    entering_note = State()
    entering_due = State()

class NewBudget(StatesGroup):
    entering_amount = State()

class NewMonthlyBudget(StatesGroup):
    entering_amount = State()

class NotifySettings(StatesGroup):
    entering_hour = State()
    entering_minute = State()

class NewRecurring(StatesGroup):
    entering_title = State()
    entering_amount = State()
    choosing_type = State()
    choosing_category = State()
    choosing_account = State()
    entering_day = State()

class NewAccount(StatesGroup):
    entering_name = State()
    choosing_kind = State()

class Transfer(StatesGroup):
    choosing_from = State()
    choosing_to = State()
    entering_amount = State()

# ---------- Клавиатуры ----------
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Доход", callback_data="add_income"),
         InlineKeyboardButton(text="➖ Расход", callback_data="add_expense")],
        [InlineKeyboardButton(text="🔄 Перевод", callback_data="transfer"),
         InlineKeyboardButton(text="⭐ Повторить", callback_data="repeat_last")],
        [InlineKeyboardButton(text="✏️ Корректировка", callback_data="adjust_balance")],
        [InlineKeyboardButton(text="💳 Счета", callback_data="accounts_menu"),
         InlineKeyboardButton(text="💵 Баланс", callback_data="balance")],
        [InlineKeyboardButton(text="🤝 Долги", callback_data="debts_menu"),
         InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="📈 График", callback_data="chart_menu"),
         InlineKeyboardButton(text="📜 История", callback_data="history")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings_menu")],
    ])

def accounts_kb(user_id):
    accounts = get_accounts(user_id)
    rows = []
    for acc_id, name, kind in accounts:
        bal = get_account_balance(user_id, acc_id)
        emoji = "💳" if kind == "card" else ("💵" if kind == "cash" else "🏦")
        label = f"{emoji} {name}: {bal:.0f} ₽"
        rows.append([InlineKeyboardButton(text=label[:60], callback_data=f"acc_view:{acc_id}")])
    rows.append([InlineKeyboardButton(text="➕ Добавить счёт", callback_data="acc_add")])
    rows.append([InlineKeyboardButton(text="⬅️ В меню", callback_data="back_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def account_picker_kb(user_id, prefix):
    """prefix — например 'tx_acc' или 'tr_from', 'tr_to', 'rec_acc', 'adj_acc'."""
    accounts = get_accounts(user_id)
    rows = []
    for acc_id, name, kind in accounts:
        bal = get_account_balance(user_id, acc_id)
        emoji = "💳" if kind == "card" else ("💵" if kind == "cash" else "🏦")
        label = f"{emoji} {name} ({bal:.0f} ₽)"
        rows.append([InlineKeyboardButton(text=label[:60], callback_data=f"{prefix}:{acc_id}")])
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def account_kind_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Карта", callback_data="acc_kind:card")],
        [InlineKeyboardButton(text="💵 Наличные", callback_data="acc_kind:cash")],
        [InlineKeyboardButton(text="🏦 Другое", callback_data="acc_kind:other")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])

def account_actions_kb(acc_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑 Удалить счёт", callback_data=f"acc_del:{acc_id}")],
        [InlineKeyboardButton(text="⬅️ К счетам", callback_data="accounts_menu")],
    ])

def categories_kb(user_id, ttype):
    categories = get_user_categories(user_id, ttype)
    rows = []
    for i in range(0, len(categories), 2):
        row = [InlineKeyboardButton(text=c, callback_data=f"cat:{ttype}:{c}")
               for c in categories[i:i+2]]
        rows.append(row)
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def categories_kb_rec(user_id, ttype):
    categories = get_user_categories(user_id, ttype)
    rows = []
    for i in range(0, len(categories), 2):
        row = [InlineKeyboardButton(text=c, callback_data=f"rec_cat:{c}")
               for c in categories[i:i+2]]
        rows.append(row)
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def after_amount_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ])

def confirm_reset_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, удалить всё", callback_data="reset_yes"),
         InlineKeyboardButton(text="❌ Отмена", callback_data="reset_no")],
    ])

def adjust_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Применить", callback_data="adjust_yes"),
         InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])

def debts_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Активные долги", callback_data="debts_list")],
        [InlineKeyboardButton(text="➕ Добавить долг", callback_data="debt_add")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_menu")],
    ])

def debt_direction_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Я дал в долг", callback_data="debt_dir:lent")],
        [InlineKeyboardButton(text="📥 Я взял в долг", callback_data="debt_dir:borrowed")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])

def debt_due_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сегодня", callback_data="debt_due:0")],
        [InlineKeyboardButton(text="Через 3 дня", callback_data="debt_due:3"),
         InlineKeyboardButton(text="Через 7 дней", callback_data="debt_due:7")],
        [InlineKeyboardButton(text="Через 30 дней", callback_data="debt_due:30")],
        [InlineKeyboardButton(text="Без срока", callback_data="debt_due:none")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])

def debt_note_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пропустить", callback_data="debt_note_skip")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])

def debt_actions_kb(debt_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Закрыть долг", callback_data=f"debt_close:{debt_id}")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"debt_del:{debt_id}")],
        [InlineKeyboardButton(text="⬅️ К списку", callback_data="debts_list")],
    ])

def settings_menu_kb(user_id):
    hour, minute, include_debts = get_user_settings(user_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏰ Время уведомлений: {hour:02d}:{minute:02d}",
                              callback_data="settings_time")],
        [InlineKeyboardButton(
            text=f"🔄 Долги в балансе: {'✅ Вкл' if include_debts else '❌ Выкл'}",
            callback_data="settings_toggle_debts")],
        [InlineKeyboardButton(text="🏷 Категории", callback_data="manage_cats")],
        [InlineKeyboardButton(text="🎯 Бюджеты", callback_data="budgets_menu")],
        [InlineKeyboardButton(text="🧾 Регулярные платежи", callback_data="recurring_menu")],
        [InlineKeyboardButton(text="🗑 Полный сброс данных", callback_data="reset_confirm")],
        [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back_menu")],
    ])

def settings_time_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="08:00", callback_data="settime:8:0"),
         InlineKeyboardButton(text="10:00", callback_data="settime:10:0"),
         InlineKeyboardButton(text="12:00", callback_data="settime:12:0")],
        [InlineKeyboardButton(text="18:00", callback_data="settime:18:0"),
         InlineKeyboardButton(text="20:00", callback_data="settime:20:0"),
         InlineKeyboardButton(text="22:00", callback_data="settime:22:0")],
        [InlineKeyboardButton(text="✏️ Своё время", callback_data="settings_custom_time")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="settings_menu")],
    ])

def manage_cats_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить категорию", callback_data="cat_add")],
        [InlineKeyboardButton(text="🗑 Удалить категорию", callback_data="cat_del")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="settings_menu")],
    ])

def cat_type_kb(prefix):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Для доходов", callback_data=f"{prefix}:income"),
         InlineKeyboardButton(text="➖ Для расходов", callback_data=f"{prefix}:expense")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])

def del_cat_list_kb(user_id, ttype):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM categories WHERE user_id=? AND type=? ORDER BY name",
                (user_id, ttype))
    cats = [r[0] for r in cur.fetchall()]
    conn.close()
    if not cats:
        return None
    rows = []
    for i in range(0, len(cats), 2):
        row = [InlineKeyboardButton(text=f"🗑 {c}", callback_data=f"delcat:{ttype}:{c}")
               for c in cats[i:i+2]]
        rows.append(row)
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def budgets_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Мои бюджеты", callback_data="budgets_list")],
        [InlineKeyboardButton(text="🎯 Общий бюджет месяца", callback_data="monthly_budget_menu")],
        [InlineKeyboardButton(text="➕ Бюджет по категории", callback_data="budget_add")],
        [InlineKeyboardButton(text="🗑 Удалить бюджет по категории", callback_data="budget_del")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="settings_menu")],
    ])

def budget_cats_kb(user_id):
    cats = [c for c in get_user_categories(user_id, "expense") if c != "Корректировка"]
    rows = []
    for i in range(0, len(cats), 2):
        row = [InlineKeyboardButton(text=c, callback_data=f"budget_cat:{c}")
               for c in cats[i:i+2]]
        rows.append(row)
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def budget_del_kb(user_id):
    budgets = get_budgets(user_id)
    if not budgets:
        return None
    rows = []
    for i in range(0, len(budgets), 2):
        row = [InlineKeyboardButton(text=f"🗑 {c} ({a:.0f})", callback_data=f"budget_del_do:{c}")
               for c, a in budgets[i:i+2]]
        rows.append(row)
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def monthly_budget_kb(user_id):
    amount = get_monthly_budget(user_id)
    rows = []
    if amount:
        rows.append([InlineKeyboardButton(text=f"💰 Текущий: {amount:.2f} ₽",
                                          callback_data="noop")])
        rows.append([InlineKeyboardButton(text="✏️ Изменить", callback_data="monthly_budget_set")])
        rows.append([InlineKeyboardButton(text="🗑 Удалить", callback_data="monthly_budget_del")])
    else:
        rows.append([InlineKeyboardButton(text="➕ Установить бюджет", callback_data="monthly_budget_set")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="budgets_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def recurring_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Мои платежи", callback_data="recurring_list")],
        [InlineKeyboardButton(text="➕ Добавить платёж", callback_data="recurring_add")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="settings_menu")],
    ])

def recurring_type_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➖ Расход (списание)", callback_data="rec_type:expense")],
        [InlineKeyboardButton(text="➕ Доход (поступление)", callback_data="rec_type:income")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])

def recurring_day_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1", callback_data="rec_day:1"),
         InlineKeyboardButton(text="5", callback_data="rec_day:5"),
         InlineKeyboardButton(text="10", callback_data="rec_day:10")],
        [InlineKeyboardButton(text="15", callback_data="rec_day:15"),
         InlineKeyboardButton(text="20", callback_data="rec_day:20"),
         InlineKeyboardButton(text="25", callback_data="rec_day:25")],
        [InlineKeyboardButton(text="28", callback_data="rec_day:28"),
         InlineKeyboardButton(text="30", callback_data="rec_day:30"),
         InlineKeyboardButton(text="31", callback_data="rec_day:31")],
        [InlineKeyboardButton(text="✏️ Свой день", callback_data="rec_custom_day")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])

def recurring_actions_kb(rec_id, active):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="⏸ Приостановить" if active else "▶️ Возобновить",
            callback_data=f"rec_toggle:{rec_id}"
        )],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"rec_del:{rec_id}")],
        [InlineKeyboardButton(text="⬅️ К списку", callback_data="recurring_list")],
    ])

def chart_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Расходы по месяцам", callback_data="chart_expenses_monthly")],
        [InlineKeyboardButton(text="📈 Доходы vs Расходы", callback_data="chart_income_vs_expense")],
        [InlineKeyboardButton(text="🥧 Топ категорий (месяц)", callback_data="chart_top_cats")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_menu")],
    ])
# ---------- Handlers ----------
@dp.message(Command("start"))
async def cmd_start(message: Message):
    get_user_settings(message.from_user.id)
    ensure_default_accounts(message.from_user.id)
    total = get_total_balance(message.from_user.id)
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"💰 Общий баланс: <b>{total:.2f} ₽</b>\n\n"
        "Я помогу контролировать твои средства, счета, долги и бюджеты.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "noop")
async def cb_noop(call: CallbackQuery):
    await call.answer()

@dp.callback_query(F.data == "back_menu")
async def cb_back_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    total = get_total_balance(call.from_user.id)
    await call.message.edit_text(
        f"Главное меню\n\n💰 Общий баланс: <b>{total:.2f} ₽</b>",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
    await call.answer()

# ---------- Счета ----------
@dp.callback_query(F.data == "accounts_menu")
async def cb_accounts_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    items, total = get_accounts_with_balances(call.from_user.id)
    if not items:
        await call.message.edit_text(
            "💳 <b>Счета</b>\n\nУ тебя пока нет счетов.",
            parse_mode="HTML",
            reply_markup=accounts_kb(call.from_user.id)
        )
        await call.answer()
        return

    text = "💳 <b>Твои счета</b>\n\n"
    for acc_id, name, kind, bal in items:
        emoji = "💳" if kind == "card" else ("💵" if kind == "cash" else "🏦")
        text += f"{emoji} <b>{name}</b>: {bal:.2f} ₽\n"
    text += f"\n━━━━━━━━━━━━━━━━\n💰 <b>Общая сумма: {total:.2f} ₽</b>"

    await call.message.edit_text(text, parse_mode="HTML",
                                 reply_markup=accounts_kb(call.from_user.id))
    await call.answer()

@dp.callback_query(F.data.startswith("acc_view:"))
async def cb_acc_view(call: CallbackQuery, state: FSMContext):
    acc_id = int(call.data.split(":")[1])
    acc = get_account(acc_id)
    if not acc or acc[1] != call.from_user.id:
        await call.answer("Не найдено", show_alert=True)
        return
    _, _, name, kind = acc
    bal = get_account_balance(call.from_user.id, acc_id)
    emoji = "💳" if kind == "card" else ("💵" if kind == "cash" else "🏦")
    text = (
        f"{emoji} <b>{name}</b>\n\n"
        f"💰 Баланс: <b>{bal:.2f} ₽</b>"
    )
    await call.message.edit_text(text, parse_mode="HTML",
                                 reply_markup=account_actions_kb(acc_id))
    await call.answer()

@dp.callback_query(F.data == "acc_add")
async def cb_acc_add(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(NewAccount.entering_name)
    await call.message.edit_text(
        "➕ <b>Новый счёт</b>\n\nВведи название (например, «Сбер», «Тинькофф»):",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ])
    )
    await call.answer()

@dp.message(NewAccount.entering_name)
async def process_acc_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name or len(name) > 30:
        await message.answer("❌ Некорректное название (до 30 символов).")
        return
    await state.update_data(acc_name=name)
    await state.set_state(NewAccount.choosing_kind)
    await message.answer(
        f"Счёт «<b>{name}</b>»\n\nВыбери тип:",
        parse_mode="HTML",
        reply_markup=account_kind_kb()
    )

@dp.callback_query(F.data.startswith("acc_kind:"))
async def cb_acc_kind(call: CallbackQuery, state: FSMContext):
    kind = call.data.split(":")[1]
    data = await state.get_data()
    name = data.get("acc_name")
    if not name:
        await call.answer("Ошибка", show_alert=True)
        return
    ok = add_account(call.from_user.id, name, kind)
    await state.clear()
    if ok:
        await call.message.edit_text(
            f"✅ Счёт <b>{name}</b> создан!",
            parse_mode="HTML",
            reply_markup=accounts_kb(call.from_user.id)
        )
        await call.answer("Создан")
    else:
        await call.message.edit_text(
            f"⚠️ Счёт <b>{name}</b> уже существует.",
            parse_mode="HTML",
            reply_markup=accounts_kb(call.from_user.id)
        )
        await call.answer()

@dp.callback_query(F.data.startswith("acc_del:"))
async def cb_acc_del(call: CallbackQuery, state: FSMContext):
    acc_id = int(call.data.split(":")[1])
    ok, info = delete_account(call.from_user.id, acc_id)
    if ok:
        await call.message.edit_text(
            f"🗑 Счёт <b>{info}</b> удалён вместе с операциями.",
            parse_mode="HTML",
            reply_markup=accounts_kb(call.from_user.id)
        )
        await call.answer("Удалён")
    else:
        await call.answer(info, show_alert=True)

# ---------- Баланс ----------
@dp.callback_query(F.data == "balance")
async def cb_balance(call: CallbackQuery, state: FSMContext):
    await state.clear()
    income, expense, _ = get_balance(call.from_user.id)
    items, total = get_accounts_with_balances(call.from_user.id)

    debts = get_active_debts(call.from_user.id)
    lent = sum(d[3] for d in debts if d[1] == "lent")
    borrowed = sum(d[3] for d in debts if d[1] == "borrowed")
    hour, minute, include_debts = get_user_settings(call.from_user.id)

    effective = total + (lent - borrowed if include_debts else 0)
    emoji = "🟢" if effective >= 0 else "🔴"

    text = (
        f"💼 <b>Твой баланс</b>\n\n"
        f"📈 Доходы: <b>{income:.2f} ₽</b>\n"
        f"📉 Расходы: <b>{expense:.2f} ₽</b>\n\n"
        f"💳 <b>По счетам:</b>\n"
    )
    for acc_id, name, kind, bal in items:
        em = "💳" if kind == "card" else ("💵" if kind == "cash" else "🏦")
        text += f"{em} {name}: <b>{bal:.2f} ₽</b>\n"
    text += f"\n💰 <b>Общая сумма: {total:.2f} ₽</b>"

    if lent or borrowed:
        text += (
            f"\n\n🤝 <b>Долги:</b>\n"
            f"📤 Мне должны: <b>{lent:.2f} ₽</b>\n"
            f"📥 Я должен: <b>{borrowed:.2f} ₽</b>\n"
        )
        if include_debts:
            text += f"\n{emoji} <b>Итоговый (с долгами): {effective:.2f} ₽</b>"
        else:
            text += (f"\n{emoji} <b>С долгами было бы: {total + lent - borrowed:.2f} ₽</b>\n"
                     f"<i>Включить в ⚙️ Настройках</i>")

    mb = get_monthly_budget(call.from_user.id)
    if mb:
        spent = get_month_spent_total(call.from_user.id)
        percent = spent / mb * 100 if mb > 0 else 0
        filled = min(10, int(percent / 10))
        bar = "█" * filled + "░" * (10 - filled)
        emoji_b = "🚨" if percent > 100 else ("⚠️" if percent >= 80 else "🟢")
        text += (f"\n\n🎯 <b>Общий бюджет месяца</b>\n"
                 f"{emoji_b} {bar} {percent:.0f}%\n"
                 f"{spent:.2f} / {mb:.2f} ₽")

    await call.message.edit_text(text, parse_mode="HTML", reply_markup=main_menu())
    await call.answer()

@dp.callback_query(F.data == "stats")
async def cb_stats(call: CallbackQuery, state: FSMContext):
    await state.clear()
    rows = get_stats(call.from_user.id)
    if not rows:
        text = "📊 Пока нет расходов."
    else:
        total = sum(r[1] for r in rows)
        text = "📊 <b>Расходы по категориям:</b>\n\n"
        for cat, amount in rows:
            percent = amount / total * 100
            bar = "█" * int(percent / 5)
            text += f"<b>{cat}</b>: {amount:.2f} ₽ ({percent:.1f}%)\n{bar}\n\n"
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=main_menu())
    await call.answer()

@dp.callback_query(F.data == "history")
async def cb_history(call: CallbackQuery, state: FSMContext):
    await state.clear()
    rows = get_history(call.from_user.id)
    if not rows:
        text = "📜 История пуста."
    else:
        accounts = {a[0]: a[1] for a in get_accounts(call.from_user.id)}
        text = "📜 <b>Последние операции:</b>\n\n"
        for ttype, amount, cat, date, acc_id in rows:
            if ttype == "income":
                sign = "➕"
            elif ttype == "expense":
                sign = "➖"
            elif ttype == "transfer_in":
                sign = "🔄⬅"
            else:
                sign = "🔄➡"
            acc_name = accounts.get(acc_id, "—")
            text += f"{sign} {amount:.2f} ₽ — {cat}\n"
            text += f"<i>{date} · {acc_name}</i>\n\n"
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=main_menu())
    await call.answer()

# ---------- Добавление операции (доход/расход) ----------
@dp.callback_query(F.data.in_({"add_income", "add_expense"}))
async def cb_add(call: CallbackQuery, state: FSMContext):
    ttype = "income" if call.data == "add_income" else "expense"
    ensure_default_accounts(call.from_user.id)
    await state.update_data(ttype=ttype)
    await state.set_state(AddOp.entering_amount)
    word = "дохода" if ttype == "income" else "расхода"
    sign = "➕" if ttype == "income" else "➖"
    await call.message.edit_text(
        f"{sign} <b>Новый {'доход' if ttype == 'income' else 'расход'}</b>\n\n"
        f"Введи сумму {word}:",
        parse_mode="HTML",
        reply_markup=after_amount_kb()
    )
    await call.answer()

@dp.message(AddOp.entering_amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи корректное положительное число.")
        return
    data = await state.get_data()
    ttype = data["ttype"]
    await state.update_data(amount=amount)
    await state.set_state(AddOp.choosing_account)
    await message.answer(
        f"💰 Сумма: <b>{amount:.2f} ₽</b>\n\nВыбери счёт:",
        parse_mode="HTML",
        reply_markup=account_picker_kb(message.from_user.id, "tx_acc")
    )

@dp.callback_query(F.data.startswith("tx_acc:"))
async def cb_tx_account(call: CallbackQuery, state: FSMContext):
    acc_id = int(call.data.split(":")[1])
    data = await state.get_data()
    ttype = data.get("ttype")
    amount = data.get("amount")
    if amount is None:
        await call.answer("⚠️ Сначала введи сумму", show_alert=True)
        return
    await state.update_data(account_id=acc_id)
    acc = get_account(acc_id)
    acc_name = acc[2] if acc else "—"
    await call.message.edit_text(
        f"💰 <b>{amount:.2f} ₽</b>\n"
        f"🏦 Счёт: <b>{acc_name}</b>\n\nВыбери категорию:",
        parse_mode="HTML",
        reply_markup=categories_kb(call.from_user.id, ttype)
    )
    await call.answer()

@dp.callback_query(F.data.startswith("cat:"))
async def cb_category(call: CallbackQuery, state: FSMContext):
    _, ttype, category = call.data.split(":", 2)
    data = await state.get_data()
    amount = data.get("amount")
    acc_id = data.get("account_id")
    if amount is None or acc_id is None:
        await call.answer("⚠️ Данные потеряны, начни заново", show_alert=True)
        await state.clear()
        return
    add_transaction(call.from_user.id, acc_id, ttype, amount, category)
    await state.clear()

    acc = get_account(acc_id)
    acc_name = acc[2] if acc else "—"
    sign = "➕" if ttype == "income" else "➖"
    text = (f"✅ <b>Записано!</b>\n\n"
            f"{sign} {amount:.2f} ₽ — <b>{category}</b>\n"
            f"🏦 {acc_name}")

    if ttype == "expense":
        warning = check_budgets_after_add(call.from_user.id, category)
        if warning:
            text += f"\n\n{warning}"

    total = get_total_balance(call.from_user.id)
    text += f"\n\n💰 Общий баланс: <b>{total:.2f} ₽</b>"
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=main_menu())
    await call.answer("Сохранено!")

@dp.callback_query(F.data == "repeat_last")
async def cb_repeat_last(call: CallbackQuery, state: FSMContext):
    await state.clear()
    last = get_last_transaction(call.from_user.id)
    if not last:
        await call.answer("Пока нет операций для повтора", show_alert=True)
        return
    ttype, amount, category, acc_id = last
    if ttype in ("transfer_in", "transfer_out"):
        await call.answer("Переводы не повторяются", show_alert=True)
        return
    if not acc_id:
        acc_id = ensure_default_accounts(call.from_user.id)
    add_transaction(call.from_user.id, acc_id, ttype, amount, category)
    acc = get_account(acc_id)
    acc_name = acc[2] if acc else "—"
    sign = "➕" if ttype == "income" else "➖"
    text = (f"⭐ <b>Повторено!</b>\n\n"
            f"{sign} {amount:.2f} ₽ — <b>{category}</b>\n"
            f"🏦 {acc_name}")
    if ttype == "expense":
        warning = check_budgets_after_add(call.from_user.id, category)
        if warning:
            text += f"\n\n{warning}"
    total = get_total_balance(call.from_user.id)
    text += f"\n\n💰 Общий баланс: <b>{total:.2f} ₽</b>"
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=main_menu())
    await call.answer("Сохранено!")

# ---------- Переводы между счетами ----------
@dp.callback_query(F.data == "transfer")
async def cb_transfer(call: CallbackQuery, state: FSMContext):
    await state.clear()
    ensure_default_accounts(call.from_user.id)
    await state.set_state(Transfer.choosing_from)
    await call.message.edit_text(
        "🔄 <b>Перевод между счетами</b>\n\nОткуда списать?",
        parse_mode="HTML",
        reply_markup=account_picker_kb(call.from_user.id, "tr_from")
    )
    await call.answer()

@dp.callback_query(F.data.startswith("tr_from:"))
async def cb_transfer_from(call: CallbackQuery, state: FSMContext):
    acc_id = int(call.data.split(":")[1])
    await state.update_data(from_acc=acc_id)
    await state.set_state(Transfer.choosing_to)
    await call.message.edit_text(
        "🔄 Куда зачислить?",
        reply_markup=account_picker_kb(call.from_user.id, "tr_to")
    )
    await call.answer()

@dp.callback_query(F.data.startswith("tr_to:"))
async def cb_transfer_to(call: CallbackQuery, state: FSMContext):
    acc_id = int(call.data.split(":")[1])
    data = await state.get_data()
    from_acc = data.get("from_acc")
    if from_acc == acc_id:
        await call.answer("Нельзя перевести на тот же счёт", show_alert=True)
        return
    await state.update_data(to_acc=acc_id)
    await state.set_state(Transfer.entering_amount)
    from_a = get_account(from_acc)
    to_a = get_account(acc_id)
    await call.message.edit_text(
        f"🔄 <b>Перевод</b>\n\n"
        f"Откуда: <b>{from_a[2] if from_a else '—'}</b>\n"
        f"Куда: <b>{to_a[2] if to_a else '—'}</b>\n\n"
        f"Введи сумму перевода:",
        parse_mode="HTML",
        reply_markup=after_amount_kb()
    )
    await call.answer()

@dp.message(Transfer.entering_amount)
async def process_transfer_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи положительное число.")
        return
    data = await state.get_data()
    from_acc = data["from_acc"]
    to_acc = data["to_acc"]
    user_id = message.from_user.id

    add_transaction(user_id, from_acc, "transfer_out", amount, "Перевод")
    add_transaction(user_id, to_acc, "transfer_in", amount, "Перевод")
    await state.clear()

    from_a = get_account(from_acc)
    to_a = get_account(to_acc)
    total = get_total_balance(user_id)
    await message.answer(
        f"✅ <b>Перевод выполнен!</b>\n\n"
        f"🔄 {amount:.2f} ₽\n"
        f"Из: <b>{from_a[2] if from_a else '—'}</b>\n"
        f"В: <b>{to_a[2] if to_a else '—'}</b>\n\n"
        f"💰 Общий баланс: <b>{total:.2f} ₽</b>",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# ---------- Корректировка ----------
@dp.callback_query(F.data == "adjust_balance")
async def cb_adjust(call: CallbackQuery, state: FSMContext):
    await state.clear()
    ensure_default_accounts(call.from_user.id)
    total = get_total_balance(call.from_user.id)
    await state.set_state(AdjustBalance.entering_amount)
    await call.message.edit_text(
        f"✏️ <b>Корректировка баланса</b>\n\n"
        f"Общий баланс: <b>{total:.2f} ₽</b>\n\n"
        f"Введи <b>фактическую</b> сумму, которая должна быть на счету,\n"
        f"к которому будем применять корректировку.",
        parse_mode="HTML",
        reply_markup=after_amount_kb()
    )
    await call.answer()

@dp.message(AdjustBalance.entering_amount)
async def process_adjust_amount(message: Message, state: FSMContext):
    try:
        target = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("❌ Введи корректное число.")
        return
    await state.update_data(target=target)
    await state.set_state(AdjustBalance.choosing_account)
    await message.answer(
        f"К какому счёту применить корректировку до <b>{target:.2f} ₽</b>?",
        parse_mode="HTML",
        reply_markup=account_picker_kb(message.from_user.id, "adj_acc")
    )

@dp.callback_query(F.data.startswith("adj_acc:"))
async def cb_adjust_account(call: CallbackQuery, state: FSMContext):
    acc_id = int(call.data.split(":")[1])
    data = await state.get_data()
    target = data.get("target")
    if target is None:
        await call.answer("Ошибка", show_alert=True)
        return
    current = get_account_balance(call.from_user.id, acc_id)
    diff = target - current
    await state.update_data(account_id=acc_id, diff=diff, current=current)
    await state.set_state(AdjustBalance.confirming)
    acc = get_account(acc_id)
    acc_name = acc[2] if acc else "—"

    if abs(diff) < 0.01:
        await state.clear()
        await call.message.edit_text(
            f"✅ Баланс счёта <b>{acc_name}</b> уже совпадает с {target:.2f} ₽.",
            parse_mode="HTML",
            reply_markup=main_menu()
        )
        await call.answer()
        return

    sign = "➕" if diff > 0 else "➖"
    action = "доход" if diff > 0 else "расход"
    await call.message.edit_text(
        f"✏️ <b>Проверь корректировку</b>\n\n"
        f"🏦 Счёт: <b>{acc_name}</b>\n"
        f"Текущий: <b>{current:.2f} ₽</b>\n"
        f"Целевой: <b>{target:.2f} ₽</b>\n"
        f"Разница: {sign} <b>{abs(diff):.2f} ₽</b>\n\n"
        f"Будет создан <i>{action}</i> на <b>{abs(diff):.2f} ₽</b>.",
        parse_mode="HTML",
        reply_markup=adjust_confirm_kb()
    )
    await call.answer()

@dp.callback_query(F.data == "adjust_yes")
async def cb_adjust_yes(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    diff = data.get("diff")
    acc_id = data.get("account_id")
    if diff is None or acc_id is None:
        await call.answer("Нет данных", show_alert=True)
        return
    ttype = "income" if diff > 0 else "expense"
    add_transaction(call.from_user.id, acc_id, ttype, abs(diff), "Корректировка")
    await state.clear()
    total = get_total_balance(call.from_user.id)
    await call.message.edit_text(
        f"✅ <b>Скорректировано!</b>\n\n"
        f"💰 Общий баланс: <b>{total:.2f} ₽</b>",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
    await call.answer("Готово")

# ---------- Долги ----------
@dp.callback_query(F.data == "debts_menu")
async def cb_debts_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    debts = get_active_debts(call.from_user.id)
    lent = sum(d[3] for d in debts if d[1] == "lent")
    borrowed = sum(d[3] for d in debts if d[1] == "borrowed")
    await call.message.edit_text(
        f"🤝 <b>Долги</b>\n\n"
        f"📤 Мне должны: <b>{lent:.2f} ₽</b>\n"
        f"📥 Я должен: <b>{borrowed:.2f} ₽</b>\n"
        f"⚖️ Итого: <b>{lent - borrowed:+.2f} ₽</b>",
        parse_mode="HTML", reply_markup=debts_menu_kb()
    )
    await call.answer()

@dp.callback_query(F.data == "debts_list")
async def cb_debts_list(call: CallbackQuery, state: FSMContext):
    debts = get_active_debts(call.from_user.id)
    if not debts:
        await call.message.edit_text("📋 Активных долгов нет.", reply_markup=debts_menu_kb())
        await call.answer()
        return
    rows = []
    for debt_id, direction, person, amount, note, due in debts:
        emoji = "📤" if direction == "lent" else "📥"
        label = f"{emoji} {person} — {amount:.0f} ₽"
        if due:
            label += f" (до {due[5:]})"
        rows.append([InlineKeyboardButton(text=label[:60], callback_data=f"debt_view:{debt_id}")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="debts_menu")])
    await call.message.edit_text(
        "📋 <b>Активные долги</b>\nНажми на долг:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )
    await call.answer()

@dp.callback_query(F.data.startswith("debt_view:"))
async def cb_debt_view(call: CallbackQuery, state: FSMContext):
    debt_id = int(call.data.split(":")[1])
    d = get_debt(debt_id)
    if not d or d[1] != call.from_user.id:
        await call.answer("Не найдено", show_alert=True)
        return
    _, _, direction, person, amount, note, due, status = d
    emoji = "📤 Я дал в долг" if direction == "lent" else "📥 Я взял в долг"
    text = f"{emoji}\n\n👤 <b>{person}</b>\n💰 Сумма: <b>{amount:.2f} ₽</b>\n"
    if due:
        text += f"📅 Срок: <b>{due}</b>\n"
    if note:
        text += f"📝 {note}\n"
    text += f"📌 Статус: <b>{'активен' if status == 'active' else 'закрыт'}</b>"
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=debt_actions_kb(debt_id))
    await call.answer()

@dp.callback_query(F.data.startswith("debt_close:"))
async def cb_debt_close(call: CallbackQuery, state: FSMContext):
    debt_id = int(call.data.split(":")[1])
    d = get_debt(debt_id)
    if not d or d[1] != call.from_user.id:
        await call.answer("Не найдено", show_alert=True)
        return
    close_debt(debt_id)
    await call.message.edit_text("✅ Долг закрыт!", reply_markup=debts_menu_kb())
    await call.answer("Закрыт")

@dp.callback_query(F.data.startswith("debt_del:"))
async def cb_debt_del(call: CallbackQuery, state: FSMContext):
    debt_id = int(call.data.split(":")[1])
    d = get_debt(debt_id)
    if not d or d[1] != call.from_user.id:
        await call.answer("Не найдено", show_alert=True)
        return
    delete_debt(debt_id)
    await call.message.edit_text("🗑 Долг удалён.", reply_markup=debts_menu_kb())
    await call.answer("Удалён")

@dp.callback_query(F.data == "debt_add")
async def cb_debt_add(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("🤝 <b>Новый долг</b>\n\nВыбери направление:",
                                 parse_mode="HTML", reply_markup=debt_direction_kb())
    await call.answer()

@dp.callback_query(F.data.startswith("debt_dir:"))
async def cb_debt_dir(call: CallbackQuery, state: FSMContext):
    direction = call.data.split(":")[1]
    await state.update_data(direction=direction)
    await state.set_state(NewDebt.entering_person)
    word = "кому дал" if direction == "lent" else "у кого взял"
    await call.message.edit_text(f"👤 Введи имя/контакт ({word}):")
    await call.answer()

@dp.message(NewDebt.entering_person)
async def process_debt_person(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name or len(name) > 50:
        await message.answer("❌ Некорректное имя.")
        return
    await state.update_data(person=name)
    await state.set_state(NewDebt.entering_amount)
    await message.answer("💰 Введи сумму долга:")

@dp.message(NewDebt.entering_amount)
async def process_debt_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи положительное число.")
        return
    await state.update_data(amount=amount)
    await state.set_state(NewDebt.entering_note)
    await message.answer("📝 Добавь заметку:", reply_markup=debt_note_kb())

@dp.callback_query(F.data == "debt_note_skip")
async def cb_debt_note_skip(call: CallbackQuery, state: FSMContext):
    await state.update_data(note="")
    await state.set_state(NewDebt.entering_due)
    await call.message.edit_text("📅 Когда нужно вернуть/забрать?", reply_markup=debt_due_kb())
    await call.answer()

@dp.message(NewDebt.entering_note)
async def process_debt_note(message: Message, state: FSMContext):
    await state.update_data(note=message.text.strip()[:200])
    await state.set_state(NewDebt.entering_due)
    await message.answer("📅 Когда нужно вернуть/забрать?", reply_markup=debt_due_kb())

@dp.callback_query(F.data.startswith("debt_due:"))
async def cb_debt_due(call: CallbackQuery, state: FSMContext):
    val = call.data.split(":")[1]
    due_date = None if val == "none" else (
        datetime.now() + timedelta(days=int(val))
    ).strftime("%Y-%m-%d")
    data = await state.get_data()
    add_debt(call.from_user.id, data["direction"], data["person"],
             data["amount"], data.get("note", ""), due_date)
    await state.clear()
    emoji = "📤" if data["direction"] == "lent" else "📥"
    due_str = f"\n📅 Срок: <b>{due_date}</b>" if due_date else ""
    await call.message.edit_text(
        f"✅ <b>Долг записан!</b>\n\n"
        f"{emoji} <b>{data['person']}</b> — <b>{data['amount']:.2f} ₽</b>{due_str}",
        parse_mode="HTML", reply_markup=debts_menu_kb()
    )
    await call.answer("Сохранено")

# ---------- Графики ----------
def _month_range(n=6):
    now = datetime.now()
    months = []
    y, m = now.year, now.month
    for _ in range(n):
        months.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return list(reversed(months))

def _get_monthly_expenses(user_id, months):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    result = {m: 0 for m in months}
    cur.execute("""
        SELECT substr(date, 1, 7) AS ym, SUM(amount)
        FROM transactions WHERE user_id=? AND type='expense' GROUP BY ym
    """, (user_id,))
    for ym, total in cur.fetchall():
        if ym in result:
            result[ym] = total
    conn.close()
    return result

def _get_monthly_income_expense(user_id, months):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    inc = {m: 0 for m in months}
    exp = {m: 0 for m in months}
    cur.execute("""
        SELECT substr(date, 1, 7) AS ym, type, SUM(amount)
        FROM transactions WHERE user_id=? GROUP BY ym, type
    """, (user_id,))
    for ym, ttype, total in cur.fetchall():
        if ym not in inc:
            continue
        if ttype == "income":
            inc[ym] = total
        elif ttype == "expense":
            exp[ym] = total
    conn.close()
    return inc, exp

def _plot_monthly_expenses(user_id, path):
    months = _month_range(6)
    data = _get_monthly_expenses(user_id, months)
    labels = [f"{m[5:]}.{m[2:4]}" for m in months]
    values = [data[m] for m in months]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color="#4A90D9")
    ax.set_title("Расходы по месяцам", fontsize=14, fontweight="bold")
    ax.set_ylabel("₽")
    ax.grid(axis="y", alpha=0.3)
    for b, v in zip(bars, values):
        if v > 0:
            ax.text(b.get_x() + b.get_width()/2, v, f"{v:.0f}",
                    ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)

def _plot_income_vs_expense(user_id, path):
    months = _month_range(6)
    inc, exp = _get_monthly_income_expense(user_id, months)
    labels = [f"{m[5:]}.{m[2:4]}" for m in months]
    inc_v = [inc[m] for m in months]
    exp_v = [exp[m] for m in months]
    x = range(len(labels))
    w = 0.4
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - w/2 for i in x], inc_v, w, label="Доходы", color="#3FBF6F")
    ax.bar([i + w/2 for i in x], exp_v, w, label="Расходы", color="#E4572E")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_title("Доходы vs Расходы", fontsize=14, fontweight="bold")
    ax.set_ylabel("₽")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)

def _plot_top_categories(user_id, path):
    month_start = datetime.now().strftime("%Y-%m-01")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT category, SUM(amount) FROM transactions
        WHERE user_id=? AND type='expense' AND date >= ?
        GROUP BY category ORDER BY SUM(amount) DESC LIMIT 8
    """, (user_id, month_start))
    rows = cur.fetchall()
    conn.close()
    fig, ax = plt.subplots(figsize=(8, 5))
    if not rows:
        ax.text(0.5, 0.5, "Нет расходов в этом месяце",
                ha="center", va="center", fontsize=14)
        ax.axis("off")
    else:
        cats = [r[0] for r in rows]
        vals = [r[1] for r in rows]
        colors = plt.cm.Set3(range(len(cats)))
        ax.pie(vals, labels=cats, autopct="%1.1f%%", colors=colors,
               startangle=90, textprops={"fontsize": 10})
        ax.set_title("Топ категорий расходов за месяц",
                     fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)

@dp.callback_query(F.data == "chart_menu")
async def cb_chart_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("📈 <b>Графики</b>\n\nВыбери тип:",
                                 parse_mode="HTML", reply_markup=chart_menu_kb())
    await call.answer()

@dp.callback_query(F.data.startswith("chart_"))
async def cb_chart(call: CallbackQuery, state: FSMContext):
    kind = call.data
    path = f"chart_{call.from_user.id}.png"
    try:
        if kind == "chart_expenses_monthly":
            _plot_monthly_expenses(call.from_user.id, path)
            caption = "📊 Расходы по месяцам (6 мес)"
        elif kind == "chart_income_vs_expense":
            _plot_income_vs_expense(call.from_user.id, path)
            caption = "📈 Доходы vs Расходы (6 мес)"
        elif kind == "chart_top_cats":
            _plot_top_categories(call.from_user.id, path)
            caption = "🥧 Топ категорий за месяц"
        else:
            await call.answer("Неизвестный тип", show_alert=True)
            return
        await call.message.answer_photo(FSInputFile(path), caption=caption)
    except Exception as e:
        await call.answer(f"Ошибка: {e}", show_alert=True)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
    await call.answer()

# ============ НАСТРОЙКИ ============
@dp.callback_query(F.data == "settings_menu")
async def cb_settings_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    hour, minute, include_debts = get_user_settings(call.from_user.id)
    await call.message.edit_text(
        f"⚙️ <b>Настройки</b>\n\n"
        f"⏰ Время уведомлений: <b>{hour:02d}:{minute:02d}</b>\n"
        f"🔄 Долги в балансе: <b>{'включено' if include_debts else 'выключено'}</b>",
        parse_mode="HTML", reply_markup=settings_menu_kb(call.from_user.id)
    )
    await call.answer()

@dp.callback_query(F.data == "settings_time")
async def cb_settings_time(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "⏰ Выбери время ежедневной проверки долгов:",
        reply_markup=settings_time_kb()
    )
    await call.answer()

@dp.callback_query(F.data.startswith("settime:"))
async def cb_settime(call: CallbackQuery, state: FSMContext):
    _, h, m = call.data.split(":")
    update_user_settings(call.from_user.id, hour=int(h), minute=int(m))
    await call.message.edit_text(
        f"✅ Время: <b>{int(h):02d}:{int(m):02d}</b>",
        parse_mode="HTML", reply_markup=settings_menu_kb(call.from_user.id)
    )
    await call.answer("Сохранено")

@dp.callback_query(F.data == "settings_custom_time")
async def cb_settings_custom_time(call: CallbackQuery, state: FSMContext):
    await state.set_state(NotifySettings.entering_hour)
    await call.message.edit_text(
        "Введи час (0-23):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ])
    )
    await call.answer()

@dp.message(NotifySettings.entering_hour)
async def process_hour(message: Message, state: FSMContext):
    try:
        h = int(message.text.strip())
        if not 0 <= h <= 23:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи число от 0 до 23.")
        return
    await state.update_data(hour=h)
    await state.set_state(NotifySettings.entering_minute)
    await message.answer("Введи минуты (0-59):")

@dp.message(NotifySettings.entering_minute)
async def process_minute(message: Message, state: FSMContext):
    try:
        m = int(message.text.strip())
        if not 0 <= m <= 59:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи число от 0 до 59.")
        return
    data = await state.get_data()
    update_user_settings(message.from_user.id, hour=data["hour"], minute=m)
    await state.clear()
    await message.answer(
        f"✅ Время: <b>{data['hour']:02d}:{m:02d}</b>",
        parse_mode="HTML", reply_markup=main_menu()
    )

@dp.callback_query(F.data == "settings_toggle_debts")
async def cb_toggle_debts(call: CallbackQuery, state: FSMContext):
    _, _, include_debts = get_user_settings(call.from_user.id)
    update_user_settings(call.from_user.id, include_debts=not include_debts)
    await cb_settings_menu(call, state)

# ---------- Категории ----------
@dp.callback_query(F.data == "manage_cats")
async def cb_manage_cats(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("🏷 <b>Управление категориями</b>",
                                 parse_mode="HTML", reply_markup=manage_cats_kb())
    await call.answer()

@dp.callback_query(F.data == "cat_add")
async def cb_cat_add(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Куда добавить?", reply_markup=cat_type_kb("newcat_type"))
    await call.answer()

@dp.callback_query(F.data.startswith("newcat_type:"))
async def cb_newcat_type(call: CallbackQuery, state: FSMContext):
    ttype = call.data.split(":")[1]
    await state.update_data(newcat_type=ttype)
    await state.set_state(NewCategory.entering_name)
    word = "дохода" if ttype == "income" else "расхода"
    await call.message.edit_text(f"Введи название новой категории для {word}:")
    await call.answer()

@dp.message(NewCategory.entering_name)
async def process_newcat_name(message: Message, state: FSMContext):
    data = await state.get_data()
    ttype = data["newcat_type"]
    name = message.text.strip()
    if not name or len(name) > 30:
        await message.answer("❌ Некорректное название.")
        return
    added = add_user_category(message.from_user.id, ttype, name)
    await state.clear()
    msg = f"✅ Категория <b>{name}</b> добавлена!" if added else "⚠️ Уже существует."
    await message.answer(msg, parse_mode="HTML", reply_markup=main_menu())

@dp.callback_query(F.data == "cat_del")
async def cb_cat_del(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Из какого списка удалить?",
                                 reply_markup=cat_type_kb("delcat_type"))
    await call.answer()

@dp.callback_query(F.data.startswith("delcat_type:"))
async def cb_delcat_type(call: CallbackQuery, state: FSMContext):
    ttype = call.data.split(":")[1]
    kb = del_cat_list_kb(call.from_user.id, ttype)
    if not kb:
        await call.message.edit_text("Нет пользовательских категорий.",
                                     reply_markup=manage_cats_kb())
        await call.answer()
        return
    await call.message.edit_text("Выбери категорию:", reply_markup=kb)
    await call.answer()

@dp.callback_query(F.data.startswith("delcat:"))
async def cb_delcat(call: CallbackQuery, state: FSMContext):
    _, ttype, name = call.data.split(":", 2)
    ok = delete_user_category(call.from_user.id, ttype, name)
    if ok:
        await call.message.edit_text(f"🗑 <b>{name}</b> удалена.",
                                     parse_mode="HTML", reply_markup=manage_cats_kb())
        await call.answer("Удалено")
    else:
        await call.answer("Не удалось", show_alert=True)

# ---------- Бюджеты ----------
@dp.callback_query(F.data == "budgets_menu")
async def cb_budgets_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        "🎯 <b>Бюджеты</b>\n\n"
        "Можно установить лимиты по категориям и общий лимит на месяц.",
        parse_mode="HTML", reply_markup=budgets_menu_kb()
    )
    await call.answer()

@dp.callback_query(F.data == "budgets_list")
async def cb_budgets_list(call: CallbackQuery, state: FSMContext):
    budgets = get_budgets(call.from_user.id)
    mb = get_monthly_budget(call.from_user.id)
    month_name = calendar.month_name[datetime.now().month]
    text = f"📋 <b>Бюджеты ({month_name})</b>\n\n"

    if mb:
        spent_total = get_month_spent_total(call.from_user.id)
        pct = (spent_total / mb * 100) if mb > 0 else 0
        filled = min(10, int(pct / 10))
        bar = "█" * filled + "░" * (10 - filled)
        emoji = "🚨" if pct > 100 else ("⚠️" if pct >= 80 else "🟢")
        text += (f"🎯 <b>ОБЩИЙ БЮДЖЕТ</b>\n"
                 f"{emoji} {bar} {pct:.0f}%\n"
                 f"{spent_total:.0f} / {mb:.0f} ₽\n\n")

    if not budgets:
        if not mb:
            text += "Пока нет ни одного бюджета."
    else:
        text += "📂 <b>По категориям:</b>\n\n"
        for cat, amount in budgets:
            spent = get_month_spent(call.from_user.id, cat)
            percent = (spent / amount * 100) if amount > 0 else 0
            filled = min(10, int(percent / 10))
            bar = "█" * filled + "░" * (10 - filled)
            emoji = "🚨" if percent > 100 else ("⚠️" if percent >= 80 else "🟢")
            text += (f"{emoji} <b>{cat}</b>\n{bar} {percent:.0f}%\n"
                     f"{spent:.0f} / {amount:.0f} ₽\n\n")
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=budgets_menu_kb())
    await call.answer()

@dp.callback_query(F.data == "budget_add")
async def cb_budget_add(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "🎯 Выбери категорию для бюджета:",
        reply_markup=budget_cats_kb(call.from_user.id)
    )
    await call.answer()

@dp.callback_query(F.data.startswith("budget_cat:"))
async def cb_budget_cat(call: CallbackQuery, state: FSMContext):
    category = call.data.split(":", 1)[1]
    await state.update_data(budget_cat=category)
    await state.set_state(NewBudget.entering_amount)
    existing = get_budget(call.from_user.id, category)
    extra = f"\n<i>Текущий: {existing:.2f} ₽</i>" if existing else ""
    await call.message.edit_text(
        f"💰 Введи лимит на месяц для <b>{category}</b>:{extra}",
        parse_mode="HTML"
    )
    await call.answer()

@dp.message(NewBudget.entering_amount)
async def process_budget_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи положительное число.")
        return
    data = await state.get_data()
    category = data["budget_cat"]
    set_budget(message.from_user.id, category, amount)
    await state.clear()
    await message.answer(
        f"✅ Бюджет на <b>{category}</b>: <b>{amount:.2f} ₽/мес</b>",
        parse_mode="HTML", reply_markup=budgets_menu_kb()
    )

@dp.callback_query(F.data == "budget_del")
async def cb_budget_del(call: CallbackQuery, state: FSMContext):
    kb = budget_del_kb(call.from_user.id)
    if not kb:
        await call.message.edit_text("Нет бюджетов.", reply_markup=budgets_menu_kb())
        await call.answer()
        return
    await call.message.edit_text("Выбери для удаления:", reply_markup=kb)
    await call.answer()

@dp.callback_query(F.data.startswith("budget_del_do:"))
async def cb_budget_del_do(call: CallbackQuery, state: FSMContext):
    category = call.data.split(":", 1)[1]
    delete_budget(call.from_user.id, category)
    await call.message.edit_text(
        f"🗑 Бюджет на <b>{category}</b> удалён.",
        parse_mode="HTML", reply_markup=budgets_menu_kb()
    )
    await call.answer("Удалено")

@dp.callback_query(F.data == "monthly_budget_menu")
async def cb_monthly_budget_menu(call: CallbackQuery, state: FSMContext):
    amount = get_monthly_budget(call.from_user.id)
    if amount:
        spent = get_month_spent_total(call.from_user.id)
        pct = (spent / amount * 100) if amount > 0 else 0
        text = (f"🎯 <b>Общий бюджет месяца</b>\n\n"
                f"Лимит: <b>{amount:.2f} ₽</b>\n"
                f"Потрачено: <b>{spent:.2f} ₽</b>\n"
                f"Осталось: <b>{amount - spent:.2f} ₽</b>\n"
                f"Использовано: <b>{pct:.0f}%</b>")
    else:
        text = "🎯 <b>Общий бюджет месяца</b>\n\nБюджет не установлен."
    await call.message.edit_text(text, parse_mode="HTML",
                                 reply_markup=monthly_budget_kb(call.from_user.id))
    await call.answer()

@dp.callback_query(F.data == "monthly_budget_set")
async def cb_monthly_budget_set(call: CallbackQuery, state: FSMContext):
    await state.set_state(NewMonthlyBudget.entering_amount)
    existing = get_monthly_budget(call.from_user.id)
    extra = f"\n<i>Текущий: {existing:.2f} ₽</i>" if existing else ""
    await call.message.edit_text(
        f"💰 Введи общий лимит на месяц:{extra}",
        parse_mode="HTML"
    )
    await call.answer()

@dp.message(NewMonthlyBudget.entering_amount)
async def process_monthly_budget_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи положительное число.")
        return
    set_monthly_budget(message.from_user.id, amount)
    await state.clear()
    await message.answer(
        f"✅ Общий бюджет месяца: <b>{amount:.2f} ₽</b>",
        parse_mode="HTML", reply_markup=budgets_menu_kb()
    )

@dp.callback_query(F.data == "monthly_budget_del")
async def cb_monthly_budget_del(call: CallbackQuery, state: FSMContext):
    delete_monthly_budget(call.from_user.id)
    await call.message.edit_text("🗑 Общий бюджет удалён.",
                                 reply_markup=budgets_menu_kb())
    await call.answer("Удалено")

# ---------- Регулярные платежи ----------
@dp.callback_query(F.data == "recurring_menu")
async def cb_recurring_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    items = get_recurring(call.from_user.id)
    total_exp = sum(i[2] for i in items if i[4] == "expense")
    total_inc = sum(i[2] for i in items if i[4] == "income")
    await call.message.edit_text(
        f"🧾 <b>Регулярные платежи</b>\n\n"
        f"Активных платежей: <b>{len(items)}</b>\n"
        f"📉 Расходов в месяц: <b>{total_exp:.2f} ₽</b>\n"
        f"📈 Доходов в месяц: <b>{total_inc:.2f} ₽</b>\n\n"
        f"<i>Каждый день бот проверяет, какой платёж нужно списать сегодня.</i>",
        parse_mode="HTML", reply_markup=recurring_menu_kb()
    )
    await call.answer()

@dp.callback_query(F.data == "recurring_list")
async def cb_recurring_list(call: CallbackQuery, state: FSMContext):
    items = get_recurring(call.from_user.id, only_active=False)
    if not items:
        await call.message.edit_text("📋 Платежей пока нет.",
                                     reply_markup=recurring_menu_kb())
        await call.answer()
        return
    rows = []
    for rec in items:
        rec_id, title, amount, category, ttype, day, active, last, acc_id = rec
        emoji = "➖" if ttype == "expense" else "➕"
        status = "" if active else " ⏸"
        label = f"{emoji} {title[:15]} — {amount:.0f} ₽ ({day}ч){status}"
        rows.append([InlineKeyboardButton(text=label[:60], callback_data=f"rec_view:{rec_id}")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="recurring_menu")])
    await call.message.edit_text(
        "📋 <b>Мои платежи</b>\nНажми на платёж:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows)
    )
    await call.answer()

@dp.callback_query(F.data.startswith("rec_view:"))
async def cb_rec_view(call: CallbackQuery, state: FSMContext):
    rec_id = int(call.data.split(":")[1])
    r = get_recurring_item(rec_id)
    if not r or r[1] != call.from_user.id:
        await call.answer("Не найдено", show_alert=True)
        return
    _, _, title, amount, category, ttype, day, active, last, acc_id = r
    acc = get_account(acc_id) if acc_id else None
    acc_name = acc[2] if acc else "—"
    emoji = "➖ Расход" if ttype == "expense" else "➕ Доход"
    text = (
        f"🧾 <b>{title}</b>\n\n"
        f"{emoji}\n"
        f"💰 Сумма: <b>{amount:.2f} ₽</b>\n"
        f"🏷 Категория: <b>{category}</b>\n"
        f"🏦 Счёт: <b>{acc_name}</b>\n"
        f"📅 День месяца: <b>{day}</b>\n"
        f"📌 Статус: <b>{'активен' if active else 'приостановлен'}</b>\n"
    )
    if last:
        text += f"🕒 Последнее списание: <b>{last}</b>"
    await call.message.edit_text(text, parse_mode="HTML",
                                 reply_markup=recurring_actions_kb(rec_id, active))
    await call.answer()

@dp.callback_query(F.data.startswith("rec_toggle:"))
async def cb_rec_toggle(call: CallbackQuery, state: FSMContext):
    rec_id = int(call.data.split(":")[1])
    r = get_recurring_item(rec_id)
    if not r or r[1] != call.from_user.id:
        await call.answer("Не найдено", show_alert=True)
        return
    toggle_recurring(rec_id)
    await cb_rec_view(call, state)

@dp.callback_query(F.data.startswith("rec_del:"))
async def cb_rec_del(call: CallbackQuery, state: FSMContext):
    rec_id = int(call.data.split(":")[1])
    r = get_recurring_item(rec_id)
    if not r or r[1] != call.from_user.id:
        await call.answer("Не найдено", show_alert=True)
        return
    delete_recurring(rec_id)
    await call.message.edit_text("🗑 Платёж удалён.", reply_markup=recurring_menu_kb())
    await call.answer("Удалён")

@dp.callback_query(F.data == "recurring_add")
async def cb_recurring_add(call: CallbackQuery, state: FSMContext):
    await state.clear()
    ensure_default_accounts(call.from_user.id)
    await state.set_state(NewRecurring.entering_title)
    await call.message.edit_text(
        "🧾 <b>Новый платёж</b>\n\nШаг 1/6: Введи название:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ])
    )
    await call.answer()

@dp.message(NewRecurring.entering_title)
async def process_rec_title(message: Message, state: FSMContext):
    title = message.text.strip()
    if not title or len(title) > 40:
        await message.answer("❌ Некорректное название (до 40 символов).")
        return
    await state.update_data(rec_title=title)
    await state.set_state(NewRecurring.entering_amount)
    await message.answer("Шаг 2/6: Введи сумму:")

@dp.message(NewRecurring.entering_amount)
async def process_rec_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи положительное число.")
        return
    await state.update_data(rec_amount=amount)
    await state.set_state(NewRecurring.choosing_type)
    await message.answer("Шаг 3/6: Тип платежа:", reply_markup=recurring_type_kb())

@dp.callback_query(F.data.startswith("rec_type:"))
async def cb_rec_type(call: CallbackQuery, state: FSMContext):
    ttype = call.data.split(":")[1]
    await state.update_data(rec_type=ttype)
    await state.set_state(NewRecurring.choosing_category)
    await call.message.edit_text(
        "Шаг 4/6: Категория:",
        reply_markup=categories_kb_rec(call.from_user.id, ttype)
    )
    await call.answer()

@dp.callback_query(F.data.startswith("rec_cat:"))
async def cb_rec_cat(call: CallbackQuery, state: FSMContext):
    category = call.data.split(":", 1)[1]
    await state.update_data(rec_category=category)
    await state.set_state(NewRecurring.choosing_account)
    await call.message.edit_text(
        "Шаг 5/6: Счёт, с которого списывать:",
        reply_markup=account_picker_kb(call.from_user.id, "rec_acc")
    )
    await call.answer()

@dp.callback_query(F.data.startswith("rec_acc:"))
async def cb_rec_acc(call: CallbackQuery, state: FSMContext):
    acc_id = int(call.data.split(":")[1])
    await state.update_data(rec_account=acc_id)
    await state.set_state(NewRecurring.entering_day)
    await call.message.edit_text(
        "Шаг 6/6: День месяца для списания:",
        reply_markup=recurring_day_kb()
    )
    await call.answer()

@dp.callback_query(F.data.startswith("rec_day:"))
async def cb_rec_day(call: CallbackQuery, state: FSMContext):
    day = int(call.data.split(":")[1])
    await _finish_recurring(call, state, day)

@dp.callback_query(F.data == "rec_custom_day")
async def cb_rec_custom_day(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Введи день месяца (1-31):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ])
    )
    await call.answer()

@dp.message(NewRecurring.entering_day)
async def process_rec_day(message: Message, state: FSMContext):
    try:
        day = int(message.text.strip())
        if not 1 <= day <= 31:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи число от 1 до 31.")
        return
    await _finish_recurring_msg(message, state, day)

async def _finish_recurring(call: CallbackQuery, state: FSMContext, day: int):
    data = await state.get_data()
    add_recurring(call.from_user.id, data["rec_title"], data["rec_amount"],
                  data["rec_category"], data["rec_type"], data["rec_account"], day)
    await state.clear()
    emoji = "➖" if data["rec_type"] == "expense" else "➕"
    await call.message.edit_text(
        f"✅ <b>Платёж добавлен!</b>\n\n"
        f"🧾 {data['rec_title']}\n"
        f"{emoji} {data['rec_amount']:.2f} ₽ ({data['rec_category']})\n"
        f"📅 {day}-е число каждого месяца",
        parse_mode="HTML", reply_markup=recurring_menu_kb()
    )
    await call.answer("Сохранено")

async def _finish_recurring_msg(message: Message, state: FSMContext, day: int):
    data = await state.get_data()
    add_recurring(message.from_user.id, data["rec_title"], data["rec_amount"],
                  data["rec_category"], data["rec_type"], data["rec_account"], day)
    await state.clear()
    emoji = "➖" if data["rec_type"] == "expense" else "➕"
    await message.answer(
        f"✅ <b>Платёж добавлен!</b>\n\n"
        f"🧾 {data['rec_title']}\n"
        f"{emoji} {data['rec_amount']:.2f} ₽ ({data['rec_category']})\n"
        f"📅 {day}-е число каждого месяца",
        parse_mode="HTML", reply_markup=recurring_menu_kb()
    )

# ---------- Экспорт ----------
@dp.callback_query(F.data == "export_excel")
async def cb_export(call: CallbackQuery, state: FSMContext):
    await state.clear()
    rows = get_all_transactions(call.from_user.id)
    if not rows:
        await call.answer("Нет данных", show_alert=True)
        return
    accounts = {a[0]: a[1] for a in get_accounts(call.from_user.id)}

    wb = Workbook()
    ws = wb.active
    ws.title = "Операции"
    ws.append(["Дата", "Тип", "Сумма (₽)", "Категория", "Счёт", "Заметка"])
    for c in ws[1]:
        c.font = c.font.copy(bold=True)
    for ttype, amount, cat, date, acc_id, note in rows:
        type_str = {"income": "Доход", "expense": "Расход",
                    "transfer_in": "Перевод (вход)",
                    "transfer_out": "Перевод (выход)"}.get(ttype, ttype)
        ws.append([date, type_str, amount, cat,
                   accounts.get(acc_id, "—"), note or ""])
    for col in ws.columns:
        max_len = max((len(str(c.value)) for c in col if c.value), default=10)
        ws.column_dimensions[col[0].column_letter].width = max_len + 3

    ws2 = wb.create_sheet("Счета")
    ws2.append(["Счёт", "Тип", "Баланс (₽)"])
    for c in ws2[1]:
        c.font = c.font.copy(bold=True)
    items, total = get_accounts_with_balances(call.from_user.id)
    for acc_id, name, kind, bal in items:
        ws2.append([name, {"card": "Карта", "cash": "Наличные"}.get(kind, "Другое"), bal])
    ws2.append([])
    ws2.append(["", "Общая сумма:", total])
    for col in ws2.columns:
        max_len = max((len(str(c.value)) for c in col if c.value), default=10)
        ws2.column_dimensions[col[0].column_letter].width = max_len + 3

    ws3 = wb.create_sheet("Долги")
    ws3.append(["Направление", "Кому", "Сумма (₽)", "Заметка", "Срок", "Статус"])
    for c in ws3[1]:
        c.font = c.font.copy(bold=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""SELECT direction, person, amount, note, due_date, status
        FROM debts WHERE user_id=? ORDER BY id""", (call.from_user.id,))
    for direction, person, amount, note, due, status in cur.fetchall():
        ws3.append(["Я дал" if direction == "lent" else "Я взял",
                    person, amount, note or "", due or "",
                    "активен" if status == "active" else "закрыт"])
    conn.close()
    for col in ws3.columns:
        max_len = max((len(str(c.value)) for c in col if c.value), default=10)
        ws3.column_dimensions[col[0].column_letter].width = max_len + 3

    ws4 = wb.create_sheet("Бюджеты")
    ws4.append(["Тип", "Категория", "Лимит/мес (₽)", "Потрачено (₽)", "Остаток (₽)"])
    for c in ws4[1]:
        c.font = c.font.copy(bold=True)
    mb = get_monthly_budget(call.from_user.id)
    if mb:
        spent_total = get_month_spent_total(call.from_user.id)
        ws4.append(["Общий", "—", mb, spent_total, mb - spent_total])
    for cat, amount in get_budgets(call.from_user.id):
        spent = get_month_spent(call.from_user.id, cat)
        ws4.append(["Категория", cat, amount, spent, amount - spent])
    for col in ws4.columns:
        max_len = max((len(str(c.value)) for c in col if c.value), default=10)
        ws4.column_dimensions[col[0].column_letter].width = max_len + 3

    ws5 = wb.create_sheet("Регулярные")
    ws5.append(["Название", "Тип", "Сумма (₽)", "Категория", "Счёт", "День", "Статус"])
    for c in ws5[1]:
        c.font = c.font.copy(bold=True)
    for rec in get_recurring(call.from_user.id, only_active=False):
        rec_id, title, amount, category, ttype, day, active, last, acc_id = rec
        ws5.append([title, "Расход" if ttype == "expense" else "Доход",
                    amount, category, accounts.get(acc_id, "—"),
                    day, "активен" if active else "приостановлен"])
    for col in ws5.columns:
        max_len = max((len(str(c.value)) for c in col if c.value), default=10)
        ws5.column_dimensions[col[0].column_letter].width = max_len + 3

    ws.append([])
    income, expense, _ = get_balance(call.from_user.id)
    ws.append(["", "", "Итого доходов:", income])
    ws.append(["", "", "Итого расходов:", expense])
    ws.append(["", "", "Общий баланс:", total])

    filename = f"finance_{call.from_user.id}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    wb.save(filename)
    await call.message.answer_document(FSInputFile(filename), caption="💾 Твой экспорт")
    try:
        os.remove(filename)
    except OSError:
        pass
    await call.answer("Готово!")

# ---------- Сброс ----------
@dp.callback_query(F.data == "reset_confirm")
async def cb_reset_confirm(call: CallbackQuery, state: FSMContext):
    await state.clear()
    income, expense, _ = get_balance(call.from_user.id)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM transactions WHERE user_id=?", (call.from_user.id,))
    count = cur.fetchone()[0]
    conn.close()
    await call.message.edit_text(
        "⚠️ <b>Полный сброс</b>\n\n"
        f"Будет удалено <b>{count}</b> операций по всем счетам.\n"
        f"📈 Доходы: {income:.2f} ₽\n"
        f"📉 Расходы: {expense:.2f} ₽\n\n"
        "❗ Действие необратимо.\n"
        "Счета и категории останутся.\n"
        "Для мягкой правки используй <b>✏️ Корректировку</b>.",
        parse_mode="HTML", reply_markup=confirm_reset_kb()
    )
    await call.answer()

@dp.callback_query(F.data == "reset_yes")
async def cb_reset_yes(call: CallbackQuery, state: FSMContext):
    deleted = reset_user(call.from_user.id)
    await state.clear()
    await call.message.edit_text(
        f"🗑 <b>Сброс выполнен</b>\n\nУдалено операций: <b>{deleted}</b>",
        parse_mode="HTML", reply_markup=main_menu()
    )
    await call.answer("Сброшено")

@dp.callback_query(F.data == "reset_no")
async def cb_reset_no(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("✅ Отменено.", reply_markup=settings_menu_kb(call.from_user.id))
    await call.answer()

# ---------- Отмена ----------
@dp.callback_query(F.data == "cancel")
async def cb_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("❌ Отменено.", reply_markup=main_menu())
    await call.answer()

@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено.", reply_markup=main_menu())

# ---------- Планировщики ----------
async def check_debts_for_user(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, direction, person, amount, note, due_date
        FROM debts
        WHERE user_id=? AND status='active' AND notified=0
          AND due_date IS NOT NULL AND due_date <= ?
    """, (user_id, today))
    rows = cur.fetchall()
    conn.close()
    count = 0
    for debt_id, direction, person, amount, note, due in rows:
        if direction == "lent":
            title = "📤 <b>Пора забрать долг!</b>"
            action = f"вернуть тебе <b>{amount:.2f} ₽</b>"
        else:
            title = "📥 <b>Пора вернуть долг!</b>"
            action = f"ты должен вернуть <b>{amount:.2f} ₽</b>"
        text = f"{title}\n\n👤 <b>{person}</b>\n💰 {action}\n📅 Срок: <b>{due}</b>"
        if note:
            text += f"\n📝 {note}"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🤝 Открыть долги", callback_data="debts_menu")]
        ])
        try:
            await bot.send_message(user_id, text, parse_mode="HTML", reply_markup=kb)
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("UPDATE debts SET notified=1 WHERE id=?", (debt_id,))
            conn.commit()
            conn.close()
            count += 1
        except Exception as e:
            print(f"Не отправить user {user_id}: {e}")
    return count

async def notify_all_users():
    now = datetime.now()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id FROM user_settings
        WHERE notify_hour=? AND notify_minute=?
    """, (now.hour, now.minute))
    users = [r[0] for r in cur.fetchall()]
    conn.close()
    for uid in users:
        await check_debts_for_user(uid)

async def process_recurring_payments():
    now = datetime.now()
    if now.hour != 9:
        return
    due = get_recurring_due()
    for rec in due:
        rec_id, user_id, title, amount, category, ttype, day, last, acc_id = rec
        if not acc_id:
            acc_id = ensure_default_accounts(user_id)
        add_transaction(user_id, acc_id, ttype, amount, category)
        today_str = now.strftime("%Y-%m-%d")
        mark_recurring_charged(rec_id, today_str)

        acc = get_account(acc_id)
        acc_name = acc[2] if acc else "—"
        sign = "➕" if ttype == "income" else "➖"
        text = (f"🧾 <b>Автосписание</b>\n\n"
                f"<b>{title}</b>\n"
                f"{sign} {amount:.2f} ₽ — {category}\n"
                f"🏦 {acc_name}\n"
                f"📅 {today_str}")

        if ttype == "expense":
            warning = check_budgets_after_add(user_id, category)
            if warning:
                text += f"\n\n{warning}"

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Настройки", callback_data="recurring_menu")]
        ])
        try:
            await bot.send_message(user_id, text, parse_mode="HTML", reply_markup=kb)
        except Exception as e:
            print(f"Ошибка отправки пользователю {user_id}: {e}")

# ---------- Функция для установки вебхука ----------
async def setup_webhook(app_url: str):
    webhook_url = f"{app_url}/webhook"
    await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
    print(f"Webhook установлен на: {webhook_url}")

async def remove_webhook():
    await bot.delete_webhook()
    print("Webhook удалён.")