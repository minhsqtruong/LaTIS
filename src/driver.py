from latis import create_test
from latis import search_op
from latis import create_op
from latis import create_include
from latis import create_header
from latis import create_footer
from latis import print_database
from latis import purge_database
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

        if (op == 'new'):
            new_op_name = arg[1]
            newpid = os.fork()
            if newpid == 0:
                create_op(new_op_name)
            pid, status = os.waitpid(newpid, 0)
        elif (op == 'print'):
            newpid = os.fork()
            if newpid == 0:
                print_database()
            pid, status = os.waitpid(newpid, 0)
        elif (op == 'purge'):
            newpid = os.fork()
            if newpid == 0:
                purge_database()
            pid, status = os.waitpid(newpid, 0)
        else:
            valid = search_op(op)
            if (valid):
                os.system('rm -rf ../run/' + op)
                for chain in range(1,int(arg[1])):
                    print("Creating " + str(chain) + "chains")
                    create_test(op, chain, arg[2])
            exit(0)
