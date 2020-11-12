import discord
from datetime import datetime
import pytz
import config
import requests

import re
import pdb
import urllib
import requests
from bs4 import BeautifulSoup

def get_election(state=None):
    query = "election results {state}".format(state=state)
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent" : MOBILE_USER_AGENT}
    resp = requests.get(URL, headers=headers)
    p = re.compile(r'%')
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

    results = []
    print(len(soup.find_all('div')), 'DIVLEN')
    for idx, g in enumerate(soup.find_all('div')):
        if 'Donald Trump' in g.text and idx>70:
            print(idx, 'TRUMP')
            name = 'Trump'
            break
        if 'Joe Biden' in g.text and idx>70:
            print(idx, 'BIDEN')
            name = 'Biden'
            break
    for g in soup.find_all('span'):
        if 'reporting' in g.text:
            print(g.text[0:4])
            reporting = g.text[0:4]
            break
    i=-1
    for g in soup.find_all('span'):
        if 'Vote count' in g.text:
            i=1
        if i>=1:
            if g.text.strip()!='':
                results.append(g.text)
            print(g.text)
            i+=1

        if len(results)==5:
            i=-1

    return "{name} lead {lead} \n Percent reporting {reporting}".format(name=name, reporting=reporting, lead=int(results[2].replace(',',''))-int(results[4].replace(',','')))


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
    if message.content.startswith('!PA'):
        election_message = get_elelection_message = get_election('PA')
        await message.channel.send(election_message)
    if message.content.startswith('!GA'):
        election_message = get_elelection_message = get_election('GA')
        await message.channel.send(election_message)
    if message.content.startswith('!AZ'):
        election_message = get_elelection_message = get_election('AZ')
        await message.channel.send(election_message)
    if message.content.startswith('!NC'):
        election_message = get_elelection_message = get_election('NC')
        await message.channel.send(election_message)
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
