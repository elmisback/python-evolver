"""evolver.py: a simple Python interface to Ken Brakke's surface evolver REPL.

# Notes
The procedures here could be generalized to allow interaction with any 
command-line REPL interface.
"""

import subprocess
import multiprocessing
import select
import fcntl, os

def _non_block_read(output):
    """Non-blocking read from a file-like object."""
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ""

class Evolver(object):
    """Represents an evolver instance."""

    def close_file(self):
        self.run_command('q', delimeter='Enter new datafile name '
                         '(none to continue, q to quit):') 
        print '\nClosed File: ' + self.working_file
        self.working_file = False

    def dump(self):
        self.run_command('dump')         

    def evolve(self, repeats=1, to_print=False):
        """Evolves a specified number of times and returns the values of
        area, energy, and scale
        """
        command = 'g ' + str(repeats)
        output = self.run_command(command)
        split_output = output.split()
        if not split_output:
        	output = self._get_response(delimeter='Enter command:')
        	split_output = output.split()
        values = list()
        for i in range(3):
            values.append(i)
        values[0] = split_output[(repeats-1)*7 + 2]
        values[1] = split_output[(repeats-1)*7 + 4]
        values[2] = split_output[(repeats-1)*7 + 6]
        print output + '\n'
        if to_print:
            print output + '\n'
        return values

    def _get_response(self, delimeter):
        """Returns evolver's output up to a delimeter string.
        
        Output is whitespace-stripped.
        """
        output = ''
        while True:
            # Wait for output.

            stdout, _, _ = select.select([self.evolver.stdout], [], [], 1)
            new = _non_block_read(self.evolver.stdout)
            end = new.find(delimeter)
                
            if end >= 0:
                return (output + new[:end]).strip()
            output += new

    def open_file(self, data_file):    
        if self.working_file: 
            print 'File already opened\n'
        else:  
            self.run_command(data_file, delimeter='Enter command: //End Of Input')
            self.working_file = data_file
            print 'Opened file: ' + data_file + '\n'

    def refine(self, repeats='1'):
        """refines a specified number of times"""
        command = 'r ' + str(repeats)
        return self.run_command(command)        

    def run_command(self, command, delimeter="Enter command:"):
        """Returns whitespace-stripped output for `command` up to `delimeter`.
        """
        # (\n executes command)
        self.evolver.stdin.write(command + '\n')
        self.evolver.stdin.flush()
        return self._get_response(delimeter)    
       
    def vertex_averaging(self, repeats='1'):
        """Averages vertices a specified number of times"""
        command = 'V '+ str(repeats)
        return self.run_command(command)    

    def __init__(self, executable):
        # We use subprocess.PIPE so this process can interact with evolver's
        # stdin/out/err streams.
        self.evolver = subprocess.Popen([executable], 
                                        stdin=subprocess.PIPE, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        # # Wait for evolver to initialize.    
        self.working_file = False
        self._get_response('Enter new datafile name '  
                           '(none to continue, q to quit):')
        
     
    def __enter__(self):
        """Enables 'with' statement."""
        return self

    def __exit__(self, *args):
        """Always stop evolver when the user is finished."""
        self.evolver.terminate() 

def main():
    """The main routine."""       

    with Evolver('/Users/kevinshebek/Documents/Evolver/src/evolver') as E:
        E.open_file('mound.fe')      
        E.evolve(1, True)
        print E.refine(1) + '\n'
        print E.vertex_averaging(1) + '\n'
        E.evolve(1, True)     

        E.close_file()  

if __name__ == "__main__":
    main()
