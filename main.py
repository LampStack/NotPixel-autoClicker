import asyncio
import sys
import os
import json

from bot.utils import logger
from bot.utils.launcher import process

async def add_sessions_to_accounts() -> None:
    accounts_file_path = 'accounts.json'  
    sessions_folder_path = 'sessions'  

    
    if os.path.exists(accounts_file_path):
        with open(accounts_file_path, 'r') as f:
            accounts = json.load(f)
    else:
        accounts = []

    
    session_files = [f for f in os.listdir(sessions_folder_path) if f.endswith('.session')]

    
    for session_file in session_files:
        session_name = session_file[:-8]  

        session_file_path = os.path.join(sessions_folder_path, session_file)
        with open(session_file_path, 'r') as f:
            phone_number = f.readline().strip()  

        if not any(account['session_name'] == session_name for account in accounts):
            accounts.append({
                "session_name": session_name,
                "phone_number": phone_number,
                "proxy": ""
            })

   
    with open(accounts_file_path, 'w') as f:
        json.dump(accounts, f, indent=4)

async def main():
    await process()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("<r>Bot stopped by user...</r>")
        sys.exit(2)
