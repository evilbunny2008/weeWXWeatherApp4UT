""" meteofrance.com forecasts """

import main
import day

def process_mf(data):
    """ Process meteofrance.com Forecasts """

    use_icons = main.get_string("use_icons", "0")
    metric = main.get_string("metric", "1")

    days = ""

    desc = data.split("<h1>", 1)[1].split("</h1>", 1)[0].strip()
    data = data.split("<!-- LISTE JOURS -->", 1)[1].split("<!-- LISTE JOURS/ -->", 1)[0].strip()

    bits = data.split('title="')
    del bits[0]
    print("")

    for bit in bits:
        myday = day.Day()
        myday.day = bit.split("<a>", 1)[1].split("</a>", 1)[0].strip()
        myday.min = bit.split('class="min-temp">', 1)[1].split('°C Minimale', 1)[0].strip()
        myday.max = bit.split('class="max-temp">', 1)[1].split('°C Maximale', 1)[0].strip()
        myday.icon = bit.split('<dd class="pic40 ', 1)[1].split('">', 1)[0].strip()

        if metric == "1":
            myday.max = myday.max + "&deg;C"
            myday.min = myday.min + "&deg;C"
        else:
            myday.max = str(round(int(myday.max) * 9 / 5 + 32)) + "&deg;F"
            myday.min = str(round(int(myday.max) * 9 / 5 + 32)) + "&deg;F"

        icon = TABLE.get(myday.icon)
        if icon is None:
            # TODO: report/log missing CSS name
            myday.icon = None
        else:
            if use_icons != "1":
                if icon.replace("_", "-") != 'j-w1-8-n"':
                    myday.icon = "wi wi-meteofrance-" + icon.replace('_', '-')
                else:
                    myday.icon = "flaticon-thermometer"
            else:
                myday.icon = "mf_" + icon + ".png"

        days += str(myday) + ","

    if days[-1:] == ",":
        days = days[:-1]
    days = "[" + days + "]"

    print(days)

    return [True, days, desc]

