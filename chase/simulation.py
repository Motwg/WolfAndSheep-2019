import csv
import json
import logging
import math
import random as ran


def distance(point1, point2):
    logging.debug("Args: {0}".format(locals()))
    if type(point1) != type(point2):
        logging.warning("Types of given arguments are different: {0} != {1}".format(point1, point2))
    logging.debug("Returns: {0}".format(((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2) ** 0.5))
    return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2) ** 0.5


class Animal:

    def __init__(self, id, x, y, move_dist):
        logging.info("{0}:[{1}, {2}]".format(id, x, y))
        self.id = id
        self.x = x
        self.y = y
        self.move_dist = move_dist

    def __lt__(self, other):
        return self.id < other.id

    def move(self, x, y):
        logging.info("{0}:[{1}, {2}] => [{3}, {4}]".format(self.id, self.x, self.y, self.x+x, self.y+y))
        self.x += x
        self.y += y

    def move_in_direction(self, direction):
        if direction == 0:
            self.move(0, self.move_dist)
        elif direction == 1:
            self.move(0, -self.move_dist)
        elif direction == 2:
            self.move(self.move_dist, 0)
        elif direction == 3:
            self.move(-self.move_dist, 0)
        elif type(direction) == Animal:
            degrees = math.atan2(direction.y-self.y, direction.x-self.x)
            self.move(
                self.move_dist * math.cos(degrees),
                self.move_dist * math.sin(degrees)
                )

    def move_in_random_direction(self):
        self.move_in_direction(ran.randint(0, 3))

    def distance(self, animal):
        return distance([self.x, self.y], [animal.x, animal.y])

    def find_the_closest_animal(self, animals):
        dist = self.distance(animals[0])
        closest = animals[0]

        for animal in animals:
            new_dist = distance([self.x, self.y], [animal.x, animal.y])
            if dist > new_dist:
                dist = new_dist
                closest = animal
        return closest

    def eaten(self):
        logging.info("Eaten: {0}:[{1}, {2}]".format(self.id, self.x, self.y))
        self.x = None
        self.y = None

    def get_pos(self):
        return [self.x, self.y]

    @staticmethod
    def generate_animals(animals_number,
                         move_range,
                         spawn_range=10.0):
        logging.debug("Args: {0}".format(locals()))

        new_animals = []
        for s in range(animals_number):
            new_animals.append(Animal(
                s + 1,
                ran.random() * spawn_range * 2 - spawn_range,
                ran.random() * spawn_range * 2 - spawn_range,
                move_range))

        logging.debug("Returns: {0}".format(new_animals))
        return new_animals


def save_json(json_data, filename='pos.json', save_dir='.'):
    logging.debug("Args: {0}".format(locals()))

    with open(save_dir+"/"+filename, 'w') as json_file:
        json.dump(json_data, json_file)


def save_csv(csv_data=None, filename='alive.csv', opening_parameter='a', save_dir='.'):
    logging.debug("Args: {0}".format(locals()))

    with open(save_dir+"/"+filename, opening_parameter, newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if csv_data is not None:
            writer.writerow(csv_data)


def simulate(wolves_sim, sheep_sim, turns_number=50, save_dir='.', wait=False):
    logging.debug("Args: {0}".format(locals()))

    sheep_eaten = []
    save_csv(None, 'alive.csv', 'w', save_dir)  # nadpisuje plik

    for t in range(turns_number):
        for s in sheep_sim:
            s.move_in_random_direction()

        for w in wolves_sim:
            closest = w.find_the_closest_animal(sheep_sim)
            if w.distance(closest) <= w.move_dist:
                w.x = closest.x
                w.y = closest.y
                closest.eaten()
                sheep_index = closest.id
                sheep_eaten.append(closest)
                sheep_sim.remove(closest)
            else:
                w.move_in_direction(closest)
                sheep_index = None

        print("Turn: {0}\n"
              "Wolf position: {1}\n"
              "Sheep alive: {2}\n"
              "Eaten sheep: {3}".format(t + 1, wolves_sim[0].get_pos(), len(sheep_sim), sheep_index))

        # zapis json i csv
        pos = {
            'round_no': t + 1,
            'wolf_pos': wolves_sim[0].get_pos(),
            'sheep_pos': list(map(Animal.get_pos, sorted(sheep_sim+sheep_eaten)))
        }
        save_json(pos, 'pos.json', save_dir)
        save_csv([t+1, len(sheep_sim)], 'alive.csv', 'a', save_dir)

        # oczekiwanie na klawisz
        if wait:
            input("Press Enter to continue...")

        # populacja owiec spadnie do 0 => koniec symulacji
        if len(sheep_sim) == 0:
            logging.info("Wolf ate every sheep. End of simulation.")
            break

    logging.debug("Returns: {0}".format(sheep_eaten))
    return sheep_eaten
