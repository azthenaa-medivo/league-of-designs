workon env1
python /root/league-of-designs/server/api/red_api.py r
sh /root/league-of-designs/server/api/postimport.sh
echo [`date +"%m-%d-%y %T"`] Red Posts Update Okay >> ~/crontab.log