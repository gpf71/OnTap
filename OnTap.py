import BreweryScraper as bs

# ======== Breweries & Logos URLS =========
Luppolo_url = 'https://luppolobrewing.ca/#today'
Luppolo_logo = 'https://tinyurl.com/y3lvyfjf'
Acres33_url = 'https://33acresbrewing.com/our-beers/'
Acres33_logo = 'https://33acresbrewing.com/app/themes/33acres/assets/images/logo.svg'
Parallel49_url = 'http://parallel49brewing.com/tasting_room'
Parallel49_logo = 'https://tinyurl.com/y3kuen5a'
RnB_url = 'https://www.randbbrewing.com/on-tap-today'
RnB_logo = 'https://tinyurl.com/y5mnjvbq'
Bomber_url = 'http://www.bomberbrewing.com/'
Bomber_logo = None
Faculty_url = 'https://www.instagram.com/facultytaps/'
Faculty_logo = 'https://tinyurl.com/y2dyjvrc'
Brassneck_url = "http://brassneck.ca/tasting-room/"
Brassneck_logo = None
StrangeFellows_url = "https://strangefellowsbrewing.com"
StrangeFellows_logo = 'https://tinyurl.com/y5aycm8f'


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
    def __init__(Brewery, fullname, shortname, url, address, location, logo, taps, fills, products):
        Brewery.name = fullname
        Brewery.shortname = shortname
        Brewery.url = url                   # today's taps
        Brewery.address = address
        Brewery.location = location
        Brewery.logo = logo
        Brewery.taps = taps
        Brewery.fills = fills
        Brewery.products = products



Luppolo = Brewery("Luppolo Brewing Co", "Luppolo", Luppolo_url,
                  '1123 Venables St, Vancouver, BC V6A 2C6', Luppolo_loc, Luppolo_logo, [], [], [])

ThirtyThreeAcres = Brewery("33 Acres Brewing Co", "33 Acres", Acres33_url, "15 W 8th Ave, Vancouver, BC V5Y 1M8",
                           Acres33_loc, Acres33_logo, [], [], [])

Parallel49 = Brewery("Parallel 49 Brewing Co", 'Parallel 49', Parallel49_url,
                     '1950 Triumph St, Vancouver, BC V5L 1K5', Parallel49_loc, Parallel49_logo, [], [], [])

RnB = Brewery("R&B Brewing Co", "R&B", RnB_url,
              '1-54 E 4th Ave, Vancouver, BC V5T 1E8', RnB_loc, RnB_logo, [], [], [])

Bomber = Brewery("Bomber Brewing Co", "Bomber", Bomber_url,
                 '1488 Adanac St, Vancouver, BC V5L 3J7', Bomber_loc, Bomber_logo, [], [], [])

Brassneck = Brewery('Brassneck Brewery', 'Brassneck', Brassneck_url,
                    '2148 Main St, Vancouver, BC V5T 3C5', Brassneck_loc, Brassneck_logo, [], [], [])

StrangeFellows = Brewery('Strange Fellows Brewing', 'Strange Fellows', StrangeFellows_url,
                         '1345 Clark Dr, Vancouver, BC V5L 3K9', StrangeFellows_loc, StrangeFellows_logo, [], [], [])

Faculty = Brewery('Faculty Brewing Co.', 'Faculty', Faculty_url, '1830 Ontario St, Vancouver, BC V5T 2W6',
                  Faculty_loc, Faculty_logo, [], [], [])

BREWERIES = [ThirtyThreeAcres, Bomber, Brassneck, Faculty, Luppolo, Parallel49, RnB, StrangeFellows]


all_breweries = [Luppolo, RnB]


# given string, return object
def getter(name_of_brewery_to_retrieve):
    # a_brewery = Brewery("",  "", "", "", "", "", [], [], [])
    for brewery in BREWERIES:
        if brewery.shortname == name_of_brewery_to_retrieve:
            return brewery
    return -1


def find_what_is_on_tap(brew_cos):

    for brew_co in brew_cos:
        if brew_co.shortname == 'Luppolo':
            bs.update_luppolo(brew_co)
        elif brew_co.shortname == '33 Acres':
            bs.update_acres33(brew_co)
        elif brew_co.shortname == 'Parallel 49':
            bs.update_parallel(brew_co)
        elif brew_co.shortname == 'R&B':
            bs.update_rnb(brew_co)
        elif brew_co.shortname == 'Bomber':
            bs.update_bomber(brew_co)
        elif brew_co.shortname == 'Brassneck':
            bs.update_brassneck(brew_co)
        elif brew_co.shortname == 'Strange Fellows':
            bs.update_strangefellows(brew_co)
        elif brew_co.shortname == 'Faculty':
            bs.update_faculty(brew_co)
        else:
            print"There was an error"


def print_todays_taps(brew_cos, beer_list_name):
    for brew_co in brew_cos:
        print"========================="
        print brew_co.name
        print"=========================\n"
        if beer_list_name == 'fills':
            print"Growler Fills"
            bs.print_beer_list(brew_co.fills)
        elif beer_list_name == 'taps':
            print"On Tap"
            bs.print_beer_list(brew_co.taps)
        else:
            print"Bottles & Cans"
            bs.print_beer_list(brew_co.products)


if __name__ == "__main__":
    brew_cos = BREWERIES
    find_what_is_on_tap(brew_cos)
    print_todays_taps(brew_cos, 'fills')


def main(brewery_name, command):

    # retrieve appropriate Brewery
    the_brewery = getter(brewery_name)
    if the_brewery == -1:
        print "There was an error."

    # get updates
    brew_cos = []
    brew_cos.append(the_brewery)
    find_what_is_on_tap(brew_cos)

    return bs.prepare_report(brew_cos, command)
