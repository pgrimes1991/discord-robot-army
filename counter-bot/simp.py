import discord
from datetime import datetime
import pytz
import config

client = discord.Client()

local = pytz.timezone ("US/Eastern")

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#
#    if message.content.startswith('$hello'):
#        await message.channel.send('Hello!')

@client.event
async def on_message(message):
    if message.content.startswith('!countstonks'):
        limit = 5000
        if ' ' in message.content:
            day = datetime.strptime(message.content.split(' ')[-1]).date()
        else:
            day = datetime.now().date()
        print('counting')
        wc_stonk = 0
        wc_jpow = 0
        messages = await message.channel.history(limit=limit).flatten()
        print(len(messages))
        for msg in messages:
            if 'stonk' in msg.content.lower():
                wc_stonk = wc_stonk + 1
            if 'pow' in msg.content.lower():
                wc_jpow = wc_jpow + 1

        await message.channel.send(f'This channel has mentioned "Stonks" {wc_stonk} times.\n This channel has mentioned JPow {wc_jpow} times.')

    if message.content.startswith('!countday'):
        limit = 5000
        if ' ' in message.content:
            day = datetime.strptime(message.content.split(' ')[-1]).date()
        else:
            day = datetime.now().date()
        print('counting')
        wc = 0
        messages = await message.channel.history(limit=limit).flatten()
        print(len(messages))
        for msg in messages:
            if day==msg.created_at.date():
                wc = wc + len(msg.content.split(' '))

        await message.channel.send(f'The word count for {day} is {wc}')

    if message.content.startswith('!countwords'):
        limit = 300
        if ' ' in message.content:
            limit = int(message.content.split(' ')[-1])
        print('counting')
        wc = 0
        messages = await message.channel.history(limit=limit).flatten()
        print(len(messages))
        for msg in messages:
            wc = wc + len(msg.content.split(' '))

        await message.channel.send(f'The word count for the last {limit} messages is {wc}')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


client.run(config.access_key)
