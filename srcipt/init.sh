#!/bin/bash

sudo -s

#create dir to save file
cd /var/www/bl/;mkdir upload;cd upload;mkdir s m p o;mkdir m/i m/a;mkdir s/i s/a;mkdir p/a p/p;
chmod 777 /var/www/bl/upload/ -R

cd /var/log/; mkdir django; cd django; touch debug.log; chmod 777 debug.log
