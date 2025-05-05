import sys
import os
import glob
import re
from unittest.mock import patch

import client

#colors
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

def redirect_mock(input_file, output_file):
    original_stdout = sys.stdout #for later reassignment
    try:
        with open(input_file, 'r') as input, open(output_file, 'w') as output:
            sys.stdout = output     #replace print to screen with print to file
            def mock_input(input_text_prompt):
                output.write(input_text_prompt) #write the prompt of input(prompt)
                output.flush() #disable buffering of output

                line = input.readline() #read a line from test file 
                output.write(line) #write a line for realistic output generation
                output.flush() #disable buffering of the output
                return line.strip('\n') #strip the newline as input() does
            
            def empty():
                return None
            
            #run the main function with the mock input and without clearing the screen and without password interaction
            with patch('builtins.input', mock_input), patch('client.clear_screen', empty), patch('getpass.getpass', mock_input):
                return client.main()


    except EOFError:
        print("Check input file")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        sys.stdout = original_stdout

def tester():
    input_files = glob.glob("testfiles/in*.txt") #finds all the input files

    test_nums = []
    for file in input_files:
        test_num = re.search(r'[0-9]+', file) #finds the test number in the filename
        #print(test_num)  #debug
        if test_num:
            test_nums.append(test_num.group(0)) #append the whole regex match to the test num list

    test_nums_ints = [int(num) for num in test_nums] #convert the test numbers to integers
    test_nums_ints.sort()
    for test_num in test_nums_ints:
        input_filepath = f"testfiles/in{test_num}.txt"
        output_filepath = f"testfiles/out{test_num}.txt"
        print(f"Test case {test_num}...", end=' ')
        #run the mock redirection
        finish = redirect_mock(input_filepath, output_filepath) #for each test case run mock
        if finish:
            print(GREEN + "Success!" + RESET)
        else:
            print(RED + "Error!" + RESET)


if __name__ == "__main__":
    tester()