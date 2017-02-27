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

    # Raspberry pi location for DS18B20 probes. Each probe serial starts with
    # "28-"
    probe_list = glob.glob('/sys/bus/w1/devices/28-*')

    # Initialize empty probe_id list
    probe_ids = []

    # Extract the probe IDs from path folder name
    for item in probe_list:
        probe_ids.append(item.split('/')[-1])

    # Get the current date & time prior to taking readings
    curr_datetime = arrow.now().format()

    # Initialize empty probe_readings dictionary
    probe_readings = {}

    # Open the 'w1_slave' file in each probe folder
    for probe in probe_ids:
        with open('/sys/bus/w1/devices/' + probe + '/w1_slave') as reading:
            # We only care about the last item on the last line of each
            # w1_slave file, so initialize temporary list to hold all file
            # contents that are read.
            temp_list = []
            for line in reading:
                temp_list.append(line.strip())
            # Deg. C reading is the last space-separated element on the last
            # line of the 'w1_slave' file. Use list slicing to eliminate 't='
            # from that element, convert to float, and divide by 1000 to add in
            # a decimal point.
            celsius_reading = round(
                float(temp_list[-1].split()[-1][2:]) / 1000, 2
                )
            # Celsius to Fahrenheit conversion equation
            fahren_reading = round(celsius_reading * 9.0 / 5.0 + 32.0, 2)
            # Add to probe_readings dictionary:
            # key = last 4 digits of temperature probe ID (is unique key)
            # value = sub-dictionary of {C:reading, F:reading} current values
            probe_readings[probe[-4:]] = {
                                    "C": celsius_reading,
                                    "F": fahren_reading
                                    }

    # Initialize empty dictionary
    current_reading = {}

    # Add current probe_readings to dictionary with curr_datetime as key
    current_reading[curr_datetime] = probe_readings

    return current_reading


if __name__ == "__main__":

    current_reading = read_probes()

    # Pretty-print JSON dump of probe readings if file is run directly.
    import json
    print json.dumps(current_reading,
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))
