
import discord
from googletrans import Translator
client = discord.Client()
translator = Translator()
token='Insert token here'
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if(message.author!=client.user):
        t=translator.detect(message.content)
        d=translator.translate(message.content)
        print(t)
        print(d)
        if('en'!=t.lang):
            await client.send_message(message.channel,"Translation : "+d.text)
 

client.run(token,bot=False)
