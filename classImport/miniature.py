import numpy as np
import math 

class Miniature:
    def __init__(self, name, movement, toughness, wounds, leadership, save, points_cost, position, weapon = {}, inv_save = 0):
        self.name = name
        self.movement = movement
        self.toughness = toughness
        self.wounds = wounds
        self.attacks = 1
        self.leadership = leadership
        self.save = save
        self.points_cost = points_cost
        self.position = position  # position on the battlefield as a tuple (x, y)
        self.weapon = weapon # can be a dict of range and melee
        self.weapon_skill = 1
        self.ballistic_skill = 1
        self.strength = 1
        self.inv_save =  inv_save 
        self.selected_weapon = ''
    
    def move(self, dx, dy, battlefield_size):
        """Move the miniature by dx, dy if the move is within the battlefield."""
        new_position = (self.position[0] + dx, self.position[1] + dy)
        if 0 <= new_position[0] < battlefield_size[0] and 0 <= new_position[1] < battlefield_size[1]:
            self.position = new_position
        else:
            return False  # The miniature has moved off the battlefield and will be removed
        return True
    
    def checkDistance(self,dx,dy):
        distance = round(math.sqrt(dx**2+dy**2),1)
        if  distance > self.movement:
            return False
        else:
            return True
    
    def choose_weapon(self, name):
        # choose a range or a melee weapon
        try:
            self.selected_weapon = name
            self.weapon_skill = self.weapon[name].weapon_skill
            self.weapon_range = self.weapon[name].range
            self.ballistic_skill = self.weapon[name].ballistic_skill
            self.strength = self.weapon[name].strength
            self.attacks = self.weapon[name].attacks
        except Exception:
            self.selected_weapon =  ''
            self.weapon_skill = 3
            self.ballistic_skill = 3
            self.strength = 3
            self.attacks = 1
