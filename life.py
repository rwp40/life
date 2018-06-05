#!/usr/bin/python
# life.py
# Usage:   life [input-file=life.inp* ] [ <iterations=1-990> ] [<debug with any char>]
# Output:  stdout
#          non-result outputs directed to stderr
# Author: Rick Penza, 2/26/2017
#                     6/01/2018                       

import sys, os, pprint, io, time
from copy import deepcopy
import numpy as np

# Defaults
DEBUG = False
DEBUGR= False
ANIM=True
inputf='life.inp'
count=10

def Process(filename,count):
    assert os.path.exists(filename), 'Cannot find the file: %s' % (filename)

    print >> sys.stderr,"Load input matrix"
    input = np.loadtxt(filename, dtype='c', delimiter=' ')
    if DEBUG:
        print >> sys.stderr,(input)

    print >> sys.stderr, "Construct n+2 X n+2 matrix, zeroed, to provide a border of dead neighbors"
    work = [['0' for i in xrange(len(input[0])+2)] for i in xrange(len(input[0])+2)]
    if DEBUG:
        pprint.pprint(work)
                
    print >> sys.stderr, "Copy n x n input matrix to larger n+1 x n+1 matrix"
    for x in range(len(input)):
        for y in range(len(input)):
            work[x+1][y+1] = input[x][y]

    if DEBUG:
        print >> sys.stderr, "Overlayed matrix"
        pprint.pprint(work)

    print >> sys.stderr, "Copy the n+1 x n+1 matrix to hold results"
    result = deepcopy(work)
    if DEBUG:
        print >> sys.stderr, "Starting matrix"
        pprint.pprint(result)

    print >> sys.stderr, "Walk through matrix and apply rules"
    Iterate(input,work,result,count)

        
def Iterate(input,work,result,level):
    print "Iteration %d" %level 
    for x in range(1,len(input)+1):
        for y in range(1,len(input)+1):
            if DEBUG:
                print >> sys.stderr, "x=%d , y=%d" % (x, y)
                print >> sys.stderr, "%d+%d+%d+%d+X+%d+%d+%d+%d" % (int(work[x-1][y-1]), int(work[x][y-1]), int(work[x+1][y-1]),\
                                                                    int(work[x-1][y]),        int(work[x+1][y]), \
                                                                    int(work[x-1][y+1]), int(work[x][y+1]), int(work[x+1][y+1]))   

            # Count this cells neighbors
            tot = int(work[x-1][y-1])   + int(work[x][y-1]) + int(work[x+1][y-1]) + \
                int(work[x-1][y])     + 0                 + int(work[x+1][y])   + \
                      int(work[x-1][y+1])   + int(work[x][y+1]) + int(work[x+1][y+1])

            if DEBUG:
                print >> sys.stderr, "Total [%d,%d] neigbors: %d" % (x, y, tot)

            # Apply live cell rules
            if int(work[x][y]) == 1:
                # rule 1
                if tot < 2:             # less than 2 means death
                    result[x][y] = '0'
                if tot in range(2,3):   # 2 or 3 means keep alive
                    result[x][y] = '1'
                if tot > 3:             # more than 3 means overpopulated, thus death
                    result[x][y] = '0'
            # Apply dead cell rule
            if int(work[x][y]) == 0:
                if tot == 3:            # exactly 3 means rebirth
                    result[x][y] = '1'

    if DEBUGR:
        print >> sys.stderr, "Evolved work matrix"
        pprint.pprint(work)
        print >> sys.stderr, " Evolved result"
        pprint.pprint(result)
        
    work = deepcopy(result)

    # Show result in orignal n x x format
    if ANIM:
        junk=os.system("clear")
        #time.sleep(1)
    print >> sys.stderr, "Output"
    for x in range(1,len(input)+1):
        for y in range(1,len(input)+1):
            print '{}'.format(result[x][y]),
        print

    print
    if level > 0:
        Iterate(input,work,result,level-1)
    return 0

#####################
###### M A I N ######
#####################

if len(sys.argv) > 3:   # anything in argv[3] specifies DEBUG mode
    DEBUG = True

if len(sys.argv) >= 3:  # iterations
    count=int(sys.argv[2])
    if count > 990:
        print "Max iterations is 990"
        count=990
              
if len(sys.argv) >= 2:
    inputf = sys.argv[1]

if DEBUG:
    print >> sys.stderr,"Input file is %s" % inputf

# Do it
Process(inputf,count) 
