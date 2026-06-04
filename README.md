# Micro:bit Intergration
Home assistant integration for Micro:bit.
Get the Micro:bit firmware from [Github releases](https://github.com/ElliNet13/hass-microbit-makecode/releases/latest) of [ElliNet13/hass-microbit](ElliNet13/hass-microbit).

## How to dev?
1. Open dev container
1. Wait for it start
1. Run `/home/vscode/.local/bin/python3.14 -m pip install --break-system-packages -r ./home-assistant-core/requirements.txt`
1. Run the test task in VS code to start home assistant
1. Ctrl+C the task
1. Start it again and this time it should actually work