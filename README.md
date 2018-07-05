# qwertee-bot-discord
b1naryth1ef/disco plugin to send tees from qwertee.com in DM.

Sending !qwertee in the channel will subscribe you to a daily qwertee update.
Sending !qwertee while subscribed will unsubscribe you.

The program parse the HTML returned by the main page.
You need to install library to make it work.

`pip install requests`

You can modify the channel on line 12 of the script :
```python
self.channel = '#YourChannelHere'
```

![Demo](https://raw.githubusercontent.com/Warths/qwertee-bot-discord/master/qwerteebot_demo.png "Demo")

Designed for python 3.5
