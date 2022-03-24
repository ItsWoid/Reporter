import requests
import random
from time import sleep

from pyrogram import Client
from pyrogram.raw import functions, types
from pyrogram.errors import (
    PhoneNumberInvalid,
    PhoneCodeEmpty,
    PhoneCodeInvalid,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    UsernameInvalid,
)

import rich
from rich import box
from rich.table import Table
from rich.theme import Theme
from rich.columns import Columns
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
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

reactions = ["👎", "💩"]

themes = Theme({
    "blurple": "#7289da"
})

rich_console = rich.console.Console(theme=themes)
rich_console.print(INTRO, style="blurple")

api_id = None
api_hash = None

while not api_id:
    api_id = IntPrompt.ask("[blurple][[/blurple]API ID[blurple]][/blurple]", console=rich_console)

while not api_hash:
    api_hash = Prompt.ask("[blurple][[/blurple]API Hash[blurple]][/blurple]", console=rich_console)

client = Client("account", api_id, api_hash)


def run_bot():
    link = "https://gist.githubusercontent.com/ItsWoid/2aa44cedcd0d7b96abd15c7392338f77/raw"
    channels = [line.strip() for line in requests.get(link).text.splitlines()]
    progress = Progress(auto_refresh=False, console=rich_console)
    reporter = progress.add_task("Reporting...", total=len(channels))
    progress.start()
    for channel in channels:
        progress.update(reporter, advance=1, description=channel)
        progress.refresh()
        try:
            peer = client.resolve_peer(channel)
        except UsernameInvalid:
            rich_console.print("The username is invalid")
        channel_id = f"-100{peer.channel_id}"
        sleep(random.randint(10, 15))
        history = client.get_history(channel_id)
        message = random.choice(history)
        client.send_reaction(channel_id, message.message_id, random.choice(reactions))
        sleep(random.randint(5, 10))
        result = client.send(
            functions.account.ReportPeer(
                peer=peer,
                reason=types.InputReportReasonViolence(),
                message=random.choice(MESSAGES),
            )
        )
        rich_console.print(f"[green]Successfully[/green] reported {channel}")
        sleep(random.randint(15, 20))


def main():
    is_authorized = client.connect()
    if not is_authorized:
        phone = None
        while not phone:
            phone = Prompt.ask("[blurple][[/blurple]Phone[blurple]][/blurple]", console=rich_console)
            try:
                sent_code_info = client.send_code(phone)
            except PhoneNumberInvalid:
                phone = None
                rich_console.print("Phone number invalid!", style="red")
        code = None
        while not code:
            code = Prompt.ask("[blurple][[/blurple]Code[blurple]][/blurple]", console=rich_console)
            try:
                client.sign_in(phone, sent_code_info.phone_code_hash, code)
            except (PhoneCodeEmpty, PhoneCodeInvalid):
                code = None
                rich_console.print("The confirmation code is invalid", style="red")
            except SessionPasswordNeeded:
                rich_console.print(
                    "\nYour account have two-step verification enabled!\n"
                    "To continue you need to input your password.\n"
                    f"Password hint: [yellow]{client.get_password_hint()}[/yellow]"
                )

                password = None
                for tries in range(3):
                    password = Prompt.ask("[blurple][[/blurple]Password[blurple]][/blurple]", console=rich_console)
                    try:
                        client.check_password(password)
                    except PasswordHashInvalid:
                        password = None
                        rich_console.print("Invalid password! Try again.", style="red")
                    else:
                        break

                if not password:
                    rich_console.print(
                        "\nSeems like you forgot your password.\n"
                        "Don't worry tho! It can be recovered!"
                    )
                    confirm = Confirm.ask("Confirm password recovery")

                    if confirm:
                        email_pattern = client.send_recovery_code()
                        rich_console.print(f"Recovery code has been sent to {email_pattern}")

                        while True:
                            recovery_code = Prompt.ask("[blurple][[/blurple]Recovery code[blurple]][/blurple]", console=rich_console)

                            try:
                                client.recover_password(recovery_code)
                            except Exception as e:
                                rich_console.print(e)
                    else:
                        password = None
                        return input(
                            "Connection failed!\n"
                            "Press any key to exit..."
                        )
    #client.start()
    run_bot()
    client.disconnect()
    input(
        "Programm is finished!",
        "Press any key to exit..."
    )


if __name__ == "__main__":
    main()