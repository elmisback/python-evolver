## python-evolver

### Usage
```
import evolver

with evolver.Evolver('/path/to/evolver') as E:
    E.run_command('foo := 3')
    output = E.run_command('print foo')
    print output  # prints the string 3
```

### Source

To download the surface evolver, see its
[homepage](http://facstaff.susqu.edu/brakke/evolver/evolver.html).
