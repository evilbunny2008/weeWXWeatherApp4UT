""" Weather.gov forecast code """

import base64
import json
import time
from io import BytesIO
import os
import re
import day
import main

try:
    import sys
    sys.path.append('../PIL/')
    from PIL import Image, ImageDraw, ImageFont
except ImportError as err:
    print(err)

NWS = {"bkn":"Y|L|Broken Clouds", "blizzard":"Y|L|Blizzard", "cold":"Y|L|Cold",
       "cloudy":"Y|L|Overcast (old cloudy)", "du":"N|M|Dust", "dust":"N|M|Dust (old)",
       "fc":"N|L|Funnel Cloud", "nsvrtsra":"N|L|Funnel Cloud (old)", "few":"Y|L|Few Clouds",
       "fg":"Y|R|Fog", "br":"Y|R|Fog \\/ mist old", "fu":"N|L|Smoke", "smoke":"N|L|Smoke (old)",
       "fzra":"Y|L|Freezing rain", "fzrara":"Y|L|Rain\\/Freezing Rain (old)",
       "fzra_sn":"Y|L|Freezing Rain\\/Snow", "mix":"Y|L|Freezing Rain\\/Snow",
       "hi_bkn":"Y|L|Broken Clouds (old)", "hi_few":"Y|L|Few Clouds (old)",
       "hi_sct":"Y|L|Scattered Clouds (old)", "hi_skc":"N|L|Clear Sky (old)",
       "hi_nbkn":"Y|L|Night Broken Clouds (old)", "hi_nfew":"Y|L|Night Few Clouds (old)",
       "hi_nsct":"Y|L|Night Scattered Clouds (old)", "hi_nskc":"N|L|Night Clear Sky (old)",
       "hi_nshwrs":"Y|R|Night Showers", "hi_ntsra":"Y|L|Night Thunderstorm",
       "hi_shwrs":"Y|R|Showers", "hi_tsra":"Y|L|Thunderstorm", "hur_warn":"Y|L|Hurrican Warning",
       "hur_watch":"Y|L|Hurricane Watch", "hurr":"Y|L|Hurrican Warning old",
       "hurr-noh":"Y|L|Hurricane Watch old", "hz":"N|L|Haze", "hazy":"N|L|Haze old",
       "hot":"N|R|Hot", "ip":"Y|L|Ice Pellets", "minus_ra":"Y|L|Stopped Raining",
       "ra1":"N|L|Stopped Raining (old)", "mist":"Y|R|Mist (fog) (old)",
       "nbkn":"Y|L|Night Broken Clouds", "nblizzard":"Y|L|Night Blizzard",
       "ncloudy":"Y|L|Overcast night(old ncloudy)", "ncold":"Y|L|Night Cold",
       "ndu":"N|M|Night Dust", "nfc":"N|L|Night Funnel Cloud", "nfew":"Y|L|Night Few Clouds",
       "nfg":"Y|R|Night Fog", "nbr":"Y|R|Night Fog\\/mist (old)", "nfu":"N|L|Night Smoke",
       "nfzra":"Y|L|Night Freezing Rain", "nfzra_sn":"Y|L|Night Freezing Rain\\/Snow",
       "nip":"Y|L|Night Ice Pellets", "novc":"Y|L|Night Overcast", "nra":"Y|30|Night Rain",
       "nraip":"Y|M|Night Rain\\/Ice Pellets", "nra_fzra":"Y|30|Night Freezing Rain",
       "nmix":"Y|30|Night Freezing Rain\\/Snow (old)", "nra_sn":"Y|M|Night Snow",
       "nrasn":"Y|M|Night Snow (old)", "nsct":"Y|L|Night Scattered Clouds",
       "pcloudyn":"Y|L|Night Partly Cloudy (old)", "nscttsra":"Y|M|Night Scattered Thunderstorm",
       "nshra":"Y|8|Night Rain Showers", "nskc":"N|L|Night Clear", "nsn":"Y|L|Night Snow",
       "nsnip":"Y|L|Night Snow\\/Ice Pellets", "nsn_ip":"Y|L|Night Snow\\/Ice Pellets (old)",
       "ntor":"N|L|Night Tornado", "ntsra":"Y|8|Night Thunderstorm",
       "nwind_bkn":"Y|5|Night Windy\\/Broken Clouds", "nwind_few":"Y|5|Night Windy\\/Few Clouds",
       "nwind_ovc":"Y|5|Night Windy\\/Overcast", "nwind_sct":"Y|5|Night Windy\\/Scattered Clouds",
       "nwind_skc":"N|5|Night Windy\\/Clear", "nwind":"N|5|Night Windy\\/Clear (old)",
       "ovc":"Y|L|Overcast", "ra":"Y|30|Rain", "raip":"Y|M|Rain\\/Ice Pellets",
       "ra_fzra":"Y|30|Rain\\/Freezing Rain", "ra_sn":"Y|M|Rain\\/Snow",
       "rasn":"Y|M|Rain\\/Snow (old)", "sct":"Y|L|name", "pcloudy":"Y|L|Partly Cloudy (old)",
       "scttsra":"Y|M|name", "shra":"Y|10|Rain Showers", "shra2":"Y|10|Rain Showers (old)",
       "skc":"N|L|Clear", "sn":"Y|L|Snow", "snip":"Y|L|Snow\\/Ice Pellets",
       "sn_ip":"Y|L|Snow\\/Ice Pellets (old)", "tcu":"Y|L|Towering Cumulus (old)",
       "tor":"N|L|Tornado", "tsra":"Y|10|Thunderstorm", "tstormn":"Y|L|Thunderstorm night (old)",
       "ts_nowarn":"Y|L|Tropical Storm", "ts_warn":"Y|L|Tropical Storm Warning",
       "tropstorm-noh":"Y|L|Tropical Storm", "tropstorm":"Y|L|Tropical Storm Warning old",
       "ts_watch":"Y|L|Tropical Storm Watch", "ts_hur_flags":"Y|L|Hurrican Warning old",
       "ts_no_flag":"Y|L|Tropical Storm old", "wind_bkn":"Y|8|Windy\\/Broken Clouds",
       "wind_few":"Y|8|Windy\\/Few Clouds", "wind_ovc":"Y|8|Windy\\/Overcast",
       "wind_sct":"Y|8|Windy\\/Scattered Clouds", "wind_skc":"N|8|Windy\\/Clear",
       "wind":"N|L|Windy\\/Clear (old)", "na":"N|L|Not Available"}

