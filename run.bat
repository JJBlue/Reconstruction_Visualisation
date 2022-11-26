SET mypath=%~dp0
python3.11 ./src/main/python/main.py -workdir "%mypath:~0,-1%\config"