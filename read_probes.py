def read_probes():
    '''
    Read the temperature from all currently-attached probes, convert reading
    to Fahrenheit, get current datetime, and return all as dictionary/JSON in
    the following format:
        { datetime: {
            probe1: {
                'Celsius': reading,
                'Fahrenheit': reading
                }
            probe2: {
                'Celsius': reading,
                'Fahrenheit': reading
                }
            ...
            }
        }
    '''

    import glob
    import arrow

    probe_list = glob.glob('/sys/bus/w1/devices/28-*')

    probe_ids = []

    for item in probe_list:
        probe_ids.append(item.split('/')[-1])

    curr_datetime = arrow.now().format()

    probe_readings = {}

    for probe in probe_ids:
        with open('/sys/bus/w1/devices/' + probe + '/w1_slave') as reading:
            temp_list = []
            for line in reading:
                temp_list.append(line.strip())
            celsius_reading = float(temp_list[-1].split()[-1][2:]) / 1000
            fahren_reading = celsius_reading * 9.0 / 5.0 + 32.0
            probe_readings[probe[-4:]] = {
                                    "C": celsius_reading,
                                    "F": fahren_reading
                                    }

    current_reading = {}

    current_reading[curr_datetime] = probe_readings

    return current_reading


if __name__ == "__main__":

    current_reading = read_probes()

    import json
    print json.dumps(current_reading,
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))
