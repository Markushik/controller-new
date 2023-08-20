import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    Row,
    Select,
    Url,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from application.tgbot.states.user import MainMenu
from ..create_menu.getters import get_subs_for_output
from ..delete_menu.handerls import on_click_get_delete_menu
from ..edit_menu.handlers import on_click_get_edit_menu
from ..extras.i18n_format import I18NFormat
from ..main_menu.getters import get_langs_for_output
from ..main_menu.handler import (
    on_click_back_to_main_menu,
    on_click_change_lang,
    on_click_get_subs_menu,
    on_click_sub_create,
)

main_menu = Dialog(
    Window(
        I18NFormat('Start-menu'),
        Group(
            Button(
                I18NFormat('My-Subscriptions'),
                id='subs_id',
                on_click=on_click_get_subs_menu,
            ),
            Row(
                SwitchTo(
                    I18NFormat('Settings'),
                    id='settings_id',
                    state=MainMenu.SETTINGS,
                ),
                SwitchTo(
                    I18NFormat('Support'),
                    id='support_id',
                    state=MainMenu.SUPPORT,
                ),
            ),
        ),
        state=MainMenu.MAIN,
    ),
    Window(
        I18NFormat('Q-A'),
        Group(
            Row(
                Url(
                    I18NFormat('Administrator'),
                    Const('tg://user?id=878406427'),
                ),
                Url(
                    Const('🐈 GitHub'),
                    Const('https://github.com/Markushik/controller-new/'),
                ),
            ),
            Button(
                I18NFormat('Back'),
                id='back_id',
                on_click=on_click_back_to_main_menu,
            ),
        ),
        state=MainMenu.SUPPORT,
    ),
    Window(
        I18NFormat('Catalog-add'),
        Group(
            Row(
                Button(
                    I18NFormat('Add'),
                    id='add_id',
                    on_click=on_click_sub_create,
                ),
                Button(
                    I18NFormat('Change'),
                    id='change_id',
                    on_click=on_click_get_edit_menu,
                ),
                Button(
                    I18NFormat('Delete'),
                    id='remove_id',
                    on_click=on_click_get_delete_menu,
                ),
            ),
            Button(
                I18NFormat('Back'),
                id='back_id',
                on_click=on_click_back_to_main_menu,
            ),
        ),
        state=MainMenu.CONTROL,
        getter=get_subs_for_output,
    ),
    Window(
        I18NFormat('Set-lang'),
        Group(
            Row(
                Select(
                    Format('{item[1]}'),
                    id='lang_id',
                    item_id_getter=operator.itemgetter(0),
                    items='langs',
                    on_click=on_click_change_lang,
                ),
            ),
            Button(
                I18NFormat('Back'),
                id='back_id',
                on_click=on_click_back_to_main_menu,
            ),
        ),
        state=MainMenu.SETTINGS,
        getter=get_langs_for_output,
    ),
)
