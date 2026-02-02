#!/bin/bash

cd dwm
make install
cd ..

cd dmenu
make install
cd ..

cd st
make install
cd ..

pacman -Sy greetd xorg-xset python-pip chromium tk tcl base-devel feh xdotool ydotool
systemctl enable greetd.service
cp greetd_config.toml /etc/greetd/config.toml
cp .xinitrc ../

pip install --break-system-packages selenium PyAutoGUI pynput requests

mkdir -p keepalive
cd keepalive
curl -fsSLO https://github.com/stigoleg/keep-alive/releases/latest/download/keep-alive_Linux_x86_64.tar.gz
tar -xzf keep-alive_Linux_x86_64.tar.gz
cp keepalive /usr/local/bin/keepalive