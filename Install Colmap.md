# Beschreibung und Befehle von

https://github.com/colmap/pycolmap
https://colmap.github.io/install.html
https://github.com/colmap/pycolmap/commit/18f2f07259c3ef8288d06a7aab3523ff423aff71

# Linux

Dependencies from the default Ubuntu repositories:
```
sudo apt-get install \
    git \
    cmake \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libboost-test-dev \
    libeigen3-dev \
    libsuitesparse-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev
```

Install Ceres Solver:
```
sudo apt-get install libatlas-base-dev libsuitesparse-dev
git clone https://ceres-solver.googlesource.com/ceres-solver
cd ceres-solver
# git checkout $(git describe --tags)                   # Checkout the latest release
git checkout 941ea13475913ef8322584f7401633de9967ccc8   # Use Ceres 2.1 or 2.0 (other throws Error; Cause: C++17 needed)
                                                        # https://github.com/colmap/colmap/issues/1482
mkdir build
cd build
cmake .. -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF
make -j2                                                # "make -j" throws Error. Use more Ram or less Cores
                                                        # https://github.com/magicleap/Atlas/issues/3
sudo make install
```

Configure and compile COLMAP:
```
git clone https://github.com/colmap/colmap.git
cd colmap
git checkout dev
mkdir build
cd build
cmake ..
make -j2
sudo make install
```

Run COLMAP (only for testing):
```
colmap -h
colmap gui
```

Build PyColmap
```
# git clone --recursive git@github.com:colmap/pycolmap.git
git clone --recursive https://github.com/colmap/pycolmap
cd pycolmap
pip install .
```

# Windows (not working yet)

Download Visual Studio 2019 at:
https://visualstudio.microsoft.com/de/vs/older-downloads/

Download Cuda at (had to run it 2x in a row):
https://developer.nvidia.com/cuda-downloads

Download CMake at:
https://cmake.org/download/

On Windows, the recommended way is to build COLMAP using vcpkg:
```
git clone https://github.com/microsoft/vcpkg
cd vcpkg
.\bootstrap-vcpkg.bat
# .\vcpkg install colmap[cuda,tests]:x64-windows
.\vcpkg.exe install colmap --triplet=x64-windows --head
# .\vcpkg install colmap[cuda-redist]:x64-windows     # To compile CUDA for multiple compute architectures
# .\vcpkg.exe install pthread --triplet=x64-windows     # https://github.com/colmap/pycolmap/issues/76
```

On Error Missing Cuda, download Cuda and/or edit Portfile:
```
# File: vcpkg\ports\cuda\portfile.cmake
# https://github.com/microsoft/vcpkg/issues/3609
set(ENV{CUDA_BIN_PATH} "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.8/bin")
```
On Error "CMake Error at scripts/cmake/vcpkg_execute_build_process.cmake:131":<br>
https://github.com/microsoft/vcpkg/issues/19561<br>
Deinstall all other Visual Studio Versions and<br>
Install Visual Studio 2019 (MSVC 2019 is needed): https://visualstudio.microsoft.com/de/vs/older-downloads/
<br><br>

Build PyColmap
Then set the `CMAKE_TOOLCHAIN_FILE` environment variable to your `vcpkg\scripts\buildsystems\vcpkg.cmake` path. For Example in powershell:
```
# git clone --recursive git@github.com:colmap/pycolmap.git
git clone --recursive https://github.com/colmap/pycolmap
cd pycolmap
$env:CMAKE_TOOLCHAIN_FILE='C:\src\vcpkg\scripts\buildsystems\vcpkg.cmake'
$env:path += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin"
# py -m pip install ./
pip install .
```