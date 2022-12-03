for /f %%i in ('python3.9 -m site --user-site') do set pypath=%%i

for %%f in (*.ui) do (
	%pypath%\..\Scripts\pyuic6.exe -x "%%~nf.ui" -o "%%~nf.py"
)