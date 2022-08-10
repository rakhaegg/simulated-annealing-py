import math
from mimetypes import init
from queue import Queue
import random
import sys
import copy


class Node:
    def __init__(self , data=None , location=None):
        self.data = data
        self.location = location
        self.utara = None
        self.selatan = None
        self.barat = None
        self.timur = None
        self.barat_laut = None
        self.timur_laut = None
        self.barat_daya = None
        self.tenggara = None

class ChessBoard:
    def __init__(self , panjang , lebar , initialState):
        self.panjang = panjang
        self.lebar = lebar
        self.data = {}
        self.utama = initialState.copy()
        self.initialState = initialState
        self.alreadyExplored = []
        self.alreadyExplored.append(initialState)
        for x in range(self.lebar):
            for y in range(self.panjang):
                if (str(x) + str(y)) in self.initialState:
                    self.data[str(x) + str(y)] = Node(data='Q'+ str(y+1), location=(x , y))
                else:
                    self.data[str(x) + str(y)] = Node(data=None, location=(x , y))
        for x in self.data.keys():
            x_int = int(x[0])
            y_int = int(x[1]) 
            if x_int == 0  and y_int == 0:
                self.data[x].selatan = self.data['10']
                self.data[x].timur = self.data['01']
                self.data[x].tenggara = self.data['11']
            if x_int == 0 and y_int != 0 and y_int != (self.panjang-1):
                self.data[x].barat = self.data[str(x_int)+str(y_int-1)]
                self.data[x].timur = self.data[str(x_int)+str(y_int+1)]
                self.data[x].tenggara = self.data[str(x_int+1)+str(y_int+1)]
                self.data[x].barat_daya = self.data[str(x_int+1)+str(y_int-1)]
                self.data[x].selatan = self.data[str(x_int+1) + str(y_int)]
            if x_int == 0 and y_int == (self.panjang-1):
                self.data[x].barat= self.data[str(x_int)+str(y_int-1)]
                self.data[x].selatan= self.data[str(x_int+1)+str(y_int)]
                self.data[x].barat_daya = self.data[str(x_int+1)+str(y_int-1)]
            if x_int != 0 and x_int != (self.lebar-1) and y_int == 0:
                self.data[x].utara= self.data[str(x_int-1)+str(y_int)]
                self.data[x].timur_laut = self.data[str(x_int-1)+str(y_int+1)]
                self.data[x].timur = self.data[str(x_int)+str(y_int+1)]
                self.data[x].tenggara = self.data[str(x_int+1) + str(y_int+1)]
                self.data[x].selatan = self.data[str(x_int+1) + str(y_int) ]
            if x_int != 0 and x_int != (self.lebar-1) and y_int != 0 and y_int != (self.panjang-1):
                self.data[x].utara = self.data[str(x_int-1) + str(y_int) ]
                self.data[x].timur_laut = self.data[str(x_int-1) + str(y_int+1)]
                self.data[x].timur = self.data[str(x_int) + str(y_int+1)]
                self.data[x].tenggara = self.data[str(x_int+1) + str(y_int+1)]
                self.data[x].selatan = self.data[str(x_int+1)+ str(y_int)]
                self.data[x].barat_daya = self.data[str(x_int+1) + str(y_int-1)]
                self.data[x].barat = self.data[str(x_int) + str(y_int -1 ) ]
                self.data[x].barat_laut = self.data[str(x_int-1) + str(y_int-1)]
            if x_int != 0 and x_int != (self.lebar-1) and y_int == (self.panjang-1):
                self.data[x].utara = self.data[str(x_int-1) + str(y_int)]
                self.data[x].barat_laut = self.data[str(x_int - 1) + str(y_int-1) ]
                self.data[x].barat =  self.data[str(x_int) + str(y_int-1)]
                self.data[x].barat_daya = self.data[str(x_int+1) + str(x_int-1)]
                self.data[x].selatan = self.data[str(x_int+1) + str(y_int)]
            if x_int == (self.lebar-1) and y_int == 0:
                self.data[x].utara = self.data[str(x_int-1) + str(y_int)]
                self.data[x].timur_laut = self.data[str(x_int-1) + str(y_int+1)]
                self.data[x].timur  = self.data[str(x_int) + str(y_int+1)]
            if x_int == (self.lebar -1 ) and y_int != 0 and y_int != (self.panjang-1):
                self.data[x].utara = self.data[str(x_int-1) + str(y_int )]
                self.data[x].timur_laut = self.data[str(x_int-1) + str(y_int+1)]
                self.data[x].timur = self.data[str(x_int) + str(y_int+1)]
                self.data[x].barat = self.data[str(x_int) + str(y_int-1)]
                self.data[x].barat_laut = self.data[str(x_int-1) + str(y_int-1)]
            if x_int == (self.lebar - 1) and y_int == (self.panjang -1):
                self.data[x].utara = self.data[str(x_int -1) + str(y_int)]
                self.data[x].barat_laut = self.data[str(x_int - 1) + str(y_int -1)]
                self.data[x].barat  = self.data[str(x_int) + str(y_int-1)]

    def checkKey(self , key , first , second , h):
        tmp = str(first) + str(second)
        if tmp not in key:
            key.append(tmp)
    
    def updateInitalState(self):
        
        while True:
            whichRow = str(random.randint(0,self.panjang-1))
            whichColumn = str(random.randint(0,self.panjang-1))
            temp = whichRow + whichColumn
            whereColumn = int(whichColumn)

            before = self.initialState.copy()
            sementara = self.initialState[whereColumn]
            self.initialState[whereColumn] = temp
            if self.initialState == before:
                # print("Sama")
                # print("Update : ", self.initialState)
                # print("Before : " , before)
                # print()
                self.initialState[whereColumn] = sementara
            else:
                
                self.data[sementara].data = None
                self.data[temp].data = 'Q' + str(whereColumn+1)
                # print("Tidak Sama")
                # print("Update : " , self.initialState)
                # print("Before : " , before)
                # print()
                break
        
    def estimateCost(self):
        key = []
        h = 0
        
        for x in self.initialState:
            parent = self.data[x]
            
            current_timur_laut = parent.timur_laut

            while current_timur_laut :
                
                if current_timur_laut.data != None:
                   
                    first = int(parent.data[1])
                    second = int(current_timur_laut.data[1])
                    if first < second:
                        self.checkKey(key , first , second , h)
                    else:
                        self.checkKey(key , second , first , h)     

                current_timur_laut = current_timur_laut.timur_laut
            current_timur = parent.timur
            while current_timur:
                if current_timur.data != None:
                   
                    first = int(parent.data[1])
                    second = int(current_timur.data[1])
                    if first < second:
                        self.checkKey(key , first , second , h)
                    else:
                        self.checkKey(key , second , first , h)    
                current_timur = current_timur.timur
                
            current_tenggara = parent.tenggara
            while current_tenggara:
                if current_tenggara.data != None:
                    
                    first = int(parent.data[1])
                    second = int(current_tenggara.data[1])
                    if first < second:
                        self.checkKey(key , first , second , h)
                    else:
                        self.checkKey(key , second , first , h)
                current_tenggara = current_tenggara.tenggara             
            current_barat = parent.barat
            while current_barat:
                if current_barat.data != None:
                    
                    first = int(parent.data[1])
                    second = int(current_barat.data[1])
                    if first < second:
                        self.checkKey(key , first , second , h)
                    else:
                        self.checkKey(key , second , first , h)
                current_barat = current_barat.barat
            
            current_barat_laut = parent.barat_laut
            while current_barat_laut:
                if current_barat_laut.data != None:
                    
                    first = int(parent.data[1])
                    second = int(current_barat_laut.data[1])
                    if first < second:
                        self.checkKey(key , first , second,h)
                    else:
                        self.checkKey(key , second , first , h)
                current_barat_laut = current_barat_laut.barat_laut            
                        
            current_barat_daya = parent.barat_daya
            while current_barat_daya:
                if current_barat_daya.data != None:
                    
                    first = int(parent.data[1])
                    second = int(current_barat_daya.data[1])
                    if first < second:
                        self.checkKey(key , first , second , h)
                    else:
                        self.checkKey(key , second , first , h)
                current_barat_daya = current_barat_daya.barat_daya
        return len(key) , key
            

class Data:
    def __init__(self , heuristic , pair,state):
        self.heuristic = heuristic
        self.pair  = pair
        self.state = state


def do_simulated_annealing():
    initial_state = ['00' , '21' , '12' ,'33']
    temp = 40
    data = []        
    for i in range(100):
        chess = ChessBoard(panjang=4 , lebar=4 ,initialState=initial_state)
        # ! Estimate Cost
        heuritstic , pair = chess.estimateCost()   
        
        current_state = chess.initialState
        #print("Current State : " , chess.initialState)

        chess.updateInitalState()
        
        candidate_state = chess.initialState.copy()
        #print("Candidate State : " , chess.initialState)

        candidate_heuristci , candidate_pair  = chess.estimateCost()
        
        delta_e = candidate_heuristci - heuritstic
        if candidate_heuristci < heuritstic:      
                # ! Replace State 
            initial_state = candidate_state  
            print("Best H " , candidate_heuristci)

            print("Pair : " , candidate_pair)      
        
        t = temp / float(i+1)
        metroprolis = math.exp(-delta_e / t)
        if delta_e < 0 or random.uniform(0,1) < metroprolis:
            initial_state = candidate_state
        
            
            
do_simulated_annealing()