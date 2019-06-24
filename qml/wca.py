""" weather.gc.ca forecasts """

import datetime
import html
import time
from bs4 import BeautifulSoup
import day
import main

FR_MONTHS = {'janvier':'January', 'février':'February', 'mars':'March', 'avril':'April',
             'mai':'May', 'juin':'June', 'juillet':'July', 'aout':'August',
             'septembre':'September', 'octobre':'October', 'novembre':'November',
             'décembre':'December'}

def process_wca(data):
    """ Process forecast for weather.gc.ca """

    metric = main.get_string("metric", "1")
    use_icons = main.get_string("use_icons", "0")

    days = ""
    last_ts = 0

    obs = data.split("Forecast issued: ", 1)[1].strip()
    obs = obs.split("</span>", 1)[0].strip()

    i = 0
    j = obs.index(":")
    hour = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    minute = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    # ampm = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    # TZ = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    # DOW = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    date = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    month = obs[i:j]
    i = j + 1
    j = len(obs)
    year = obs[i:j]

    # obs = hour + ":" + minute + " " + ampm + " " + date + " " + month + " " + year
    obs = year + "-" + month + "-" + date + " " + hour + ":" + minute# + " " + ampm
    # "h:mm aa d MMMM yyyy"
    # last_ts = timestamp = time.mktime(time.strptime(obs, '%Y-%B-%d %I:%M %p'))
    last_ts = timestamp = time.mktime(time.strptime(obs, '%Y-%B-%d %I:%M'))
    date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
    year = datetime.datetime.fromtimestamp(last_ts).strftime("%Y")

    desc = data.split('<dt>Observed at:</dt>', 1)[1]
    desc = desc.split('<dd class="mrgn-bttm-0">', 1)[1].split("</dd>", 1)[0].strip()

    data = data.split('<div class="div-table">', 1)[1].strip()
    data = data.split('<section><details open="open" class="wxo-detailedfore">', 1)[0].strip()
    data = data[:-7].strip()

    doc = BeautifulSoup(data, "html.parser")
    div = doc.find_all("div", class_="div-column")

    j = 0
    while j < len(div):
        myday1 = day.Day()
        myday2 = day.Day()

        head1 = head2 = ""
        content1 = content2 = ""
        img1 = img2 = ""
        maxtemp = mintemp = ""
        pop1 = "0%"
        pop2 = "0%"

        if '<div class="div-row div-row1 div-row-head greybkgrd">' not in str(div[j]):
            head1 = str(div[j]).split('<div class="div-row div-row1 div-row-head">', 1)[1]
            head1 = head1.split("</div>", 1)[0].strip()
            tmpday = head1.split("<br/>", 1)[1]
            month = tmpday.split('title="', 1)[1].split('"', 1)[0].strip()
            tmpday = tmpday.split("\xa0", 1)[0].strip()
            date = tmpday + " " + month + " " + year
            timestamp1 = time.mktime(time.strptime(date, '%d %B %Y'))

            maxtemp = str(div[j]).split('title="max">', 1)[1].split("°", 1)[0].strip()
            if metric == "1":
                maxtemp += "&deg;C"
            else:
                maxtemp = str(round(int(maxtemp) * 9 / 5 + 32)) + "&deg;F"

            mystr = str(div[j]).split('<div class="div-row div-row2 div-row-data">', 1)[1]
            mystr = mystr.split('</div>', 1)[0].strip()

            if '<p class="mrgn-bttm-0 pop text-center" title="' in mystr:
                pop1 = mystr.split('<small>', 1)[1].split('</small>', 1)[0].strip()

        if '<div class="div-row div-row3 div-row-head greybkgrd">' not in str(div[j]):
            if '<div class="div-row div-row3 div-row-head" ' in str(div[j]):
                head2 = str(div[j])
                head2 = head2.split('<div class="div-row div-row3 div-row-head" title="', 1)[1]
                head2 = head2.split("</div>", 1)[0].split('">', 1)[0].strip()
                bits = head2.split("\xa0")
                tmpday = bits[1]
                month = bits[2]
                date = tmpday + " " + month + " " + year
                timestamp2 = time.mktime(time.strptime(date, '%d %B %Y'))
            else:
                head2 = str(div[j]).split('<div class="div-row div-row3 div-row-head">', 1)[1]
                head2 = head2.split("</div>", 1)[0].strip()
                timestamp2 = last_ts

            mintemp = str(div[j]).split('title="min">', 1)[1].split("°", 1)[0].strip()
            if metric == "1":
                mintemp += "&deg;C"
            else:
                mintemp = str(round(int(mintemp) * 9 / 5 + 32)) + "&deg;F"

            mystr = str(div[j]).split('<div class="div-row div-row4 div-row-data">', 1)[1]
            mystr = mystr.split('</div>', 1)[0].strip()

            if '<p class="mrgn-bttm-0 pop text-center" title="' in mystr:
                pop2 = mystr.split('<small>', 1)[1].split('</small>', 1)[0].strip()

        srcs = [img['src'] for img in div[j].find_all('img')]
        alts = [alt['alt'] for alt in div[j].find_all('img')]

        if head1 != "":
            count = len(srcs)
            if count > 0:
                img1 = srcs[0]
                content1 = alts[0]

            if head2 != "":
                if count > 1:
                    img2 = srcs[1]
                    content2 = alts[1]
        else:
            count = len(srcs)
            if count > 0:
                img2 = srcs[0]
                content2 = alts[0]

        if head1 != "":
            img1 = img1[14:-4]
            if use_icons == "1":
                img1 = "wca" + img1 + ".png"
            else:
                if img1 == "26":
                    img1 = "flaticon-thermometer"
                else:
                    img1 = "wi wi-weather-gc-ca-" + img1

            myday1.text = content1
            myday1.icon = img1
            myday1.max = maxtemp
            last_ts = myday1.timestamp = timestamp1
            myday1.day = datetime.datetime.fromtimestamp(myday1.timestamp).strftime("%A")
            myday1.min = pop1

            days += str(myday1) + ","

        if head2 != "":
            img2 = img2[14:-4]
            if use_icons == "1":
                img2 = "wca" + img2 + ".png"
            else:
                if img2 == "26":
                    img2 = "flaticon-thermometer"
                else:
                    img2 = "wi wi-weather-gc-ca-" + img2

            myday2.text = content2
            myday2.icon = img2
            myday2.max = mintemp
            last_ts = myday2.timestamp = timestamp2
            myday2.day = datetime.datetime.fromtimestamp(myday2.timestamp).strftime("%A")
            myday2.day += " Night"
            myday2.min = pop2

            days += str(myday2) + ","

        j += 1

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_wcafr(data):
    """ Process forecast for weather.gc.ca in French """

    metric = main.get_string("metric", "1")
    use_icons = main.get_string("use_icons", "0")

    days = ""
    last_ts = 0

    obs = data.split("Prévisions émises à : ", 1)[1].strip()
    obs = obs.split("</span>", 1)[0].strip()

    # 16h00 HAP le vendredi 24 mai 2019

    i = 0
    j = obs.index("h")
    hour = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    minute = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    # ampm = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    # le
    i = j + 1
    j = obs.index(" ", i)
    # DOW = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    date = obs[i:j]
    i = j + 1
    j = obs.index(" ", i)
    month = obs[i:j]
    i = j + 1
    j = len(obs)
    year = obs[i:j]

    month = FR_MONTHS[month]

    # obs = hour + ":" + minute + " " + ampm + " " + date + " " + month + " " + year
    obs = year + "-" + month + "-" + date + " " + hour + ":" + minute# + " " + ampm
    # "h:mm aa d MMMM yyyy"
    # last_ts = timestamp = time.mktime(time.strptime(obs, '%Y-%B-%d %I:%M %p'))
    last_ts = timestamp = time.mktime(time.strptime(obs, '%Y-%B-%d %H:%M'))
    date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
    year = datetime.datetime.fromtimestamp(last_ts).strftime("%Y")

    desc = data.split('<dt>Enregistrées à :</dt>', 1)[1]
    desc = desc.split('<dd class="mrgn-bttm-0">', 1)[1].split("</dd>", 1)[0].strip()

    data = data.split('<div class="div-table">', 1)[1].strip()
    data = data.split('<section><details open="open" class="wxo-detailedfore">', 1)[0].strip()
    data = data[:-7].strip()

    doc = BeautifulSoup(data, "html.parser")
    div = doc.find_all("div", class_="div-column")

    j = 0
    while j < len(div):
        myday1 = day.Day()
        myday2 = day.Day()

        head1 = head2 = ""
        content1 = content2 = ""
        img1 = img2 = ""
        maxtemp = mintemp = ""
        pop1 = "0%"
        pop2 = "0%"

        if '<div class="div-row div-row1 div-row-head greybkgrd">' not in str(div[j]):
            head1 = str(div[j]).split('<div class="div-row div-row1 div-row-head">', 1)[1]
            head1 = head1.split("</div>", 1)[0].strip()
            tmpday = head1.split("<br/>", 1)[1]
            month = tmpday.split('title="', 1)[1].split('"', 1)[0].strip()
            tmpday = tmpday.split(" ", 1)[0].strip()
            month = FR_MONTHS[month]
            date = tmpday + " " + month + " " + year
            timestamp1 = time.mktime(time.strptime(date, '%d %B %Y'))

            maxtemp = str(int(str(div[j]).split('title="max">', 1)[1].split("°", 1)[0].strip()))
            if metric == "1":
                maxtemp += "&deg;C"
            else:
                maxtemp = str(round(int(maxtemp) * 9 / 5 + 32)) + "&deg;F"

            mystr = str(div[j]).split('<div class="div-row div-row2 div-row-data">', 1)[1]
            mystr = mystr.split('</div>', 1)[0].strip()

            if '<p class="mrgn-bttm-0 pop text-center" title="' in mystr:
                pop1 = mystr.split('<small>', 1)[1].split('</small>', 1)[0].strip()

        if '<div class="div-row div-row3 div-row-head greybkgrd">' not in str(div[j]):
            if '<div class="div-row div-row3 div-row-head" ' in str(div[j]):
                head2 = str(div[j])
                head2 = head2.split('<div class="div-row div-row3 div-row-head" title="', 1)[1]
                head2 = head2.split("</div>", 1)[0].split('">', 1)[0].strip()
                # print(head2)
                # Dimanche soir et nuit, 26 mai
                # nuit,\xa026\xa0mai
                bits = head2.split("\xa0")
                tmpday = bits[-2]
                month = bits[-1]
                month = FR_MONTHS[month]
                date = tmpday + " " + month + " " + year
                timestamp2 = time.mktime(time.strptime(date, '%d %B %Y'))
            else:
                head2 = str(div[j]).split('<div class="div-row div-row3 div-row-head">', 1)[1]
                head2 = head2.split("</div>", 1)[0].strip()
                timestamp2 = last_ts

            mintemp = str(int(str(div[j]).split('title="min">', 1)[1].split("°", 1)[0].strip()))
            if metric == "1":
                mintemp += "&deg;C"
            else:
                mintemp = str(round(int(mintemp) * 9 / 5 + 32)) + "&deg;F"

            mystr = str(div[j]).split('<div class="div-row div-row4 div-row-data">', 1)[1]
            mystr = mystr.split('</div>', 1)[0].strip()

            if '<p class="mrgn-bttm-0 pop text-center" title="' in mystr:
                pop2 = mystr.split('<small>', 1)[1].split('</small>', 1)[0].strip()

        srcs = [img['src'] for img in div[j].find_all('img')]
        alts = [alt['alt'] for alt in div[j].find_all('img')]

        if head1 != "":
            count = len(srcs)
            if count > 0:
                img1 = srcs[0]
                content1 = alts[0]

            if head2 != "":
                if count > 1:
                    img2 = srcs[1]
                    content2 = alts[1]
        else:
            count = len(srcs)
            if count > 0:
                img2 = srcs[0]
                content2 = alts[0]

        if head1 != "":
            img1 = img1[14:-4]
            if use_icons == "1":
                img1 = "wca" + img1 + ".png"
            else:
                if img1 == "26":
                    img1 = "flaticon-thermometer"
                else:
                    img1 = "wi wi-weather-gc-ca-" + img1

            myday1.text = html.escape(content1)
            myday1.icon = img1
            myday1.max = maxtemp
            last_ts = myday1.timestamp = timestamp1
            myday1.day = datetime.datetime.fromtimestamp(myday1.timestamp).strftime("%A")
            myday1.min = pop1

            days += str(myday1) + ","

        if head2 != "":
            img2 = img2[14:-4]
            if use_icons == "1":
                img2 = "wca" + img2 + ".png"
            else:
                if img2 == "26":
                    img2 = "flaticon-thermometer"
                else:
                    img2 = "wi wi-weather-gc-ca-" + img2

            myday2.text = html.escape(content2)
            myday2.icon = img2
            myday2.max = mintemp
            last_ts = myday2.timestamp = timestamp2
            myday2.day = datetime.datetime.fromtimestamp(myday2.timestamp).strftime("%A")
            myday2.day += " Night"
            myday2.min = pop2

            days += str(myday2) + ","

        j += 1

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]
