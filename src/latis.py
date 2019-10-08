import os
import sys
import csv
import sys
import time
import shutil
import pickle
from subprocess import call
from pathlib import Path
import pyfiglet

#===============================================================================
#                               Shell helpers
#===============================================================================

def interface(string):
    os.system("clear")
    columns = shutil.get_terminal_size().columns
    custom_fig = pyfiglet.figlet_format("LaTIS")
    print(custom_fig.center(columns))
    print(string)

def help():
    print("\n \t <macro name> <num chains> <num trials> <Enter> to execute benchmark on old macro")
    print("\t new <macro name> <Enter> to write new macro ISA benchmark")
    print("\t print <Enter> to print existing ISA in the benchmark database")
    print("\t help <Enter> to pull up this menu")
    print("\t purge <Enter> to delete the entire database")
    print("\t exit <Enter> to exit child thread or end LaTIS")
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


#===============================================================================
#                           DB Entry class
#===============================================================================

class db_entry:
    def __init__(self, index, isa_name, include='default', header='default', footer='default'):
        self.index = index
        self.isa_name = isa_name
        self.include = include
        self.header = header
        self.footer = footer
        self.__macro()

#---------------------------Macro initiation------------------------------------

    def __chain_testcall(self):
        self.test_call += self.call + '('
        for var in self.inputname:
            self.test_call += var
            self.test_call += ','
        self.test_call = self.test_call[:-1]
        self.test_call += ');'

    def __get_variable(self): #TODO make it idiot proof
        try:
            interface("Ok so your macro name is \'" + self.call +"\' with " + str(self.numinput) + " arguments. List first from last arguments in <type> | <name> | <value> | format.")
            self.inputname = []
            self.inputtype = []
            self.inputval = []
            self.test_call = ''
            for i in range(self.numinput):
                user_string = checkinput().split('|')
                self.inputtype.append(user_string[0].replace(' ', ''))
                self.inputname.append(user_string[1].replace(' ', ''))
                self.inputval.append(user_string[2].replace(' ', ''))
                self.test_call += user_string[0] + ' ' + user_string[1] + '=' + user_string[2] + ';'
        except:
            interface("Oops...your format is wrong, return to menu now. Idiot proof needed for better feature")
            time.sleep(2)
            os.__exit(0)

    def __get_call(self):
        try:
            interface("""How would a program calls your new macro? For example: my_macro(var1, var2, var3) """)
            user_string = checkinput()
            self.call = user_string.split('(')[0]
            self.numinput = len(user_string.split(','))
        except:
            interface("Oops...your format is wrong, return to menu now. Idiot proof needed for better feature")
            time.sleep(2)
            os.__exit(0)

    def __compile_macro(self):
        # get new macro
        include_string = ''
        if (self.include == 'default'):
            with open ("../db/include.csv") as db:
                lines = db.readlines()
                include_string = lines[1].replace('$','\n');
        else:
            pass #TODO allow user to pick include string

        test_src = include_string + self.macro +  "int main(void){" + self.test_call + "printf(\"Sucessful compilation from gcc \\n \"); return 0;}"
        os.system('rm -rf ../tmp/test_src.c')
        interface('I am going to try to compile your macro')
        with open("../tmp/test_src.c", "w") as tf:
            tf.write(test_src)
        os.system('rm -rf test_src')
        os.system('gcc -march=native -o test_src ../tmp/test_src.c -O')
        os.system('./test_src')

    def __macro(self):
        # create new macro
        interface("Ok Let's define a new macro... I am going to take you to vim")
        time.sleep(2)
        EDITOR = os.environ.get('EDITOR', 'vim')
        initial_message = 'Please write your macro in this tmp file (Remember to delete me)'
        macro_message = ''
        os.system('rm -rf ../tmp/macro.tmp')
        with open("../tmp/macro.tmp","w") as tf:
            tf.write(initial_message)
            tf.flush()
            call([EDITOR, tf.name])
            tf.seek(0)

        # get new macro
        self.macro = Path('../tmp/macro.tmp').read_text()

        # get new call
        self.__get_call()

        # get new input
        self.__get_variable()

        self.__chain_testcall()

        # try to compile
        self.__compile_macro()

        user_string = ''
        while(user_string != 'none'):
            print("Would you like to debug anything? <macro> <call> <none>")
            user_string = checkinput()
            if (user_string == 'macro'):
                interface("Ok Let's check your macro file... I am going to take you to vim")
                time.sleep(1)
                EDITOR = os.environ.get('EDITOR', 'vim')
                with open("../tmp/macro.tmp","a+") as tf:
                    call([EDITOR, tf.name])
                    tf.seek(0)

                self.macro = Path('../tmp/macro.tmp').read_text()
                self.__compile_macro()

            if (user_string == 'call'):
                self.__get_call()
                self.__get_variable()
                self.__chain_testcall()
                self.__compile_macro()

        interface("Would you like to commit this new entry to isa database? <yes> <no>")
        user_string = checkinput()
        if (user_string == 'yes'):
            self.commit = True
        elif (user_string == 'no'):
            self.commit = False

