import BreweryResources as br
from datetime import *

class GeoLocation:
    def __init__(location, full, lat, lon):
        location.full = full
        location.lat = lat
        location.lon = lon


Luppolo_loc = GeoLocation('49.2770256,-123.0806085', 49.2770256, -123.0806085)
Acres33_loc = GeoLocation('49.2639299,-123.1053388', 49.2639299, -123.1053388)
Parallel49_loc = GeoLocation('49.283834,-123.0643609', 49.283834, -123.0643609)
RnB_loc = GeoLocation('49.2672357,-123.1033402', 49.2672357, -123.1033402)
Bomber_loc = GeoLocation('49.2774278,-123.0745619', 49.2774278, -123.0745619)
Brassneck_loc = GeoLocation('49.2657634,-123.1004459', 49.2657634, -123.1004459)
StrangeFellows_loc = GeoLocation('49.2725296,-123.0778392', 49.2725296, -123.0778392)
Faculty_loc = GeoLocation('49.2686702,-123.1045352', 49.2686702, -123.1045352)


class Brewery:
    def __init__(Brewery, fullname, shortname, url, updated, address, location, logo, taps, fills, products):
        Brewery.name = fullname
        Brewery.shortname = shortname
        Brewery.url = url
        Brewery.updated = updated   # date taps, fills, products were retrieved
        Brewery.address = address
        Brewery.location = location
        Brewery.logo = logo
        Brewery.taps = taps
        Brewery.fills = fills
        Brewery.products = products


Luppolo = Brewery("Luppolo Brewing Co", "Luppolo", br.Luppolo_url, date(2009, 9, 21),
                  '1123 Venables St, Vancouver, BC V6A 2C6', Luppolo_loc, br.Luppolo_logo, [], [], [])

ThirtyThreeAcres = Brewery("33 Acres Brewing Co", "33 Acres", br.Acres33_url, date(2009, 9, 21),
                           "15 W 8th Ave, Vancouver, BC V5Y 1M8", Acres33_loc, br.Acres33_logo, [], [], [])

Parallel49 = Brewery("Parallel 49 Brewing Co", 'Parallel 49', br.Parallel49_url, date(2009, 9, 21),
                     '1950 Triumph St, Vancouver, BC V5L 1K5', Parallel49_loc, br.Parallel49_logo, [], [], [])

RnB = Brewery("R&B Brewing Co", "R&B", br.RnB_url, date(2009, 9, 21),
              '1-54 E 4th Ave, Vancouver, BC V5T 1E8', RnB_loc, br.RnB_logo, [], [], [])

Bomber = Brewery("Bomber Brewing Co", "Bomber", br.Bomber_url, date(2009, 9, 21),
                 '1488 Adanac St, Vancouver, BC V5L 3J7', Bomber_loc, br.Bomber_logo, [], [], [])

Brassneck = Brewery('Brassneck Brewery', 'Brassneck', br.Brassneck_url, date(2009, 9, 21),
                    '2148 Main St, Vancouver, BC V5T 3C5', Brassneck_loc, br.Brassneck_logo, [], [], [])

StrangeFellows = Brewery('Strange Fellows Brewing', 'Strange Fellows', br.StrangeFellows_url, date(2009, 9, 21),
                         '1345 Clark Dr, Vancouver, BC V5L 3K9', StrangeFellows_loc, br.StrangeFellows_logo, [], [], [])

Faculty = Brewery('Faculty Brewing Co.', 'Faculty', br.Faculty_url, date(2009, 9, 21),
                  '1830 Ontario St, Vancouver, BC V5T 2W6', Faculty_loc, br.Faculty_logo, [], [], [])

BREWERIES = [ThirtyThreeAcres, Bomber, Brassneck, Faculty, Luppolo, Parallel49, RnB, StrangeFellows]
# for testing: BREWERIES = [ThirtyThreeAcres, Bomber]
