#!/usr/bin/python3

"""blah!"""

import json

class Day(object):
    """ Store day details in a class """

    day = ""
    icon = ""
    text = ""
    max = ""
    min = ""
    timestamp = 0

    def __init__(self):
        pass

    def __str__(self):

        output = {}
        output['day'] = self.day
        output['icon'] = self.icon
        output['text'] = self.text
        output['max'] = self.max
        output['min'] = self.min
        output['timestamp'] = self.timestamp
        # dd MMM yyyy HH:mm
        # output['ftime'] = datetime.datetime.fromtimestamp(self.timestamp)
        # output['ftime'] = output['ftime'].strftime("%d %b. %Y %H:%M")

        return json.dumps(output)
