for /f %%i in ('python3 -m site --user-site') do set pypath=%%i
%pypath%\..\Scripts\pyuic6.exe -x main-window.ui -o main-window.py