import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from googletrans import Translator
import discord
from random import randint
import re
import requests, uuid
#===============================================================================================#
client = discord.Client()
translator = Translator()
#===============================================================================================#
@client.event
async def on_message(message):
    if (message.author == client.user):
        return
    #===========================================================================================#
    authenticator = IAMAuthenticator('<api key>')
    language_translator = LanguageTranslatorV3(
    version='<version>',
    authenticator=authenticator)
    language_translator.set_service_url('<service url>')
    #===========================================================================================#
    subscription_key = '<api key>'
    endpoint = '<service url>'
    pathtranslate = '<translate path>'
    pathtransliterate = '<transliterate path>'
    pathdetect = '<detect language path>'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': '<location>',
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())}
    #===========================================================================================#
    print('===========================================================================================')
    t=str(message.content)
    print('Message :',t)
    x=re.findall(r'<@!?[0-9]+>',t)#find mentions
    y=re.findall(r'<A?:\w+:[0-9]+>',t)#find reactions, including animated ones
    z=re.findall(r'<#[0-9]+>',t)#find channel mentions
    print('mentions :',x)
    print('reactions :',y)
    print('channel mentions :',z)
    if(len(x)>0):
        for i in x: t=t.replace(i,"@")
    if(len(y)>0):
        for i in y: t=t.replace(i,":")
    if(len(z)>0):
        for i in z: t=t.replace(i,"#")
    print('Sanitized Message :',t)
    try:
        body = [{'text': t}]
        constructed_url = endpoint + pathdetect
        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        print('Microsoft Translator Detection Data :')
        print('Language :',response[0]['language'])
        print('Score :',response[0]['score'])
        if response[0]['score'] < 0.6 or 'en' in response[0]['language']:
            return
        l=response[0]['language']
    except Exception as e:
        print('Microsoft Translator generated an Error, using Google Translator instead :\n',str(e))
        l = translator.detect(t)
        print('Google Translator Detection Data :',l)
        if l.confidence < 0.6 or 'en' in str(l.lang):
            return
        l=l.lang
        pass
    #===========================================================================================#
    try:
        constructed_url = endpoint+pathtranslate+'&to=en'
        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        tr=(response[0]['translations'][0]['text'])
    except Exception as z:
        print('Microsoft Translator generated an Error, using IBM Watson instead :\n',str(z))
        translation = language_translator.translate(text=t,model_id=l+'-en').get_result()
        tr=(dict(json.loads(json.dumps(translation, indent=2, ensure_ascii=False)).items())['translations'][0]['translation'])
    except Exception as e:
        print('IBM Watson generated an Error, using Google Translator instead :\n',str(e))
        tr=translator.translate(t).text
        pass
    print('Translated Text :',tr)
    if(str(tr).lower().strip()==str(t).lower().strip()):
        return
    await message.channel.send("Translation : " + tr)
    print('===========================================================================================')

@client.event
async def on_ready():
    print("Logged In")
    
client.run('<bot token>',bot=True)
