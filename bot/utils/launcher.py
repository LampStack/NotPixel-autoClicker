import asyncio
import argparse
from random import randint
from typing import Any
from better_proxy import Proxy

from bot.config import settings
from bot.core.image_checker import participate, reacheble
from bot.utils import logger
from bot.core.tapper import run_tapper
from bot.core.registrator import register_sessions, get_tg_client
from bot.utils.accounts import Accounts
from bot.utils.firstrun import load_session_names

art_work = """
██████╗  ██████╗ ██╗    ██╗███████╗██████╗  ██████╗ ██████╗ ██████╗ ███████╗███████╗
██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝██║     ██║   ██║██║  ██║█████╗  ███████╗
██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗██║     ██║   ██║██║  ██║██╔══╝  ╚════██║
██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║╚██████╗╚██████╔╝██████╔╝███████╗███████║
╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
                                                                                    
███╗   ██╗ ██████╗ ████████╗██████╗ ██╗██╗  ██╗███████╗██╗                          
████╗  ██║██╔═══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝██╔════╝██║                          
██╔██╗ ██║██║   ██║   ██║   ██████╔╝██║ ╚███╔╝ █████╗  ██║                          
██║╚██╗██║██║   ██║   ██║   ██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║                          
██║ ╚████║╚██████╔╝   ██║   ██║     ██║██╔╝ ██╗███████╗███████╗                     
╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝                                                            
                                                                 by @osClub                                    
"""

version = "6.5v"

start_text = """                                             
Select an action:

    1. Run bot
    2. Create session
    
"""


def get_proxy(raw_proxy: str) -> Proxy:
    return Proxy.from_str(proxy=raw_proxy).as_url if raw_proxy else None


async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, help="Action to perform")
    action = parser.parse_args().action

    if not action:
        await reacheble()
        print('\033[1m' + '\033[92m' + art_work + '\033[0m')
        print('\033[1m' + '\033[93m' + version + '\033[0m')

        #if settings.AUTO_TASK:
            #logger.warning("Auto Task is enabled, it is dangerous functional")

        print(start_text)

        while True:
            action = input("> ")

            if not action.isdigit():
                logger.warning("Action must be number")
            elif action not in ["1", "2", "3"]:
                logger.warning("Action must be 1, 2 or 3")
            else:
                action = int(action)
                break

    used_session_names = load_session_names()

    if action == 3:
        username = input("> Provide your telegram username to write you(without @): ")
        await participate(username)
    elif action == 2:
        await register_sessions()
    elif action == 1:
        accounts = await Accounts().get_accounts()
        await run_tasks(accounts=accounts, used_session_names=used_session_names)


async def run_tasks(accounts: [Any, Any, list], used_session_names: [str]):
    tasks = []
    for account in accounts:
        session_name, user_agent, raw_proxy = account.values()
        first_run = session_name not in used_session_names
        tg_client = await get_tg_client(session_name=session_name, proxy=raw_proxy)
        proxy = get_proxy(raw_proxy=raw_proxy)
        tasks.append(asyncio.create_task(run_tapper(tg_client=tg_client, user_agent=user_agent, proxy=proxy, first_run=first_run)))
        await asyncio.sleep(randint(5, 20))

    await asyncio.gather(*tasks)
