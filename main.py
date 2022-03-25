import argparse
import requests
import random
from time import sleep

from pyrogram import Client
from pyrogram.raw import functions, types
from pyrogram.errors import (
    PhoneNumberInvalid,
    PhoneCodeEmpty,
    PhoneCodeInvalid,
    ReactionInvalid,
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
    "Propaganda. Dissemination of incorrect information, which leads to the escalation of interethnic conflict. Block it as soon as possible!",
    "Interethnic conflict. Dissemination of incorrect information that misleads users and exacerbates interethnic conflict. Block it!",
    "Розпалення військового конфлікту. Контент групи/каналу використовується у цілях вчинення дій, що розпалюють військовий конфлікт та призводять до збільшення кількості людських жертв. Будь ласка, заблокуйте його якомога швидше!",
]

reactions = ["👎", "💩"]


def run_bot():
    link = "https://gist.githubusercontent.com/ItsWoid/2aa44cedcd0d7b96abd15c7392338f77/raw"
    channels = [line.strip() for line in requests.get(link).text.splitlines()]
    progress = Progress(auto_refresh=False, console=rich_console)
    reporter = progress.add_task("Reporting...", total=len(channels))
    progress.start()
    for channel in channels:
        progress.update(reporter, description=f"Resolving {channel}...")
        progress.refresh()
        try:
            peer = client.resolve_peer(channel)
        except UsernameInvalid:
            rich_console.print(f"[red]Failed[/red] to resolve {channel}")
        else:
            channel_id = f"-100{peer.channel_id}"
            sleep(random.randint(15, 20))
            progress.update(reporter, description=f"Getting messages...")
            progress.refresh()
            history = client.get_history(channel_id)
            message = random.choice(history)
            try:
                progress.update(reporter, description="Reacting to the random message...")
                progress.refresh()
                client.send_reaction(channel_id, message.message_id, random.choice(reactions))
            except ReactionInvalid:
                progress.update(reporter, description="Failed to add reaction. Waiting...")
                progress.refresh()
                sleep(random.randint(20, 30))
            sleep(random.randint(15, 20))
            result = client.send(
                functions.account.ReportPeer(
                    peer=peer,
                    reason=types.InputReportReasonViolence(),
                    message=random.choice(MESSAGES),
                )
            )
            progress.update(
                reporter,
                advance=1,
                description=f"[green]Successfully[/green] reported [yellow]{channel}[/yellow]. Waiting...",
            )
            progress.refresh()
            sleep(random.randint(30, 60))


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
                            "Press enter to exit..."
                        )
    user = client.get_me()
    table_info = Table(show_edge=False, show_header=False, box=box.MINIMAL)
    table_info.add_row(f"Connected: [blurple]{user.username}[/blurple]")
    rich_console.print(
        Columns(
            [Panel(table_info, border_style="blurple")],
            align="center",
        )
    )
    run_bot()
    client.log_out()
    input(
        "Programm is finished!",
        "Press enter to exit..."
    )


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-id",
        type=int,
        default=None,
        help="Telegram API ID",
    )
    parser.add_argument(
        "--api-hash",
        default=None,
        help="Telegram API Hash",
    )
    return parser


if __name__ == "__main__":
    args = init_argparse().parse_args()

    api_id = args.api_id
    api_hash = args.api_hash

    themes = Theme({
        "blurple": "#7289da"
    })

    rich_console = rich.console.Console(theme=themes, force_terminal=True)
    rich_console.print(INTRO, style="blurple")

    while not api_id:
        api_id = IntPrompt.ask("[blurple][[/blurple]API ID[blurple]][/blurple]", console=rich_console)

    while not api_hash:
        api_hash = Prompt.ask("[blurple][[/blurple]API Hash[blurple]][/blurple]", console=rich_console)

    client = Client("account", api_id, api_hash)

    main()