#===============================================================================
#                           Shell Functions
#===============================================================================

def search_op(op):
    interface("Searching...")
    with open('../db/isa.db', 'rb') as db:
        object_list = pickle.load(db)
    object_list.pop(0)
    for entry in object_list:
        if(entry.isa_name == op):
            return True
    print("ISA not found, type any keys to return to main menu")
    checkinput()
    return False

def create_test(op, num_chains, num_trials):
    num_chains = str(num_chains)
    isa = 0
    with open('../db/isa.db', 'rb') as db:
        object_list = pickle.load(db)
    object_list.pop(0)
    for entry in object_list:
        if(entry.isa_name == op):
            isa = entry

    with open ("../db/include.csv") as db:
        lines = db.readlines()
        include_string = lines[1].replace('$','\n');

    with open ("../db/header.csv") as db:
        lines = db.readlines()
        header_string = lines[1].replace('$','\n');

    with open ("../db/footer.csv") as db:
        lines = db.readlines()
        footer_string = lines[1].replace('$','\n');

    file_name = '../run/' + op + '/' + num_chains + '.c'
    os.system('rm -rf' + file_name)
    os.system('mkdir ../run/' + op)
    os.system('touch ' + file_name)
    f = open(file_name, 'w+')
    f.write(include_string)
    f.write(isa.macro)
    f.write(header_string)
    input_string = ""
    call_string = ""
    for chain in range(int(num_chains)):
        call_string += isa.call + "("
        for i in range(isa.numinput):
            call_string += isa.inputname[i] + str(chain) + ','
            input_string += entry.inputtype[i] + " " + entry.inputname[i] + str(chain) + "=" + entry.inputval[i] + ";\n"
        call_string = call_string[:-1]
        call_string += ");\n"
    f.write(input_string)
    f.write("start = rdtsc(); \n")
    for trial in range(int(num_trials)):
        f.write(call_string)
    f.write("end = rdtsc(); \n")
    f.write("float cycles = (float) (end - start);\n")
    f.write("printf(\""+ "With " + str(num_chains) + " chains :%f\\n \", cycles);")
    f.write(footer_string)
    f.close()
    os.system('gcc -O -march=native -o ../run/' + op + '/' + num_chains + '.o ' + file_name)

def create_op(op,include='default', header='default', footer='default'):
    current_size = 0
    object_list = []
    with open('../db/isa.db', 'rb') as db:
        object_list = pickle.load(db)

    current_size = object_list[0]
    new_index = current_size + 1
    new_entry = db_entry(new_index, op, include, header, footer)
    object_list[0] = new_index
    object_list.append(new_entry)
    if (new_entry.commit == True):
        with open('../db/isa.db', 'wb') as db:
            pickle.dump(object_list, db, pickle.HIGHEST_PROTOCOL)
    os._exit(0)

def create_include():
    pass

def create_header():
    pass

def create_footer():
    pass

def purge_database():
    interface("Are you sure you want to purge the database? <yes> <no>")
    user_string = checkinput().split()[0]
    if (user_string == 'yes'):
        os.system('rm -rf ../db/isa.db')
        os.system('touch ../db/isa.db')
        object_list = [0]
        with open('../db/isa.db', 'wb') as db:
            pickle.dump(object_list, db, pickle.HIGHEST_PROTOCOL)
        os._exit(0)

def print_database():
    with open('../db/isa.db', 'rb') as db:
        object_list = pickle.load(db)

    size = object_list[0]
    print("There are " + str(size) + " instructions in the database")
    for entry in object_list[1:]:
        print("="*50)
        print("Index: " + str(entry.index))
        print("Name: " + str(entry.isa_name))
        print("\nMacro: ")
        print(str(entry.macro))
        print("\nVariable:")
        for i in range(entry.numinput):
            print(entry.inputtype[i] + " " + entry.inputname[i] + " " + entry.inputval[i])
        print("\nInclude: ")
        print(str(entry.include))
    print("="*50)
    print("Type any keys to return to main menu")
    user_string = checkinput()
