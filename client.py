import re
import xmlrpc.client
from typing import List, Tuple
import os
import getpass

server_ip = "localhost"
server_port = 8000

#colors
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

#clear function
def clear_screen():
    os.system('cls||clear') #clear the screen for unix or windows
    return

#validations
#validate the tfn format
def validate_tfn(tfn):
    return bool(re.match('^[0-9]{8}$', tfn))

#validate the person id format
def validate_person_id(person_id):
    return bool(re.match('^[0-9]{6}$', person_id))

#validate the email format
def validate_email(email):
    return bool(re.match('^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$', email))

#validate the income and tax withheld format
def validate_value(value):
    return bool(re.match('^[0-9,.-]+$', value))

class TaxClient:
    #constructor 
    def __init__(self):
        self.person_id= ""
        self.tfn = ""
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.has_phic = False
        self.has_tfn = False
        self.income_data = []
        self.server = None
        self.is_register = False

    def welcome_menu(self):
        options = {
            '1': "Login",
            '2': "Register",
            '3': "Guest",
            '4': "Exit"
        }
        print("\n" + "="*50)#border
        print(BLUE + "Welcome to the Personal Income Tax Return Estimate (PITRE) System" + RESET)
        print("\n" + "="*50 + "\n") #border

        print("Please select how you would like to proceed by entering the number:")
        print("-" * 50)
        # Display options clearly
        for num, action in options.items():
            print(f"           {num}. {action}")
        print("-" * 50)
        while True:
            choice = input("Enter your choice: ")
            print("-" * 50)
            if choice == '1':
                return self.login()
            elif choice == '2':
                return self.register()
            elif choice == '3':
                return self.guest()
            elif choice == '4':
                print(GREEN + "Exiting the program..." + RESET)
                exit()
            else:
                print(RED + "Option not available. Please enter a valid option number (1, 2, 3, or 4)." + RESET)
                print("-" * 50)

    def guest(self):
        #ask for TFN
        clear_screen()
        print(BLUE + "Welcome to the Personal Income Tax Return Estimate (PITRE) System" + RESET)
        if (input("Do you have a Tax File Number? (yes/no): ").lower() == 'yes'):
            self.has_tfn = True

        #collect person id
        while 1:
            self.person_id = input("Enter your 6-digit Person ID: ")
            if validate_person_id(self.person_id):
                break
            print(RED+"Invalid Person ID format. Please enter 6 digits."+RESET)


        if self.has_tfn:
            #collect tfn
            while 1:
                self.tfn = input("Enter your 8-digit Tax File Number: ")
                if validate_tfn(self.tfn):
                    break
                print(RED+"Invalid TFN format. Please enter 8 digits."+RESET)

        else:
            #collect income data
            print("Enter your biweekly income data (1-26 entries):")
            count = 0
            while count < 26:
                income = input(f"Enter taxable income #{count + 1} (or -1 to finish): ")
                if not validate_value(income):
                    print(RED + "Invalid input. Please enter a valid number." + RESET)
                    continue
                income = float(income.replace(',', ''))
                if income == -1:
                    if count < 1:
                        print(RED + "You must enter at least one income entry." + RESET)
                        continue
                    break
                tax = input(f"Enter tax withheld for income #{count + 1}: ")

                while not validate_value(tax):
                    print(RED + "Invalid input. Please enter a valid number." + RESET)
                    tax = input(f"Enter tax withheld for income #{count + 1}: ")
                    continue
                tax = float(tax.replace(',', ''))
                if tax < 0 or tax > income or income < 0:
                    print(RED + "Invalid input. Tax withheld must be less than or equal to income and both must be non-negative." + RESET)
                    continue
                self.income_data.append((income, tax))
                count += 1

        #private health insurance cover

        if(input("Do you have Private Health Insurance Cover? (yes/no): ").lower() == 'yes'):
            self.has_phic = True



    def login(self):
        clear_screen()
        print("=" * 50)
        print(BLUE + "Please enter your credentials to log into the system" + RESET)
        print("=" * 50)
        #login to the server
        while 1:
            self.person_id = input("Enter your 6-digit Person ID: ")
            if validate_person_id(self.person_id):
                break
            print(RED + "Invalid Person ID format. Please enter 6 digits." + RESET)
        
        password = getpass.getpass("Enter your password: ")

        user = self.server.login(self.person_id, password) #autheticate with server
        if not isinstance(user, str):
            print(GREEN + "Login successful." + RESET)
        else:
            print(RED + user + RESET)
            return False
        

        self.tfn = user[1] 
        self.first_name = user[2]
        self.last_name = user[3]
        self.email = user[4]
        self.has_phic = user[5]
        if self.tfn == "":
            print("Enter your biweekly income data (1-26 entries):")
            count = 0
            while count < 26:
                income = input(f"Enter taxable income #{count + 1} (or -1 to finish): ")
                if not validate_value(income):
                    print(RED + "Invalid input. Please enter a valid number." + RESET)
                    continue
                income = float(income.replace(',', ''))
                if income == -1:
                    if count < 1:
                        print(RED + "You must enter at least one income entry." + RESET)
                        continue
                    break
                tax = input(f"Enter tax withheld for income #{count + 1}: ")

                while not validate_value(tax):
                    print(RED + "Invalid input. Please enter a valid number." + RESET)
                    tax = input(f"Enter tax withheld for income #{count + 1}: ")
                    continue
                tax = float(tax.replace(',', ''))
                if tax < 0 or tax > income or income < 0:
                    print(RED + "Invalid input. Tax withheld must be less than or equal to income and both must be non-negative." + RESET)
                    continue
                self.income_data.append((income, tax))
                count += 1



        
    def register(self):
        clear_screen()
        print("=" * 50)
        print(BLUE + "Please enter your credentials to register" + RESET)
        print("=" * 50)
        if (input("Do you have a Tax File Number? (yes/no): ").lower() == 'yes'):
            self.has_tfn = True

        #collect person id
        while 1:
            self.person_id = input("Enter your 6-digit Person ID: ")
            if validate_person_id(self.person_id):
                break
            print(RED+"Invalid Person ID format. Please enter 6 digits."+RESET)


        if self.has_tfn:
            #collect tfn
            while 1:
                self.tfn = input("Enter your 8-digit Tax File Number: ")
                if validate_tfn(self.tfn):
                    break
                print(RED+"Invalid TFN format. Please enter 8 digits."+RESET)

        #collect personal details
        self.first_name = input("Enter your first name: ")
        self.last_name = input("Enter your last name: ")
        
        #collect email
        while 1:
            self.email = input("Enter your email address: ")
            if validate_email(self.email):
                break
            print("Invalid email format. Please try again.")
        

        if(input("Do you have Private Health Insurance Cover? (yes/no): ").lower() == 'yes'):
            self.has_phic = True

        password = input("Enter your password: ")


        if self.server.register(self.person_id, self.tfn, self.first_name, self.last_name, self.email, self.has_phic, password) == True:
            print(GREEN + "Registration successful." + RESET)
            self.is_register = True
        else:
            print(RED + "Registration failed. Please try again." + RESET)
            return False


    def generate_send_data(self):
        return {
            "person_id": self.person_id,
            "tfn": self.tfn,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "has_phic": self.has_phic,
            "income_data": self.income_data
        }

    def send_to_server(self):
        try:
            # print("Sending data to server...")
            response = self.server.estimator(self.generate_send_data())
            return response
        except ConnectionRefusedError:
            print(RED + "Could not connect to the server. Please try again." + RESET)
            return "Could not connect to the server. Please try again."
        except xmlrpc.client.Fault or Exception:
            print(RED + "An error occurred." + RESET)
            return "An error occurred."


