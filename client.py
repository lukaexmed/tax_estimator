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
        # self.result: Optional[Dict[str, float]] = None
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
        has_tfn = input("Do you have a Tax File Number? (yes/no): ").lower() == 'yes'

        #collect person id
        while 1:
            self.person_id = input("Enter your 6-digit Person ID: ")
            if self.validate_person_id(self.person_id):
                break
            print("Invalid Person ID format. Please enter 6 digits.")

        if has_tfn:
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
            print("\nEnter your biweekly income data (1-26 entries):")
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
        self.has_phic = input("Do you have Private Health Insurance Cover? (yes/no): ").lower() == 'yes'

    def send_to_server(self):
        """Placeholder for RPC call to server."""
        # TODO: Implement actual RPC call
        data = {
            "person_id": self.person_id,
            "tfn": self.tfn,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "has_phic": self.has_phic,
            "income_data": self.income_data
        }
        
        # Placeholder for RPC call
        print("Sending data to server...")
        return {"estimate": 0.0}  # Placeholder response

    def run(self):
        print("Welcome to the Personal Income Tax Return Estimate (PITRE) System")
        self.collect_user_data()
        
        #send data to server
        result = self.send_to_server()
        
        #display results
        print("\nTax Return Estimate Results:")
        print(f"Estimated tax return: ${result['estimate']:.2f}")


def main():
    client = TaxClient()
    client.run()

#entry point
if __name__ == "__main__":
    main()
