from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button, NumberedPager
from aiogram_dialog.widgets.text import Jinja, Const, ScrollingText, Format

from tgbot.handlers.client import (on_click_get_help, on_click_get_settings, on_click_get_subs,
                                   on_click_start_create_sub,
                                   on_click_back_to_main, get_subs)
from tgbot.states.user import UserSG

VERY_LONG_TEXT = """❓ <b>ЧаВо</b>\n
<b>1. Для чего этот бот?</b>
<i>— Бот создан, с целью напомнить пользователю, когда истечет его пробная подписка в каком-либо сервисе.</i>\n
<b>2. Какие сервисы можно добавлять?</b>
<i>— Неважно где вы оформили подписку, можно добавлять любые сервисы.</i>\n
<b>3. Как добавить сервис?</b>
<i>— Перейдите в раздел "Мои подписки" и нажмите кнопку "Добавить". Заполняйте данные, строго следуя инструкциям:
сначала введите название, следующим шагом введите кол-во. месяцев (число), затем выберите на календаре, когда 
напомнить о списании. Подтвердите правильность, и подписка будет добавлена.</i>
"""

main_menu = Dialog(
    Window(
        Jinja("<b>CONTROLLER</b> — ..."),
        Button(Const("🗂 Мои подписки"), id="subs_id", on_click=on_click_get_subs),
        Row(
            Button(Const("⚙️ Настройки"), id="settings_id", on_click=on_click_get_settings),
            Button(Const("🆘 Поддержка"), id="help_id", on_click=on_click_get_help),
        ),
        state=UserSG.MAIN,
    ),
    Window(
        ScrollingText(
            text=Jinja(VERY_LONG_TEXT),
            id="text_scroll",
            page_size=1000,
        ),
        NumberedPager(
            scroll="text_scroll",
        ),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_back_to_main),
        state=UserSG.HELP,
    ),
    Window(
        Format("🗂️ <b>Каталог активных подписок:</b>\n\n"
               "{subs}"),
        Row(
            Button(Const("Добавить"), id="add_id", on_click=on_click_start_create_sub),
            Button(Const("Удалить"), id="remove_id", on_click=on_click_get_help),
        ),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_back_to_main),
        state=UserSG.SUBS,
        getter=get_subs
    ),
    Window(
        Jinja("Settings"),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_back_to_main),
        state=UserSG.DONATE,
    ),

)
