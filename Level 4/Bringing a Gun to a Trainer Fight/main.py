from math import atan2, ceil, sqrt

class Entity():
    def __init__(self,coord):
        self.x = coord[0]
        self.y = coord[1]
        
    def distance(self,p):
        return sqrt((self.x-p.x)**2 + (self.y-p.y)**2)

    def angle(self,p):
        return atan2(p.y-self.y, p.x-self.x)
    
class Room():
    def __init__(self,dim,player,trainer,dist):
        self.wid = dim[0]
        self.hig = dim[1]
        self.original_player = Entity(player)
        self.original_trainer = Entity(trainer)
        self.max_dist = dist
        self.players = []
        self.trainers = []
    
    def mirror(self): 
        # Replicate the room along x and y axis to analyse linearly bouncings
        # There's no need to replicate the room more than the distance will cover

        # converting to float is needed in python2.7 because otherwise the division gives an int
        x_mult = int(ceil((self.original_player.x + self.max_dist)/float(self.wid)))
        y_mult = int(ceil((self.original_player.y + self.max_dist)/float(self.hig)))

        q1_pl,q1_tr = [],[]

        for i in range(x_mult):

            if i % 2 == 0:
                px = self.wid*i + self.original_player.x
                tx = self.wid*i + self.original_trainer.x
            else:
                px = self.wid*(i+1) - self.original_player.x
                tx = self.wid*(i+1) - self.original_trainer.x

            for j in range(y_mult):
                
                if j % 2 == 0:
                    py = self.hig*j + self.original_player.y
                    ty = self.hig*j + self.original_trainer.y
                else:
                    py = self.hig*(j+1) - self.original_player.y
                    ty = self.hig*(j+1) - self.original_trainer.y

                #add to the list if reachable
                pl,tr = Entity([px,py]), Entity([tx,ty])
                q1_pl.append(pl)
                q1_tr.append(tr)
        
        # Now we replicate the positions for all other quadrants (from 2nd to 4th)
        
        #2nd
        qn_pl,qn_tr = [],[]
        for p in q1_pl:
            pl = Entity([-p.x,p.y])
            qn_pl.append(pl)
        for t in q1_tr:
            tr = Entity([-t.x,t.y])
            qn_tr.append(tr)
        #3rd
        for p in q1_pl:
            pl = Entity([-p.x,-p.y])
            qn_pl.append(pl)
        for t in q1_tr:
            tr = Entity([-t.x,-t.y])
            qn_tr.append(tr)
        #4th
        for p in q1_pl:
            pl = Entity([p.x,-p.y])
            qn_pl.append(pl)
        for t in q1_tr:
            tr = Entity([t.x,-t.y])
            qn_tr.append(tr)

        # we discard the original position of the player from the list  
        del q1_pl[0]

        # filter unreachable dests
        for x in q1_pl+qn_pl:
            if self.original_player.distance(x) <= self.max_dist:
                self.players.append(x)
        for x in q1_tr+qn_tr:
            if self.original_player.distance(x) <= self.max_dist:
                self.trainers.append(x)

    def shoot(self):
        targets = dict()
        # save the target depending on the angle needed
        # if two targets are alligned -> same angle -> the one hitted is the closest

        # save in a dictionary to have O(1) search by key(angle)
        # then we save the distance of the target and its type (P or T)

        # iterate firstly through all player positions
        for p in self.players:
            angle = self.original_player.angle(p)
            dist = self.original_player.distance(p)
            if angle in targets and targets[angle][1] <= dist:
                continue
            targets[angle] = ['P', dist]

        # finally, we iterate through all trainers
        for t in self.trainers:
            angle = self.original_player.angle(t)
            dist = self.original_player.distance(t)
            if angle in targets and targets[angle][1] <= dist:
                continue
            targets[angle] = ['T', dist]

        directions = 0
        for _,x in targets.items():
            if x[0] == 'T':
                directions += 1

        return directions

def solution(dimensions, your_position, trainer_position, distance):
    r = Room(dimensions,your_position,trainer_position,distance)
    r.mirror()
    return r.shoot()


# Test cases
dimensions = [3,2]
trainer_pos = [1,1]
player_pos = [2,1]
distance = 4
print(solution(dimensions, trainer_pos, player_pos, distance)) #7

dimensions = [300,275]
trainer_pos = [150,150]
player_pos = [185,100]
distance = 500
print(solution(dimensions, trainer_pos, player_pos, distance)) #9

dimensions = [2, 5]
trainer_pos = [1, 2]
player_pos = [1, 4]
distance = 11
print(solution(dimensions, trainer_pos, player_pos, distance)) #27

dimensions = [23, 10]
trainer_pos = [6, 4]
player_pos = [3, 2]
distance = 23
print(solution(dimensions, trainer_pos, player_pos, distance)) #8

dimensions = [300, 275]
trainer_pos = [150, 150]
player_pos = [180, 100]
distance = 500
print(solution(dimensions, trainer_pos, player_pos, distance)) #9

dimensions = [1250, 1250]
trainer_pos = [1000, 1000]
player_pos = [500, 400]
distance = 10000
print(solution(dimensions, trainer_pos, player_pos, distance)) #196