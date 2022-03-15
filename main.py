import asyncio
import requests
import random

from telethon import TelegramClient, functions, types

MESSAGES = [
    "The channel undermines the integrity of the Ukrainian state. Spreading fake news, misleading and misleading people. Block it as soon as possible!",
    "There are many posts with threats against the Ukrainian military. Lots of photos of the dead, blood and weapons. Block it!",
    "Propaganda of the war in Ukraine. Propaganda of murders of Ukrainians and Ukrainian soldiers. Block it!",
    "Dissemination of military personal data. Block the channel!",
    "Publication of military deaths, brutal killings, violence and hostilities. Please block the channel!",
    "Пропаганда. Розповсюдження некоректної інформації (пропаганда), що призводить до розпалення міжнаціонального конфлікту. Заблокуйте його якомога швидше!",
    "Міжнаціональний конфлікт. Розповсюдження некоректної інформації, яка вводить в оману користувачів та посилює міжнаціональний конфлікт. Заблокуйте його",
    "Розпалення військового конфлікту. Контент групи/каналу використовується у цілях вчинення дій, що розпалюють військовий конфлікт та призводять до збільшення кількості людських жертв. Будь ласка, заблокуйте його якомога швидше!",
]


api_id = input("API ID: ")
api_hash = input("API Hash: ")

client = TelegramClient("account", api_id, api_hash)


async def run_bot():
    await client.start()
    link = "https://gist.githubusercontent.com/ItsWoid/2aa44cedcd0d7b96abd15c7392338f77/raw"
    channels = [line.strip() for line in requests.get(link).text.splitlines()]
    print(channels)
    for channel in channels:
        try:
            result = await client(
                functions.account.ReportPeerRequest(
                    peer=channel,
                    reason=types.InputReportReasonViolence(),
                    message=random.choice(MESSAGES),
                )
            )
            print(result)
        except Exception:
            print("Fail")
        await asyncio.sleep(random.randint(15, 20))


with client:
    client.loop.run_until_complete(run_bot())