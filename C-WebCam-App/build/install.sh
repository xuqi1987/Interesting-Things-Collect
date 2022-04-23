#!/bin/sh
sudo apt-get install yasm

# ffmpeg install shell script.
# 1. download source
test -f ffmpeg-1.0.tar.gz || wget http://www.ffmpeg.org/releases/ffmpeg-1.0.tar.gz &&

# 2. tar and cd dir.
tar -xzvf ffmpeg-1.0.tar.gz && cd ffmpeg-1.0 &&

# 3.config
# 配置过程中缺什么，下载什么，直到配置完成。例如提示缺少yasm:apt-get install yasmapt-get install yasm
./configure --enable-gpl --enable-shared --enable-pthreads &&


# 4. build
make &&

# 5. install
make install &&
make install-libs


sudo locale-gen
sudo dpkg-reconfigure locales

sudo apt-get install libx11-dev
sudo apt-get install libxtst-dev
sudo apt-get install libavcodec-dev libswscale-dev libx264-dev

