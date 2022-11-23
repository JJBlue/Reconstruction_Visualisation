# Beschreibung und Befehle von

http://www.open3d.org/docs/release/compilation.html#compilation

# Windows

Install Python from Website (not from the Store)
Download latest Release von Open3D hier: https://github.com/isl-org/Open3D

```
git clone https://github.com/isl-org/Open3D
cd Open3D
mkdir build
cd build

# python3 -c "import os, sys; print(os.path.dirname(sys.executable))"

# $env:path += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin"
$env:path += ";C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin"

# cmake -G "Visual Studio 16 2019" -A x64 -DPYTHON_EXECUTABLE:FILEPATH="C:\Users\Julian\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0" ..
# cmake -G "Visual Studio 16 2019" -A x64 -DPYTHON_EXECUTABLE:FILEPATH="C:\\Program Files\\Python311" ..
# cmake -G "Visual Studio 16 2019" -A x64 ..
cmake -G "Visual Studio 17 2022" -A x64 -DPYTHON_EXECUTABLE:FILEPATH="C:\\Program Files\\Python311" ..
# cmake -G "Visual Studio 17 2022" -A x64 ..

cmake --build . --config Release --target ALL_BUILD

# While programm is running. Replace folder (Open3D\build\_deps\ext_pybind11-src) with latest release from pybind11

cmake --build . --config Release --target INSTALL
# cmake --build . --config Release --target pip-package
```