import BreweryScraper as bs
import Brewery as b
from datetime import date


# given string, return appropriate Brewery object
def getter(name_of_brewery_to_retrieve):
    for brewery in b.BREWERIES:
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
            print_beer_list(brew_co.fills)
        elif beer_list_name == 'taps':
            print"On Tap"
            print_beer_list(brew_co.taps)
        else:
            print"Bottles & Cans"
            print_beer_list(brew_co.products)
        print"\n"


def prepare_report(brew_cos, beer_list_name):
    # prep report
    todays_report = []
    today = str(date.today())
    if beer_list_name == 'fills':
        todays_report.append(today + " GROWLER FILLS: ")
    elif beer_list_name == 'taps':
        todays_report.append(today + " ON TAP: ")
    else:
        todays_report.append(today + " BOTTLES & CANS: ")
    # add contents
    for brew_co in brew_cos:
        todays_report.append("`" + brew_co.name + "`" + ":")
        todays_report.extend(getattr(brew_co, beer_list_name))
    return todays_report


def print_beer_list(beer_list):
    print"-------------------------"
    for b in beer_list:
        print b


if __name__ == "__main__":
    brew_cos = b.BREWERIES
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

    return prepare_report(brew_cos, command)
