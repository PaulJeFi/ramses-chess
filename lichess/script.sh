#!/bin/bash
cd "$(dirname "$0")"
git clone https://github.com/lichess-bot-devs/lichess-bot.git
cd lichess-bot
pip3 install -r requirements.txt
cd ..
cp config.yml lichess-bot/config.yml
cp exe.sh lichess-bot/engines/exe.sh
cd lichess-bot
chmod +x engines/exe.sh
python3 lichess-bot.py -v