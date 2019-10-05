from latis import create_test
from latis import search_op
from latis import create_op
from latis import create_include
from latis import create_header
from latis import create_footer
from latis import print_database
import sys

if __name__ == "__main__":
    op = sys.argv[1]
    if (op == 'new'):
        create_op(sys.argv[2])
    elif (op == 'include'):
        create_include()
    elif (op == 'header'):
        create_header()
    elif (op == 'footer'):
        create_footer()
    elif (op == 'print'):
        print_database()
    else:
        entry = search_op(op)

    if (entry == 0):
        print("Error: operation not found in database, specify <op> = 'new' to add new operation")
    else:
        for num_chains in range(1,int(max_module)):
            op = create_test(op)
