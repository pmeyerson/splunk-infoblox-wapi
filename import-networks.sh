#!/bin/bash
# Schedule this via cron
# EX: #*/5 * * * 1-5 /home/user/import-networks.sh >> /home/user/cron.log 2>&1

python3 /home/user/import-networks.py  #replace with path to import-networks.py
cp /home/user/networks.csv /opt/splunk/etc/apps/search/lookups/  # ensure path is correct to splunk home
# chown splunk:splunk /opt/splunk/etc/apps/search/lookups/networks.csv   # Should execute as splunk user


