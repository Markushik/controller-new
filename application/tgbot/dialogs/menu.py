import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button, Url, Select, Column, Group
from aiogram_dialog.widgets.text import Const, Format

from application.tgbot.dialogs.format import I18NFormat
from application.tgbot.handlers.client import (get_subs_for_output, on_click_get_subs_menu, on_click_get_settings_menu,
                                               on_click_get_help_menu, on_click_back_to_main_menu,
                                               on_click_get_delete_menu, on_click_sub_create, get_subs_for_delete,
                                               on_click_sub_selected, on_click_sub_delete, on_click_sub_not_delete,
                                               get_langs_for_output, on_click_change_lang)
from application.tgbot.states.user import UserSG

main_menu = Dialog(
    Window(
        I18NFormat("Start-menu"),
        Group(
            Button(I18NFormat("My-Subscriptions"), id="subs_id", on_click=on_click_get_subs_menu),
            Row(
                Button(I18NFormat("Settings"), id="settings_id", on_click=on_click_get_settings_menu),
                Button(I18NFormat("Support"), id="help_id", on_click=on_click_get_help_menu),
            )
        ),
        state=UserSG.MAIN,
    ),
    Window(
        I18NFormat("Q-A"),
        Group(
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
        ),
        state=UserSG.HELP
    ),
    Window(
        I18NFormat("Catalog-add"),
        Group(
            Row(
                Button(I18NFormat("Add"), id="add_id", on_click=on_click_sub_create),
                Button(I18NFormat("Delete"), id="remove_id", on_click=on_click_get_delete_menu),
            ),
            Button(I18NFormat("Back"), id="back_id", on_click=on_click_back_to_main_menu)
        ),
        state=UserSG.SUBS,
        getter=get_subs_for_output
    ),
    Window(
        I18NFormat("Catalog-remove"),
        Group(
            Column(
                Select(
                    Format("{item[1]} — {item[2]}"),
                    id="delete_id",
                    item_id_getter=operator.itemgetter(0),
                    items="subs",
                    on_click=on_click_sub_selected,
                ),
            ),
            Button(I18NFormat("Back"), id="back_id", on_click=on_click_get_subs_menu)
        ),
        state=UserSG.DELETE,
        getter=get_subs_for_delete,
    ),
    Window(
        I18NFormat("Set-lang"),
        Group(
            Row(
                Select(
                    Format("{item[1]}"),
                    id="lang_id",
                    item_id_getter=operator.itemgetter(0),
                    items="langs",
                    on_click=on_click_change_lang,
                ),
            ),
            Button(I18NFormat("Back"), id="back_id", on_click=on_click_get_subs_menu)
        ),
        state=UserSG.SETTINGS,
        getter=get_langs_for_output
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