FONT = ImageFont.FreeTypeFont("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf", \
                              size=10)

def combine_images(bmp1, bmp2, fimg, simg, fnum, snum):
    """ Combine weather.gov images for forecast """

    x_1, y_1 = bmp1.size
    x_2, y_2 = bmp2.size

    bits = NWS[fimg].split("|")
    # print("NWS[" + fimg + "] == " + NWS[fimg])
    # print("bits[1] == " + bits[1])
    if bits[1] == "L":
        bmp1 = bmp1.crop((0, 0, x_1 // 2, y_1))
    elif bits[1] == "R":
        bmp1 = bmp1.crop((x_1 // 2, 0, x_1, y_1))
    else:
        bmp1 = bmp1.crop((x_1 // 4, 0, x_1 * 3 // 4, y_1))

    bits = NWS[simg].split("|")
    # print("NWS[" + simg + "] == " + NWS[simg])
    # print("bits[1] == " + bits[1])
    if bits[1] == "L":
        bmp2 = bmp2.crop((0, 0, x_2 // 2, y_2))
    elif bits[1] == "R":
        bmp2 = bmp2.crop((x_2 // 2, 0, x_2, y_2))
    else:
        bmp2 = bmp2.crop((x_2 // 4, 0, x_2 * 3 // 4, y_2))

    bmp = Image.new("RGBA", (x_1, y_1), (0, 0, 0, 255))
    bmp.paste(bmp1, (0, 0))
    bmp.paste(bmp2, (x_1 // 2, 0))

    bmp = do_text(bmp, fnum, snum)

    return img_to_base64(bmp)

def do_text(bmp, fnum, snum):
    """ Combine the text functions """

    x_1, y_1 = bmp.size

    draw = ImageDraw.Draw(bmp, 'RGBA')

    if fnum != "%" or snum != "%":
        draw.rectangle((0, y_1 - 14, x_1 - 1, y_1 - 1), outline=(0, 0, 0, 255),
                       fill=(255, 255, 255, 0))

    if fnum != "%" and snum != "%":
        # Draw arrow
        draw.line((x_1 // 2 + 5, y_1 - 9, x_1 // 2 + 8, y_1 - 7), fill="#00487b")
        draw.line((x_1 // 2 - 8, y_1 - 7, x_1 // 2 + 8, y_1 - 7), fill="#00487b")
        draw.line((x_1 // 2 + 5, y_1 - 5, x_1 // 2 + 8, y_1 - 7), fill="#00487b")

    if fnum != "%":
        draw.text((2, y_1 - 12), fnum, font=FONT, fill="#00487b")

    if snum != "%":
        draw.text((x_1 - 30, y_1 - 12), snum, font=FONT, fill="#00487b")

    del draw

    return bmp

def img_to_base64(bmp):
    """ Save image in base64 string """

    buffer = BytesIO()
    bmp.save(buffer, format="JPEG")
    myimage = str(base64.b64encode(buffer.getvalue()))

    return "data:image/jpeg;base64," + myimage[2:-1]

def combine_image(bmp, fnum, snum):
    """ Combine weather.gov forecast with image """

    bmp = do_text(bmp, fnum, snum)
    return img_to_base64(bmp)

def process_wgov(data):
    """ Process the data from weather.gov """

    metric = main.get_string("metric", "1")

    days = ""

    jobj = json.loads(data)

    desc = jobj['currentobservation']['name']
    # tmp = jobj['creationDate']
    # date = tmp[:-3] + tmp[-2:]
    # print(date)

    # timestamp = time.mktime(time.strptime(date, '%Y-%m-%dT%H:%M:%S%z'))

    period_name = jobj['time']['startPeriodName']
    valid_time = jobj['time']['startValidTime']
    weather = jobj['data']['weather']
    icon_link = jobj['data']['iconLink']
    temperature = jobj['data']['temperature']

    rng = range(0, len(period_name))

    for i in rng:
        myday = day.Day()
        # https://forecast.weather.gov/newimages/medium/bkn.png
        # DualImage.php?i=bkn&j=scttsra&jp=30
        # https://forecast.weather.gov/DualImage.php?i=bkn&j=scttsra&jp=30
        icon_link[i] = icon_link[i].replace("http://", "https://").replace(".png", ".jpg").strip()

        file_name = "wgov" + os.path.basename(icon_link[i])
        if file_name.startswith("wgovDualImage.php"):
            tmp = icon_link[i].split("?", 1)[1].strip()
            fimg = simg = ""
            fper = sper = ""
            lines = tmp.split("&")
            for line in lines:
                line = line.strip()
                bits = line.split("=", 1)
                if bits[0].strip() == "i":
                    fimg = "wgov" + bits[1].strip() + ".jpg"
                if bits[0].strip() == "j":
                    simg = "wgov" + bits[1].strip() + ".jpg"
                if bits[0].strip() == "ip":
                    fper = bits[1].strip()
                if bits[0].strip() == "jp":
                    sper = bits[1].strip()

            bmp1 = Image.open(main.CACHEBASE + "/" + fimg).convert("RGBA")

            if fimg != simg:
                bmp2 = Image.open(main.CACHEBASE + "/" + simg).convert("RGBA")
                icon_link[i] = combine_images(bmp1, bmp2, fimg[4:-4], simg[4:-4],
                                              fper + "%", sper + "%")
            else:
                icon_link[i] = combine_image(bmp1, fper + "%", sper + "%")
        else:
            match = re.search(r"\d{2,3}", file_name)
            if match is not None:
                file_name = re.sub(r'\d{2,3}\.jpg$', ".jpg", file_name)
                bmp1 = Image.open(main.CACHEBASE + "/" + file_name).convert("RGBA")
                icon_link[i] = combine_image(bmp1, match.group(0) + "%", "%")
            else:
                icon_link[i] = file_name

        tmp = valid_time[i]
        date = tmp[:-3] + tmp[-2:]

        myday.timestamp = time.mktime(time.strptime(date, '%Y-%m-%dT%H:%M:%S%z'))
        myday.day = period_name[i]

        myday.max = temperature[i] + "&deg;F"
        if metric == "1":
            myday.max = str(round((float(temperature[i]) - 32) * 5 / 9)) + "&deg;C"

        myday.text = weather[i]
        myday.icon = icon_link[i]

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    return [True, days, desc]
