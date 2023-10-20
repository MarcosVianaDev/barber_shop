copy barber_api.service file
to /etc/systemd/system/ folder

active/enable the service
run sudo systemctl start firstproject
run sudo systemctl enable firstproject

copy barber_api file
to /etc/nginx/sites-enabled folder

cd /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/barber_api barber_api

run sudo service nginx restart

insert 192.168.1.31 barber_api in sudo nano /etc/hosts

run curl barber_api