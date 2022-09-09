#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" & >/dev/null && pwd )"

echo $SCRIPT_DIR 

sudo dpkg -i requirements/*.deb

MATHSATLIB_DIR="${SCRIPT_DIR}/lib/mathsat-5.6.6/" 
echo $MATHSATLIB_DIR
sudo ln -sf "${MATHSATLIB_DIR}/include/mathsat.h" /usr/local/include/mathsat.h
sudo ln -sf "${MATHSATLIB_DIR}/include/mathsat.h" /usr/local/include/mathsatll.h
sudo ln -sf "${MATHSATLIB_DIR}/include/mathsataig.h" /usr/local/include/mathsataig.h
sudo ln -sf "${MATHSATLIB_DIR}/lib/libmathsat.a" /usr/local/lib/libmathsat.a
sudo ln -sf "${MATHSATLIB_DIR}/lib/libmathsat.so" /usr/local/lib/libmathsat.so


cd lib/FuseIC3
mkdir build
cd build
cmake ..
make

cd ../../..
python3 -m venv venv-tolerancetool
source venv-tolerancetool/bin/activate
pip3 install -r requirements/requirements.txt --no-index --find-links requirements
