from disco.bot import Bot, Plugin
from disco.types.message import MessageEmbed
import requests
import datetime
import time
import threading
import json

class QwerteePlugin(Plugin):

    def load(self, ctx):
        self.channel = '#bot'
        self.dm_channels = []
        try:
            self.dm_channels = self.save_load()
        except FileNotFoundError:
            self.save_write()
        self.tees = self.get_qwertees()

    def save_load(self):
        with open('users.json', 'r') as save_file:
            return json.loads(save_file.read())['data']

    def save_write(self):
        with open('users.json', 'w') as save_file:
            data = {'data': self.dm_channels}
            json.dump(data, save_file, indent=4)

    @Plugin.listen('Ready')
    def ready(self, ctx):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    @Plugin.command('qwertee', '[pseudo:str...]')
    def on_qwertee_command(self, event):
        found = False
        index = 0
        user_dm_channel = [int(str(event.author.open_dm())), str(event.author)]
        for i in range(0, self.dm_channels.__len__()):
            if user_dm_channel[0] in self.dm_channels[i]:
                found = True
                index = i
        if str(event.channel) == '#testing':
            if found:
                self.dm_channels.pop(index)
                event.msg.reply('%s, tu ne recevras plus les modèles de T-shirt de Qwertee.com.'
                                % event.author)
            else:
                self.dm_channels.append(user_dm_channel)
                event.msg.reply('%s, tu recevras les modèles de T-shirt de Qwertee.com quotidiennement en message privé !'
                                % event.author)
                self.send_tees(user_dm_channel[0], user_dm_channel[1])
        self.save_write()


    def run(self):
        messages_sent = False
        when = 8
        while True:
            current_time = datetime.datetime.now()
            if current_time.hour == when and not messages_sent:
                messages_sent = True
                self.tees = self.get_qwertees()
                for channel in self.dm_channels:
                    self.send_tees(channel[0], channel[1])
            elif current_time.hour != when and messages_sent:
                messages_sent = False
            time.sleep(5)

    def send_tees(self, channel, nickname):
        print('Sending Tees to %s' % nickname)
        for tee in self.tees:
            self.client.api.channels_messages_create(channel, embed=tee.embed)

    def get_qwertees(self):
        tees = []
        while True:
            r = requests.get('https://www.qwertee.com')
            if r.status_code == 200:
                html = r.content.decode()
                html = html.split('<div class="index-tee')
                for i in range(1,4):
                    tee = Qwertee(self.get_html_tag_content(html[i], 'data-name'),
                                  self.get_html_tag_content(html[i], 'data-user'),
                                  self.get_html_tag_content(html[i], 'data-tee-price-eur'),
                                  self.get_html_tag_content(html[i], 'data-hoodie-price-eur'),
                                  self.get_html_tag_content(html[i], 'data-pulloverhoodie-price-eur'),
                                  self.get_html_tag_content(html[i], 'data-sweater-price-eur'),
                                  self.get_html_tag_content(html[i], 'data-print-price-eur'),
                                  self.get_html_tag_content(html[i], 'source srcset'))
                    tees.append(tee)
                return tees
            time.sleep(60)

    @staticmethod
    def get_html_tag_content(content, target):
        try:
            content = content.split(target)
            content = content[1].split('"')
            return content[1]
        except:
            return 'Error'



class Qwertee:

    def __init__(self, name, author, price_tee, price_hoodie, price_pullover, price_sweater, price_print, image):
        self.name = name
        self.author = author
        self.price_tee = price_tee
        self.price_hoodie = price_hoodie
        self.price_pullover = price_pullover
        self.price_sweater = price_sweater
        self.price_print = price_print
        self.image = 'https:' + image
        self.link = 'https://www.qwertee.com/'
        self.embed = self.get_embed_tee()

    def get_embed_tee(self):
        embed = MessageEmbed(title=('"%s" designé par %s !' %
                                    (self.name.capitalize(), self.author.capitalize())),
                             url=self.link)
        embed.set_author(name='QwerteeBot - T-Shirt quotidiens !',
                         icon_url='https://static-cdn.jtvnw.net/badges/v1/3e636937-64e0-4e93-80c2-ec3c4389472e/1')
        embed.set_thumbnail(url=self.image)
        embed.add_field(name='T-shirt : ', value='%s€' % self.price_tee, inline=True)
        embed.add_field(name='Hoodie : ', value='%s€' % self.price_hoodie, inline=True)
        embed.add_field(name='Pullover : ', value='%s€' % self.price_pullover, inline=True)
        embed.add_field(name='Sweat : ', value='%s€' % self.price_sweater, inline=True)
        embed.add_field(name='Tableau : ', value='%s€' % self.price_print, inline=True)
        return embed
