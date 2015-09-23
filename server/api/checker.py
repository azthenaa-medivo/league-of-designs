if __name__ == '__main__':
    import requests
    import datetime
    from red_api import RiotAPI
    from time import sleep

    api = RiotAPI()

    last = {r: None for r in RiotAPI.realms}
    while True:
        for r in RiotAPI.realms:
            reds = api.get_red_posts(r).json()
            if reds[0] != last[r]:
                print('New red posts ! (realm : %s, date : %s)' %(r, datetime.datetime.today().isoformat()))
                api.store_red_posts(reds, r)
                del(reds[0]['region'])
                del(reds[0]['post_id'])
                last[r] = reds[0]
        sleep(10)
