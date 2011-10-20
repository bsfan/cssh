#!/bin/sh
pyversion=$(python -V 2>&1 |cut -d' ' -f2|cut -d'.' -f1,2)
if [ $pyversion != '2.7'  ]
then
    echo 'Python 2.7 is required'
fi
echo 'import Crypto'|python
if [ $? != '0' ]
then
    tar vxf pycrypto-2.3.tar.gz
    cd pycrypto-2.3
    python setup.py build
    python setup.py test
    if [ $? == '0' ]
    then 
        python setup.py install
    fi
echo $1
fi
rm -rf pycrypto-2.3
