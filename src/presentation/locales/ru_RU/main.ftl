settings = ⚙️ Настройки
support = 🆘 Поддержка
my-subscriptions = 🗂️ Мои подписки
administrator = 👨‍💻 Администратор
back = ↩️ Назад

add = Добавить
delete = Удалить
change = Изменить

title = Название
months = Месяцы
date = Дату
renew = Продлить

start-menu = <b>Subscriptions Controller</b> — <b>лучший</b> способ <b>контролировать</b> свои подписки

            📣 <b>Обязательно</b> добавляйте свои подписки в <b>наш сервис</b>, чтобы получать <b>уведомления</b> о ближайшем списании

select-lang = 🌍 <b>Выберите</b> язык, на котором <b>будет общаться</b> бот:

faq = <b>❓ ЧаВо</b>

          <b>1. Для чего этот бот?</b>
          <i>— Бот создан, с целью напомнить пользователю, когда истечет его подписка в каком-либо сервисе.</i>

          <b>2. Какие сервисы можно добавлять?</b>
          <i>— Неважно где вы оформили подписку, можно добавлять любые сервисы.</i>

          <b>3. Как добавить сервис?</b>
          <i>— Перейдите в раздел Мои подписки и нажмите кнопку Добавить. Заполняйте данные, строго следуя инструкциям: сначала введите название, следующим шагом введите кол-во.бли месяцев (число), затем выберите на календаре, когда напомнить о списании. Подтвердите правильность, и подписка будет добавлена.</i>


catalog-add = <b>🗂️ Каталог добавленных подписок:</b>

               { $subs }

catalog-remove = <b>🗂️ Каталог удаления подписок:</b>

                { $message }

catalog-edit = <b>🗂️ Каталог изменения подписок:</b>

                { $message }

conformation = <b>Вы действительно</b> хотите <b>удалить</b> подписку?

add-service-title = Как называется <b>сервис</b> на который Вы <b>подписались</b>?

                    <b>Пример:</b> <code>Tinkoff Premium</code>

add-service-months = Сколько <b>месяцев</b> будет действовать подписка?

                    <b>Пример:</b> <code>12 (мес.)</code>

add-calendar-date = В какую <b>дату</b> оповестить о <b>ближайшем списании</b>?

check-form = 📩 Проверьте <b>правильность</b> введённых данных:

             <b>Сервис:</b> <code>{ $service }</code>
             <b>Длительность:</b> <code>{ $months } (мес.)</code>
             <b>Оповестить: </b> <code>{ $reminder }</code>

nothing-delete = <b>🤷‍♂️ Кажется</b>, здесь <b>нечего удалять...</b>

nothing-output = <b>🤷‍♂️ Кажется</b>, мы ничего <b>не нашли...</b>

set-for-delete = <b>Выберите</b> подписку, которую <b>хотите удалить</b>:

set-for-edit = <b>Выберите</b> подписку, которую <b>хотите изменить</b>:

error-subs-limit = <b>🚫 Ошибка:</b> Достигнут лимит подписок

error-len-limit = <b>🚫 Ошибка:</b> Достигнут лимит символов

error-unsupported-char = <b>🚫 Ошибка:</b> Введены недопустимые символы

error-range-reached = <b>🚫 Ошибка:</b> Достигнут диапазон значений

approve-sub-add = <b>✅ Одобрено:</b> Данные успешно записаны

error-sub-add = <b>❎ Отклонено:</b> Данные не записаны

approve-sub-delete = <b>✅ Одобрено:</b> Подписка успешно удалена

reject-sub-delete = <b>❎ Отклонено:</b> Подписка не удалена

approve-sub-edit = <b>✅ Одобрено:</b> Подписка успешно изменена

reject-sub-edit = <b>❎ Отклонено:</b> Подписка не изменена

notification-message = <b>🔔 Уведомление</b>
                       <b>Напоминаем Вам</b>, что ваша подписка <code>{ $service }</code> скоро <b>закончится</b>!

select-parameters = Выберите <b>параметр</b>, который <b>хотите изменить</b>:

edit-form = Выберите <b>подписку</b>, которую <b>хотите изменить</b>:

check-title-form = 📩 Проверьте <b>правильность</b> изменения данных:

                  <b>{ $service_old_title }</b> → <b>{ $service_new_title }</b>

check-months-form = 📩 Проверьте <b>правильность</b> изменения данных:

                  <code>{ $service_old_months } (мес.)</code> → <code>{ $service_new_months } (мес.)</code>

check-reminder-form = 📩 Проверьте <b>правильность</b> изменения данных:

                  <b>{ $service_old_reminder }</b> → <b>{ $service_new_reminder }</b>