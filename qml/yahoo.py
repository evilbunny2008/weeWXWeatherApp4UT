""" Process Yahoo forecasts """

import os
import time
from bs4 import BeautifulSoup
import day
import forecasts
import main

def process_day(tmpstr, startid, metric):
    """ Extract data based on the id number """

    last_ts = int(time.time())

    if startid == 196:
        endid = startid + 24
    else:
        endid = startid + 19

    tmpstr = tmpstr.split('<span data-reactid="' + str(startid) + '">', 1)[1]
    tmpstr, rest = tmpstr.split('data-reactid="' + str(endid) + '">', 1)
    dow = tmpstr.split('</span>', 1)[0].strip()
    last_ts = timestamp = forecasts.convert_day_to_ts(dow, last_ts)
    text = tmpstr.split('<img alt="', 1)[1].split('"', 1)[0].strip()
    icon = tmpstr.split('<img alt="', 1)[1].split('"', 1)[1]
    icon = icon.split('src="', 1)[1].split('"', 1)[0].strip()
    # pop = tmpstr.split('Precipitation: ', 1)[1].split('"', 1)[0].strip()
    maxtemp = tmpstr.split('data-reactid="' + str(startid + 10)  + '">', 1)[1]
    maxtemp = maxtemp.split('</span>', 1)[0]
    mintemp = tmpstr.split('data-reactid="' + str(startid + 13)  + '">', 1)[1]
    mintemp = mintemp.split('</span>', 1)[0]

    soup = BeautifulSoup(maxtemp, "html.parser")
    maxtemp = soup.text[:-1]
    soup = BeautifulSoup(mintemp, "html.parser")
    mintemp = soup.text[:-1]

    if metric == "1":
        maxtemp = str(round((int(maxtemp) - 32) * 5 / 9)) + "&deg;C"
        mintemp = str(round((int(mintemp) - 32) * 5 / 9)) + "&deg;C"
    else:
        maxtemp += "&deg;F"
        mintemp += "&deg;F"

    myday = day.Day()

    myday.day = dow
    myday.timestamp = timestamp
    myday.text = text
    myday.icon = icon
    myday.min = mintemp
    myday.max = maxtemp

    return myday, rest

def check_files(url):
    """ Download missing icons as needed """

    file_name = os.path.basename(url)
    if not os.path.isfile(main.CACHEBASE + "/" + "yahoo-" + file_name):
        print("File not found: " + "yahoo-" + file_name)
        print("downloading...")

        new_url = 'http://delungra.com/weewx/yahoo-missing.php?filename=' + file_name
        ret = main.download(new_url)
        if ret[0] is True:
            main.write_binary("yahoo-" + file_name, ret[1], main.CACHEBASE)
        else:
            return [False, "Failed to successfully download icon"]

    return [True, "yahoo-" + file_name]

def process_yahoo(data):
    """ Process Yahoo forecast """

    metric = main.get_string("metric", "1")

    days = ""

    bits = data.split('data-reactid="7">', 7)
    print(bits)
    town, rest = bits[7].split('</h1>', 1)
    country, rest = rest.split('data-reactid="8">', 1)[1].split('</div>', 1)
    desc = town.strip() + ", " + country.strip()

    daynums = [196, 221, 241, 261, 281, 301, 321, 341, 361, 381]
    for startid in daynums:
        myday, rest = process_day(rest, startid, metric)
        ret = check_files(myday.icon)
        if ret[0] is True:
            myday.icon = ret[1]
        else:
            return ret

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]
