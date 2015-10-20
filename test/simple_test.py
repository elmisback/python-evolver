import evolver
import logging

evolver.logger.setLevel(logging.DEBUG)
evolver.logger.addHandler(logging.StreamHandler())

def main():
    """The main method."""

    with evolver.Evolver() as E:
        print E.run_command('foo := 3')
        print E.run_command('print foo')

if __name__ == "__main__":
    main()
