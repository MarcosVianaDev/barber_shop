copy barber_shop.service file
to /etc/systemd/system/ folder

active/enable the service
run sudo systemctl start barber_shop
run sudo systemctl enable barber_shop

sudo systemctl daemon-reload
sudo systemctl enable barber_shop
sudo systemctl start barber_shop

copy barber_shop file
to /etc/nginx/sites-enabled folder

cd /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/barber_shop barber_shop

run sudo service nginx restart

insert 192.168.1.31 barber_shop in sudo nano /etc/hosts

run curl barber_shop