def display_results(result): 
    if isinstance(result, str):
        print(RED + result + RESET)
        return False
    print(GREEN + "Tax Return Estimate Results" + RESET)
    # print(f"Annual Taxable Income: ${result['annual_taxable_income']:,.2f}")
    # print(f"Total Tax Withheld: ${result['total_tax_witheld']:,.2f}")
    # print(f"Total Net Income: ${result['total_net_income']:,.2f}")
    # print(f"Medicare Levy: ${result['medicare_levy']:,.2f}")
    # print(f"Tax Liability: ${result['tax_liability']:,.2f}")
    if(result['estimated_tax_refund'] < 0):
        print(GREEN + f"Tax Owed: ${abs(result['estimated_tax_refund']):,.2f}" + RESET)
    else:
        print(GREEN + f"Tax Refund: ${result['estimated_tax_refund']:,.2f}" + RESET)


def main():
    client = TaxClient()
    clear_screen()
    try:
        #connect to server
        client.server = xmlrpc.client.ServerProxy(f"http://{server_ip}:{server_port}/")
        #ping server
        client.server.ping()
    except ConnectionRefusedError:
        print(RED + "Could not connect to the server." + RESET)
        return 
    except xmlrpc.client.Fault or Exception:
        print(RED + "A error occurred." + RESET)
        return
    
    if client.welcome_menu() == False:
        return False
    #send data to server
    if client.is_register:
        return True


    result = client.send_to_server()
    #display results
    if display_results(result) == False:
        return False
    return True


#entry point
if __name__ == "__main__":
    main()

