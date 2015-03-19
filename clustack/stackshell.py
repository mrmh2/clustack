"""Load the named stack and start a shell with a suitable modified environment.
"""

import argparse

from stack import load_stack_by_name

def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('stack_name', help="Name of stack to load")

    args = parser.parse_args()

    st = load_stack_by_name(args.stack_name)

    st.env_manager.my_env['PS1'] = "<{0}>".format(args.stack_name) + st.env_manager.PS1

    st.shell()

if __name__ == '__main__':
    main()
