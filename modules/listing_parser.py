import csv

from listing import Listing

# parse each line of the input into a dictionary
def parse(path):
    with open(path, 'rb') as fp:
        headers = csv.reader(fp).next()
        reader = csv.DictReader(fp, fieldnames=headers)
        return [line for line in reader]

# return a list of Listings
def get_all_listings():
    listings = list()
    for line in parse("../sf_mf.csv"):
        # we can get an exception trying to create the listing if the fields are incorrect/missing
        try:
            listings.append(Listing(**line))
        except Exception as e:
            #print e
            pass
    return listings

def main():
    print parse("./sf_mf.csv")

if __name__ == "__main__":
    main()
