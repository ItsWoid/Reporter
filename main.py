import argparse
import asyncio
import requests
import random

from telethon import TelegramClient, functions, types

import rich
from rich import box
from rich.table import Table
from rich.theme import Theme
from rich.columns import Columns
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.progress import TextColumn, BarColumn, Progress

INTRO = """

██████╗░███████╗██████╗░░█████╗░██████╗░████████╗███████╗██████╗░
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██████╔╝█████╗░░██████╔╝██║░░██║██████╔╝░░░██║░░░█████╗░░██████╔╝
██╔══██╗██╔══╝░░██╔═══╝░██║░░██║██╔══██╗░░░██║░░░██╔══╝░░██╔══██╗
██║░░██║███████╗██║░░░░░╚█████╔╝██║░░██║░░░██║░░░███████╗██║░░██║
╚═╝░░╚═╝╚══════╝╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
"""

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

themes = Theme({
    "blurple": "#7289da"
})

table_info = Table(show_edge=False, show_header=False)
table_info.add_row("Released", "Test lol")

rich_console = rich.console.Console(theme=themes)
rich_console.print(INTRO, style="blurple")

api_id = None
api_hash = None

while not api_id:
    api_id = IntPrompt.ask("[blurple][[/blurple]API ID[blurple]][/blurple]", console=rich_console)

while not api_hash:
    api_hash = Prompt.ask("[blurple][[/blurple]API Hash[blurple]][/blurple]", console=rich_console)

client = TelegramClient("account", api_id, api_hash)


async def main():
    await client.start(phone=lambda: input("Test: "), code_callback=lambda: input("Another test: "))
    link = "https://gist.githubusercontent.com/ItsWoid/2aa44cedcd0d7b96abd15c7392338f77/raw"
    channels = [line.strip() for line in requests.get(link).text.splitlines()]
    progress = Progress(auto_refresh=False, console=rich_console)
    reporter = progress.add_task("Reporting...", total=len(channels))
    progress.start()
    for channel in channels:
        progress.update(reporter, advance=1, description=channel)
        progress.refresh()
        try:
            result = await client(
                functions.account.ReportPeerRequest(
                    peer=channel,
                    reason=types.InputReportReasonViolence(),
                    message=random.choice(MESSAGES),
                )
            )
            rich_console.print(f"[green]Successfully[/green] reported {channel}")
        except Exception:
            rich_console.print(f"[red]Failed[/red] to report {channel}")
        await asyncio.sleep(random.randint(15, 20))


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())