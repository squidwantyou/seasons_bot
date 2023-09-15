#!/usr/bin/env python
import sys,os
import numpy as np
from copy import deepcopy
import itertools

N = 5
class ms:
    def __init__(self, size = (N,N) ):
        self.board = np.ndarray( shape = size, dtype = int )  
        self.coords = list()
        for i in range(N):
            for j in range(N):
                self.coords.append( (i,j) )
                self.board[i,j] = 9

        self.nb = dict()
        for i in range(N):
            for j in range(N):
                self.nb[ (i,j) ] = set()
                xlower = max( i-1, 0)
                xupper = min( i+1, N-1 ) 
                ylower = max( j-1, 0)
                yupper = min( j+1, N-1 ) 
                for x in range(xlower,xupper+1):
                    for y in range(ylower,yupper+1):
                        if (x,y) != (i,j):
                            self.nb[ (i,j) ].add( (x,y) )

    def assign(self, x,y, num ):
        assert 0<=num<=8
        self.board[x,y] = num

    def get_hints(self):
        hints = list()
        for c in self.coords:
            if self.board[c] != 9:
                hints.append( (c,self.board[c] ) )
        self.hints = sorted( hints, key = lambda x:x[1] , reverse = True)
        return self.hints

    def update_nb(self):
        for (h,x) in  self.get_hints():
            for b in self.nb:
                if h in self.nb[b]:
                    self.nb[b].remove(h)
        return self.nb

    def accept( self, c_h, hint_number ,case ):
        # print("X",c_h, hint_number,case)
        s = 0
        nb = self.nb[c_h]
        for c in case:
            if c in nb:
                s += 1
        # print( "Y", s,hint_number, s == hint_number )
        return s == hint_number

    def solve(self):
        nb_list = deepcopy( self.update_nb() )
        hlist = self.get_hints()

        c_c = set()
        knownpool = [ (), ]

        while True:
            # set current hint as first hint 
            c_h,hint_number = hlist.pop(0)
            # print("A",c_h,hint_number)

            # A 
            # get permutation coords
            a = nb_list[c_h]
            # print("B",a)

            tmp_a = a - c_c 
            # print("C",tmp_a)
            c_c = c_c | a
            # print("D",c_c)

            # permutation  coords
            pool = list()
            for i in range(0,hint_number+1):
                pool.extend( list(itertools.combinations(tmp_a,i) ) )
            # print("E",pool)

            # combine new permutation of known
            newpool = set()
            for tmpi in knownpool:
                for tmpj in pool :
                    newpool.add( tmpi + tmpj )
            knownpool = newpool 

            # check new hint
            tmp_knownpool = deepcopy( knownpool )
            for case in knownpool:
                if not self.accept( c_h, hint_number ,case ):
                    tmp_knownpool.remove( case )
            knownpool = tmp_knownpool

            if len(knownpool) == 0: # if no result:
                return False # return False
            else:
                if len(hlist) == 0 : # if no more hints:
                    print(knownpool)
                    return len(knownpool)
                else:
                    continue
                    # if only one result:
                        # return 1
                    # if multiple results:
                        # return N




a = ms()
a.assign( 0, 0, 1 )
a.assign( 0, 1, 1 )
a.assign( 1, 1, 3 )
a.assign( 1, 3, 1 )
a.assign( 2, 1, 6 )
a.assign( 2, 3, 2 )
a.assign( 4, 0, 2 )
a.assign( 4, 2, 2 )
a.assign( 4, 3, 1 )
  
print(a.solve())
print(a.board)
