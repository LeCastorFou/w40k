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

theGame.create_unit("Ork Boyz Squad",'ok',(5, 5, 1, 6, 6, 7),(theGame.xsize-1,theGame.ysize-1),{'choppa':Weapon('choppa','melee',3,0,3,0,4,-1,1),'shoota':Weapon('shoota','range',2,18,0,5,4,0,1)},6,'P2')

theGame.syncro_squads_units()

theGame.display_all_attached_units()

theGame.updateTempGrid()

theGame.launchSimu2Units(100,True)

theGame.displayGame2D('sm','ok')