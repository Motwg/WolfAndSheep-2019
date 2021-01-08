from chase import simulation as chase
import argparse
import os
import configparser
import logging

name = "chase"


def parse_args():
    parser = argparse.ArgumentParser(description='Symulacja wilka i owiec.')
    parser.add_argument('-l', '--log', metavar='LEVEL', dest='log_level', default=None,
                        help='zapis zdarzeń do dziennika, gdzie LEVEL - poziom zdarzeń (DEBUG, INFO, WARNING, ERROR lub CRITICAL)')
    parser.add_argument('-c', '--config', metavar='FILE', dest='config_file', default=os.curdir+'/config/config.ini',
                        help='dodatkowy plik konfiguracyjny, gdzie FILE - nazwa pliku')
    parser.add_argument('-d', '--dir', metavar='DIR', dest='dir', default='files',
                        help='podkatalog, w którym mają zostać zapisane pliki pos.json, alive.csv oraz chase.log, gdzie DIR - nazwa podkatalogu')
    parser.add_argument('-r', '--rounds', metavar='NUM', type=int, default=50, dest='turns',
                        help='liczba tur, gdzie NUM - liczba całkowita')
    parser.add_argument('-s', '--sheep', metavar='NUM', type=int, default=15, dest='sheeps_number',
                        help='liczba owiec, gdzie NUM - liczba całkowita')
    parser.add_argument('-w', '--wait', action='store_const', default=False, const=True,
                        help='oczekiwanie na naciśnięcie klawisza po wyświetlaniu podstawowych informacji o stanie symulacji na zakończenie każdej tury')
    return parser.parse_args()


def check_if_positive(values):
    logging.debug("Args: {0}".format(locals()))
    for v in values:
        if v < 0:
            logging.error("{0} from {1} is negative".format(v, locals()))
            raise ValueError("One of config variables is negative")


# arg parsing
args = parse_args()

if args.dir != '.':
    os.makedirs(args.dir, exist_ok=True)

# logging
if args.log_level is not None:
    logging.basicConfig(level=args.log_level, filename=(args.dir+'/chase.log'), filemode='w',
                        format='%(levelname)-8s %(funcName)-20s %(message)s')
else:
    logging.disable()

# config
config = configparser.ConfigParser()
if config.read(args.config_file):
    init_pos_limit = config.getfloat('Terrain', 'InitPosLimit')
    sheep_move_dist = config.getfloat('Movement', 'SheepMoveDist')
    wolf_move_dist = config.getfloat('Movement', 'WolfMoveDist')
else:
    init_pos_limit = 10.0
    sheep_move_dist = 1.0
    wolf_move_dist = 0.5
check_if_positive([init_pos_limit, sheep_move_dist, wolf_move_dist])


# app =========================================================================================
sheep = chase.Animal.generate_animals(args.sheeps_number, sheep_move_dist, init_pos_limit)
wolves = chase.Animal.generate_animals(1, wolf_move_dist, init_pos_limit)
chase.simulate(wolves, sheep, args.turns, args.dir, args.wait)


