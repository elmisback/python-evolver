## python-evolver

### Setup

Make sure evolver is on the system path. This is as simple as running

```
ln -s /Absolute/path/to/evolver /usr/local/bin/evolver
```

### Usage
```
import evolver

with evolver.Evolver('/path/to/evolver') as E:
    E.run_command('foo := 3')
    output = E.run_command('print foo')
    print(output) # prints the string 3
```

### Development

Get [pip](http://pip.readthedocs.org/en/stable/installing/). [Clone the
repository](https://help.github.com/articles/cloning-a-repository/) and run 

```
pip install --editable /path/to/repo
```

### Source

To download the surface evolver, see its
[homepage](http://facstaff.susqu.edu/brakke/evolver/evolver.html).
