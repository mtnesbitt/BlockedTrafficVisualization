import requests
import json


def info_generator():
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

            yield (lon, lat, attack_protocol)


def get_color(protocol):
    if protocol == 'tcp':
        return 'r'
    elif protocol == 'udp':
        return 'b'
    elif protocol == 'icmp':
        return 'g'
    elif protocol == 'gre':
        return 'c'
    else:
        return 'k'


class AttackInfoManager:

    def __init__(self, num_values, initial_size, reduction_amount):
        self.num_values = num_values
        self.lons = []
        self.lats = []
        self.sizes = []
        self.colors = []
        self.initial_size = initial_size
        self.reduction_amount = reduction_amount
        self.g = info_generator()

        for count in range(num_values):
            (lon, lat, attack_protocol) = next(self.g)
            self.lons.append(lon)
            self.lats.append(lat)
            self.colors.append(get_color(attack_protocol))
            self.sizes.append(self.initial_size)

    def update(self):
        if self.sizes[0] - self.reduction_amount == 0:
            for count in range(self.num_values):
                self.lons.pop(0)
                self.lats.pop(0)
                self.sizes.pop(0)
                self.colors.pop(0)

        for index in range(len(self.sizes)):
            self.sizes[index] -= self.reduction_amount

        for count in range(self.num_values):
            (lon, lat, attack_protocol) = next(self.g)
            self.lons.append(lon)
            self.lats.append(lat)
            self.colors.append(get_color(attack_protocol))
            self.sizes.append(self.initial_size)

    def get_lons(self):
        return self.lons

    def get_lats(self):
        return self.lats

    def get_sizes(self):
        return self.sizes

    def get_colors(self):
        return self.colors
