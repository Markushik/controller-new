settings = ⚙️ Settings
support = 🆘 Support
my-subscriptions = 🗂️ My Subscriptions
administrator = 👨‍💻 Administrator
back = ↩️ Back

add = Add
delete = Delete
change = Change

title = Title
months = Months
date = Date
renew = Renew

select-lang = 🌍 <b>Select</b> the language in which <b>the bot will communicate</b>:

catalog-add = <b>🗂️ Subscriptions add catalog:</b>

              { $subs }

catalog-remove = <b>🗂️ Subscription removal catalog:</b>

                { $message }

catalog-edit = <b>🗂️ Subscription editing catalog:</b>

               { $message }

conformation = <b>Are you sure</b> you want to <b>delete</b> the subscription?

faq = <b>❓ FAQ</b>

          <b>1. What is this bot for?</b>
          <i>— The bot was created to remind the user when his subscription to any service expires.</i>

          <b>2. What services can be added?</b>
          <i>— It doesn't matter where you subscribed, you can add any services.</i>

          <b>3. How to add a service?</b>
          <i>— Go to the My Subscriptions section and click the Add button. Fill in the data strictly following the instructions: first enter the name, next step enter the quantity. months (number), then select on the calendar when remind you to write off. Confirm that the subscription is correct and the subscription will be added.</i>

add-service-title = What is the name of the <b>service</b> that you <b>subscribed to</b>?

                    <b>Example:</b> <code>Tinkoff Premium</code>
add-service-months = How many <b>months</b> will the subscription last?

                    <b>Example:</b> <code>12 (mon.)</code>

add-calendar-date = What <b>date</b> to notify about the <b>next write-off</b>?

check-form = 📩 Check <b>correctness</b> of the entered data:

             <b>Service:</b> <code>{ $service }</code>
             <b>Duration:</b> <code>{ $months } (mon.)</code>
             <b>Notify: </b> <code>{ $reminder }</code>

start-menu = <b>Subscriptions Controller</b> — is the <b>best</b> way to <b>control</b> your subscriptions

            📣 <b>Required</b> add your subscriptions to <b>our service</b> to receive <b>notifications</b> about the next charge

nothing-delete = <b>🤷‍♂️ It seems</b>, there is <b>nothing to delete here...</b>

nothing-output = <b>🤷‍♂️ It seems</b> that we <b>haven't found anything...</b>

set-for-delete = <b>Select</b> the subscription that you <b>want to delete</b>:

set-for-edit = <b>Select</b> the subscription that you <b>want to change</b>:

error-subs-limit = <b>🚫 Error:</b> Subscription limit reached

error-len-limit = <b>🚫 Error:</b> Character limit reached

error-unsupported-char = <b>🚫 Error:</b> Invalid characters entered

error-range-reached = <b>🚫 Error:</b> Value range reached

approve-sub-add = <b>✅ Approved:</b> Data written successfully

error-sub-add = <b>❎ Rejected:</b> Data not recorded

approve-sub-delete = <b>✅ Approved:</b> Subscription successfully deleted

reject-sub-delete = <b>❎ Rejected:</b> Subscription not deleted

approve-sub-edit = <b>✅ Approved:</b> Subscription changed successfully

reject-sub-edit = <b>❎ Rejected:</b> Subscription not changed

notification-message = <b>🔔 Notification</b>
                       <b>We remind you</b> that your <code>{ $service }</code> subscription will soon <b>end</b>!

select-parameters = Select the <b>parameter</b> that you <b>want to change</b>:

edit-form = Select the <b>subscription</b> that you <b>want to change</b>:

check-title-form = 📩 Check <b>correctness</b> of data changes:

                  <b>{ $service_old_title }</b> → <b>{ $service_new_title }</b>

check-months-form = 📩 Check <b>correctness</b> of data changes:

                  <code>{ $service_old_months } (mon.)</code> → <code>{ $service_new_months } (mon.)</code>

check-reminder-form = 📩 Check <b>correctness</b> of data changes:

                  <b>{ $service_old_reminder }</b> → <b>{ $service_new_reminder }</b>