import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
client = commands.Bot('')
url='http://makautexam.net/'
r1=requests.get(url)
@tasks.loop(seconds=1.0)#seconds is time interval between successive tasks, can be changed.
async def my_task():
    global r1
    r2=requests.get(url)
    if(r1.text!=r2.text):
        r1=r2
        soup=BeautifulSoup(r2.content,'html.parser')
        message_=str(soup.find('ul',{'class':'notice'}).a.next_element).strip()+"\n"+url+str(soup.find('ul',{'class':'notice'}).a.get('href'))
        await client.get_channel('<channel id>').send(message_)
@client.event
async def on_ready():
    print("Logged In")
    my_task.start()
client.run('<bot token>',bot=True)#if its a user account then set bot=False

