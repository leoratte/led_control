#!/bin/bash
use_webpage=false
read -p "Do you want to enable a local webpage(y/N)?" yn
case $yn in
    [Yy]* ) use_webpage=true;;
    * ) use_webpage=false;;
esac

apt install pigpio python3 python3-pip -y
if $use_webpage
  then
    apt install nginx -y
fi
pip3 install websockets
pip3 install pigpio
mkdir /opt/led_control
cp -t /opt/led_control led.py start.py animation.py control.py util.py config.json animations.py
cp led_control.service /etc/systemd/system
systemctl enable pigpiod
systemctl start pigpiod
systemctl enable led_control
systemctl start led_control
if $use_webpage
  then
    wget https://github.com/leoratte/led_control_app/releases/download/v0.2.0-alpha/www.zip
    mkdir www
    unzip -d www www.zip
    cp -r www/* /var/www/html
    systemctl enable nginx
    systemctl start nginx
fi
