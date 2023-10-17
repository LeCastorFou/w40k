import random
import numpy as np
import math 

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap


from classImport.weapon import Weapon
from classImport.miniature import Miniature
from classImport.units import Unit, UnitList
from classImport.playground import PlayGround

class Game:
    def __init__(self,xsize,ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.grid = PlayGround([xsize,ysize])
        self.allUnitsP1 =  UnitList()
        self.allUnitsP2 =  UnitList()
    
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

    
    
  
