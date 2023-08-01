from datetime import date
from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView,
    CalendarMonthView,
    CalendarScopeView,
    CalendarYearsView,
)
from aiogram_dialog.widgets.text import Text, Format
from babel.dates import get_day_names, get_month_names


class WeekDay(Text):
    async def _render_text(self, data, dialog_manager: DialogManager) -> str:
        selected_date: date = data['date']
        session = dialog_manager.middleware_data['session']
        language = await session.get_user_language(
            user_id=dialog_manager.event.from_user.id
        )
        return get_day_names(
            width='short',
            context='stand-alone',
            locale=language,
        )[selected_date.weekday()].title()


class Month(Text):
    async def _render_text(self, data, dialog_manager: DialogManager) -> str:
        selected_date: date = data['date']
        session = dialog_manager.middleware_data['session']
        language = await session.get_user_language(
            user_id=dialog_manager.event.from_user.id
        )
        return get_month_names(
            'wide',
            context='stand-alone',
            locale=language,
        )[selected_date.month].title()


class CustomCalendar(Calendar):
    def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                self.config,
                header_text=Month(),
                weekday_text=WeekDay(),
                next_month_text=Month() + ' →',
                prev_month_text='← ' + Month(),
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                self.config,
                month_text=Month(),
                header_text=Format('{date:%Y}'),
                this_month_text='[ ' + Month() + ' ]',
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
                self.config,
            ),
        }
