#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This is where the fun starts! """

import configparser
import datetime
from ftplib import FTP
import os
import json
import zipfile
import sys
import socket
import time
import requests
import forecasts
import meteofrance
import wca
import wgov
import yahoo

try:
    sys.path.append('../PIL/')
    from PIL import Image
except ImportError as err:
    print(err)

APP_ID = os.environ.get("APP_ID", "").split('_')[0]
CONFIGBASE = os.environ.get("XDG_CONFIG_HOME", "/tmp") + "/" + APP_ID
CACHEBASE = os.environ.get("XDG_CACHE_HOME", "/tmp") + "/" + APP_ID
APPBASE = os.environ.get("APP_DIR", "/tmp")

HEADERS = {}
HEADERS['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " + \
                        "(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

SESSION = requests.Session()
SESSION.headers = HEADERS

INIGO_VERSION = 4000

ICON_VERSION = 10
ICON_URL = "https://github.com/evilbunny2008/weeWXWeatherApp/releases/download/0.8.25/icons.zip"

# for a in os.environ:
#     print('Var: ', a, 'Value: ', os.getenv(a))

def download(url):
    """ Download json string from server based on a bounding box """

    if url.startswith("http"):
        try:
            ret = SESSION.get(url)
        except Exception as error:
            return [False, str(error)]

        if ret.ok:
            if 'aemet' in url.lower():
                content = ret.content.decode('iso-8859-15').encode('utf8')
            else:
                content = ret.content

            return [True, content]

        return [False, "Failed to download " + url + ", error status: " + str(ret.status_code)]
    elif url.startswith("ftp"):
        url = url[6:]
        hostname, url = url.split('/', 1)
        url = "/" + url
        filename = os.path.basename(url)
        url = url[:-1 * len(filename)]

        ftp = FTP(hostname)
        ftp.login()
        ftp.cwd(url)

        with open(CACHEBASE + "/tempfile.txt", 'wb') as file_name:
            def callback(data):
                """ Write FTP response to localfile """
                file_name.write(data)

            ftp.retrbinary('RETR %s' % filename, callback)

        ret = read_file("/tempfile.txt", CACHEBASE)
        ret[1] = ret[1].encode("utf8")
        os.remove(CACHEBASE + "/tempfile.txt")
        return ret
    else:
        return [False, "Unknown URL handle, can't continue, url: '" + url + "'"]

def check_paths():
    """ check and make directories as needed. """

    os.makedirs(CONFIGBASE, exist_ok=True)
    os.makedirs(CACHEBASE, exist_ok=True)

def get_string(key, defval):
    """ Get key value pair from config.ini """

    check_paths()

    config = configparser.ConfigParser()
    try:
        config.read(CONFIGBASE + "/config.ini")
        val = config['DEFAULT'][key]
        if val.strip() != "":
            return val.strip()
    except Exception:
        pass

    return defval

def set_string(key, val):
    """ Save key value pair to config.ini """

    check_paths()

    config = configparser.ConfigParser()
    try:
        config.read(CONFIGBASE + "/config.ini")
        config['DEFAULT'][key] = val
        with open(CONFIGBASE + '/config.ini', 'w') as configfile:
            config.write(configfile)
        return True
    except Exception:
        pass

    return False

def read_file(filename, directory=CONFIGBASE):
    """ Read content from a file """

    check_paths()

    try:
        filename = directory + "/" + filename
        my_file = open(filename, "r")
        ret = my_file.read()
        try:
            ret = ret.decode('utf8')
        except Exception as error:
            pass

        my_file.close()
    except Exception as error:
        return [False, str(error)]

    return [True, ret]

def write_file(filename, mydata, directory=CONFIGBASE):
    """ save data to a file """

    check_paths()
    filename = directory + "/" + filename
    my_file = open(filename, "w")
    try:
        my_file.write(mydata)
    except TypeError:
        my_file.write(mydata.decode('utf8'))
    my_file.close()
    print("Wrote to: " + filename)

def write_binary(filename, binary, directory=CONFIGBASE):
    """ save data to a file """

    check_paths()
    filename = directory + "/" + filename
    my_file = open(filename, "wb")
    my_file.write(binary)
    my_file.close()
    print("Wrote to: " + filename)

def download_data(data_url="", force_download=False):
    """ download and save data to local file """

    if data_url is False or data_url == "":
        data_url = get_string("data_url", "")

    if data_url is False or data_url == "":
        return [False, "Data URL is not set"]

    if os.path.exists(CONFIGBASE + "/data.txt"):
        if time.time() - os.path.getmtime(CONFIGBASE + "/data.txt") > 270:
            force_download = True

    if force_download is True or not os.path.exists(CONFIGBASE + "/data.txt"):
        data = download(data_url)
        if data[0] is False:
            data[1] = str(data[1])
            return data

        if data[1] == "":
            return [False, "Failed to download data.txt from " + data_url]

        bits = data[1].decode('utf8').strip().split("|")
        if int(bits[0]) < INIGO_VERSION:
            return [False, "This app has been updated but the server you are connecting to " + \
                    "hasn't updated the Inigo Plugin for weeWX. Fields may not show up " + \
                    "properly until weeWX is updated."]

        data = ""
        del bits[0]
        for bit in bits:
            if data != "":
                data += "|"
            data += bit

        write_file("data.txt", data)
        return [True, data.encode('utf8')]

    data = read_file("data.txt")
    return [data[0], data[1].encode('utf8')]

def check_for_icons():
    """ Check to see if the icons already exists in the cache dir """

    files = ["aemet_11_g.png", "apixu_113.png", "bom1.png", "bom2clear.png", "dwd_pic_0_8.png",
             "i1.png", "met0.png", "mf_j_w1_0_n_2.png", "ms_cloudy.png", "smn_wi_cloudy.png",
             "wca00.png", "wgovbkn.jpg", "wzclear.png", "y01d.png", "yrno01d.png", 'yahoo0.gif',
             "yahoo-clear_day@2x.png"]

    for my_file in files:
        if not os.path.isfile(CACHEBASE + "/" + my_file):
            return [False, "One or more icons was missing, will download again"]

    return [True, "Icons were found and will be used."]

def get_radar(radar_url="", rad_type="", force_download=False):
    """ Get the radar image and display it """

    width = height = 0

    if radar_url == "":
        radar_url = get_string("radar_url", "")

    if rad_type == "":
        rad_type = get_string("rad_type", "")

    if radar_url == "":
        return [False, "Radar URL is not set."]

    if rad_type == "image":

        if os.path.exists(CACHEBASE + "/radar.gif"):
            if time.time() - os.path.getmtime(CACHEBASE + "/radar.gif") > 570:
                force_download = True

        if force_download is True or not os.path.exists(CACHEBASE + "/radar.gif"):
            dled = download(radar_url)
            if dled[0] is False:
                dled[1] = str(dled[1])
                return dled
            write_binary("radar.gif", dled[1], CACHEBASE)

        picture = Image.open(CACHEBASE + '/radar.gif')
        width, height = picture.size
    else:
        dled = download(radar_url)
        if dled[0] is False:
            dled[1] = str(dled[1])
            return dled

    return [True, "Radar URL was ok", width, height]

def get_forecast(forecast_url="", force_download=False):
    """ Get a forecast and display it """

    if forecast_url == "":
        forecast_url = get_string("forecast_url", "")

    if forecast_url == "":
        return [False, "Forecast URL is not set"]

    if os.path.exists(CONFIGBASE + "/forecast.txt"):
        if time.time() - os.path.getmtime(CONFIGBASE + "/forecast.txt") > 7170:
            force_download = True

    if force_download is True or not os.path.exists(CONFIGBASE + "/forecast.txt"):
        data = download(forecast_url)
        if data[0] is False:
            data[1] = str(data[1])
            return data

        if data[1].strip() == "":
            return [False, "Failed to download forecast from " + forecast_url]

        write_file("forecast.txt", data[1])

        return [True, data[1]]

    data = read_file("forecast.txt")
    return [True, data]

def process_forecast(force_download=False):
    """ Process forecast data ready to display """

    if os.path.exists(CONFIGBASE + "/forecast.txt"):
        if time.time() - os.path.getmtime(CONFIGBASE + "/forecast.txt") > 7170:
            force_download = True

    if force_download is True or not os.path.exists(CONFIGBASE + "/forecast.txt"):
        ret = get_forecast(force_download=True)
        if ret[0] is False:
            return ret

    ftime = os.path.getmtime(CONFIGBASE + "/forecast.txt")
    ftime = datetime.datetime.fromtimestamp(ftime)
    ftime = ftime.strftime("%d %b %Y %H:%M")

    data = read_file("forecast.txt")
    if data[0] is False:
        data[1] = str(data[1])
        return data

    fctype = get_string("fctype", "yahoo")

    if fctype == "yahoo":
        ret = yahoo.process_yahoo(data[1])
    elif fctype == "weatherzone":
        ret = forecasts.process_wz(data[1])
    elif fctype == "yr.no":
        ret = forecasts.process_yrno(data[1])
    elif fctype == "bom.gov.au":
        ret = forecasts.process_bom1(data[1])
    elif fctype == "wmo.int":
        ret = forecasts.process_wmo(data[1])
    elif fctype == "weather.gov":
        ret = wgov.process_wgov(data[1])
    elif fctype == "weather.gc.ca":
        ret = wca.process_wca(data[1])
    elif fctype == "weather.gc.ca-fr":
        ret = wca.process_wcafr(data[1])
    elif fctype == "metoffice.gov.uk":
        ret = forecasts.process_metoffice(data[1])
    elif fctype == "bom2":
        ret = forecasts.process_bom2(data[1])
    elif fctype == "aemet.es":
        ret = forecasts.process_aemet(data[1])
    elif fctype == "dwd.de":
        ret = forecasts.process_dwd(data[1])
    elif fctype == "metservice.com":
        ret = forecasts.process_metservice(data[1])
    elif fctype == "meteofrance.com":
        ret = meteofrance.process_mf(data[1])
    elif fctype == "darksky.net":
        ret = forecasts.process_darksky(data[1])
    elif fctype == "openweathermap.org":
        ret = forecasts.process_owm(data[1])
    elif fctype == "apixu.com":
        ret = forecasts.process_apixu(data[1])
    elif fctype == "weather.com":
        ret = forecasts.process_wcom(data[1])
    elif fctype == "met.ie":
        ret = forecasts.process_metie(data[1])
    else:
        ret = [False, "fctype is '" + fctype + "' which is invalid or not coded yet.", ""]

    if ret[0] is False:
        ret[1] = str(ret[1])

    return ret[0], ret[1], fctype, ftime, ret[2]

def refresh_forecast():
    """ Deal with refreshes from the GUI """

    ret = get_forecast()
    if ret[0] is False:
        return ret

    ret = process_forecast()
    return ret

def get_custom():
    """ Get the custom url from config """

    url = get_string('custom_url', '')
    return [True, url]

def deal_with_url(url):
    """ Split the URL into host, port and file path """

    if url.startswith("http://"):
        proto = "http"
    elif url.startswith("https://"):
        return [False, "https isn't supported atm...", "", "", ""]
    else:
        return [False, "Invalid URL for webcam, please check your settings...", "", "", ""]

    hostname, rest = url.split("://", 1)[1].split("/", 1)
    hostname, port = hostname.strip().split(":")
    rest = "/" + rest.strip()

    return [True, proto, hostname, port, rest]

def get_webcam(webcam_url="", force_download=True):
    """ download webcam image """

    width = height = 0

    if webcam_url == "":
        webcam_url = get_string('webcam_url', '')

    if webcam_url == "":
        return [False, "Webcam URL is not set"]

    if os.path.exists(CACHEBASE + "/webcam.jpg"):
        if time.time() - os.path.getmtime(CACHEBASE + "/webcam.jpg") > 270:
            force_download = True

    if force_download is True or not os.path.exists(CACHEBASE + "/webcam.jpg"):
        if webcam_url.lower().endswith('mjpg') or webcam_url.lower().endswith('mjpeg'):
            data = b""

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                ret = deal_with_url(webcam_url)
                if ret is False:
                    return ret

                print(webcam_url)
                print(ret)
                sock.connect((ret[2], int(ret[3])))
                ret[4] = 'GET ' + ret[4] + ' HTTP/1.0\r\n\r\n'
                sock.sendall(ret[4].encode('utf8'))
                data = sock.recv(1024)
                lines = data.split(b"\r\n")
                file_size = lines[len(lines) - 3].decode('utf8')
                file_size = file_size.split(':', 1)[1].strip()
                file_size = int(file_size)
                data = lines[len(lines) - 1]
                while len(data) < file_size:
                    req_size = file_size - len(data)
                    if req_size > 1024:
                        req_size = 1024
                    data += sock.recv(req_size)

                sock.close()
                write_binary('webcam.jpg', data, CACHEBASE)
                im1 = Image.open(CACHEBASE + "/webcam.jpg")
                im2 = im1.transpose(Image.ROTATE_270)
                im2.save(CACHEBASE + "/webcam.jpg")
        else:
            dled = download(webcam_url)
            if dled[0] is False:
                dled[1] = str(dled[1])
                return dled

            write_binary("webcam.jpg", dled[1], CACHEBASE)
            im1 = Image.open(CACHEBASE + "/webcam.jpg")
            im2 = im1.transpose(Image.ROTATE_270)
            im2.save(CACHEBASE + "/webcam.jpg")

    picture = Image.open(CACHEBASE + '/webcam.jpg')
    width, height = picture.size

    return [True, "Webcam URL was ok", width, height]

def get_config():
    """ open and parse the config file """

    settings_url = get_string('settings_url', 'https://example.com/weewx/inigo-settings.txt')
    indoor_readings = get_string('indoor_readings', '0')
    dark_theme = get_string('dark_theme', '0')
    metric = get_string('metric', '1')
    update_freq = get_string('update_freq', '1')
    show_radar = get_string('show_radar', '1')
    use_icons = get_string('use_icons', '0')
    saved = get_string('saved', '0')
    rad_type = get_string('rad_type', 'image')
    radar_url = get_string('radar_url', '')
    fctype = get_string('fctype', 'yahoo')
    wifidownload = get_string('wifidownload', '0')

    return [settings_url, indoor_readings, dark_theme, metric, show_radar, use_icons, saved,
            CACHEBASE, rad_type, radar_url, fctype, APPBASE, update_freq, wifidownload]

def save_config(settings_url, indoor_readings, dark_theme, metric,
                show_radar, use_icons, update_freq, wifidownload):
    """ Save config variables to ini file """

    if indoor_readings:
        indoor_readings = "1"
    else:
        indoor_readings = "0"

    if dark_theme:
        dark_theme = "1"
    else:
        dark_theme = "0"

    if metric:
        metric = "1"
    else:
        metric = "0"

    if show_radar:
        show_radar = "1"
    else:
        show_radar = "0"

    if use_icons:
        use_icons = "1"
    else:
        use_icons = "0"

    if wifidownload:
        wifidownload = "1"
    else:
        wifidownload = "0"

    if update_freq < 0 or update_freq > 5:
        update_freq = "1"
    else:
        update_freq = str(update_freq)

    set_string('settings_url', settings_url)
    set_string('indoor_readings', indoor_readings)
    set_string('dark_theme', dark_theme)
    set_string('metric', metric)
    set_string('show_radar', show_radar)
    set_string('use_icons', use_icons)
    set_string('saved', '1')
    set_string('update_freq', update_freq)
    set_string('wifidownload', wifidownload)

    olddata = get_string('data_url', '')
    oldradar = get_string('radar_url', '')
    oldforecast = get_string('forecast_url', '')
    oldwebcam = get_string('webcam_url', '')
    oldcustom = get_string('custom_url', '')

    data_url = ""
    rad_type = ""
    radar_url = ""
    fctype = "image"
    forecast_url = ""
    webcam_url = ""
    custom_url = ""

    settings = download(settings_url)
    if settings[0] is False:
        settings[1] = str(settings[1])
        return settings

    for line in settings[1].decode('utf8').strip().split("\n"):
        if line.split("=", 1)[0] == "data":
            data_url = line.split("=", 1)[1].strip()
        if line.split("=", 1)[0] == "radtype":
            rad_type = line.split("=", 1)[1].strip().lower()
        if line.split("=", 1)[0] == "radar":
            radar_url = line.split("=", 1)[1].strip()
        if line.split("=", 1)[0] == "fctype":
            fctype = line.split("=", 1)[1].strip().lower()
        if line.split("=", 1)[0] == "forecast":
            forecast_url = line.split("=", 1)[1].strip()
        if line.split("=", 1)[0] == "webcam":
            webcam_url = line.split("=", 1)[1].strip()
        if line.split("=", 1)[0] == "custom":
            custom_url = line.split("=", 1)[1].strip()

    if data_url[0] == "":
        return [False, "Data file url not found."]

    if fctype is False or fctype == "":
        fctype = "yahoo"

    if rad_type != "webpage":
        rad_type = "image"

    if data_url == "" or data_url == "https://example.com/weewx/inigo-data.txt":
        return [False, "Invalid data URL supplied. Please check the URL before trying again."]

    if data_url != olddata:
        data = download_data(data_url, True)
        if data[0] is False:
            data[1] = str(data[1])
            return data

    if radar_url != "" and radar_url != oldradar:
        ret = get_radar(radar_url, rad_type, True)
        if ret[0] is False:
            ret[1] = str(ret[1])
            return ret

    bomtown = metierev = ""
    lat = lon = "0.0"

    if forecast_url != "" and forecast_url != oldforecast:
        if fctype == "yahoo":
            if not forecast_url.startswith("http"):
                return [False, "Yahoo API recently changed, you need to update your settings."]
        elif fctype == "weatherzone":
            forecast_url = "https://rss.weatherzone.com.au/?u=12994-1285&lt=aploc&lc=" + \
                           forecast_url + "&obs=0&fc=1&warn=0"
        elif fctype == "yr.no":
            pass
        elif fctype == "bom.gov.au":
            bomtown = forecast_url.split(",", 1)[1].strip()
            forecast_url = "ftp://ftp.bom.gov.au/anon/gen/fwo/" + \
                           forecast_url.split(",", 1)[0].strip() + ".xml"
            set_string("bomtown", bomtown)
        elif fctype == "wmo.int":
            if not forecast_url.startswith("http"):
                forecast_url = "https://worldweather.wmo.int/en/json/" + forecast_url.strip() + \
                               "_en.xml"
        elif fctype == "weather.gov":
            if "?" in forecast_url:
                forecast_url = forecast_url.split("?", 1)[1]
                if "lat" not in forecast_url or "lon" not in forecast_url:
                    return [False, "Failed to get a valid url or coordinates."]

                for bit in forecast_url.split("&"):
                    if bit.startswith("lat="):
                        lat = bit[4:].strip()
                    if bit.startswith("lon="):
                        lon = bit[4:].strip()

            else:
                lat = forecast_url.split(",", 1)[0]
                lon = forecast_url.split(",", 1)[1]

            if lat == "0.0" and lon == "0.0":
                return [False, "Longitude or Latitude was not specified for weather.gov forecasts"]

            forecast_url = "https://forecast.weather.gov/MapClick.php?lat=" + lat + "&lon=" + \
                            lon + "&unit=0&lg=english&FcstType=json"
        elif fctype == "weather.gc.ca":
            pass
        elif fctype == "weather.gc.ca-fr":
            pass
        elif fctype == "metoffice.gov.uk":
            pass
        elif fctype == "bom2":
            pass
        elif fctype == "aemet.es":
            pass
        elif fctype == "dwd.de":
            pass
        elif fctype == "metservice.com":
            forecast_url = "https://www.metservice.com/publicData/localForecast" + forecast_url
        elif fctype == "meteofrance.com":
            pass
        elif fctype == "darksky.net":
            forecast_url += "?exclude=currently,minutely,hourly,alerts,flags&lang=en"
            if metric == "1":
                forecast_url += "&units=ca"
        elif fctype == "openweathermap.org":
            if metric:
                forecast_url += "&units=metric"
            else:
                forecast_url += "&units=imperial"
        elif fctype == "apixu.com":
            forecast_url += "&days=10"
        elif fctype == "weather.com":
            forecast_url = "https://api.weather.com/v2/turbo/vt1dailyForecast?apiKey=d522" + \
                           "aa97197fd864d36b418f39ebb323&format=json&geocode=" + forecast_url + \
                           "&language=en-US"
            if metric:
                forecast_url += "&units=m"
            else:
                forecast_url += "&units=e"
        elif fctype == "met.ie":
            metierev = "https://prodapi.metweb.ie/location/reverse/" + \
                       forecast_url.replace(",", "/")
            forecast_url = "https://prodapi.metweb.ie/weather/daily/" + \
                           forecast_url.replace(",", "/") + "/10"

            metierev = download(metierev)
            metierev[1] = metierev[1].decode('utf8')
            if metierev[0] is False:
                metierev[1] = str(metierev[1])
                return metierev

            jobj = json.loads(metierev[1].strip())
            metierev = jobj["city"] + ", Ireland"
            set_string("metierev", metierev)
        else:
            return [False, "Forecast type '" + fctype + "' isn't a valid option."]

        data = get_forecast(forecast_url, True)
        if data[0] is False:
            data[1] = str(data[1])
            return data

    if (fctype == "weather.gov" or fctype == "yahoo") and use_icons != "1":
        return [False, "Forecast type '" + fctype + "' needs to have icons available, " + \
                       "Please switch to using icons and try again."]

    if use_icons == "1" and \
        (check_for_icons()[0] is False or int(get_string("icon_version", 0)) < ICON_VERSION):
        binfile = download(ICON_URL)
        if not binfile[0]:
            binfile[1] = str(binfile[1])
            return binfile

        write_binary("icons.zip", binfile[1], CACHEBASE)
        zip_ref = zipfile.ZipFile(CACHEBASE + "/icons.zip", 'r')
        zip_ref.extractall(CACHEBASE + "/")
        zip_ref.close()
        set_string('icon_version', str(ICON_VERSION))

    if webcam_url != "" and webcam_url != oldwebcam:
        dled = get_webcam(webcam_url, True)
        if dled[0] is False:
            dled[1] = str(dled[1])
            return dled

    if custom_url != "" and custom_url != oldcustom:
        dled = download(custom_url)
        if dled[0] is False:
            dled[1] = str(dled[1])
            return dled

    set_string('data_url', data_url)
    set_string('rad_type', rad_type)
    set_string('radar_url', radar_url)
    set_string('fctype', fctype)
    set_string('forecast_url', forecast_url)
    set_string('webcam_url', webcam_url)
    set_string('custom_url', custom_url)

    return [True, "Everything looks a-ok...", rad_type, radar_url, fctype]

TMP = read_file("/assets/apixu.json", APPBASE)
CONDITIONS = json.loads(TMP[1])
    