import random
import re
import xmlrpc.client
from typing import List, Tuple
import os
import time


CURSOR = '\033[1A'
CLEAR = '\x1b[2K'
CLEAR_LINE = CURSOR + CLEAR
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

def clear_line():
    print(CLEAR_LINE, end='')

def clear_screen():
    os.system('cls||clear') #clear the scr for unix or windows



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

    #validate the tfn format
    def validate_tfn(self, tfn):
        return bool(re.match('^[0-9]{8}$', tfn))

    #validate the person id format
    def validate_person_id(self, person_id):
        return bool(re.match('^[0-9]{6}$', person_id))
    
    #validate the email format
    def validate_email(self, email):
        return bool(re.match('^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$', email))
    
    def validate_value(self, value):
        return bool(re.match('^[0-9,.-]+$', value))

    def collect_user_data(self):
        #ask for TFN
        if (input("Do you have a Tax File Number? (yes/no): ").lower() == 'yes'):
            self.has_tfn = True

        #collect person id
        while 1:
            self.person_id = input("Enter your 6-digit Person ID: ")
            if self.validate_person_id(self.person_id):
                break
            print(RED+"Invalid Person ID format. Please enter 6 digits."+RESET)


        if self.has_tfn:
            #collect tfn
            while 1:
                self.tfn = input("Enter your 8-digit Tax File Number: ")
                if self.validate_tfn(self.tfn):
                    break
                print(RED+"Invalid TFN format. Please enter 8 digits."+RESET)

            # #collect personal details
            # self.first_name = input("Enter your first name: ")
            # self.last_name = input("Enter your last name: ")
            
            # #collect email
            # while 1:
            #     self.email = input("Enter your email address: ")
            #     if self.validate_email(self.email):
            #         break
            #     print("Invalid email format. Please try again.")
        else:
            #collect income data
            print("Enter your biweekly income data (1-26 entries):")
            count = 0
            while count < 26:
                income = input(f"Enter taxable income #{count + 1} (or -1 to finish): ")
                if not self.validate_value(income):
                    print(RED + "Invalid input. Please enter a valid number." + RESET)
                    continue
                income = float(income.replace(',', ''))
                if income == -1:
                    if count < 1:
                        print(RED + "You must enter at least one income entry." + RESET)
                        continue
                    break
                tax = input(f"Enter tax withheld for income #{count + 1}: ")

                while not self.validate_value(tax):
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
    clear_screen()
    print(BLUE + "Welcome to the Personal Income Tax Return Estimate (PITRE) System" + RESET)
    if isinstance(result, str):
        print(RED + result + RESET)
        return
    print(GREEN + "Tax Return Estimate Results:" + RESET)
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
    print(BLUE + "Welcome to the Personal Income Tax Return Estimate (PITRE) System" + RESET)
    try:
        #connect to server
        client.server = xmlrpc.client.ServerProxy("http://localhost:8000/")
        #ping server
        client.server.ping()
    except ConnectionRefusedError:
        print(RED + "Could not connect to the server." + RESET)
        return
    except xmlrpc.client.Fault or Exception:
        print(RED + "A error occurred." + RESET)
        return
    
    #collect user data
    client.collect_user_data()
    #send data to server
    result = client.send_to_server()
    #display results
    display_results(result)


#entry point
if __name__ == "__main__":
    main()
