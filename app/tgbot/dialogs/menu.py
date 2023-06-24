import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button, Url, Select, Column
from aiogram_dialog.widgets.text import Jinja, Const, Format

from app.tgbot.handlers.client import (get_subs_for_output, on_click_get_subs_menu, on_click_get_settings_menu,
                                       on_click_get_help_menu, on_click_back_to_main_menu, on_click_get_delete_menu,
                                       on_click_start_create_sub, get_subs_for_delete, on_click_sub_selected,
                                       on_click_sub_delete, on_click_sub_not_delete)
from app.tgbot.states.user import UserSG

main_menu = Dialog(
    Window(
        Jinja("<b>CONTROLLER</b> — <b>наверное</b>, <b>лучший способ</b>, "
              "чтобы <b>напомнить</b> об <b>истечении подписки</b>.\n\n"
              "📣 <i><b>Обязательно</b> добавляйте в наш сервис свои <b>подписки</b>. Мы\n"
              "позаботимся о <b>Вас</b>, и <b>отправим Вам</b> уведомление о ближайшем <b>списании</b></i>"),
        Button(Const("🗂️ Мои подписки"), id="subs_id", on_click=on_click_get_subs_menu),
        Row(
            Button(Const("⚙️ Настройки"), id="settings_id", on_click=on_click_get_settings_menu),
            Button(Const("🆘 Поддержка"), id="help_id", on_click=on_click_get_help_menu),
        ),
        state=UserSG.MAIN,
    ),
    Window(
        Jinja("❓ <b>ЧаВо</b>\n\n"
              "<b>1. Для чего этот бот?</b>\n"
              "<i>— Бот создан, с целью напомнить пользователю, "
              "когда истечет его подписка в каком-либо сервисе.</i>\n\n"
              "<b>2. Какие сервисы можно добавлять?</b>\n"
              "<i>— Неважно где вы оформили подписку, можно добавлять любые сервисы.</i>\n\n"
              "<b>3. Как добавить сервис?</b>\n"
              "<i>— Перейдите в раздел Мои подписки и нажмите кнопку Добавить.\t"
              "Заполняйте данные, строго следуя инструкциям:\t"
              "сначала введите название, следующим шагом введите кол-во. месяцев (число), затем выберите на календаре,\t"
              "когда напомнить о списании. Подтвердите правильность, и подписка будет добавлена.</i>"),
        Row(
            Url(
                Const("👨‍💻 Администратор"),
                Const("tg://user?id=878406427")
            ),
            Url(
                Const("🐈 GitHub"),
                Const("https://github.com/Markushik/controller-new/")
            )
        ),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_back_to_main_menu),
        state=UserSG.HELP,
        disable_web_page_preview=True
    ),
    Window(
        Format("🗂️ <b>Каталог добавленных подписок:</b>\n\n"
               "{subs}"),
        Row(
            Button(Const("Добавить"), id="add_id", on_click=on_click_start_create_sub),
            Button(Const("Удалить"), id="remove_id", on_click=on_click_get_delete_menu),
        ),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_back_to_main_menu),
        state=UserSG.SUBS,
        getter=get_subs_for_output
    ),
    Window(
        Jinja("🌍 <b>Выберите</b> язык, на котором <b>будет общаться</b> бот:"),
        Row(
            Button(Const("🇷🇺 Русский"), id="ru_lang_id"),
            Button(Const("🇬🇧 Английский"), id="en_lang_id")
        ),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_back_to_main_menu),
        state=UserSG.SETTINGS,
    ),
    Window(
        Format("{message}"),
        Column(
            Select(
                Format("{item[0]} — {item[2]}"),
                id="delete_id",
                item_id_getter=operator.itemgetter(1),
                items="subs",
                on_click=on_click_sub_selected,
            ),
        ),
        Button(Const("↩️ Назад"), id="back_id", on_click=on_click_get_subs_menu),
        state=UserSG.DELETE,
        getter=get_subs_for_delete,
    ),
    Window(
        Jinja("<b>Вы действительно</b> хотите <b>удалить</b> подписку?"),
        Row(
            Button(Const("✅"), id="confirm_delete_id", on_click=on_click_sub_delete),
            Button(Const("❎"), id="reject_delete_id", on_click=on_click_sub_not_delete),
        ),
        state=UserSG.CHECK_DELETE
    )
)
