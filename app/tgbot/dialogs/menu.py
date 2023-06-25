import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button, Url, Select, Column
from aiogram_dialog.widgets.text import Jinja, Const, Format

from app.tgbot.dialogs.format import I18NFormat
from app.tgbot.handlers.client import (get_subs_for_output, on_click_get_subs_menu, on_click_get_settings_menu,
                                       on_click_get_help_menu, on_click_back_to_main_menu, on_click_get_delete_menu,
                                       on_click_start_create_sub, get_subs_for_delete, on_click_sub_selected,
                                       on_click_sub_delete, on_click_sub_not_delete, on_click_change_lang_to_ru,
                                       on_click_change_lang_to_en)
from app.tgbot.states.user import UserSG

main_menu = Dialog(
    Window(
        Jinja("<b>CONTROLLER</b> — <b>наверное</b>, <b>лучший способ</b>, "
              "чтобы <b>напомнить</b> об <b>истечении подписки</b>.\n\n"
              "📣 <i><b>Обязательно</b> добавляйте в наш сервис свои <b>подписки</b>. Мы\n"
              "позаботимся о <b>Вас</b>, и <b>отправим Вам</b> уведомление о ближайшем <b>списании</b></i>"),
        Button(I18NFormat("My-Subscriptions"), id="subs_id", on_click=on_click_get_subs_menu),
        Row(
            Button(I18NFormat("Settings"), id="settings_id", on_click=on_click_get_settings_menu),
            Button(I18NFormat("Support"), id="help_id", on_click=on_click_get_help_menu),
        ),
        state=UserSG.MAIN,
    ),
    Window(
        I18NFormat("Q-A"),
        Row(
            Url(
                I18NFormat("Administrator"),
                Const("tg://user?id=878406427")
            ),
            Url(
                Const("🐈 GitHub"),
                Const("https://github.com/Markushik/controller-new/")
            )
        ),
        Button(I18NFormat("Back"), id="back_id", on_click=on_click_back_to_main_menu),
        state=UserSG.HELP,
        disable_web_page_preview=True
    ),
    Window(
        I18NFormat("Catalog-add"),
        Row(
            Button(I18NFormat("Add"), id="add_id", on_click=on_click_start_create_sub),
            Button(I18NFormat("Delete"), id="remove_id", on_click=on_click_get_delete_menu),
        ),
        Button(I18NFormat("Back"), id="back_id", on_click=on_click_back_to_main_menu),
        state=UserSG.SUBS,
        getter=get_subs_for_output
    ),
    Window(
        I18NFormat("Catalog-remove"),
        Column(
            Select(
                Format("{item[0]} — {item[2]}"),
                id="delete_id",
                item_id_getter=operator.itemgetter(1),
                items="subs",
                on_click=on_click_sub_selected,
            ),
        ),
        Button(I18NFormat("Back"), id="back_id", on_click=on_click_get_subs_menu),
        state=UserSG.DELETE,
        getter=get_subs_for_delete,
    ),
    Window(
        I18NFormat("Set-lang"),
        Row(
            Button(I18NFormat("Russian"), id="ru_lang_id", on_click=on_click_change_lang_to_ru),
            Button(I18NFormat("English"), id="en_lang_id", on_click=on_click_change_lang_to_en)
        ),
        Button(I18NFormat("Back"), id="back_id", on_click=on_click_back_to_main_menu),
        state=UserSG.SETTINGS,
    ),
    Window(
        I18NFormat("Are-you-sure"),
        Row(
            Button(Const("✅"), id="confirm_delete_id", on_click=on_click_sub_delete),
            Button(Const("❎"), id="reject_delete_id", on_click=on_click_sub_not_delete),
        ),
        state=UserSG.CHECK_DELETE
    )
)
