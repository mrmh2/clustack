import blueprint
from stack import Stack
from component import Package

def main():
    s = Stack()
    print s

    #print s.env_manager

    p_ncurses = Package('python')

    s.add_component(p_ncurses)
    s.add_component(Package('gcc'))

    #print s.env_manager

    s.shell()

if __name__ == "__main__":
    main()
