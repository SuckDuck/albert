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

pacman -Sy greetd xorg-xset python-pip chromium
systemctl enable greetd.service
cp greetd_config.toml /etc/greetd/config.toml
cp .xinitrc ../

pip install --break-system-packages selenium PyAutoGUI