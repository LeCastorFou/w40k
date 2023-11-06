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

class Game:
    def __init__(self,xsize,ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.grid = PlayGround([xsize,ysize])
        self.allUnitsP1 =  UnitList()
        self.allUnitsP2 =  UnitList()
        self.total_reward = 0
        self.current_reward = 0
        self.nb_mini_init_p1 = 0
        self.nb_mini_init_p2 = 0
        self.nb_mini_p1 = 0
        self.nb_mini_p2 = 0
        self.actions_dict = {
                0: 'N',
                1: 'NW',
                2: 'W',
                3: 'SW',
                4: 'S',
                5: 'SE',
                6: 'E',
                7: 'NE',
                8: 'range',
            }
        self.num_actions = len(self.actions_dict)
        self.status = 'playing'

        # Exploration factor
        self.epsilon = 0.1
    
    def create_unit(self,unit_name, unit_short_name, fig_attribute, main_fig_pos, weapons, n_fig,player):
        squad = Unit(unit_name,unit_short_name, 2, self.allUnitsP1,self.allUnitsP2)
        if player == 'P1':
            self.allUnitsP1.allUnits.append(squad)
        else:
            self.allUnitsP2.allUnits.append(squad) 
        mouv,thou,wounds,lead,save,point = fig_attribute
        for i in range(n_fig):
            squad.add_miniature( f"{squad.shortname}{i+1}", mouv, thou, wounds, lead, save, point, main_fig_pos, self.grid, weapons)
    
    def list_P1_units(self):
        print(" ## ALL P1 UNITS :")
        for unit in self.allUnitsP1.allUnits:
            print(unit.name)
        print("###########")

    def list_P2_units(self):
        print(" ## ALL P2 UNITS :")
        for unit in self.allUnitsP2.allUnits:
            print(unit.name)
        print("###########")
    
    def get_nb_P1_mini(self):
        nb = 0
        for unit in self.allUnitsP1.allUnits:
            for mini in unit.miniatures:
                nb += 1
        return nb

    def get_nb_P2_mini(self):
        nb = 0
        for unit in self.allUnitsP2.allUnits:
            for mini in unit.miniatures:
                nb += 1
        return nb
       
    def observe1D(self):
        array = self.grid.occupation
        prefix_mapping = {}
        current_number = 1
        
        # Create a mapping of prefixes to numbers
        for row in array:
            for item in row:
                if item.strip():  # Check if the string is not empty and not just spaces
                    prefix = item[:2]  # Get the first two letters
                    if prefix not in prefix_mapping:
                        prefix_mapping[prefix] = current_number
                        current_number += 1
        
        # Replace the prefixes in the array
        new_array = np.zeros_like(array, dtype=int)
        for i, row in enumerate(array):
            for j, item in enumerate(row):
                if item.strip():
                    prefix = item[:2]
                    new_array[i, j] = prefix_mapping[prefix]

        return new_array.reshape((1, -1))

    def syncro_squads_units(self):
        # Make all unit aware of the other units
        for unit in self.allUnitsP1.allUnits:
            unit.allUnitsP1 = self.allUnitsP1
            unit.allUnitsP2 = self.allUnitsP2
        
        for unit in self.allUnitsP2.allUnits:
            unit.allUnitsP1 = self.allUnitsP1
            unit.allUnitsP2 = self.allUnitsP2
    
    def display_all_attached_units(self):
        print("## P1 units :")
        for unit in self.allUnitsP1.allUnits:
            print(f"-{unit.name}")
            print(" -> as acces to these units:")
            unit.allUnitsP1.dumpUnits()
            unit.allUnitsP2.dumpUnits()
            print("####")
        print("## P2 units :")
        for unit in self.allUnitsP2.allUnits:
            print(f"-{unit.name}")
            print(" -> as acces to these units:")
            unit.allUnitsP1.dumpUnits()
            unit.allUnitsP2.dumpUnits()
            print("####")

    def updateTempGrid(self):
        self.grid.temporalGrid = np.append(self.grid.temporalGrid, np.array([self.grid.occupation]),axis=0)
    
    def unitSelection(self,unit_short_name):
        selected_unit = self.allUnitsP1.allUnits[0]
        player = 'P1'
        for e in self.allUnitsP1.allUnits:
            if unit_short_name == e.shortname:
                selected_unit = e
                player = 'P1'
    
        for e in self.allUnitsP2.allUnits:
            if unit_short_name == e.shortname:
                selected_unit = e
                player = 'P2'
       
        return selected_unit, player
    
    def moveUnit(self,unit_short_name,xmove_squad,ymove_squad,is_simu = False):
        print( 'moving by : x = ', xmove_squad,' / y = ',ymove_squad) if not is_simu else None
        
        selected_unit, player = self.unitSelection(unit_short_name)
  
        selected_unit.move_unit_through_playground(xmove_squad,ymove_squad,self.grid,player,is_simu=is_simu)
        self.updateTempGrid()
    
    def moveUnitShortCut(self,unit_short_name,is_simu = False):
        direction = input('Mouvement direction ? N, NW, W, SW, S, SE, E, NE -> ')
        if direction == 'N':
            self.moveUnit(unit_short_name,-6,0,is_simu )
        elif direction == 'NW':
            self.moveUnit(unit_short_name,-4,4,is_simu)
        elif direction == 'W':
            self.moveUnit(unit_short_name,0,6,is_simu )
        elif direction == 'SW':
            self.moveUnit(unit_short_name,4,4,is_simu )
        elif direction == 'S':
            self.moveUnit(unit_short_name,6,0,is_simu)
        elif direction == 'SE':
            self.moveUnit(unit_short_name,4,-4,is_simu)
        elif direction == 'E':
            self.moveUnit(unit_short_name,0,-6,is_simu)
        elif direction == 'NE':
            self.moveUnit(unit_short_name,-4,-4,is_simu)
        print( 'moving in direction : x = ', direction,) if not is_simu else None
    
    def moveUnitShortCutAuto(self,unit_short_name,direction,is_simu = True):
        if direction == 'N':
            self.moveUnit(unit_short_name,-6,0,is_simu )
        elif direction == 'NW':
            self.moveUnit(unit_short_name,-4,4,is_simu)
        elif direction == 'W':
            self.moveUnit(unit_short_name,0,6,is_simu )
        elif direction == 'SW':
            self.moveUnit(unit_short_name,4,4,is_simu )
        elif direction == 'S':
            self.moveUnit(unit_short_name,6,0,is_simu)
        elif direction == 'SE':
            self.moveUnit(unit_short_name,4,-4,is_simu)
        elif direction == 'E':
            self.moveUnit(unit_short_name,0,-6,is_simu)
        elif direction == 'NE':
            self.moveUnit(unit_short_name,-4,-4,is_simu)
    
    def rangeAttack(self, unit_short_name, target_unit, is_simu = False):
        selected_unit, player = self.unitSelection(unit_short_name)
        target_unit, player = self.unitSelection(target_unit)
        selected_unit.distant_combat_attack(target_unit,self.grid,is_simu)
        self.updateTempGrid()
        
    def launchSimu2Units(self,steps,is_simu):
        # Take fist unit of each player and run random mouvement 
        for i in range(steps):
            if len(self.allUnitsP1.allUnits[0].miniatures) == 0 or len(self.allUnitsP2.allUnits[0].miniatures) == 0:
                break
            print("################ squad move #################""") if not is_simu else None
            xmove_squad = random.randint(-self.allUnitsP1.allUnits[0].get_unit_mouvement(), self.allUnitsP1.allUnits[0].get_unit_mouvement())
            ymove_squad =(-1)**random.randint(1, 2)*(math.floor( math.sqrt(self.allUnitsP1.allUnits[0].get_unit_mouvement()**2 - xmove_squad**2)))
            print(xmove_squad,ymove_squad) if not is_simu else None
            self.allUnitsP1.allUnits[0].move_unit_through_playground(xmove_squad,ymove_squad,self.grid,'P1',is_simu=is_simu)
            if len(self.allUnitsP1.allUnits[0].miniatures) == 0 or len(self.allUnitsP2.allUnits[0].miniatures) == 0:
                break
            print("################ oppo move #################""") if not is_simu else None
            xmove_oppo = random.randint(-self.allUnitsP2.allUnits[0].get_unit_mouvement(), self.allUnitsP2.allUnits[0].get_unit_mouvement())
            ymove_oppo = (-1)**random.randint(1, 2)*(math.floor( math.sqrt(self.allUnitsP2.allUnits[0].get_unit_mouvement()**2 - xmove_oppo**2)))
            print(xmove_oppo,ymove_oppo)if not is_simu else None
            self.allUnitsP2.allUnits[0].move_unit_through_playground(xmove_oppo,ymove_oppo,self.grid,'P2',is_simu=is_simu)
            
            self.updateTempGrid()
    
    def displayGame2D(self,short_name_unit_p1,short_name_unit_p2):
        data = np.array(self.grid.temporalGrid)
        
        self.p1unitcolor = 'blue'
        self.p2unitcolor = 'red'
        self.backgroundcolor = 'white'
        ### Animation
        def map_colors(arr):
            def get_color(value):
                if value.startswith(short_name_unit_p1):
                    return 0
                elif value.startswith(short_name_unit_p2):
                    return 1
                else:
                    return 2
            vfunc = np.vectorize(get_color)
            return vfunc(arr)
        # Step 4: Create an animation
        fig, ax = plt.subplots()


        # Creating a custom color map

        cmap = ListedColormap([self.p1unitcolor, self.p2unitcolor, self.backgroundcolor])

        def update(num, data):
            ax.clear()
            colored_data = map_colors(data[num, :, :])
            ax.imshow(colored_data, aspect='auto', cmap=cmap)
            ax.set_title(f'Time step: {num}')

        ani = animation.FuncAnimation(fig, update, frames=range(data.shape[0]), fargs=(data,), interval=1000)
        plt.show()
    
    def initNbMinis(self):
        self.nb_mini_init_p1 = self.get_nb_P1_mini()
        self.nb_mini_init_p2 = self.get_nb_P2_mini()
        self.nb_mini_p1 = self.nb_mini_init_p1
        self.nb_mini_p2 = self.nb_mini_init_p2

    def updateNbMinis(self):
        # update le nombre de mini a chaque phase pour avoir le dernier nombre
        self.nb_mini_p1 = self.get_nb_P1_mini()
        self.nb_mini_p2 = self.get_nb_P2_mini()

    def storeNbMinis(self):
        self.nb_mini_init_p1 = self.nb_mini_p1
        self.nb_mini_init_p2 = self.nb_mini_p2

    def get_reward(self):
        if self.nb_mini_p1 == self.nb_mini_init_p1:
            self.current_reward = 0.04
            self.total_reward += self.current_reward
            print('No loss')
        
        if self.nb_mini_p2  == self.nb_mini_init_p2:
            self.current_reward = -0.06
            self.total_reward -= self.current_reward
            print('No loss for the oppo')
        
        if self.nb_mini_p2  < self.nb_mini_init_p2:
            self.current_reward = 0.06
            self.total_reward += self.current_reward
            print('Loss for the opp')
        
        if self.nb_mini_p2  == 0:
            self.current_reward = 1
            self.total_reward += self.current_reward
            self.status = 'win'
            print('oppo annilated')
        
        if self.nb_mini_p1  == 0:
            self.current_reward = -1
            self.total_reward += self.current_reward
            self.status = 'lose'
            print('player annilated')
    
    def getGameState(self):
        return self.observe1D(), self.current_reward, self.status


    
    
  
