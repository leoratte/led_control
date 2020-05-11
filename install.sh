#!/bin/bash
apt install pigpio nginx python3
pip3 install websockets
mkdir /opt/led_control
cp -t=/opt/led_control start.py control.py led.py animation.py util.py config.json
cp led_control.service /etc/systemd/system
systemctl enable pigpiod
systemctl start pigpiod
systemctl enable led_control.service
systemctl start led_control.service
cp html/* /var/www/html
service nginx start
