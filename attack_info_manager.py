import requests
import json

import time
import datetime
import ast


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

    def __init__(self, initial_size, reduction_amount):
        self.lons = []
        self.lats = []
        self.sizes = []
        self.colors = []
        self.initial_size = initial_size
        self.reduction_amount = reduction_amount
        self.get_attacks()
        self.num_values = 0

    def get_attacks(self):
        locations = {}
        attack_times = []

        starting_time = datetime.datetime.now() - datetime.timedelta(seconds=30)

        r1 = requests.get('http://10.230.1.59:5000/timestamp?t=' + str(starting_time))

        while True:

            attacks = ast.literal_eval(r1.text)
            self.num_values = attacks

            for a in attacks:
                (attack_time, attack_ip, attack_protocol) = a.split(",")
                attack_times.append(attack_time)

                if attack_ip not in locations:

                    r2 = requests.get('http://localhost:8080/json/' + attack_ip)
                    info = json.loads(r2.text)
                    locations[attack_ip] = (float(info['latitude']), float(info['longitude']))

                    lat = float(info['latitude'])
                    lon = float(info['longitude'])

                else:
                    (lat, lon) = locations[attack_ip]

                self.lons.append(lon)
                self.lats.append(lat)
                self.colors.append(get_color(attack_protocol))
                self.sizes.append(self.initial_size)

                if a is attacks[-1]:
                    new_attack_time = a.split(",")[0]
                    r1 = requests.get('http://10.230.1.59:5000/timestamp?t=' + str(new_attack_time))

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
