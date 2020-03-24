# WhatsappBot

A bot for whatsapp that is used for sending invitation links to groups.

The general mechanism is:

  - Connecting manually to "https://web.whatsapp.com/" by scanning the QR code via the sender's phone
  - Having a spam group where the bot can spam with mesasging links 
	- Links of the form "https://api.whatsapp.com/send?phone={number}" 
	- They don't add the phone number to the cell but start a chat with it
  - Clicking the link and start a chat with the number
  - Send the invitation

You can add phone numbers manually to the phones list in main or adding them as a new line to the a file.

Dont forget to update PHONE_LIST_FILE to the file's name.