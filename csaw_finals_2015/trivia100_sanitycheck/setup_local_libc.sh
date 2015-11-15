#!/bin/sh
cp libc.so.6_3f6aaa980b58f7c7590dee12d731e099 libc-9.99.so
ln -s libc-9.99.so libc.so.6 

export LD_LIBRARY_PATH=$(pwd)
bash

rm ./libc.so.6 ./libc-9.99.so
