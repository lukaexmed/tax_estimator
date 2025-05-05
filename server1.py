from time import sleep
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

my_ip="localhost"
my_port=8000
data_ip="localhost"
data_port=8001

class TaxServer:
    def __init__(self):
        self.tax_rate = [
            (0, 18200, 0, 0),
            (18201, 45000, 0.19, 0),
            (45001, 120000, 0.325, 5092),
            (120001, 180000, 0.37, 29467),
            (180001, float('inf'), 0.45, 51667)
        ]
        self.mls = [
            (0, 90000, 0.02),
            (90001, 105000, 0.01),
            (105001, 140000, 0.0125),
            (140001, float('inf'), 0.015)
        ]
        self.ml = 0.02

    #calculate tax based on the tax rate
    def calculate_tax(self, annual_income):
        tax = 0
        for min, max, rate, base in self.tax_rate:
            if annual_income >= min and annual_income <= max:
                tax = base + rate*(annual_income - min + 1)
                #print(f"{tax} = {base} + {rate} * ({annual_income} - {min} + 1)")
                break
        return tax

    #calculate medicare levy based on the income and if the person has private health insurance
    def calculate_ml(self, annual_income, has_phic):
        medicare = annual_income * self.ml
        if not has_phic:
            for min, max, rate in self.mls:
                if annual_income >= min and annual_income <= max:
                    medicare += annual_income * rate
                    break
        return medicare
    
    def ping(self):
        return "Pong"
    

    def estimator(self, data):
        sum_taxable_income = 0
        sum_witheld = 0
        count = 1
        if data["tfn"] != "":
            income_data = self.fetch_PITD(data["tfn"])
            if isinstance(income_data, str):
                return income_data #return the error message
            income_data = income_data["income_data"]
            tfn = data["tfn"]
        else:
            tfn = "No TFN"
            income_data = data["income_data"] #income data suoplied by the user

        #iterate through income data for and calculate the total income and tax withheld
        for income, withheld in income_data:
            sum_taxable_income += income
            sum_witheld += withheld
            print(f"Income #{count}: {income}, Withheld #{count}: {withheld}\n") #logging
            count += 1

        #calculate tax and medicare levy
        tax = self.calculate_tax(sum_taxable_income)
        medicare = self.calculate_ml(sum_taxable_income, data["has_phic"])

        return {            
            "person_id": data["person_id"],
            "tfn": tfn,
            "annual_taxable_income": round(sum_taxable_income,2),
            "total_tax_witheld": round(sum_witheld,2),
            "total_net_income": round(sum_taxable_income - tax - medicare, 2),
            # "medicare": round(medicare, 2),
            # "tax": round(tax, 2),
            "estimated_tax_refund": round(sum_witheld - tax - medicare, 2),
        }
    
    def fetch_PITD(self, tfn):
        try:
            #connect to database server
            print("Connecting to database server...")
            db_server = xmlrpc.client.ServerProxy(f"http://{data_ip}:{data_port}/")
            #ping server
            db_server.ping()
            print("Connected to database server.")
        except ConnectionRefusedError:
            print("Could not connect to the database server.")
            return "Could not connect to the database server."
        except (xmlrpc.client.Fault, Exception):
            print("An error occurred.")
            return "An error occurred."
        
        tfn_data = db_server.get_taxpayer(tfn)
        return tfn_data
    
    def login(self, person_id, password):
        try:
            #connect to database server
            print("Connecting to database server...")
            db_server = xmlrpc.client.ServerProxy(f"http://{data_ip}:{data_port}/")
            #ping server
            db_server.ping()
            print("Connected to database server.")
        except ConnectionRefusedError:
            print("Could not connect to the database server.")
            return "Could not connect to the database server."
        except (xmlrpc.client.Fault, Exception):
            print("An error occurred.")
            return "An error occurred."
        
        user = db_server.login_user(person_id, password)
        return user

    def register(self, person_id, tfn, first_name, last_name, email, has_phic, password):
        try:
            #connect to database server
            print("Connecting to database server...")
            db_server = xmlrpc.client.ServerProxy(f"http://{data_ip}:{data_port}/")
            #ping server
            db_server.ping()
            print("Connected to database server.")
        except ConnectionRefusedError:
            print("Could not connect to the database server.")
            return "Could not connect to the database server."
        except (xmlrpc.client.Fault, Exception):
            print("An error occurred.")
            return "An error occurred."
        
        user = db_server.register_user(person_id, tfn, first_name, last_name, email, has_phic, password)
        return user

def main():
    #create server
    server = SimpleXMLRPCServer((my_ip, my_port))
    #create instance of the server and register it
    tax_server = TaxServer()
    server.register_instance(tax_server)

    print(f"Tax Return Estimate Server is running on {my_ip}, port {my_port}...")
        
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

if __name__ == "__main__":
    main()