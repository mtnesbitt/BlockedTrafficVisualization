import requests
import json
import more_itertools
import time


def generate_locations():

    filename = '20170531-inbound-block-ips-protocol.txt'

    locations = {}

    with open(filename, 'r') as f:
        for line in f:
            (attack_date, attack_time, attack_ip, attack_protocol) = line.split()

            if attack_ip not in locations:

                r = requests.get('http://localhost:8080/json/' + attack_ip)

                info = json.loads(r.text)

                locations[attack_ip] = (float(info['latitude']), float(info['longitude']))

                lat = float(info['latitude'])
                lon = float(info['longitude'])
            else:
                (lat, lon) = locations[attack_ip]

            yield (lon, lat)


def get_data(num_points):
    count = 0

    lons = []
    lats = []

    for lon, lat in generate_locations():
        lons.append(lon)
        lats.append(lat)

        count += 1
        if count == num_points:
            break


        if count % 100 == 0:
            print(count)

    return lons, lats


class DataProducer:

    def __init__(self):
        self.base_time = time.time()
        self.generator = more_itertools.peekable(generate_locations())

    def has_next(self):
        return self.generator.peek().attack_time < time.time()

    def next(self):
        if not self.has_next():
            raise Exception('next called when not items ready')

        return next(self.generator)


class AttackInstance:

    def __init__(self, attack_timestamp, attack_ip, attack_lon, attack_lat, attack_protocol):
        self.attack_timestamp = attack_timestamp
        self.attack_ip = attack_ip
        self.attack_lon = attack_lon
        setl.attack_lat = attack_lat
        self.attack_protocol = attack_protocol
