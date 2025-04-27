from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from typing import Dict, List, Tuple, Optional
import re

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

    def calculate_tax(self, annual_income):
        tax = 0
        for min, max, rate, base in self.tax_rate:
            if annual_income >= min and annual_income <= max:
                tax = base + rate*(annual_income - min-1)
                break
        return tax

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
    

    def calculate_tax_estimate(self, data):
        sum_income = 0
        sum_witheld = 0
        count = 1
        for income, withheld in data["income_data"]:
            sum_income += income
            sum_witheld += withheld
            print(f"Income nr. {count}: {income}, Withheld nr. {count}: {withheld}\n")
            count += 1

        tax = self.calculate_tax(sum_income) + self.calculate_ml(sum_income, data["has_phic"])

        result = {            
            "person_id": data["person_id"],
            "tfn": data["tfn"],
            "annual_taxable_income": round(sum_income,2),
            "total_tax_witheld": round(sum_witheld,2),
            "total_net_income": round(sum_income - tax, 2),
            "estimated_tax_refund": round(sum_witheld - tax, 2),
        }
        return result

def main():
    # Create server
    server = SimpleXMLRPCServer(("localhost", 8000))
    # server.register_introspection_functions()

    # Register the TaxServer instance
    tax_server = TaxServer()
    server.register_instance(tax_server)

    print("Tax Return Estimate Server is running on port 8000...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

if __name__ == "__main__":
    main()