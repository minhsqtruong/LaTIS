import os
import sys
import csv
import sys
import tempfile
from subprocess import call

class db_entry:
    def __init__(self, index, isa_name):
        self.index = index
        self.isa_name = isa_name

    def add_attribute(path_to_file, attribute_name):
        if (attribute_name == 'macro'):
            with open(path_to_file) as tmp:
                self.macro = tmp.readlines()[0]
        elif (attribute_name == 'input'):
            with open(path_to_file) as tmp:
                lines = tmp.readlines()
                for line in lines:
                    self.input.append(line)
        elif (attribute_name == 'call'):
            with open(path_to_file) as tmp:
                self.call = tmp.readlines()[0]

    def save_entry():
        pass



def create_test(op, num_trials, num_chains):
    pass

def create_test():
    pass

def search_op():
    pass

def create_op(op):
    current_size = 0
    EDITOR = os.environ.get('EDITOR', 'vim')
    with open('../db/isa.csv') as db:
        #get size of current isa database
        current_size = db.readlines()[0]

    new_index = int(current_size) + 1
    new_entry= db_entry(new_index, op)

    # create new macro
    initial_message = 'Please write your macro in this tmp file (Remember to delete me)'
    macro_message = ''
    os.system('rm -rf ../tmp/macro.tmp')
    with open("../tmp/macro.tmp","w") as tf:
        tf.write(initial_message)
        tf.flush()
        call([EDITOR, tf.name])
        tf.seek(0)
        macro_message = tf.read()
    print(macro_message)
    # create new variables

    # create new call



def create_include():
    pass

def create_header():
    pass

def create_footer():
    pass

def print_database():
    pass
