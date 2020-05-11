#!/bin/bash
apt install pigpio nginx python3 python3-pip -y
pip3 install websockets
pip3 install pigpio
mkdir /opt/led_control
cp -t /opt/led_control led.py start.py animation.py control.py util.py config.json
cp led_control.service /etc/systemd/system
systemctl enable pigpiod
systemctl start pigpiod
systemctl enable led_control.service
systemctl start led_control.service
cp html/* /var/www/html
service nginx start
