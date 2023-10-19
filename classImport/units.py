import random
import numpy as np
import math 

from miniature import Miniature

class UnitList:
    def __init__(self):
        self.allUnits = []
    
    def findUnit(self,shortname):
        for unit in self.allUnits:
            if unit.shortname == shortname:
                return unit
    
    def dumpUnits(self):
        for unit in self.allUnits:
            print(f'    -{unit.name}')

class Unit:
    def __init__(self, name,shortname, cohesion,allUnitsP1, allUnitsP2):
        self.name = name
        self.shortname = shortname
        self.cohesion = cohesion
        self.miniatures = []
        self.is_destroyed == False
        self.unitList = allUnitsP1
        self.allUnitsP1 = allUnitsP1
        self.allUnitsP2 = allUnitsP2

    def add_miniature(self, name, movement, toughness, wounds, leadership, save, points_cost, position,playground, weapon={}, inv_save = 0):
        new_miniature = Miniature(name, movement, toughness, wounds, leadership, save, points_cost, position, weapon, inv_save)
        playground.add_mini(name,position,new_miniature)
        self.miniatures.append(new_miniature)

    def get_unit_miniatures_names(self):
        print( [e.name for e in self.miniatures])

    def get_unit_miniatures_position(self):
        print( [e.position for e in self.miniatures])

    def get_unit_leadership(self):
        return max([miniature.leadership for miniature in self.miniatures])

    def get_unit_mouvement(self):
        try:
            return max([miniature.movement for miniature in self.miniatures])
        except Exception:
            return 0
        
    def get_unit_points_cost(self):
        return sum([miniature.points_cost for miniature in self.miniatures])

    def get_unit_positions(self):
        return [miniature.position for miniature in self.miniatures]

    def move_unit(self, dx, dy, battlefield_size):
        """Move the unit by dx, dy, but not more than the unit's movement. Remove any miniatures that move off the battlefield."""
        dx, dy = min(dx, self.get_unit_movement()), min(dy, self.get_unit_movement())
        for miniature in self.miniatures[:]:  # Copy the list so we can modify it while iterating
            if not miniature.move(dx, dy, battlefield_size):
                self.miniatures.remove(miniature)
                print(f"{miniature.name} has moved off the battlefield and has been destroyed.")
    
    def move_unit_through_playground(self, dx, dy, playground,player,is_simu):
        """Move the entire unit by dx, dy on the given playground."""
        if self.checkOppoAround(playground,player,is_simu):
            return None
        if self.miniatures[0].checkDistance(dx,dy):# Check if the minis can move such a distance
            for mini in self.miniatures:
                old_pos = mini.position
                mini.move(dx, dy, playground.size)  # Move mini
                new_pos = playground.move_mini(old_pos, mini.position, mini.name)  # Update playground
                mini.position = new_pos  # Update mini's position if it was changed by playground
        # regroup all minis of the same unit
        playground.regroup_unit(self.miniatures[0].name[:2],self.miniatures)
        # check if in contact with other oppo mini
        self.checkOppoAround(playground,player,is_simu)
    
    def checkOppoAround(self, playground,player,is_simu):
        n_in_contact = 0
        for mini in self.miniatures:
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]: # Check all around position
                try:
                    if not playground.is_empty(mini.position[0]+dx,mini.position[1]+dy): # check if not empty
                        if not playground.occupation[mini.position[0]+dx,mini.position[1]+dy].startswith(mini.name[:2]): # check if from another squad
                            if (mini.position[0],mini.position[1]) != (0,0) and (mini.position[0],mini.position[1]) != (1,0) and (mini.position[0],mini.position[1]) != (0,1): # avoid edge side effect
                                oppo_shortname = playground.occupation[mini.position[0]+dx,mini.position[1]+dy][:2]
                                n_in_contact += 1
                except Exception:
                    pass
        if n_in_contact > 0:
            print(f'Unit of {player} in contact with {oppo_shortname}')
            if player == 'P1':
                oppoUnits = self.allUnitsP2
            if player == 'P2':
                oppoUnits = self.allUnitsP1
            oppo = oppoUnits.findUnit(oppo_shortname)
            self.close_combat_attack(oppo, playground,is_simu)
            return True
        else :
            return False
        
    def select_weapons(self,type,is_simu):
        i = 0 # minis counter
        is_applied = False 
        for m in self.miniatures :
            # check if user wants to apply the same weapons to every minis
            if not is_applied:            
                print(f'{m.name} available weapons : ') if not is_simu else None
                all_weapons = []
                for w in m.weapon:
                    if m.weapon[w].type == type:
                        all_weapons = all_weapons +[w]
                print(all_weapons) if not is_simu else None
                if len(all_weapons) == 1 or is_simu:
                    w_choosed = all_weapons[0]
                    m.choose_weapon(w_choosed)
                else:
                    w_choosed = input('Choose weapon : ')
                    m.choose_weapon(w_choosed)
            if i == 0:
                if is_simu:
                    is_applied == True 
                else:
                    is_applied = input('Apply to all unit if available ? (y/n) ')
                    is_applied = True if is_applied == 'y' else False
                if is_applied:
                    default_weapon  =  w_choosed
            else:
                all_weapons = []
                for w in m.weapon:
                    all_weapons = all_weapons + [w]
                if is_applied and default_weapon in all_weapons:
                        print(f'{m.name} default weapon : {default_weapon}') if not is_simu else None
                        m.choose_weapon(w_choosed)
                else:
                    print(f'{m.name} available weapons : ') if not is_simu else None
                    all_weapons = []
                    for w in m.weapon:
                        if m.weapon[w].type == type:
                            all_weapons = all_weapons + [w]
                    print(all_weapons) if not is_simu else None
                    if len(all_weapons) == 1 or is_simu:
                        w_choosed = all_weapons[0]
                        m.choose_weapon(w_choosed)
                    else:
                        w_choosed = input('Choose weapon : ')
                        m.choose_weapon(w_choosed)
            i += 1

    def is_destroyed(self):
        """Return True if the unit is destroyed, False otherwise."""
        if len(self.miniatures) == 0:
            self.is_destroyed == True
            return True
        return False
    
    def remove_random_miniature(self):
        """Remove a random miniature from the unit."""
        if self.miniatures:
            index_to_remove = random.randint(0, len(self.miniatures) - 1)
            self.miniatures.pop(index_to_remove)
            
    def close_combat_attack(self, target_unit,playground,is_simu):
        """Attack another unit in close combat."""
        n_in_contact = 0
        for our_miniature in self.miniatures:
            # Step 1: Check if in range
            for their_miniature in target_unit.miniatures:
                if abs(our_miniature.position[0] - their_miniature.position[0]) <= 1 and abs(our_miniature.position[1] - their_miniature.position[1]) <= 1:
                    n_in_contact += 1  # We found a target miniature in range
        if n_in_contact ==  0:
            return None
        
        print(f"{self.name} is attaking {target_unit.name} ################") if not is_simu else None
        self.select_weapons('melee',is_simu)
        for our_miniature in self.miniatures:
            # Step 1: Check if in range
            for their_miniature in target_unit.miniatures:
                if abs(our_miniature.position[0] - their_miniature.position[0]) <= 1 and abs(our_miniature.position[1] - their_miniature.position[1]) <= 1:
                    break  # We found a target miniature in range
            else:
                continue  # No miniature in range, try the next one in our unit

            # Step 2: Roll to hit
            hits = 0
            for _ in range(our_miniature.attacks):
                if random.randint(1, 6) >= our_miniature.weapon_skill:
                    hits += 1

            # Step 3: Roll to wound
            wounds = 0
            for _ in range(hits):
                dice_roll = random.randint(1, 6)
                if our_miniature.strength >= 2*their_miniature.toughness:
                    if dice_roll >= 2:  
                        wounds += 1
                elif our_miniature.strength > their_miniature.toughness:
                    if dice_roll >= 3:  
                        wounds += 1
                elif our_miniature.strength == their_miniature.toughness:
                    if dice_roll >= 4:  
                        wounds += 1
                elif our_miniature.strength*2  <= their_miniature.toughness:
                    if dice_roll >= 6 : 
                        wounds += 1
                elif our_miniature.strength  < their_miniature.toughness:
                    if dice_roll >= 5 :  
                        wounds += 1
                
            
            print(f"{our_miniature.name} deals {wounds} wounds!") if not is_simu else None

            if wounds > 0:
                # allocated wounds
                all_minis = []
                n_tm  = 0
                for their_miniature in target_unit.miniatures:
                    all_minis = all_minis +[f" {n_tm} : {their_miniature.name}"]
                    n_tm += 1
                print(all_minis) if not is_simu else None
                if is_simu:
                    selected_mini = 0
                else:
                    selected_mini = input('Select target: ')
                is_one_selected = False

                for their_miniature in target_unit.miniatures:
                    if their_miniature.name == selected_mini:
                        is_one_selected = True
                        target_mini = their_miniature
                if not is_one_selected:
                    target_mini =  target_unit.miniatures[0]

                # Step 4: Saving throws
                unsaved_wounds = 0
                for _ in range(wounds):
                    if random.randint(1, 6) < target_mini.save - our_miniature.weapon[our_miniature.selected_weapon].armour_penetration:
                        if target_mini.inv_save != 0:
                            if random.randint(1, 6) < target_mini.inv_save :
                                unsaved_wounds += 1
                            else:
                                print(f"{target_mini.name} saved the wound!") if not is_simu else None
                        else:
                            unsaved_wounds += 1
                    else:
                        print(f"{target_mini.name} saved the wound!") if not is_simu else None

                        

                # Step 5: Inflict damage
                print(f"{our_miniature.name} deals {unsaved_wounds} damage!") if not is_simu else None
                for _ in range(unsaved_wounds):
                    target_mini.wounds = target_mini.wounds - our_miniature.weapon[our_miniature.selected_weapon].damage
                    if target_mini.wounds <= 0:
                        print(f"{target_mini.name} is destroyed") if not is_simu else None
                        playground.occupation[target_mini.position[0],target_mini.position[1]] = '   '
                        pos_mini = 0
                        for their_miniature in target_unit.miniatures:
                            pos_mini += 1
                            if target_mini.name == their_miniature.name:  
                                target_unit.miniatures.pop(pos_mini-1) 
                                break
                        break

                # Check if target unit is destroyed
                if target_unit.is_destroyed():
                    print(f"{target_unit.name} has been destroyed!") if not is_simu else None
                
        print('remaining opponent minis') if not is_simu else None
        for their_miniature in target_unit.miniatures:
            print(f"{their_miniature.name} pv :{ their_miniature.wounds}" ) if not is_simu else None

    def distant_combat_attack(self, target_unit,playground,is_simu):
        """Attack another unit in close combat."""
        print(f"####### {self.name} is firing at {target_unit.name} #########") if not is_simu else None
        self.select_weapons('range',is_simu)
        
        for our_miniature in self.miniatures:
            # Step 1: Check if in range
            for their_miniature in target_unit.miniatures:
                dist = math.sqrt(abs(our_miniature.position[0] - their_miniature.position[0])**2 + abs(our_miniature.position[1] - their_miniature.position[1])**2)
                if  dist <= our_miniature.weapon_range  :
                    break  # We found a target miniature in range
            else:
                print(f"{their_miniature.name[:2]} not in range for {our_miniature.name}, distance = {dist} and range = {our_miniature.weapon_range}", )
                continue  # No miniature in range, try the next one in our unit

            # Step 2: Roll to hit
            hits = 0
            for _ in range(our_miniature.attacks):
                if random.randint(1, 6) >= our_miniature.ballistic_skill:
                    hits += 1

            # Step 3: Roll to wound
            wounds = 0
            for _ in range(hits):
                dice_roll = random.randint(1, 6)
                if our_miniature.strength >= 2*their_miniature.toughness:
                    if dice_roll >= 2:  
                        wounds += 1
                elif our_miniature.strength > their_miniature.toughness:
                    if dice_roll >= 3:  
                        wounds += 1
                elif our_miniature.strength == their_miniature.toughness:
                    if dice_roll >= 4:  
                        wounds += 1
                elif our_miniature.strength*2  <= their_miniature.toughness:
                    if dice_roll >= 6 : 
                        wounds += 1
                elif our_miniature.strength  < their_miniature.toughness:
                    if dice_roll >= 5 :  
                        wounds += 1
                
            
            print(f"{our_miniature.name} deals {wounds} wounds!") if not is_simu else None

            if wounds > 0:
                # allocated wounds
                all_minis = []
                n_tm  = 0
                for their_miniature in target_unit.miniatures:
                    all_minis = all_minis +[f" {n_tm} : {their_miniature.name}"]
                    n_tm += 1
                print(all_minis) if not is_simu else None
                if is_simu:
                    selected_mini = 0
                else:
                    selected_mini = input('Select target: ')
                is_one_selected = False

                for their_miniature in target_unit.miniatures:
                    if their_miniature.name == selected_mini:
                        is_one_selected = True
                        target_mini = their_miniature
                if not is_one_selected:
                    target_mini =  target_unit.miniatures[0]

                # Step 4: Saving throws
                unsaved_wounds = 0
                for _ in range(wounds):
                    if random.randint(1, 6) < target_mini.save - our_miniature.weapon[our_miniature.selected_weapon].armour_penetration:
                        if target_mini.inv_save != 0:
                            if random.randint(1, 6) < target_mini.inv_save :
                                unsaved_wounds += 1
                            else:
                                print(f"{target_mini.name} saved the wound!") if not is_simu else None
                        else:
                            print(f"{target_mini.name} saved FAILED!") if not is_simu else None
                            unsaved_wounds += 1
                    else:
                        print(f"{target_mini.name} saved the wound!") if not is_simu else None

                        

                # Step 5: Inflict damage
                print(f"{our_miniature.name} deals {unsaved_wounds} damage!") if not is_simu else None
                for _ in range(unsaved_wounds):
                    target_mini.wounds = target_mini.wounds - our_miniature.weapon[our_miniature.selected_weapon].damage
                    if target_mini.wounds <= 0:
                        print(f"{target_mini.name} is destroyed") if not is_simu else None
                        playground.occupation[target_mini.position[0],target_mini.position[1]] = '   '
                        pos_mini = 0
                        for their_miniature in target_unit.miniatures:
                            pos_mini += 1
                            if target_mini.name == their_miniature.name:  
                                target_unit.miniatures.pop(pos_mini-1) 
                                break
                        break

                # Check if target unit is destroyed
                if target_unit.is_destroyed():
                    print(f"{target_unit.name} has been destroyed!") if not is_simu else None
                
        print('remaining opponent minis') if not is_simu else None
        for their_miniature in target_unit.miniatures:
            print(f"{their_miniature.name} pv :{ their_miniature.wounds}" ) if not is_simu else None
