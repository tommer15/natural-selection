import random

class Blob:

    def __init__(self, location, speed, color):
        self.color = color
        self.location = location
        self.speed = speed
        self.ready_to_reproduce = False
        self.death_time = False


    def move(self, world_size):
        debug_mode = False
        starting_location = self.location

        h_boundary = 0.5
        v_boundary = 0.5
        if debug_mode: print(starting_location)
        if starting_location[0] < 0.05*world_size:
            if debug_mode: print('very close to left most edge')
            h_boundary = 0

        if starting_location[0] > 0.95*world_size:
            h_boundary = 1
            if debug_mode: print('very close to right most edge')

        if starting_location[1] < 0.05*world_size:
            v_boundary = 0
            if debug_mode: print('very close to highest edge')

        if starting_location[1] > 0.95*world_size:
            v_boundary = 1
            if debug_mode: print('very close to lowest edge')


        step_seed_h = random.random()
        if step_seed_h > h_boundary:
            step_h = 1 * self.speed
        else:
            step_h = -1 * self.speed

        step_seed_v = random.random()
        if step_seed_v > v_boundary :
            step_v = 1 * self.speed
        else:
            step_v = -1 * self.speed

        end_location = starting_location.copy()
        end_location[0] = end_location[0] + step_h
        end_location[1] = end_location[1] + step_v
        self.location = end_location

    def die(self):
        self.death_time = True

    def reproduce(self):
        self.ready_to_reproduce = True
