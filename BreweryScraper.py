from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from datetime import *
import BreweryResources as br
import json
import requests

#  ====== Global Helper Functions =========


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def combine_name_style_abv(fill_name, fill_style, fill_abv):
    list_of_beers = []
    for (n, s, a) in zip(fill_name, fill_style, fill_abv):
        beer = n + " " + s + " " + a + "\n"
        list_of_beers.append(beer)
    return list_of_beers


def combine_name_abv(fill_name, fill_abv):
    list_of_beers = []
    for (n, a) in zip(fill_name, fill_abv):
        beer = n + " " + a + "\n"
        list_of_beers.append(beer)
    return list_of_beers


def instagram_login():
    driver = webdriver.Chrome()
    driver.get(br.Instagram)
    usernameinput = driver.find_elements_by_css_selector('form input')[0]
    passwordinput = driver.find_elements_by_css_selector('form input')[1]
    usernameinput.send_keys(br.username)
    passwordinput.send_keys(br.password)
    return driver


def add_line_break(beer_list):
    formatted_list = []
    for beer in beer_list:
        formatted_list.append(beer + "\n")
    return formatted_list


# ========= Luppolo Brewing ===========


def update_luppolo(brew_co):
    # information is already current
    if brew_co.updated == date.today():
        return
    page = requests.get(brew_co.url)
    tree = html.fromstring(page.content)
    brew_co.fills = tree.xpath('//*[@id="today"]/div/div[1]/div[1]/div/p[2]/text()')
    add_line_break(brew_co.fills)
    brew_co.taps = tree.xpath('//*[@id="today"]/div/div[1]/div[1]/div/p[3]/text()')
    add_line_break(brew_co.taps)
    brew_co.products = tree.xpath('//*[@id="today"]/div/div[1]/div[1]/div/p[4]/text()')
    add_line_break(brew_co.products)
    brew_co.updated = date.today()

# # ========= 33 Acres Brewing Co. ==========


def update_acres33(brew_co):
    # information is already current
    if brew_co.updated == date.today():
        return
    page = requests.get(brew_co.url)
    tree = html.fromstring(page.content)

    beers = tree.xpath('//*[@id="beers"]/div[1]/div[1]/div[2]/h1/text()')
    more_beers = tree.xpath('//*[@id="beers"]/div/div/div/a')
    for node in more_beers:
        beers.append(node.attrib["alt"])
    available = tree.xpath('//*[@id="beers"]/div/div/div/h2/text()')

    for (beer, avail) in zip(beers, available):
        if "Glasses" in avail:
            brew_co.taps.append(beer)
        if "Growler" in avail:
            brew_co.fills.append(beer)
        if "Bottled" in avail:
            brew_co.products.append(beer)
    brew_co.updated = date.today()


# ===== Parallel 49 Brewing =============


