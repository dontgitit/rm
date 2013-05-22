import json

#from applications.rent.modules import listing_parser
import listing_parser
import indexer
import time_utils

FILTERS = ['city', 'state', 'zip_code', 'bedrooms', 'sq_ft']

def index():
    listings = listing_parser.get_all_listings()

    filters = dict((k, sorted(set(map(lambda p: getattr(p, k), listings)))) for k in FILTERS)

    print listings[0]
    for k, v in filters.iteritems():
        print "%s=%s" % (k, v)

    options = dict()
    options['filters'] = filters
    return options

def compute_index():
    print request.vars
    params = json.loads(request.vars.params)
    print params
    filters = dict(map(lambda (k, v): (k, map(json.loads, v) if v else None), params.iteritems()))
    print filters
    for filter_name in FILTERS:
        print "%s: %s" % (filter_name, filters[filter_name])
    first_dt, last_dt, indexes = indexer.compute_indexes(filters=filters)
    return response.json(dict(indexes=map(lambda (index, val): (time_utils.period2jsdate(index, first_dt), val), enumerate(map(lambda x: x[0], indexes.tolist())))))
