echo [`date +"%m-%d-%y %T"`] Red Posts update
workon env1
python ~/server/api/red_api.py r
sh ~/server/api/postimport.sh