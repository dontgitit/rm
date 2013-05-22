import collections
import datetime
import re

import numpy as np

from time_utils import date2period, DATE_FORMAT
from listing import Listing, ListingKey
import index_calculator
import listing_parser

def sort_by_date(p1, p2):
    return cmp(p1.date_posted, p2.date_posted)

def _debug_print_dict(by_key):
    for key, by_period in by_key.iteritems():
        print key
        for period, entries in by_period.iteritems():
            print "\t%s %s" % (key.address, period)
            for entry in entries:
                print "\t\t%s" % entry

def avg_price(properties):
    return sum(map(lambda p: p.eff_rent, properties))/float(len(properties))

def generate_time_row(t1, t2, num_periods):
    l = [0] * num_periods
    if t1 != 0:
        l[t1-1] = -1
    l[t2-1] = 1
    return l

def get_ln_price_move(p1, p2):
    return np.log(float(p2)/p1)

# filter listings according to some filters - filters is a dict of field name to acceptable values
def filter_listings(listings, filters):
    for listing in listings:
        include = True
        for filter_name, filter_values in filters.iteritems():
            if not filter_values:
                continue
            if getattr(listing, filter_name) not in filter_values:
                include = False
                #print 'skipping %s (%s) because of %s=%s' % (listing, listing.bedrooms,  filter_name, filter_values)
                break
        if include:
            yield listing
           
# the heart and soul of the code...     
def compute_indexes(filters=None):
    if not filters:
        filters = list()
        
    # get all listings
    listings = listing_parser.get_all_listings()
    
    # filter by the selected criteria
    listings = filter_listings(listings, filters)

    # sort the listings by date posted, so we can get the number of periods (by getting the first and last). This also means later when we find repeat sales they'll be in order
    listings = sorted(listings, cmp=sort_by_date)

    # get the first date so we have it for our starting period...
    first_date = datetime.datetime.strptime(listings[0].date_posted, DATE_FORMAT)
    # ...and the last
    last_date = datetime.datetime.strptime(listings[-1].date_posted, DATE_FORMAT)
    # ...and the number of periods, so we know how many columns to have in our time matrix
    num_periods = date2period(last_date, first_date)

    # we're going to want to know the listing's period number several times, so precompute it once. this is kind of ugly. 
    # TODO: move this
    for listing in listings:
        listing.calc_period(first_date)

    # create a mapping: unique-listing -> periods -> [list of listings per periods (there can be multiple sales within a single period)]
    by_key = collections.OrderedDict()
    for listing in listings:
        if listing.key not in by_key:
            by_key[listing.key] = collections.OrderedDict()
        equivalent_listings_by_period = by_key[listing.key]
        if listing.period not in equivalent_listings_by_period:
            equivalent_listings_by_period[listing.period] = list()
        equivalent_listings_by_period[listing.period].append(listing)

    #_debug_print_dict(by_key)

    # setup matricies for the calculator
    times = list() # Z, the time matrix
    prices = list() # Y, the price matrix

    # populate our matricies
    for key, by_period in by_key.iteritems():
        periods = by_period.keys()
        for i in range(len(periods) - 1):
            t1 = periods[i]
            t2 = periods[i+1]
            # if there is more than one sale within one period, "guessimate" it as a single sale of price avg(prices)
            # TODO: maybe improve this?
            p1 = avg_price(by_period[t1])
            p2 = avg_price(by_period[t2])
            times.append(generate_time_row(t1, t2, num_periods)) # row in Z
            prices.append([get_ln_price_move(p1, p2)]) # row in Y
            
            #print "for period\n\t%s\n\t%s\n\t\t made\n\t\t%s\n\t\t%s" % (by_period[t1], by_period[t2], prices[-1], times[-1])
    
    # return the first and last dates, and the results!
    return first_date, last_date, index_calculator.calc(np.array(prices), np.array(times))
    
def main():
    print compute_indexes()

if __name__ == "__main__":
    main()
