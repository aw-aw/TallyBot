# TallyBot
A discord bot for automated tallying.

Quick Start:

+n item: This will add "n" to the value of "item" in the database. The bot will send no reply.
+count: This will sum all of the values of all items. The bot will send a reply with the total sum.
+count item: This will get the value of a certain item. The bot will send a reply with the found value, or a scripted not found message if the value does not exist.
+items: This will get all the items with their corresponding values. The bot will send a reply with all the items and values, separated with new lines.
-item: This will remove one from the value of the item. The bot will not send a reply, unless the item is not found
