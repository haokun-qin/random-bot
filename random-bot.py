import discord
from bs4 import BeautifulSoup, SoupStrainer
import os
import urllib.request
import requests
import asyncio
import json
import random
import inflect
from replit import db
from random import randint
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

client = discord.Client()

url = 'https://random-word-api.herokuapp.com/word?number=1'
p = inflect.engine()

def get_name():
  print(names)
  name = random.choice(names)
  return (name)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('{0.user} has been initialized'
  .format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if str.lower(message.content) == 'communism':
    await message.channel.send('yes comrade')
    await message.channel.send('https://tenor.com/view/renge-non-biyori-salute-gif-4749194')

  if (str.lower(message.content) == 'capitalism') or (str.lower(message.content) == 'socialism'):
    await message.channel.send('no comrade')
    await message.channel.send('https://tenor.com/view/renge-tears-sad-crying-upset-gif-9192490')

  if message.content.startswith('?random wisdom'):  
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith("?random up to "):
    up_to = msg.split("?random up to ",1)[1]
    numbers = []
    count = 1
    print(up_to)
    while (count <= int(up_to)):
      numbers = numbers + [count]
      count = count + 1
    await message.channel.send(random.choice(numbers))

  if msg.startswith("?random down to "):
    down_to = msg.split("?random down to ",1)[1]
    numbers = []
    count = -1
    print(down_to)
    while (count >= int(down_to)):
      numbers = numbers + [count]
      count = count - 1
    await message.channel.send(random.choice(numbers))

  if message.content.startswith('?random range '): 
    range = msg.split("?random range ",1)[1]
    range = range + " "
    range_arr = []
    number = ""
    for elem in range:
      if (elem == " "):
        if (number != "") & (number != " "):
          range_arr = range_arr + [number]
        number = ""
      else:
        number = number + elem
    lo = int(range_arr[0])
    hi = int(range_arr[1])
    result = randint(lo, hi)
    await message.channel.send(result)

  
  if message.content.startswith('?random image'): 
    search = msg.split("?random image",1)[1]

    html_page = requests.get('https://source.unsplash.com/random')

    link = html_page.url   
    print(link)
       
    await message.channel.send(link)


  if message.content.startswith('?random name '): 
    member_str = message.mentions[0].id
    guild_id = message.guild.id
    guild = client.get_guild(guild_id)
    member = await guild.fetch_member(member_str)
    print(member_str)
    r = requests.get(url)
    text = r.text  
    username = (text[2:-2]+ str(randint(0,100))) 
    await member.edit(nick=username)
    await message.channel.send('haha ur name has been changed to ' + username)

  if msg.startswith("?random cb "):
    data = msg.split("?random cb ",1)[1]
    data = data + " "
    options = []
    print(data)
    word = ""
    for elem in data:
      if (elem == " "):
        if (word != "") & (word != " "):
          options = options + [word]
        word = ""
      else:
        word = word + elem
    await message.channel.send(random.choice(options))

  if msg.startswith("?random help"):

    await message.channel.send('`?random wisdom returns a random quote`')
    await message.channel.send('`?random cb [a] [b] [c] returns a message choosing from [a] [b] [c] ...`')
    await message.channel.send('`?random up to [a] returns an integer from 0 up to [a]`')
    await message.channel.send('`?random name [a] renames [a] to a random username`')
    await message.channel.send('`?random down to [a] returns an integer from 0 down to [a]`')
    await message.channel.send('`?random range [a] [b] returns an integer from [a] to [b]`')
    await message.channel.send('`?random vote [a] [b] [c] ... starts a vote between [a] [b] [c] ...`')
    await message.channel.send('`?random image sends a random image`')


  if msg.startswith("?random vote "):
    data = msg.split("?random vote ",1)[1]
    data = data + " "
    options = []
    print(data)
    word = ""
    for elem in data:
      if (elem == " "):
        if (word != "") & (word != " "):
          options = options + [word]
        word = ""
      else:
        word = word + elem

    options_len = len(options)
    print(len(options))

    i = 0

    while (i < options_len) & (i < 9):
      emoji_num = p.number_to_words(i+1)
      await message.channel.send(':' + emoji_num + ': ' + options[i])
      i = i + 1

    number_emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]


    msg2 = await message.channel.send('Cast your vote!')

    i = 0

    while (i < options_len) & (i < 9):
      await msg2.add_reaction(number_emojis[i])
      i = i + 1


client.run(os.getenv('RANDOM-TOKEN'))    