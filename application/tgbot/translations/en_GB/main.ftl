Settings = ⚙️ Settings
Support = 🆘 Support
My-Subscriptions = 🗂️ My Subscriptions
Back = ↩️ Back
Administrator = 👨‍💻 Administrator
Add = Add
Delete = Delete
Change = Change
Title = Title
Months = Months
Date = Date
Set-lang = 🌍 <b>Select</b> the language in which <b>the bot will communicate</b>:

Catalog-add = <b>🗂️ Subscriptions add catalog:</b>

              { $subs }

Catalog-change = Change

Catalog-remove = <b>🗂️ Subscription removal catalog:</b>

                { $message }

Catalog-edit = <b>🗂️ Subscription editing catalog:</b>

               { $message }

Are-you-sure = <b>Are you sure</b> you want to <b>delete</b> the subscription?

Q-A = <b>❓ Q&A</b>

          <b>1. What is this bot for?</b>
          <i>— The bot was created to remind the user when his subscription to any service expires.</i>

          <b>2. What services can be added?</b>
          <i>— It doesn't matter where you subscribed, you can add any services.</i>

          <b>3. How to add a service?</b>
          <i>— Go to the My Subscriptions section and click the Add button. Fill in the data strictly following the instructions: first enter the name, next step enter the quantity. months (number), then select on the calendar when remind you to write off. Confirm that the subscription is correct and the subscription will be added.</i>

Add-service-title = What is the name of the <b>service</b> that you <b>subscribed to</b>?

                    <b>Example:</b> <code>Tinkoff Premium</code>
Add-service-months = How many <b>months</b> will the subscription last?

                    <b>Example:</b> <code>12 (mon.)</code>

Add-calendar-date = What <b>date</b> to notify about the <b>next write-off</b>?

Check-form = 📩 Check <b>correctness</b> of the entered data:

             <b>Service:</b> <code>{ $service }</code>
             <b>Duration:</b> <code>{ $months } (mon.)</code>
             <b>Notify: </b> <code>{ $reminder }</code>

Start-menu = <b>Subscriptions Controller</b> — is the <b>best</b> way to <b>control</b> your subscriptions

            📣 <b>Required</b> add your subscriptions to <b>our service</b> to receive <b>notifications</b> about the next charge

Nothing-delete = <b>🤷‍♂️ It seems</b>, there is <b>nothing to delete here...</b>

Nothing-output = <b>🤷‍♂️ It seems</b> that we <b>haven't found anything...</b>

Set-for-delete = <b>Select</b> the subscription that you <b>want to delete</b>:

Set-for-edit = <b>Select</b> the subscription that you <b>want to change</b>:

Error-subs-limit = <b>🚫 Error:</b> Subscription limit reached

Error-len-limit = <b>🚫 Error:</b> Character limit reached

Error-unsupported-char = <b>🚫 Error:</b> Invalid characters entered

Error-range-reached = <b>🚫 Error:</b> Value range reached

Approve-sub-add = <b>✅ Approved:</b> Data written successfully

Error-sub-add = <b>❎ Rejected:</b> Data not recorded

Approve-sub-delete = <b>✅ Approved:</b> Subscription successfully deleted

Reject-sub-delete = <b>❎ Rejected:</b> Subscription not deleted

Approve-sub-edit = <b>✅ Approved:</b> Subscription changed successfully

Reject-sub-edit = <b>❎ Rejected:</b> Subscription not changed

Notification-message = <b>🔔 Notification</b>
                       <b>We remind you</b> that your <code>{ $service }</code> subscription will soon <b>end</b>!

Renew-subscription = Renew subscription

Set-parameters = Select the <b>parameter</b> that you <b>want to change</b>:

Edit-form = Select the <b>subscription</b> that you <b>want to change</b>:

Check-title-form = 📩 Check <b>correctness</b> of data changes:

                  <b>{ $service_old_title }</b> → <b>{ $service_new_title }</b>

Check-months-form = 📩 Check <b>correctness</b> of data changes:

                  <code>{ $service_old_months } (mon.)</code> → <code>{ $service_new_months } (mon.)</code>

Check-reminder-form = 📩 Check <b>correctness</b> of data changes:

                  <b>{ $service_old_reminder }</b> → <b>{ $service_new_reminder }</b>