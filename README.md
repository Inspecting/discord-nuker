Join my discord and there you can give me suggestions on what to add. https://discord.gg/DfW4y6tNVn

This bot is not for malicious intent and is only for testing purposes. This can be bannable on discord if you use this for anything malicous. Use at your own risk.

This is a discord nuker bot. It is very easy to use. I will provide a tutorial on how to get the channel id and authorization. Getting url and authorization requires web version of discord.

Requirments:
Download python at https://www.python.org/downloads/. Download latest version and install. Make sure to add python to path in the installation menu or it won't work. After you install python open up. You also need pip I think, correct me if I'm wrong in issues. If you do need it then go to https://www.geeksforgeeks.org/how-to-install-pip-on-windows/ and that will show you how.

Tutorial:

How to get channel-id?
First go onto the web version of discord and then go to the channel you would like to start spamming in. Look at the url of the channel, it should like like https://discord.com/channels/NUMBERS/channel-id.
You need to copy NUMBERS2, the very last numbers of the link. Paste those numbers in config on the url section. Where it says CHANNEL-ID-HERE, replace that text with the numbers.

How to get authorization?
First you need to go onto any channel you want. Open inspect element and go to network. After that send a random message in the server and you should see something called "messages" appear in the network. If you don't see it or the messages won't send to the channel just wait a second or retry to send the message until you see "messages". Click on messages and and you should be under headers. If you aren't then make sure you are. Scroll down until you see Request Headers and after you find that you will see something called authorization not to far under that. Copy the authorization message and replace it there it says "DISCORD AUTHORIZATION TOKEN HERE". Make sure to save the config and you should be done. double click on "run" and it should start. You need the python installed into path.
