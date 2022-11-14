SET mypath=%~dp0
python ./src/main/python/main.py -workdir "%mypath:~0,-1%\config"