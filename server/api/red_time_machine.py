"""Recovers every redpost you want as long as it was posted after the Boards migration (~08/09/2013)."""

if __name__ == '__main__':
    import argparse
    import logging as log
    import time
    from datetime import datetime, timedelta
    from red_api import RiotAPI

    def mkdate(datestr):
        return datetime(*(time.strptime(datestr, '%Y-%m-%d'))[:6])

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--increment', nargs='?', type=int, default=10, help="Specify the increment (in minutes) for each step. Default is 10 minutes.")
    parser.add_argument('-e', '--end', nargs='?', type=mkdate, default=datetime.min, help="Specify the stop date (format YYYY-MM-DD). By default, ends when request result is empty.")
    parser.add_argument('-s', '--start', nargs='?', type=mkdate, default=datetime.utcnow(), help="Specify the start date (format YYYY-MM-DD). By default, starts now.")
    parser.add_argument('-v', '--verbose', help="increase output verbosity", action='store_true')
    args = parser.parse_args()
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    current = args.start
    log.info('Start date : ' + current.isoformat())
    log.info('End date : ' + args.end.isoformat())
    log.info('Check every %d minutes' % args.increment)
    api = RiotAPI()
    # stats
    loops = 0
    while True:
        loops += 1
        log.info("Loop %d, time is %s" %(loops, current.isoformat()))
        res = api.get_red_posts_and_store(parameters={'created_to': current.isoformat()})
        if res == 0 or current < args.end:
            break
        current -= timedelta(minutes=args.increment)
    print('Done. %d loops.' % loops)