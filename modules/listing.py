from time_utils import date2period

class InvalidAddressException(Exception):
    pass

# used to "uniquely" identify a property
class ListingKey(object):
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        self._keys = kwargs.keys()
        
    def __eq__(self, other):
        if set(self._keys) != set(other._keys):
            return False
        for key in self._keys:
            if getattr(self, key) != getattr(other, key):
                return False
        return True

    def __hash__(self):
        return reduce(lambda current, k: current ^ hash(getattr(self, k)), self._keys, 0)

    def __repr__(self):
        return "ListingKey[%s]" % ', '.join(["%s=%s" % (key, getattr(self, key)) for key in self._keys])

# represents a listing
class Listing(object):

    def __init__(self, first_dt = None, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        # there were some typos in the data....
        if self.city == "San Franisco" or self.city == "San Francsico":
            self.city = "San Francisco"
        self.eff_rent = int(self.eff_rent)
        self.sq_ft = int(self.sq_ft)
        self.zip_code = int(self.zip_code)
        self.bedrooms = int(self.bedrooms)
        
        parts = self.address.split()
        # more filtering for typos; normally you only expect the first "word" in an address to be a number, i.e. 56 Awesome St; something like "56 Awesome St 52 Hahaha" is not a real address
        for part in parts[1:]:
            try:
                int(part)
                #print "suspicious address %s" % self.address
                raise InvalidAddressException()
            except InvalidAddressException as iae:
                raise
                #print iae
            except Exception as e:
                #print e
                pass
        
        # perform some mangling on the address to correct for typos/differences betwene systems...:
        # replace street with st, avenue with ave, ave with av, boulevard with blvd, place with pl, and get rid of spaces
        self.address = self.address.lower().strip().strip(".,").replace("street", "st").replace("avenue", "ave").replace("ave", "av").replace("boulevard", "blvd").replace("place", "pl").replace(" ", "")

        # uniquely identify properties by combo of address, zip code, and sq ft
        # TODO: make this dynamic later
        self.key = ListingKey(address = self.address, zip_code = self.zip_code, sq_ft = self.sq_ft)

    # sets this listing's period (by default, each period is a month starting from first_dt
    # TODO: make period length dynamic
    def calc_period(self, first_dt):
        self.period = date2period(self.date_posted, first_dt)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s, %s, %s, %s" % (self.date_posted, self.address, self.sq_ft, self.eff_rent)
