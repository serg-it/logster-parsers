import time
import re
from pygster.pygster_helper import PygsterParsingException, PygsterParser, MetricObject


class HAProxyPygster(PygsterParser):

    def __init__(self, option_string=None):
        '''Initialize any data structures or variables needed for keeping track
        of the tasty bits we find in the log we are parsing.'''

        self.http_1x = {
            'requests': 0,
            'time': 0,
            'bytes': 0,
        }
        self.http_2x = {
            'requests': 0,
            'time': 0,
            'bytes': 0,
        }
        self.http_3x = {
            'requests': 0,
            'time': 0,
            'bytes': 0,
        }
        self.http_4x = {
            'requests': 0,
            'time': 0,
            'bytes': 0,
        }
        self.http_5x = {
            'requests': 0,
            'time': 0,
            'bytes': 0,
        }

        # Regular expression for matching lines we are interested in, and capturing
        # fields from the line (in this case, http_status_code).
        self.reg = re.compile('.* \d+/\d+/\d+/\d+/(?P<time>\d+) (?P<status>\d+) (?P<bytes>\d+) .*')


    def parse_line(self, line):
        '''This function should digest the contents of one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''

        try:
            # Apply regular expression to each line and extract interesting bits.
            regMatch = self.reg.match(line)

            if regMatch:
                line_log = regMatch.groupdict()
                status = int(line_log['status'])

                if (status < 200):
                    self.http_1x['requests'] += 1
                    self.http_1x['time'] += int(line_log['time'])
                    self.http_1x['bytes'] += int(line_log['bytes'])
                elif (status < 300):
                    self.http_2x['requests'] += 1
                    self.http_2x['time'] += int(line_log['time'])
                    self.http_2x['bytes'] += int(line_log['bytes'])
                elif (status < 400):
                    self.http_3x['requests'] += 1
                    self.http_3x['time'] += int(line_log['time'])
                    self.http_3x['bytes'] += int(line_log['bytes'])
                elif (status < 500):
                    self.http_4x['requests'] += 1
                    self.http_4x['time'] += int(line_log['time'])
                    self.http_4x['bytes'] += int(line_log['bytes'])
                else:
                    self.http_5x['requests'] += 1
                    self.http_5x['time'] += int(line_log['time'])
                    self.http_5x['bytes'] += int(line_log['bytes'])

            else:
                raise PygsterParsingException("regmatch failed to match")

        except Exception as e:
            raise PygsterParsingException("regmatch or contents failed with %s" % e)

    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''
        self.duration = float(duration)

        # Return a list of metrics objects
        return [
            MetricObject("1xx.count", self.http_1x['requests'], metric_type='c'),
            MetricObject("1xx.time", self.http_1x['time'], metric_type='ms'),
            MetricObject("1xx.size", self.http_1x['bytes'], metric_type='b'),
            MetricObject("2xx.count", self.http_2x['requests'], metric_type='c'),
            MetricObject("2xx.time", self.http_2x['time'], metric_type='ms'),
            MetricObject("2xx.size", self.http_2x['bytes'], metric_type='b'),
            MetricObject("3xx.count", self.http_3x['requests'], metric_type='c'),
            MetricObject("3xx.time", self.http_3x['time'], metric_type='ms'),
            MetricObject("3xx.size", self.http_3x['bytes'], metric_type='b'),
            MetricObject("4xx.count", self.http_4x['requests'], metric_type='c'),
            MetricObject("4xx.time", self.http_4x['time'], metric_type='ms'),
            MetricObject("4xx.size", self.http_4x['bytes'], metric_type='b'),
            MetricObject("5xx.count", self.http_5x['requests'], metric_type='c'),
            MetricObject("5xx.time", self.http_5x['time'], metric_type='ms'),
            MetricObject("5xx.size", self.http_5x['bytes'], metric_type='b'),
        ]
