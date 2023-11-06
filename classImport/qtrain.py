import datetime
from experience import Experience
from game import Game
import random
import json
import os, sys, time, datetime, json, random
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD , Adam, RMSprop
from keras.layers import PReLU
import matplotlib.pyplot as plt

def format_time(seconds):
    if seconds < 400:
        s = float(seconds)
        return "%.1f seconds" % (s,)
    elif seconds < 4000:
        m = seconds / 60.0
        return "%.2f minutes" % (m,)
    else:
        h = seconds / 3600.0
        return "%.2f hours" % (h,)
    

def qtrain(model, game, **opt):
    epsilon = 0.1
    n_epoch = opt.get('n_epoch', 15000)
    max_memory = opt.get('max_memory', 1000)
    data_size = opt.get('data_size', 50)
    weights_file = opt.get('weights_file', "")
    name = opt.get('name', 'model')
    start_time = datetime.datetime.now()

    # If you want to continue training from a previous model,
    # just supply the h5 file name to weights_file option
    if weights_file:
        print("loading weights from file: %s" % (weights_file,))
        model.load_weights(weights_file)


    # Initialize experience replay object
    experience = Experience(model, max_memory=max_memory)

    win_history = []   # history of win/lose game
    hsize = game.grid.occupation.size//2   # history window size
    win_rate = 0.0
    imctr = 1

    for epoch in range(n_epoch):
        print(f'######## EPOCH : {epoch}')
        loss = 0.0
        game_over = False

        # get initial envstate (1d flattened canvas)
        envstate = game.observe1D()

        n_episodes = 0
        while not game_over:
            valid_actions = list(game.actions_dict.keys())
            if not valid_actions: break
            prev_envstate = envstate
            # Get next action
            if np.random.rand() < epsilon:
                action = random.choice(valid_actions)
            else:
                action = np.argmax(experience.predict(prev_envstate))
            print(f"action : {action}, {game.actions_dict[action]}")
            #game.moveUnitShortCutAuto('sm',game.actions_dict[action])
            if game.actions_dict[action] != 'range':
                game.moveUnitShortCutAuto('sm',game.actions_dict[action],is_simu = True)
            else:
                game.rangeAttack('sm','ok',True) # attack a distance sm sur ork

            game.updateNbMinis() # update le nombre de fig de chaque joueur apres combat
            game.get_reward() # active la récompense de ce tour
            game.storeNbMinis() # stocke le nb de fig de chauqe joueur pour le comparer a l evolution au prochain tour 
            print(f'Score total : {game.total_reward}')
            print(f'Nb SM : {game.nb_mini_p1} et Nb ORK : {game.nb_mini_p2}')
            # Apply action, get reward and new envstate
            envstate, reward, game_status = game.getGameState()
            if game_status == 'win':
                win_history.append(1)
                game_over = True
            elif game_status == 'lose':
                win_history.append(0)
                game_over = True
            else:
                game_over = False

            # Store episode (experience)
            episode = [prev_envstate, action, reward, envstate, game_over]
            experience.remember(episode)
            n_episodes += 1

            # Train neural network model
            inputs, targets = experience.get_data(data_size=data_size)
            h = model.fit(
                inputs,
                targets,
                epochs=8,
                batch_size=16,
                verbose=0,
            )
            loss = model.evaluate(inputs, targets, verbose=0)

        if len(win_history) > hsize:
            win_rate = sum(win_history[-hsize:]) / hsize
    
        dt = datetime.datetime.now() - start_time
        t = format_time(dt.total_seconds())
        template = "Epoch: {:03d}/{:d} | Loss: {:.4f} | Episodes: {:d} | Win count: {:d} | Win rate: {:.3f} | time: {}"
        print(template.format(epoch, n_epoch-1, loss, n_episodes, sum(win_history), win_rate, t))
        # we simply check if training has exhausted all free cells and if in all
        # cases the agent won
        if win_rate > 0.9 : epsilon = 0.05

    # Save trained model weights and architecture, this will be used by the visualization code
    h5file = name + ".h5"
    json_file = name + ".json"
    model.save_weights(h5file, overwrite=True)
    with open(json_file, "w") as outfile:
        json.dump(model.to_json(), outfile)
    end_time = datetime.datetime.now()
    dt = datetime.datetime.now() - start_time
    seconds = dt.total_seconds()
    t = format_time(seconds)
    print('files: %s, %s' % (h5file, json_file))
    print("n_epoch: %d, max_mem: %d, data: %d, time: %s" % (epoch, max_memory, data_size, t))
    return seconds

def build_model(grid,num_actions, lr=0.001):
    model = Sequential()
    model.add(Dense(grid.size, input_shape=(grid.size,)))
    model.add(PReLU())
    model.add(Dense(grid.size))
    model.add(PReLU())
    model.add(Dense(num_actions))
    model.compile(optimizer='adam', loss='mse')
    return model

import random
import numpy as np
import math 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

from weapon import Weapon
from miniature import Miniature
from units import Unit, UnitList
from playground import PlayGround
from game import Game

theGame = Game(40,40)

theGame.create_unit("Space Marine Squad",'sm',(6, 4, 2, 6, 3, 13),(1,1),{'chain saw':Weapon('chain saw','melee',4,0,3,0,4,-1,1),'bolter':Weapon('bolt','range',1,12,0,3,4,0,1)},6,'P1')

theGame.create_unit("Ork Boyz Squad",'ok',(5, 5, 1, 6, 6, 7),(theGame.xsize-5,theGame.ysize-5),{'choppa':Weapon('choppa','melee',3,0,3,0,4,-1,1),'shoota':Weapon('shoota','range',2,18,0,5,4,0,1)},6,'P2')

theGame.syncro_squads_units()

theGame.display_all_attached_units()

theGame.updateTempGrid()

#theGame.moveUnitShortCut('sm')
#theGame.rangeAttack('sm', 'ok', is_simu = False)
print(theGame.grid.occupation)
print(theGame.observe1D())

model = build_model(theGame.grid.occupation,theGame.num_actions)

theGame.observe1D()

qtrain(model, theGame, n_epoch=10, max_memory=8*theGame.observe1D().size, data_size=32)