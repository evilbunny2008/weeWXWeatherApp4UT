#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Handle various forecasts """

import datetime
import time
import json
import os
import collections
import xmltodict
import day
import main

DE_DAYS = {"monday": "Montag", "tuesday": "Dienstag", "wednesday": "Mittwoch",
           "thursday": "Donnerstag", "friday": "Freitag", "saturday": "Samstag",
           "sunday": "Sonntag"}

def convert_day_to_ts(day_name, last_ts, lang="en_AU"):
    """ Search for the current day name and turn it into a timestamp """

    start_ts = last_ts
    day_name = day_name.lower()

    while True:
        ftime = datetime.datetime.fromtimestamp(last_ts)
        ftime = ftime.strftime("%A").lower()

        if lang == "en_AU":
            # print("ftime == " + ftime + ", day_name == " + day_name)
            if day_name.startswith(ftime):
                return last_ts
        elif lang == "de_DE":
            if day_name.startswith(DE_DAYS[ftime].lower()):
                return last_ts

        last_ts += 86400

        if last_ts > start_ts + 864000:
            return 0

def process_wz(data):
    """ Process Weather Zone forecast """

    jobj = xmltodict.parse(data)
    jobj = jobj['rss']['channel']

    pub_date = jobj["pubDate"]
    desc = jobj["title"]
    # Sun, 12 May 2019 08:56:04 +1000
    # EEE, dd MMM yyyy HH:mm:ss Z
    last_ts = time.mktime(time.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z'))

    mydesc = jobj['item'][0]["description"].split("<b>")

    days = ""

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    for line in mydesc:
        line = line.strip()
        if line == "":
            continue

        tmp = line.split("</b>", 1)
        myday = day.Day()
        myday.timestamp = convert_day_to_ts(tmp[0].strip(), last_ts)
        if myday.timestamp != 0:
            myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")
        else:
            myday.day = tmp[0].strip()

        if len(tmp) <= 1:
            continue

        mybits = tmp[1].strip().split("<br />")
        mybits[1] = mybits[1].strip()

        tmpstr = '<img src="http://www.weatherzone.com.au/images/icons/fcast_30/'
        myimg = mybits[1].replace(tmpstr, "")
        myimg = myimg.replace("\">", "").replace(".gif", "").replace("_", "-").strip()

        myday.text = mybits[2].strip()
        myrange = mybits[3].split(" - ", 1)

        if use_icons != "1":
            if myimg != "frost-then-sunny":
                myday.icon = "wi wi-weatherzone-" + myimg
            else:
                myday.icon = "flaticon-thermometer"
        else:
            myday.icon = "wz" + myimg.replace("-", "_") + ".png"

        myday.max = myrange[1].strip()
        myday.min = myrange[0].strip()

        if metric != "1":
            myday.max = round(float(myrange[1][:-7]) * 9.0 / 5.0 + 32.0, 0) + "&deg;F"
            myday.min = round(float(myrange[0][:-7]) * 9.0 / 5.0 + 32.0, 0) + "&deg;F"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_yrno(data):
    """ Process yr.no forecast """

    use_icons = main.get_string("use_icons", "0")

    jobj = xmltodict.parse(data)
    jobj = jobj['weatherdata']
    location = jobj['location']
    desc = location['name'] + ", " + location['country']

    days = ""
    jarr = jobj['forecast']['tabular']['time']

    for line in jarr:
        myday = day.Day()
        from_time = line['@from']
        to_time = line['@to']
        code = line['symbol']['@var']
        myday.min = line['precipitation']['@value'] + "mm"
        myday.max = line['temperature']['@value'] + "&deg;C"

        myday.text = line['windSpeed']['@name'] + ", " + line['windSpeed']['@mps'] + "m/s from the "
        myday.text += line['windDirection']['@name']

        date1 = time.mktime(time.strptime(from_time, '%Y-%m-%dT%H:%M:%S'))
        date2 = time.mktime(time.strptime(to_time, '%Y-%m-%dT%H:%M:%S'))

        myday.timestamp = date1
        from_time = datetime.datetime.fromtimestamp(date1).strftime("%H:%M")
        to_time = datetime.datetime.fromtimestamp(date2).strftime("%H:%M")
        date = datetime.datetime.fromtimestamp(date1).strftime("%A")
        myday.day = date + ": " + from_time + "-" + to_time

        if use_icons != "1":
            myday.icon = "wi wi-yrno-" + code
        else:
            myday.icon = "yrno" + code + ".png"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_bom1(data):
    """ Process BoM FTP forecast """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")
    bomtown = main.get_string("bomtown", "")

    if bomtown == "":
        return [False, "Town or suburb not set, update settings.txt"]

    jobj = xmltodict.parse(data)['product']
    # content = jobj["amoc"]["issue-time-local"]['#text']

    days = ""
    loc_content = None

    for area in jobj["forecast"]["area"]:
        if bomtown == area['@description']:
            loc_content = area
            break

    if loc_content is None:
        return[False, "Unable to match '" + bomtown + "'", ""]

    jobj = loc_content
    desc = jobj["@description"] + ", Australia"

    for forecast in jobj['forecast-period']:
        myday = day.Day()
        start_time = forecast['@start-time-local'][:-6]
        myday.timestamp = time.mktime(time.strptime(start_time, '%Y-%m-%dT%H:%M:%S'))
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")

        if forecast['@index'] != "0":
            for i in range(len(forecast['element'])):
                if forecast['element'][i]['@type'] == "forecast_icon_code":
                    myday.icon = forecast['element'][i]['#text']
                if forecast['element'][i]['@type'] == "air_temperature_minimum":
                    myday.min = forecast['element'][i]['#text']
                if forecast['element'][i]['@type'] == "air_temperature_maximum":
                    myday.max = forecast['element'][i]['#text']
        else:
            try:
                myday.icon = forecast['element']['#text']
            except Exception:
                for i in range(len(forecast['element'])):
                    if forecast['element'][i]['@type'] == "forecast_icon_code":
                        myday.icon = forecast['element'][i]['#text']

        for i in range(len(forecast['text'])):
            if forecast['text'][i]['@type'] == "precis":
                myday.text = forecast['text'][i]['#text']

        if use_icons != "1":
            if myday.icon != "14":
                myday.icon = "wi wi-bom-ftp-" + myday.icon
            else:
                myday.icon = "flaticon-thermometer"
        else:
            myday.icon = "bom" + myday.icon + ".png"

        if metric == "1":
            myday.max += "&deg;C"
            myday.min += "&deg;C"
        else:
            myday.min = str(round(float(myday.min) * 9.0 / 5.0 + 32.0)) + "&deg;F"
            myday.max = str(round(float(myday.max) * 9.0 / 5.0 + 32.0)) + "&deg;F"

        if myday.max == "&deg;C" or myday.max == "&deg;F" or myday.max == "":
            myday.max = "N/A"

        if myday.min == "&deg;C" or myday.min == "&deg;F":
            myday.min = ""

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_wmo(data):
    """ Process WMO forecast """

    metric = main.get_string("metric", "1")

    days = ""

    jobj = json.loads(data)

    desc = jobj['city']['cityName'] + ", " + jobj['city']['member']['memName']
    # tmp = jobj['city']['forecast']['issueDate']

    # "yyyy-MM-dd HH:mm:ss"
    # timestamp = time.mktime(time.strptime(tmp, '%Y-%m-%d %H:%M:%S'))

    jarr = jobj['city']['forecast']['forecastDay']
    for j in jarr:
        myday = day.Day()
        myday.timestamp = time.mktime(time.strptime(j['forecastDate'], '%Y-%m-%d'))
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")

        myday.text = j['weather']
        myday.max = j['maxTemp'] + "&deg;C"
        myday.min = j['minTemp'] + "&deg;C"
        if metric != "1":
            myday.max = j['maxTempF'] + "&deg;F"
            myday.min = j['minTempF'] + "&deg;F"

        code = str(j['weatherIcon'])[:-2]

        if code == "28":
            myday.icon = "flaticon-cactus"
        elif code == "29" or code == "30":
            myday.icon = "flaticon-thermometer"
        elif code == "32":
            myday.icon = "flaticon-cold"
        elif code == "33":
            myday.icon = "flaticon-warm"
        elif code == "34":
            myday.icon = "flaticon-cool"
        else:
            myday.icon = "wi wi-wmo-" + code

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_metoffice(data):
    """ Process MET Office forecasts """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    days = ""

    desc = data.split('<title>', 1)[1].split(' weather - Met Office</title>', 1)[0].strip()
    forecasts = data.split('<ul id="dayNav"', 2)[1].split('</ul>', 2)[0].split('<li')
    del forecasts[0]
    for line in forecasts:
        myday = day.Day()
        myday.day = line.split('data-tab-id="', 1)[1].split('"')[0].strip()
        myday.timestamp = time.mktime(time.strptime(myday.day, '%Y-%m-%d'))
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")

        myday.icon = "https://beta.metoffice.gov.uk" + line.split('<img class="icon"')[1]
        myday.icon = myday.icon.split('src="')[1].split('">')[0].strip()

        myday.icon = os.path.basename(myday.icon).replace(".svg", ".png").strip()
        myday.min = line.split('<span class="tab-temp-low"', 1)[1].split('">')[1]
        myday.min = myday.min.split("</span>", 1)[0].strip()
        myday.max = line.split('<span class="tab-temp-high"', 1)[1].split('">')[1]
        myday.max = myday.max.split("</span>")[0].strip()
        myday.text = line.split('<div class="summary-text', 1)[1].split('">', 3)[2]
        myday.text = myday.text.split("</div>", 1)[0]
        myday.text = myday.text.replace('</span>', '').replace('<span>', '').strip()

        if metric == "1":
            myday.min += "C"
            myday.max += "C"
        else:
            myday.min = str(round(float(myday.min) * 9.0 / 5.0 + 32.0)) + "&deg;F"
            myday.max = str(round(float(myday.max) * 9.0 / 5.0 + 32.0)) + "&deg;F"

        if use_icons == "1":
            myday.icon = "met" + myday.icon
        else:
            myday.icon = "wi wi-metoffice-" + myday.icon[:-4]

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_bom2(data):
    """ Process BoM forecasts method 2 """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    desc = data.split('<title>', 1)[1].split(' Weather - Bureau of Meteorology</title>', 1)[0]
    desc = desc + ", Australia"

    data = data.split('<div class="forecasts">', 1)[1]
    days = ""

    bits = data.split('<dl class="forecast-summary">')
    del bits[0]
    bit = bits[0]

    myday = day.Day()
    myday.day = bit.split('<a href="', 1)[1].split('">', 1)[0].split("/forecast/detailed/#d", 1)[1]
    myday.timestamp = time.mktime(time.strptime(myday.day, '%Y-%m-%d'))
    myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")

    myday.icon = bit.split("<img src=\"", 1)[1].split("\" alt=\"", 1)[0]
    myday.icon = myday.icon.strip()

    if '<dd class="max">' in bit:
        myday.max = bit.split('<dd class="max">', 1)[1].split('</dd>', 1)[0].strip()

    if '<dd class="min">' in bit:
        myday.min = bit.split("<dd class=\"min\">")[1].split("</dd>")[0].strip()

    myday.text = bit.split('<dd class="summary">', 1)[1].split('</dd>', 1)[0].strip()

    file_name = os.path.basename(myday.icon)[:-4]
    if use_icons != "1":
        if file_name != "frost":
            myday.icon = "wi wi-bom-" + file_name
        else:
            myday.icon = "flaticon-thermometer"
    else:
        myday.icon = "bom2" + file_name.replace('-', '_') + ".png"

    myday.max = myday.max.replace("°C", "").replace("&deg;C", "").strip()
    myday.min = myday.min.replace("°C", "").replace("&deg;C", "").strip()

    if metric == "1":
        myday.max += "&deg;C"
        myday.min += "&deg;C"
    else:
        if myday.min != "":
            myday.min = str(round(float(myday.min) * 9.0 / 5.0 + 32.0)) + "&deg;F"

        if myday.max != "":
            myday.max = str(round(float(myday.max) * 9.0 / 5.0 + 32.0)) + "&deg;F"

    if myday.min.startswith("&deg;"):
        myday.min = ""

    if myday.max == "" or myday.max.startswith("&deg;"):
        myday.max = "N/A"

    days += str(myday) + ","

    del bits[0]

    for bit in bits:
        if '</div>' in bit:
            bit = bit.split('</div>', 1)[0].strip()

        myday = day.Day()
        myday.day = bit.split('<a href="', 1)[1].split('">', 1)[0]
        myday.day = myday.day.split("/forecast/detailed/#d", 1)[1].strip()
        myday.timestamp = time.mktime(time.strptime(myday.day, '%Y-%m-%d'))
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")

        myday.icon = bit.split('<img src="', 1)[1].split('" alt="', 1)[0].strip()
        myday.max = bit.split('<dd class="max">')[1].split('</dd>')[0].strip()
        myday.min = bit.split('<dd class="min">')[1].split('</dd>')[0].strip()
        myday.text = bit.split('<dd class="summary">', 1)[1].split('</dd>', 1)[0].strip()

        file_name = os.path.basename(myday.icon)[:-4]
        if use_icons != "1":
            if file_name != "frost":
                myday.icon = "wi wi-bom-" + file_name
            else:
                myday.icon = "flaticon-thermometer"
        else:
            myday.icon = "bom2" + file_name.replace('-', '_') + ".png"

        myday.max = myday.max.replace("°C", "").replace("&deg;C", "").strip()
        myday.min = myday.min.replace("°C", "").replace("&deg;C", "").strip()

        if metric == "1":
            myday.max += "&deg;C"
            myday.min += "&deg;C"
        else:
            if myday.min != "":
                myday.min = str(round(float(myday.min) * 9.0 / 5.0 + 32.0)) + "&deg;F"

            if myday.max != "":
                myday.max = str(round(float(myday.max) * 9.0 / 5.0 + 32.0)) + "&deg;F"

        if myday.min.startswith("&deg;"):
            myday.min = ""

        if myday.max == "" or myday.max.startswith("&deg;"):
            myday.max = "N/A"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_aemet(data):
    """ Process AEMET forecasts """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    jobj = xmltodict.parse(data)

    jobj = jobj["root"]
    desc = jobj["nombre"] + ", " + jobj["provincia"]
    # print(desc)

    # elaborado = jobj["elaborado"]
    # yyyy-MM-dd'T'HH:mm:ss
    # timestamp = time.mktime(time.strptime(elaborado, "%Y-%m-%dT%H:%M:%S"))
    # dayname = datetime.datetime.fromtimestamp(timestamp).strftime("%A -- %H:%M")
    # print(dayname)

    days = ""

    dates = jobj['prediccion']['dia']
    for date in dates:
        myday = day.Day()
        myday.day = date['@fecha']
        myday.timestamp = time.mktime(time.strptime(myday.day, "%Y-%m-%d"))
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")

        myday.max = date['temperatura']['maxima']
        myday.min = date['temperatura']['minima']

        if isinstance(date['estado_cielo'], collections.OrderedDict):
            myday.text = date['estado_cielo']['@descripcion']
            myday.icon = date['estado_cielo']['#text']
        elif isinstance(date['estado_cielo'], list):
            for i in date['estado_cielo']:
                try:
                    if isinstance(i, collections.OrderedDict) and i['#text'] != "":
                        myday.text = i['@descripcion']
                        myday.icon = i['#text']
                        # print(myday)
                        break
                except KeyError:
                    pass

        if use_icons != "1":
            if myday.icon != "7":
                myday.icon = "wi wi-aemet-" + myday.icon
            else:
                myday.icon = "flaticon-thermometer"
        else:
            myday.icon = "aemet_" + myday.icon + "_g.png"

        if metric == "1":
            myday.max += "&deg;C"
            myday.min += "&deg;C"
        else:
            if myday.min != "":
                myday.min = str(round(float(myday.min) * 9.0 / 5.0 + 32.0)) + "&deg;F"

            if myday.max != "":
                myday.max = str(round(float(myday.max) * 9.0 / 5.0 + 32.0)) + "&deg;F"

        if myday.min.startswith("&deg;"):
            myday.min = ""

        if myday.max == "" or myday.max.startswith("&deg;"):
            myday.max = "N/A"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_dwd(data):
    """ Process DWD.de forecasts """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    days = ""

    bits = data.split("<title>", 1)[1]
    desc = bits.split("</title>", 1)[0]
    desc = desc.split(' - ', 2)[2].strip()

    ftime = data.split('<tr class="headRow">', 1)[1].split('</tr>', 1)[0].strip()
    date = ftime.split('<td width="30%" class="stattime">', 1)[1].split('</td>', 1)[0].strip()
    ftime = date + " " + ftime.split('<td width="40%" class="stattime">', 2)[1]
    ftime = ftime.split(' Uhr</td>', 1)[0].strip()
    # dd.MM.yyyy HH
    last_ts = time.mktime(time.strptime(ftime, "%d.%m.%Y %H"))
    # dayname = datetime.datetime.fromtimestamp(timestamp).strftime("%A -- %Y-%m-%d %H")
    # print(dayname)

    data = data.split('<td width="40%" class="statwert">Vorhersage</td>', 1)[1]
    data = data.split('</table>', 1)[0].strip()
    lines = data.split('<tr')
    del lines[0]
    for line in lines:
        myday = day.Day()

        if len(line.split('<td ><b>')) > 1:
            myday.day = line.split('<td ><b>', 1)[1].split('</b></td>', 1)[0].strip()
        else:
            myday.day = line.split('<td><b>', 1)[1].split('</b></td>', 1)[0].strip()

        myday.timestamp = convert_day_to_ts(myday.day, last_ts, "de_DE")

        if len(line.split('<td ><img name="piktogramm" src="', 2)) > 1:
            myday.icon = line.split('<td ><img name="piktogramm" src="', 1)[1]
            myday.icon = myday.icon.split('" width="50" alt="', 1)[0].strip()
        else:
            myday.icon = line.split('<td><img name="piktogramm" src="', 1)[1]
            myday.icon = myday.icon.split('" width="50" alt="', 1)[0].strip()

        for i in line.split('<td'):
            if 'Grad' in i:
                myday.max = i
                myday.max = myday.max.split('Grad', 1)[0].strip()[1:]
                break

        myday.icon = myday.icon.replace('/DE/wetter/_functions/piktos/vhs_', '')
        myday.icon = myday.icon.replace('?__blob=normal', '').strip()
        myday.icon = "dwd_" + myday.icon.replace('-', '_')

        if use_icons != "1":
            myday.icon = myday.icon[4:-4]
            if myday.icon != "pic-48" and myday.icon != "pic-66" and myday.icon != "pic67":
                myday.icon = "wi wi-dwd-" + myday.icon
            else:
                myday.icon = "flaticon-thermometer"

        if metric == "1":
            myday.max += "&deg;C"
        else:
            if myday.max != "":
                myday.max = str(round(float(myday.max) * 9.0 / 5.0 + 32.0)) + "&deg;F"

        if not myday.max.startswith('&deg;'):
            days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_metservice(data):
    """ Process metservice forecasts """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    days = ""

    jobj = json.loads(data)
    loop = jobj['days']
    # ftime = loop[0]["issuedAtISO"]
    desc = jobj["locationECWasp"] + ", New Zealand"

    for jtmp in loop:
        myday = day.Day()
        jtmp['dateISO'] = jtmp['dateISO'][:-6]
        myday.timestamp = time.mktime(time.strptime(jtmp['dateISO'], "%Y-%m-%dT%H:%M:%S"))
        myday.day = jtmp["dow"]
        myday.text = jtmp["forecast"]
        myday.max = jtmp["max"]
        myday.min = jtmp["min"]

        if "partDayData" in jtmp:
            myday.icon = jtmp["partDayData"]["afternoon"]["forecastWord"]
        else:
            myday.icon = jtmp["forecastWord"]

        myday.icon = myday.icon.lower().replace(" ", "-").strip()

        if use_icons != "1":
            if myday.icon != "frost":
                myday.icon = "wi wi-metservice-" + myday.icon
            else:
                myday.icon = "flaticon-thermometer"
        else:
            myday.icon = myday.icon.replace("-", "_")
            myday.icon = "ms_" + myday.icon + ".png"

        if metric:
            myday.max += "&deg;C"
            myday.min += "&deg;C"
        else:
            myday.max = str(round(float(myday.max) * 9.0 / 5.0 + 32.0)) + "&deg;F"
            myday.min = str(round(float(myday.min) * 9.0 / 5.0 + 32.0)) + "&deg;F"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_darksky(data):
    """ Process darksky forecasts """

    metric = main.get_string("metric", "1")

    days = ""

    jobj = json.loads(data)
    desc = str(jobj["latitude"]) + ", " + str(jobj["longitude"])
    daily = jobj["daily"]

    for jarr in daily["data"]:
        myday = day.Day()
        myday.icon = jarr["icon"]
        myday.timestamp = jarr['time']
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")
        myday.max = str(round(float(jarr['temperatureHigh'])))
        myday.min = str(round(float(jarr['temperatureLow'])))

        if metric == "1":
            myday.max += "&deg;C"
            myday.min += "&deg;C"
        else:
            myday.max += "&deg;F"
            myday.min += "&deg;F"

        myday.icon = "wi wi-forecast-io-" + myday.icon
        myday.text = jarr["summary"]

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    print(days)

    return [True, days, desc]

def process_owm(data):
    """ Process OpenWeatherMap.org forecasts """

    metric = main.get_string("metric", "1")

    days = ""

    jobj = json.loads(data)

    desc = jobj["city"]["name"] + ", " + jobj["city"]["country"]

    for j in jobj['list']:
        myday = day.Day()
        myday.timestamp = j['dt']
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")
        myday.max = str(round(float(j['temp']['max'])))
        myday.min = str(round(float(j['temp']['min'])))
        weather = j['weather'][0]

        myday.text = weather['description']
        myday.icon = weather['icon']
        if not myday.icon.endswith('n'):
            myday.icon = "wi wi-owm-day-" + str(weather['id'])
        else:
            myday.icon = "wi wi-owm-night-" + str(weather['id'])

        if metric == "1":
            myday.max += "&deg;C"
            myday.min += "&deg;C"
        else:
            myday.max += "&deg;F"
            myday.min += "&deg;F"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_apixu(data):
    """ Process apixu.com forecasts """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    days = ""

    jobj = json.loads(data)
    desc = jobj["location"]["name"] + ", " + jobj["location"]["country"]
    for j in jobj["forecast"]["forecastday"]:
        myday = day.Day()
        myday.timestamp = j['date_epoch']
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")
        this_day = j["day"]

        if metric == "1":
            myday.min = str(this_day['mintemp_c']) + "&deg;C"
            myday.max = str(this_day['maxtemp_c']) + "&deg;C"
        else:
            myday.min = str(this_day['mintemp_f']) + "&deg;F"
            myday.max = str(this_day['maxtemp_f']) + "&deg;F"

        for cond in main.CONDITIONS:
            if cond["code"] == this_day["condition"]["code"]:
                myday.icon = str(cond["icon"])
                myday.text = cond["day"]
                break

        if use_icons != "1":
            myday.icon = "wi wi-apixu-" + myday.icon
        else:
            myday.icon = "apixu_" + myday.icon + ".png"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_wcom(data):
    """ Process weather.com forecasts """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    days = ""

    jobj = json.loads(data)
    desc = jobj["id"]

    valid_date = jobj["vt1dailyForecast"]["validDate"]
    icons = jobj["vt1dailyForecast"]["day"]["icon"]
    phrase = jobj["vt1dailyForecast"]["day"]["phrase"]
    day_temp = jobj["vt1dailyForecast"]["day"]["temperature"]
    night_temp = jobj["vt1dailyForecast"]["night"]["temperature"]

    rng = range(len(valid_date))
    for i in rng:
        myday = day.Day()
        myday.timestamp = time.mktime(time.strptime(valid_date[i], '%Y-%m-%dT%H:%M:%S%z'))
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")
        myday.text = phrase[i]
        myday.icon = icons[i]
        myday.max = str(day_temp[i])
        myday.min = str(night_temp[i])

        if use_icons != "1":
            myday.icon = "wi wi-yahoo-" + myday.icon
        else:
            myday.icon = "yahoo" + str(myday.icon) + ".gif"

        if metric == "1":
            myday.max += "&deg;C"
            myday.min += "&deg;C"
        else:
            myday.max += "&deg;F"
            myday.min += "&deg;F"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]

def process_metie(data):
    """ Process met.ie forecasts """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    days = ""

    desc = main.get_string('metierev', '')
    for jobj in json.loads(data):
        myday = day.Day()
        tmp_day = jobj["date"] + "T" + jobj["time"]
        myday.timestamp = time.mktime(time.strptime(tmp_day, '%Y-%m-%dT%H:%M'))
        myday.day = datetime.datetime.fromtimestamp(myday.timestamp).strftime("%A")
        myday.max = str(jobj["temperature"])
        myday.icon = jobj["weatherNumber"]
        myday.text = jobj["weatherDescription"]

        if use_icons != "1":
            myday.icon = "wi wi-met-ie-" + myday.icon
        else:
            myday.icon = "y" + myday.icon + ".png"

        if metric == "1":
            myday.max += "&deg;C"
        else:
            myday.max = str(round(float(myday.max) * 9.0 / 5.0 + 32.0)) + "&deg;F"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]
