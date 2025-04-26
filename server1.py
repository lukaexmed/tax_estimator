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

    def calculate_tax_estimate(self, data: Dict) -> Dict:

        return {"estimate": 0.0, "error": str(e)}

def main():
    # Create server
    server = SimpleXMLRPCServer(("localhost", 8000),
                               requestHandler=SimpleXMLRPCRequestHandler,
                               allow_none=True)
    server.register_introspection_functions()

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