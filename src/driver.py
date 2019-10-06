from latis import create_test
from latis import search_op
from latis import create_op
from latis import create_include
from latis import create_header
from latis import create_footer
from latis import print_database
from latis import interface, help, checkinput
import pyfiglet
import sys
import os
import shutil

if __name__ == "__main__":
    while True:
        interface("Hi! what would you like to do?")
        help()
        arg = checkinput().split()
        op = arg[0]
        new_op_name = arg[1]

        if (op == 'new'):
            newpid = os.fork()
            if newpid == 0:
                create_op(new_op_name)
            pid, status = os.waitpid(newpid, 0)

        else:
            print("Error: Option not found")
            arg = checkinput().split()
    # if (op == 'new'):
    #     create_op(new_op_name)
    # elif (op == 'include'):
    #     create_include()
    # elif (op == 'header'):
    #     create_header()
    # elif (op == 'footer'):
    #     create_footer()
    # elif (op == 'print'):
    #     print_database()
    # else:
    #     entry = search_op(op)
    #
    # if (entry == 0):
    #     print("Error: operation not found in database, specify <op> = 'new' to add new operation")
    # else:
    #     for num_chains in range(1,int(max_module)):
    #         op = create_test(op)
