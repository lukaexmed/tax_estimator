from xmlrpc.server import SimpleXMLRPCServer


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
                print(f"{tax} = {base} + {rate} * ({annual_income} - {min} + 1)")
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
        sum_income = 0
        sum_witheld = 0
        count = 1
        #iterate through income data for and calculate the total income and tax withheld
        for income, withheld in data["income_data"]:
            sum_income += income
            sum_witheld += withheld
            print(f"Income #{count}: {income}, Withheld #{count}: {withheld}\n")
            count += 1

        #calculate tax and medicare levy
        tax = self.calculate_tax(sum_income)
        medicare = self.calculate_ml(sum_income, data["has_phic"])

        result = {            
            "person_id": data["person_id"],
            "tfn": data["tfn"],
            "annual_taxable_income": round(sum_income,2),
            "total_tax_witheld": round(sum_witheld,2),
            "total_net_income": round(sum_income - tax - medicare, 2),
            "medicare_levy": round(medicare, 2),
            "tax_liability": round(tax, 2),
            "estimated_tax_refund": round(sum_witheld - tax - medicare, 2),
        }
        return result

def main():
    #create server
    server = SimpleXMLRPCServer(("localhost", 8000))
    #create instance of the server and register it
    tax_server = TaxServer()
    server.register_instance(tax_server)

    print("Tax Return Estimate Server is running on localhost, port 8000...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

if __name__ == "__main__":
    main()