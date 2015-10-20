import subprocess
import multiprocessing
import select
import fcntl, os
import re
import matplotlib.pyplot as plt
import numpy as np
import time

from evolver import Evolver


def find_values(fileloc, phrase):
	wf = open(fileloc, 'r')
	words = wf.read().split()
	i = 0
	param = list()
	for x in words:
		if x == phrase:
			param.append(words[i + 2])
			break
		i += 1
	return param

def define_values(bo):
	wf = open('./dropSinusoidal.fe', 'r')
	m = wf.read()
	m = re.sub('Bo = \w*.\w*', 'Bo = %f' % bo, m)
	wf = open('./dropSinusoidal.fe', 'w')
	wf.write(m)

def main():
    """The main routine."""

    with Evolver('/Users/kevinshebek/Documents/Evolver/src/evolver') as E:
        
        n = 1000
    	init_bo = 0
    	params = np.empty([3, n])

    	for i in range(n):
    		print '-----------------\nTime Around ' + str(i)
    		
    		bo = init_bo + 0.05*i
    		define_values(bo)
    		E.open_file('dropSinusoidal.fe')   		

    		for j in range(1):
    			#E.refine(1)
    			vals = E.evolve(1)   			

    		E.run_command('car_app')
    		E.run_command('car')
    		E.run_command('')
    		E.run_command('dump')
    		E.run_command('')
    		E.close_file()
    		 		
    		params[0, i] = bo
    		params[1, i] = find_values('/Users/kevinshebek/Desktop/EvSc/dropSinusoidal.fe.dmp', 'contact_angle_right')[0]
    		params[2, i] = find_values('/Users/kevinshebek/Desktop/EvSc/dropSinusoidal.fe.dmp', 'contact_angle_right_app')[0]
    		
    		

    	print 'To Plot'
    	plt.plot(params[0, :], params[1, :], label="Contact Angle")
    	plt.plot(params[0, :], params[2, :], label="Apparent Contact Angle")
    	plt.ylabel('Contact Angle')
    	plt.xlabel('Bond Number (Bo)')
    	plt.legend()
    	plt.show()       

if __name__ == "__main__":
    main()
