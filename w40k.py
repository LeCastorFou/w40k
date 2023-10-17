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

x_size = 10
y_size = 10
grid = PlayGround([x_size,y_size])
allUnitsP1 =  UnitList()
allUnitsP2 =  UnitList()

# FIG
# name, movement, toughness, wounds, leadership, save, points_cost, position,
# WEAPON
# name, type, attacks, range, weapon_skill, ballistic_skill, strength, armour_penetration, damage

squad = Unit("Space Marine Squad",'sm', 2,allUnitsP1,allUnitsP2)
allUnitsP1.allUnits.append(squad)
for i in range(6):
    squad.add_miniature(f"{squad.shortname}{i+1}", 6, 4, 2, 6, 3, 13, (1, 1),grid, {'chain saw':Weapon('chain saw','melee',4,0,3,0,4,-1,1),'bolter':Weapon('bolt','range',1,12,0,3,4,0,1)})


oppo = Unit("Ork Boyz Squad",'ok', 2,allUnitsP1,allUnitsP2)
allUnitsP2.allUnits.append(oppo)
for i in range(6):
    oppo.add_miniature(f"{oppo.shortname}{i+1}", 5, 5, 1, 6, 6, 7, (x_size-1, y_size-1),grid,{'choppa':Weapon('choppa','melee',3,0,3,0,4,-1,1),'shoota':Weapon('shoota','range',2,18,0,5,4,0,1)})  # Positioned within 1" of the Space Marines
'''
oppo = Unit("Magnus",'ok', 2,allUnitsP1,allUnitsP2)
allUnitsP2.allUnits.append(oppo)
oppo.add_miniature(f"ok1", 14, 11, 16, 5, 2, 300, (x_size-1, y_size-1),grid,{'blade':Weapon('blade','melee',14,0,2,0,8,-1,1)}, inv_save = 4)  # Positioned within 1" of the Space Marines
'''
# Make all unit aware of the other units
squad.allUnitsP1 = allUnitsP1
squad.allUnitsP2 = allUnitsP2
oppo.allUnitsP1 = allUnitsP1
oppo.allUnitsP2 = allUnitsP2


#print(grid.occupation)
#print('##################')
#squad.distant_combat_attack(oppo,grid,False)
#oppo.distant_combat_attack(squad,grid,False)
grid.temporalGrid = np.append(grid.temporalGrid, np.array([grid.occupation]),axis=0)

is_simu = True
for i in range(100):
    if len(squad.miniatures) == 0 or len(oppo.miniatures) == 0:
        break
    print("################ squad move #################""") if not is_simu else None
    xmove_squad = random.randint(-squad.get_unit_mouvement(), squad.get_unit_mouvement())
    ymove_squad =(-1)**random.randint(1, 2)*(math.floor( math.sqrt(squad.get_unit_mouvement()**2 - xmove_squad**2)))
    print(xmove_squad,ymove_squad) if not is_simu else None
    squad.move_unit_through_playground(xmove_squad,ymove_squad,grid,'P1',is_simu=is_simu)
    if len(squad.miniatures) == 0 or len(oppo.miniatures) == 0:
        break
    print("################ oppo move #################""") if not is_simu else None
    xmove_oppo = random.randint(-oppo.get_unit_mouvement(), oppo.get_unit_mouvement())
    ymove_oppo = (-1)**random.randint(1, 2)*(math.floor( math.sqrt(oppo.get_unit_mouvement()**2 - xmove_oppo**2)))
    print(xmove_oppo,ymove_oppo)if not is_simu else None
    oppo.move_unit_through_playground(xmove_oppo,ymove_oppo,grid,'P2',is_simu=is_simu)
    
    grid.temporalGrid = np.append(grid.temporalGrid, np.array([grid.occupation]),axis=0)


print('##################')
data = np.array(grid.temporalGrid)
#print(data)
#print(data.shape)
### Animation
def map_colors(arr):
    def get_color(value):
        if value.startswith('sm'):
            return 0
        elif value.startswith('ok'):
            return 1
        else:
            return 2
    vfunc = np.vectorize(get_color)
    return vfunc(arr)
# Step 4: Create an animation
fig, ax = plt.subplots()


# Creating a custom color map

cmap = ListedColormap(['blue', 'red', 'white'])

def update(num, data):
    ax.clear()
    colored_data = map_colors(data[num, :, :])
    ax.imshow(colored_data, aspect='auto', cmap=cmap)
    ax.set_title(f'Time step: {num}')

ani = animation.FuncAnimation(fig, update, frames=range(data.shape[0]), fargs=(data,), interval=1000)
plt.show()

"""
orks_wins = 0
sm_wins = 0
draws = 0
n_simu = 1000
sm_start = True

for _ in range(n_simu):
    squad = Unit("Space Marine Squad", 2)
    for i in range(6):
        squad.add_miniature(f"Space Marine {i+1} ", 6, 4, 2, 3, 6, 13, (5, 10), {'cs':Weapon('cs','melee',4,0,3,0,4,-1,1),'bolter':Weapon('bolt','range',1,12,0,3,4,0,1)})

    #space_marine_squad.add_miniature(f"Space Marine Leader ", 6, 4, 1, 7, 3, 13, (5, 10), {'mega blades':Weapon('blades','melee',3,0,4,0,5,0,1),'megabolter':Weapon('bolter','range',1,12,0,4,5,0,1)})
    
    oppo = Unit("Ork Boyz Squad", 2)
    for i in range(6):
        oppo.add_miniature(f"Ork Boy {i+1}", 6, 5, 2, 6, 5, 7, (6, 11),{'choppa':Weapon('choppa','melee',3,0,3,0,4,-1,1),'shoota':Weapon('shoota','range',2,18,0,5,4,0,1)})  # Positioned within 1" of the Space Marines
    '''
    oppo = Unit("Magnus", 2)
    oppo.add_miniature(f"Magnus", 14, 11, 16, 5, 2, 300, (6, 11),{'blade':Weapon('blade','melee',14,0,2,0,8,-1,1)}, inv_save = 4)  # Positioned within 1" of the Space Marines
    '''

    # Set up battlefield
    battlefield_size = (44, 60)
    if n_simu == 1:
        if sm_start:
            squad.close_combat_attack(oppo,grid,False)
            oppo.close_combat_attack(squad,grid,False)
        else:
            oppo.close_combat_attack(squad,grid,False)
            squad.close_combat_attack(oppo,grid,False)
    else:
        if sm_start:
            squad.close_combat_attack(oppo,grid,True)
            oppo.close_combat_attack(squad,grid,True)
        else:
            oppo.close_combat_attack(squad,grid,True)
            squad.close_combat_attack(oppo,grid,True)
    
    sm_pv = 0
    for mini in squad.miniatures:
        sm_pv = sm_pv + mini.wounds 
    
    orks_pv = 0
    for mini in oppo.miniatures:
        orks_pv = orks_pv + mini.wounds 
    print(f"pv {squad.name} : {sm_pv}, pv {oppo.name} : {orks_pv}")
    if sm_pv < orks_pv :
        orks_wins +=1
    elif sm_pv  == orks_pv :
        draws += 1
    else:
        sm_wins += 1

print( "############ RESULTS ############")
print(f"{squad.name} = {(sm_wins/n_simu)*100} %")
print(f"{oppo.name} = {(orks_wins/n_simu)*100} %")
print(f"DRAWS = {(draws/n_simu)*100} %")
print( "#################################")
"""