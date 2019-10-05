import os
import sys
import csv
import sys
import time
import shutil
from subprocess import call
from pathlib import Path
import pyfiglet

def interface(string):
    os.system("clear")
    columns = shutil.get_terminal_size().columns
    custom_fig = pyfiglet.figlet_format("LaTIS")
    print(custom_fig.center(columns))
    print(string)

def help():
    print("\n \t <macro name> <Enter> to execute benchmark on old macro")
    print("\t new <macro name> <Enter> to write new macro ISA benchmark")
    print("\t print <Enter> to print existing ISA in the benchmark database")
    print("\t help <Enter> to pull up this menu")
    print("\t exit <Enter> to exit LaTIS")
    print("\n")

def checkinput():
    user_string = input("<LaTIS> ")
    if (user_string == 'help'):
        help()
        user_string = checkinput()
    if (user_string == 'exit'):
        os.system('clear')
        exit()
    if (user_string == ''):
        user_string = checkinput()
    return user_string

class db_entry:
    def __init__(self, index, isa_name, include='default', header='default', footer='default'):
        self.index = index
        self.isa_name = isa_name
        self.include = include
        self.header = header
        self.footer = footer
        self.__macro()

    def save_entry():
        pass

    def __macro(self):
        # create new macro
        interface("Ok Let's define a new macro... I am going to take you to vim")
        time.sleep(3)
        EDITOR = os.environ.get('EDITOR', 'vim')
        initial_message = 'Please write your macro in this tmp file (Remember to delete me)'
        macro_message = ''
        os.system('rm -rf ../tmp/macro.tmp')
        with open("../tmp/macro.tmp","w") as tf:
            tf.write(initial_message)
            tf.flush()
            call([EDITOR, tf.name])
            tf.seek(0)

        self.macro = Path('../tmp/macro.tmp').read_text()

        # get new macro
        include_string = ''
        if (self.include == 'default'):
            with open ("../db/include.csv") as db:
                lines = list(csv.reader(db))
                include_string = lines[1][1].replace(':','\n');
                assert lines[1][0] == '0', "Default include index is not 0"
        else:
            pass #TODO allow user to pick include string

        # get new call

        interface("""How would a program calls your new macro? For example: my_macro(var1, var2, var3) """)
        user_string = checkinput()
        self.call = user_string.split('(')[0]
        self.numinput = len(user_string.split(','))

        # get new input
        interface("Ok so your macro name is \'" + self.call +"\' with " + str(self.numinput) + " arguments. List first from last arguments in <type> <name> <value> format.")
        self.inputname = []
        self.inputtype = []
        self.inputval = []
        test_call = ''
        for i in range(self.numinput):
            user_string = checkinput().split()
            self.inputtype.append(user_string[0])
            self.inputname.append(user_string[1])
            self.inputval.append(user_string[2])

            test_call += user_string[0] + ' ' + user_string[1] + '=' + user_string[2] + ';'



        test_call += self.call + '('
        for var in self.inputname:
            test_call += var
            test_call += ','
        test_call = test_call[:-1]
        test_call += ');'

        test_src = include_string + self.macro +  "int main(void){" + test_call + "; printf(\"Sucessful compilation from gcc \n \") return 0;};"
        os.system('rm -rf ../tmp/test_src.c')
        interface('I am going to try to compile your macro')
        with open("../tmp/test_src.c", "w") as tf:
            tf.write(test_src)
        os.system('gcc -o test_src ../tmp/test_src.c -O')






def create_test(op, num_trials, num_chains):
    pass

def create_test():
    pass

def search_op():
    pass

def create_op(op,include='default', header='default', footer='default'):
    current_size = 0
    with open('../db/isa.csv') as db:
        #get size of current isa database
        current_size = db.readlines()[0]

    new_index = int(current_size) + 1
    new_entry= db_entry(new_index, op, include, header, footer)


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