def maketable():
    """ Preload css names to image names """

    table = {}

    table.update({"N_W1_0-N_0": "n_w2_1"})
    table.update({"N_W2_1": "n_w2_1"})
    table.update({"N_W1_0-N_7": "n_w2_1"})
    table.update({"J_W1_0-N": "n_w2_1"})
    table.update({"J_W1_0-N_0": "n_w2_1"})
    table.update({"J_W2_1": "n_w2_1"})

    table.update({"J_W1_0-N_5": "j_w1_0_n_5"})

    table.update({"N_W1_0-N_5": "n_w1_0_n_5"})

    table.update({"J_W2_2": "j_w1_0_n_2"})
    table.update({"J_W1_0-N_1": "j_w1_0_n_2"})
    table.update({"J_W1_0-N_2": "j_w1_0_n_2"})
    table.update({"J_W1_0-N_4": "j_w1_0_n_2"})
    table.update({"J_W1_0-N_6": "j_w1_0_n_2"})

    table.update({"N_W2_2": "n_w2_2"})
    table.update({"N_W1_0-N_1": "n_w2_2"})
    table.update({"N_W1_0-N_2": "n_w2_2"})
    table.update({"N_W1_0-N_4": "n_w2_2"})
    table.update({"N_W1_0-N_6": "n_w2_2"})

    table.update({"J_W1_0-N_3": "j_w2_3"})
    table.update({"N_W1_0-N_3": "j_w2_3"})
    table.update({"J_W2_3": "j_w2_3"})
    table.update({"N_W2_3": "j_w2_3"})

    table.update({"J_W1_1-N": "j_w1_1_n"})
    table.update({"J_W1_2-N": "j_w1_1_n"})
    table.update({"J_W1_33-N": "j_w1_1_n"})

    table.update({"N_W1_1-N": "n_w1_1_n"})
    table.update({"N_W1_2-N": "n_w1_1_n"})
    table.update({"N_W1_33-N": "n_w1_1_n"})

    table.update({"N_W1_1-N_3": "n_w1_1_n_3"})
    table.update({"J_W1_1-N_3": "n_w1_1_n_3"})
    table.update({"N_W1_2-N_3": "n_w1_1_n_3"})
    table.update({"J_W1_2-N_3": "n_w1_1_n_3"})
    table.update({"N_W1_33-N_3": "n_w1_1_n_3"})
    table.update({"J_W1_33-N_3": "n_w1_1_n_3"})

    table.update({"J_W1_3-N": "j_w2_4"})
    table.update({"N_W1_3-N": "j_w2_4"})
    table.update({"J_W2_4": "j_w2_4"})
    table.update({"N_W2_4": "j_w2_4"})

    table.update({"J_W1_4-N": "j_w2_5"})
    table.update({"J_W1_5-N": "j_w2_5"})
    table.update({"J_W1_6-N": "j_w2_5"})
    table.update({"J_W2_5": "j_w2_5"})
    table.update({"N_W2_5": "j_w2_5"})
    table.update({"N_W1_4-N": "j_w2_5"})
    table.update({"N_W1_5-N": "j_w2_5"})
    table.update({"N_W1_6-N": "j_w2_5"})

    table.update({"J_W1_7-N": "j_w1_7_n"})
    table.update({"N_W1_7-N": "j_w1_7_n"})

    table.update({"J_W1_8-N": "j_w1_8_n"})

    table.update({"N_W1_8-N": "n_w1_8_n"})

    table.update({"N_W1_8-N_3": "n_w1_8_n_3"})
    table.update({"J_W1_8-N_3": "n_w1_8_n_3"})

    table.update({"J_W1_9-N": "j_w2_6"})
    table.update({"J_W1_18-N": "j_w2_6"})
    table.update({"J_W1_30-N": "j_w2_6"})
    table.update({"J_W2_6": "j_w2_6"})
    table.update({"J_W2_12": "j_w2_6"})

    table.update({"N_W1_9-N": "n_w2_6"})
    table.update({"N_W1_18-N": "n_w2_6"})
    table.update({"N_W1_30-N": "n_w2_6"})
    table.update({"N_W2_6": "n_w2_6"})
    table.update({"N_W2_12": "n_w2_6"})

    table.update({"J_W1_9-N_3": "j_w1_9_n_3"})
    table.update({"N_W1_9-N_3": "j_w1_9_n_3"})
    table.update({"J_W1_18-N_3": "j_w1_9_n_3"})
    table.update({"N_W1_18-N_3": "j_w1_9_n_3"})
    table.update({"J_W1_30-N_3": "j_w1_9_n_3"})
    table.update({"N_W1_30-N_3": "j_w1_9_n_3"})

    table.update({"J_W1_19-N": "large_10_a"})
    table.update({"J_W2_8": "j_w2_8"})
    table.update({"J_W2_14": "j_w2_8"})

    table.update({"N_W1_19-N": "large_10_b"})
    table.update({"N_W2_8": "n_w2_8"})
    table.update({"N_W2_14": "n_w2_8"})

    table.update({"J_W1_10-N": "j_w1_10_n"})
    table.update({"J_W1_19-N": "j_w1_10_n"})
    table.update({"N_W1_10-N": "j_w1_10_n"})
    table.update({"N_W1_19-N": "j_w1_10_n"})

    table.update({"J_W1_11-N": "j_w2_9"})
    table.update({"N_W1_11-N": "j_w2_9"})
    table.update({"J_W2_9": "j_w2_9"})
    table.update({"N_W2_9": "j_w2_9"})

    table.update({"J_W1_32": "j_w1_32"})
    table.update({"J_W2_16": "j_w1_32"})

    table.update({"N_W1_32": "n_w1_32"})
    table.update({"N_W2_16": "n_w1_32"})

    table.update({"J_W1_12": "j_w1_12"})
    table.update({"N_W1_12": "j_w1_12"})
    table.update({"J_W1_32-N_3": "j_w1_12"})
    table.update({"N_W1_32-N_3": "j_w1_12"})
    table.update({"J_W2_17": "j_w1_12"})
    table.update({"N_W2_17": "j_w1_12"})

    table.update({"J_W1_13": "j_w2_13"})
    table.update({"J_W1_21": "j_w2_13"})
    table.update({"J_W2_7": "j_w2_13"})
    table.update({"J_W2_13": "j_w2_13"})

    table.update({"N_W1_13": "n_w1_13"})
    table.update({"N_W1_21": "n_w1_13"})
    table.update({"N_W2_7": "n_w1_13"})
    table.update({"N_W2_13": "n_w1_13"})

    table.update({"J_W1_13-N_3": "j_w_w1_13_n_3"})
    table.update({"N_W1_13-N_3": "j_w_w1_13_n_3"})
    table.update({"J_W1_21-N_3": "j_w_w1_13_n_3"})
    table.update({"N_W1_21-N_3": "j_w_w1_13_n_3"})

    table.update({"J_W1_14": "j_w1_14"})
    table.update({"J_W1_20": "j_w1_14"})

    table.update({"N_W1_14": "n_w1_14"})
    table.update({"N_W1_20": "n_w1_14"})

    table.update({"J_W1_20-N_3": "j_w1_14_n_3"})
    table.update({"N_W1_20-N_3": "j_w1_14_n_3"})
    table.update({"N_W1_14-N_3": "j_w1_14_n_3"})
    table.update({"J_W1_14-N_3": "j_w1_14_n_3"})

    table.update({"J_W1_15": "j_w2_10"})
    table.update({"J_W1_22": "j_w2_10"})
    table.update({"J_W2_10": "j_w2_10"})
    table.update({"J_W2_15": "j_w2_10"})
    table.update({"J_W2_19": "j_w2_10"})

    table.update({"N_W1_15": "n_w1_15"})
    table.update({"N_W1_22": "n_w1_15"})
    table.update({"N_W2_10": "n_w1_15"})
    table.update({"N_W2_15": "n_w1_15"})
    table.update({"N_W2_19": "n_w1_15"})

    table.update({"J_W1_22-N_3": "j_w1_16_n_3"})
    table.update({"N_W1_22-N_3": "j_w1_16_n_3"})
    table.update({"J_W1_15-N_3": "j_w1_16_n_3"})
    table.update({"N_W1_15-N_3": "j_w1_16_n_3"})
    table.update({"W1_16": "j_w1_16_n_3"})
    table.update({"J_W1_16-N": "j_w1_16_n_3"})
    table.update({"N_W1_16-N": "j_w1_16_n_3"})

    table.update({"J_W1_17-N": "n_w2_11"})
    table.update({"N_W1_17-N": "n_w2_11"})
    table.update({"N_W2_11": "n_w2_11"})
    table.update({"J_W2_11": "n_w2_11"})

    table.update({"J_W1_23-N": "j_w1_29-n"})
    table.update({"J_W1_28-N": "j_w1_29-n"})
    table.update({"J_W1_29-N": "j_w1_29-n"})

    table.update({"N_W1_23-N": "n_w1_28_n"})
    table.update({"N_W1_28-N": "n_w1_28_n"})
    table.update({"N_W1_29-N": "n_w1_28_n"})

    table.update({"J_W1_23-N_3": "n_w1_23_n_3"})
    table.update({"N_W1_23-N_3": "n_w1_23_n_3"})
    table.update({"J_W1_28-N_3": "n_w1_23_n_3"})
    table.update({"N_W1_28-N_3": "n_w1_23_n_3"})
    table.update({"J_W1_29-N_3": "n_w1_23_n_3"})
    table.update({"N_W1_29-N_3": "n_w1_23_n_3"})

    table.update({"J_W1_24-N": "j_w2_18"})
    table.update({"J_W1_26-N": "j_w2_18"})
    table.update({"J_W1_31-N": "j_w2_18"})
    table.update({"J_W2_18": "j_w2_18"})

    table.update({"N_W1_24-N": "n_w2_18"})
    table.update({"N_W1_26-N": "n_w2_18"})
    table.update({"N_W1_31-N": "n_w2_18"})
    table.update({"N_W2_18": "n_w2_18"})

    table.update({"J_W1_24-N_3": "j_w1_24_n_3"})
    table.update({"J_W1_31-N_3": "j_w1_24_n_3"})
    table.update({"J_W1_26-N_3": "j_w1_24_n_3"})
    table.update({"N_W1_26-N_3": "j_w1_24_n_3"})
    table.update({"N_W1_24-N_3": "j_w1_24_n_3"})
    table.update({"N_W1_31-N_3": "j_w1_24_n_3"})

    table.update({"J_W1_25-N": "j_w1_27_n"})
    table.update({"J_W1_27-N": "j_w1_27_n"})

    table.update({"N_W1_25-N": "n_w1_27_n"})
    table.update({"N_W1_27-N": "n_w1_27_n"})

    table.update({"J_W1_25-N_3": "n_w1_27_n_3"})
    table.update({"N_W1_25-N_3": "n_w1_27_n_3"})
    table.update({"J_W1_27-N_3": "n_w1_27_n_3"})
    table.update({"N_W1_27-N_3": "n_w1_27_n_3"})

    table.update({"J_W1_32-N_2": "j_w1_32_n_2"})

    return table

TABLE = maketable()
