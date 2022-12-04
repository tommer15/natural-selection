import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from blob_class import Blob
import random


animate = False


world_size = 100
initial_number_of_blobs = 100
length_of_day = 1
number_of_days = 50
number_of_sims = 100
random_generation_num = 0

sim_pop_size_over_time_list = []
sim_black_pop_size_over_time_list = []
sim_white_pop_size_over_time_list = []

for sim_number in range(number_of_sims):
    print('sim number ' + str(sim_number), end = '...')
    c = np.zeros([world_size, world_size])
    Blobs_list = []
    pop_size_list = []
    black_pop_size_list = []
    white_pop_size_list = []

    print('seeding', end = '...')
    for blob_num in range(initial_number_of_blobs):
        y_i_loc = int(random.random() * world_size - 5)
        x_i_loc = int(random.random() * world_size - 5)
        Blobs_list.append(Blob([x_i_loc,y_i_loc], int(random.random() * 2 + 1), 'white'))

    print('simulating', end = '...')

    arr = []
    for d in range(number_of_days):
        pop_size_list.append(len(Blobs_list))
        #print('day' + str(d) + ' - ' + str(len(Blobs_list)) + ' Blobs')
        for t in range(length_of_day): #timesteps in days
            c = np.zeros([world_size, world_size])
            for blob_num in range(len(Blobs_list)):
                Blobs_list[blob_num].move(world_size)
                c[Blobs_list[blob_num].location[0],Blobs_list[blob_num].location[1]] += 1
            arr.append(c)

        kill_list = []
        for blob_num in range(len(Blobs_list)):
            die_chance = random.random()
            reproduce_chance = random.random()
            if die_chance >= 0.98:
                Blobs_list[blob_num].die()
            if reproduce_chance >= 0.98:
                Blobs_list[blob_num].reproduce()

            if Blobs_list[blob_num].death_time:
                kill_list.append(blob_num)
                pass
            else:
                if Blobs_list[blob_num].ready_to_reproduce:
                    Blobs_list.append(Blob([Blobs_list[blob_num].location[0], Blobs_list[blob_num].location[1]],
                                           int(random.random() * 2 + 1), 'white'))
                    Blobs_list[blob_num].ready_to_reproduce = False
        for i in range(random_generation_num):
            Blobs_list.append(Blob([10,10],int(random.random() * 2 + 1), 'black'))

        for index, item in enumerate(Blobs_list.copy()):
            if index in kill_list:
                Blobs_list.remove(item)

        #census
        number_of_blacks = 0
        number_of_whites = 0
        for blob_num in range(len(Blobs_list)):
            if Blobs_list[blob_num].color == 'black':
                number_of_blacks += 1
            if Blobs_list[blob_num].color == 'white':
                number_of_whites += 1
        black_pop_size_list.append(number_of_blacks)
        white_pop_size_list.append(number_of_whites)

    sim_pop_size_over_time_list.append(pop_size_list)
    sim_black_pop_size_over_time_list.append(black_pop_size_list)
    sim_white_pop_size_over_time_list.append(white_pop_size_list)

    print('!')
if animate:
    print('animating')
    fig = plt.figure()
    i=0
    im = plt.imshow(arr[0], animated=True)
    title = plt.title('dafdfa')
    def updatefig(*args):
        global i
        title.set_text('Day: ' + str(int(i/length_of_day)) + '.. Time' + str(i))
        if (i<(length_of_day*number_of_days-1)):
            i += 1
        else:
            i=0
        im.set_array(arr[i])
        return im,
    ani = animation.FuncAnimation(fig, updatefig,  blit=True)
    plt.show()
else:
    print('plotting')
    #generate average
    avg_pop_size = []
    for i in range(len(pop_size_list)):
        avg_pop_size.append(np.mean([sublist[i] for sublist in sim_pop_size_over_time_list]))
    for i in range(len(sim_pop_size_over_time_list)):
        plt.plot(np.arange(0,len(pop_size_list),1), sim_pop_size_over_time_list[i], alpha=0.2)
    plt.plot(np.arange(0, len(pop_size_list), 1), avg_pop_size)
    plt.show()


    print('plotting')
    #generate average
    avg_black_pop_size = []
    avg_white_pop_size = []
    for i in range(len(pop_size_list)):
        avg_white_pop_size.append(np.mean([sublist[i] for sublist in sim_white_pop_size_over_time_list]))
        avg_black_pop_size.append(np.mean([sublist[i] for sublist in sim_black_pop_size_over_time_list]))
    plt.plot(np.arange(0, len(pop_size_list), 1), avg_white_pop_size, label = 'white')
    plt.plot(np.arange(0, len(pop_size_list), 1), avg_black_pop_size, label='black')
    plt.legend()
    plt.show()