def update_parallel(brew_co):
    # information is already current
    if brew_co.updated == date.today():
        return

    # On Tap & Fills
    page = requests.get(brew_co.url)
    tree = html.fromstring(page.content)

    beernames = tree.xpath('//*[@class="beer-details--inner"]/span[1]/text()')
    beertypes = tree.xpath('//*[@class="beer-details--inner"]/span[2]/text()')
    beerabv = tree.xpath('//*[@class="alc-percentage"]/text()')

    brew_co.taps = combine_name_style_abv(beernames, beertypes, beerabv)
    brew_co.fills = brew_co.taps

    # Cans & Bottles
    driver = webdriver.Chrome()
    driver.get(br.parallel49_product_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    beer_containers = soup.find_all('div', {'class': 'our-beers-container container'})
    for container in beer_containers:
        beer_list = []
        beer_list.append(container.find('h3').text + ": ")
        beers = container.find_all('a')
        for item in beers:
            name = item.text
            names = name.split('\n')
            name = names[3] + '(' + names[2] + ')'
            beer_list.append(name)
        brew_co.products.append(beer_list)
    brew_co.updated = date.today()


# ======== R&B Brewing ============


def update_rnb(brew_co):
    # information is already current
    if brew_co.updated == date.today():
        return
    page = requests.get(brew_co.url)
    tree = html.fromstring(page.content)

    beers_ids = []

    # text descriptions unreliable; grab beer label images and match to beer names
    beerimage_ids = tree.xpath('//*[@class="style-j23ppv2aimageItem_imgBorder"]/div/img')

    for image in beerimage_ids:
        beers_ids.append(image.attrib["id"])

    for (id, name) in zip(br.rnb_image_ids, br.rnb_names):
        if id in beers_ids:
            brew_co.taps.append(name)

    brew_co.fills = brew_co.taps
    brew_co.products = ['No Information Available']
    brew_co.updated = date.today()


# ======= Bomber Brewing =========


def update_bomber(brew_co):
    # information is already current
    if brew_co.updated == date.today():
        return
    # otherwise, get the page
    driver = webdriver.Chrome()
    driver.get(brew_co.url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # beer information is in three containers
    beer_containers = soup.find_all('div', {'class': 'section-items-container'})

    i = 0
    for container in beer_containers:
        # list of beers in the container
        items = container.find_all('div', {'class': "item-bg-color menu-item"})
        if i == 0:
            brew_co.fills = bomber_helper(items)
        if i == 1:
            brew_co.taps = bomber_helper(items)
        if i == 2:
            brew_co.products = bomber_helper(items)
        i += 1
    brew_co.updated = date.today()


def bomber_helper(beer_list):
    name_list = []
    style_list = []
    abv_list = []
    # parse name, style, abv
    for bomb_beers in beer_list:
        name = bomb_beers.span.contents[1]  # using contents[] bc don't want the nested/child nodes
        name_list.append(name)
        style = bomb_beers.find('span', {'class': 'beer-style'}).text
        style_list.append(style)
        abv = bomb_beers.find('span', {'class': 'abv'}).text
        abv_list.append(abv)
    return combine_name_abv(name_list, abv_list)


# ======= Brassneck ========r


def update_brassneck(brew_co):
    # information is already current
    if brew_co.updated == date.today():
        return
    # otherwise, update
    driver = webdriver.Chrome()
    driver.get(brew_co.url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # get everything that is on tap
    on_tap_container  = soup.find('div', {'id': 'ontap-footer'})
    on_tap_items = on_tap_container.find_all('a')
    brew_co.taps = brassneck_helper(on_tap_items)
    brew_co.fills = brew_co.taps

    # get everything that is available in cans
    cans_container = soup.find('div', {'id': 'fills-footer'})
    items_in_cans = cans_container.find_all('a')
    brew_co.products = brassneck_helper(items_in_cans)

    brew_co.updated = date.today()

def brassneck_helper(item_list):
    list_of_names = []
    list_of_styles = []
    list_of_abv = []
    # parse name, style, abv; clean up where necessary
    for beers in item_list:
        name = beers.span.text
        list_of_names.append(name)
        temp = beers.contents[1].text
        temp = remove_prefix(temp, "\nkind: ")
        temps = temp.partition("\nabv: ")
        style = temps[0]
        abv = temps[2][:-2]
        list_of_styles.append(style)
        list_of_abv.append(abv)
    return combine_name_style_abv(list_of_names, list_of_styles, list_of_abv)


# ====== Strange Fellows Brewing =======


def update_strangefellows(brew_co):
    # information is already current
    if brew_co.updated == date.today():
        return
    # otherwise, update
    driver = webdriver.Chrome()
    driver.get(brew_co.url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # find info on beers
    strange_beers = soup.find_all('div', {'class': 'col-md-4'})

    i = 0
    for category in strange_beers:
        # get list of available beers
        beers_in_category = []
        for a_tag in category.find_all('a'):
            beers_in_category.append(a_tag.text)
        if i == 0:
            brew_co.fills = strange_fellows_helper(beers_in_category)
            brew_co.taps = brew_co.fills
        if i == 1:
            brew_co.products = strange_fellows_helper(beers_in_category)
        if i == 2:
            brew_co.products.extend(strange_fellows_helper(beers_in_category))
        i += 1
    brew_co.updated = date.today()


def strange_fellows_helper(beers_in_cat):
    b_name = []
    b_style = []
    b_abv = []
    # parse list of beer info
    x = 0
    for beers in beers_in_cat:
        if x % 2 == 0:
            name = remove_prefix(beers, '\n')
            name = name[:-2]
            name = name.strip()
            b_name.append(name)
        else:
            parts = beers.split('|')
            style = remove_prefix(parts[0], '\n')
            style = style.strip()
            abv = remove_prefix(parts[1], '\n\n')
            abv = abv[:-1].strip()
            b_style.append(style)
            b_abv.append(abv)
        x += 1
    return combine_name_style_abv(b_name, b_style, b_abv)


# # ========= Faculty Brewing ============


def update_faculty(brew_co):
    # information is already current
    if brew_co.updated == date.today():
        return
    # otherwise, navigate to instagram page 'facultytaps', select most recent post
    driver = instagram_login()
    driver.get(brew_co.url)
    first_post = driver.find_element_by_css_selector("#react-root > section > main > div > div._2z6nI "
                                                     "> article > div > div > div > div > a")
    first_post.click()

    # grab the script that contains json object, trim everything else
    target = driver.find_element_by_xpath('/html/body/script[1]')
    mytarget = target.get_attribute('text')
    mytarget = remove_prefix(mytarget, 'window._sharedData = ')
    mytarget = mytarget[:-1]
    driver.quit()

    # load json object, navigate to desired information
    acquired = json.loads(mytarget)
    navigating = acquired['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][0]
    taps_info = navigating['node']['edge_media_to_caption']['edges'][0]['node']['text']

    # extract beer information
    breaking = taps_info.split('\n')

    i = 2       # skip date, skip 'Glasses and Growler Fills:'
    while breaking[i] != '':
        brew_co.fills.append(breaking[i])
        brew_co.taps.append(breaking[i])
        i += 1

    i += 2      # skip blank, skip 'Glasses Fills Only:'
    while breaking[i] != '':
        brew_co.taps.append(breaking[i])
        i += 1

    brew_co.products = ['No Information Available']
    brew_co.updated = date.today()


