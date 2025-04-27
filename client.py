import random
import re
import xmlrpc.client
from typing import List, Tuple, Dict, Optional


class TaxClient:
    #constructor 
    def __init__(self):
        self.person_id: str = ""
        self.tfn: str = ""
        self.first_name: str = ""
        self.last_name: str = ""
        self.email: str = ""
        self.has_phic: bool = False
        self.has_tfn: bool = False
        self.income_data: List[Tuple[float, float]] = []
        self.server = xmlrpc.client.ServerProxy("http://localhost:8000/")

    #validate the tfn format
    def validate_tfn(self, tfn):
        return bool(re.match('^[0-9]{8}$', tfn))

    #validate the person id format
    def validate_person_id(self, person_id):
        return bool(re.match('^[0-9]{6}$', person_id))
    
    #validate the email format
    def validate_email(self, email):
        return bool(re.match('^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$', email))

    def collect_user_data(self):
        #ask for TFN
        if (input("Do you have a Tax File Number? (yes/no): ").lower() == 'yes'):
            self.has_tfn = True

        #collect person id
        while 1:
            self.person_id = input("Enter your 6-digit Person ID: ")
            if self.validate_person_id(self.person_id):
                break
            print("Invalid Person ID format. Please enter 6 digits.")

        if self.has_tfn:
            #collect tfn
            while 1:
                self.tfn = input("Enter your 8-digit Tax File Number: ")
                if self.validate_tfn(self.tfn):
                    break
                print("Invalid TFN format. Please enter 8 digits.")

            #collect personal details
            self.first_name = input("Enter your first name: ")
            self.last_name = input("Enter your last name: ")
            
            #collect email
            while 1:
                self.email = input("Enter your email address: ")
                if self.validate_email(self.email):
                    break
                print("Invalid email format. Please try again.")
        else:
            #collect income data
            print("Enter your biweekly income data (1-26 entries):")
            count = 0
            while count < 26:
                income = float(input(f"Enter taxable income #{count + 1} (or -1 to finish): "))
                if income == -1:
                    if count < 1:
                        print("You must enter at least one income entry.")
                        continue
                    break
                tax = float(input(f"Enter tax withheld for income #{count + 1}: "))
                if tax < 0 or tax > income or income < 0:
                    print("Invalid input. Tax withheld must be less than or equal to income and both must be non-negative.")
                    continue
                self.income_data.append((income, tax))
                count += 1

        #private health insurance cover

        if(input("Do you have Private Health Insurance Cover? (yes/no): ").lower() == 'yes'):
            self.has_phic = True

    def empty_return_data(self):
        return {
            "person_id": "",
            "tfn": "",
            "annual_taxable_income": 0.0,
            "total_tax_witheld": 0.0,
            "total_net_income": 0.0,
            "estimated_tax_refund": 0.0
        }
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
            print("Sending data to server...")
            response = self.server.calculate_tax_estimate(self.generate_send_data())
            return response
        except ConnectionRefusedError:
            print("Could not connect to the server.")
            return self.empty_return_data()
        except xmlrpc.client.Fault or Exception:
            print("A error occurred.")
            return self.empty_return_data()


    def run(self):
        print("Welcome to the Personal Income Tax Return Estimate (PITRE) System")
        try:
            #connect to server
            print("Connecting to server...")
            self.server = xmlrpc.client.ServerProxy("http://localhost:8000/")
            #ping server
            self.server.ping()
            print("Connected to server.")
        except ConnectionRefusedError:
            print("Could not connect to the server.")
            return
        except xmlrpc.client.Fault or Exception:
            print("A error occurred.")
            return
        #collect user data
        self.collect_user_data()

        #send data to server
        result = self.send_to_server()
        #display results
        print("\nTax Return Estimate Results:")
        print(f"Annual Taxable Income: ${result['annual_taxable_income']:,.2f}")
        # print(f"Total Tax Withheld: ${result['total_tax_witheld']:,.2f}")
        # print(f"Total Net Income: ${result['total_net_income']:,.2f}")
        # print(f"Estimated Tax Refund: ${result['estimated_tax_refund']:,.2f}")


def main():
    client = TaxClient()
    client.run()

#entry point
if __name__ == "__main__":
    main()
