cd /root/league-of-designs/server/maintenance
python switch.py 1
cd /root/league-of-designs
git remote update
git reset --hard origin/master
echo 'DEBUG = False' > /root/league-of-designs/lod_django/league_of_designs/prod.py
cd /root/league-of-designs/server/django/
python generate_key.py
cd /root/league-of-designs/lod_django
python manage.py collectstatic
apache2ctl restart
cd /root/league-of-designs/server/maintenance
python switch.py 0
