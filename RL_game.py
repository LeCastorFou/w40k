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
from classImport.game import Game

theGame = Game(20,20)

theGame.create_unit("Space Marine Squad",'sm',(6, 4, 2, 6, 3, 13),(1,1),{'chain saw':Weapon('chain saw','melee',4,0,3,0,4,-1,1),'bolter':Weapon('bolt','range',1,12,0,3,4,0,1)},6,'P1')

theGame.create_unit("Ork Boyz Squad",'ok',(5, 5, 1, 6, 6, 7),(theGame.xsize-5,theGame.ysize-5),{'choppa':Weapon('choppa','melee',3,0,3,0,4,-1,1),'shoota':Weapon('shoota','range',2,18,0,5,4,0,1)},6,'P2')

theGame.syncro_squads_units()

theGame.display_all_attached_units()

theGame.updateTempGrid()

theGame.initNbMinis()



for i in range(100):
    print('##############')
    print(f'Nb SM INIT : {theGame.nb_mini_init_p1} et Nb ORK INIT : {theGame.nb_mini_init_p2}')
    rd_act_nb = random.randint(0,theGame.num_actions-1)
    if theGame.actions_dict[rd_act_nb] != 'range':
        theGame.moveUnitShortCutAuto('sm',theGame.actions_dict[rd_act_nb],is_simu = True)
    else:
        theGame.rangeAttack('sm','ok',False) # attack a distance sm sur ork

    theGame.updateNbMinis() # update le nombre de fig de chaque joueur apres combat
    theGame.get_reward() # active la récompense de ce tour
    theGame.storeNbMinis() # stocke le nb de fig de chauqe joueur pour le comparer a l evolution au prochain tour 
    print(f'Score total : {theGame.total_reward}')

    print(f'Nb SM : {theGame.nb_mini_p1} et Nb ORK : {theGame.nb_mini_p2}')

    # Si un des joueurs n'a plus de fig la partie est terminée
    if theGame.nb_mini_p1 == 0 or theGame.nb_mini_p2 == 0:
        break

    
theGame.displayGame2D('sm','ok')
