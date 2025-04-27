from xmlrpc.server import SimpleXMLRPCServer
import sqlite3


class DatabaseServer:
    def __init__(self):
        self.db_path = "PITD_database.db"
        self.init_db()
        self.taxpayer1 = [
            (1, 2412.00, 515.12, 1896.88),
            (2, 2412.00, 515.12, 1896.88),
            (3, 2412.00, 515.12, 1896.88),
            (4, 2412.00, 515.12, 1896.88),
            (5, 2412.00, 515.12, 1896.88),
            (6, 2412.00, 515.12, 1896.88),
            (7, 2412.00, 515.12, 1896.88),
            (8, 2412.00, 515.12, 1896.88),
            (9, 2412.00, 515.12, 1896.88),
            (10, 2412.00, 515.12, 1896.88),
            (11, 2412.00, 515.12, 1896.88),
            (12, 2412.00, 515.12, 1896.88),
            (13, 2412.00, 515.12, 1896.88),
            (14, 2412.00, 515.12, 1896.88),
            (15, 2412.00, 515.12, 1896.88),
            (16, 2412.00, 515.12, 1896.88),
            (17, 2412.00, 515.12, 1896.88),
            (18, 2412.00, 515.12, 1896.88),
            (19, 2412.00, 515.12, 1896.88),
            (20, 2412.00, 515.12, 1896.88),
            (21, 2412.00, 515.12, 1896.88),
            (22, 2412.00, 515.12, 1896.88),
            (23, 2412.00, 515.12, 1896.88),
            (24, 2412.00, 515.12, 1896.88),
            (25, 2412.00, 515.12, 1896.88),
        ]
        self.taxpayer2 = [
            (1, 2418.82, 506.50, 1821.89),
            (2, 2521.14, 537.41, 1955.58),
            (3, 2288.67, 479.57, 1773.01),
            (4, 2364.01, 502.60, 1833.14),
            (5, 2155.84, 451.03, 1689.00),
            (6, 2398.17, 509.41, 1856.78),
            (7, 2487.59, 521.48, 1921.84),
            (8, 2310.11, 482.85, 1792.52),
            (9, 2244.63, 469.20, 1741.20),
            (10, 2331.88, 490.38, 1807.45),
            (11, 2465.76, 516.52, 1904.25),
            (12, 2199.98, 460.20, 1713.19),
            (13, 2376.37, 500.36, 1846.62),
            (14, 2443.59, 512.09, 1887.93),
            (15, 2509.80, 526.90, 1945.59),
            (16, 2277.43, 477.55, 1763.69),
            (17, 2352.77, 498.33, 1824.84),
            (18, 2407.41, 505.04, 1866.33),
            (19, 2223.39, 465.14, 1724.76),
            (20, 2477.00, 523.61, 1913.95),
            (21, 2300.87, 481.24, 1785.24),
            (22, 2532.38, 531.84, 1965.10),
            (23, 2294.75, 480.23, 1780.43),
            (24, 2454.83, 514.88, 1896.20),
            (25, 2387.93, 503.78, 1850.89),
            (26, 2434.27, 507.50, 1880.60)
        ]   

    def init_db(self):
        """Initialize the SQLite database and create the table if it doesn't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Taxpayers ( 
                    tfn TEXT PRIMARY KEY UNIQUE
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS PayrollEntry ( 
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tfn TEXT,
                    pay_period_number INTEGER, 
                    taxable_wage REAL,
                    tax_witholdings REAL, 
                    net_wage REAL,
                    UNIQUE(tfn, pay_period_number),
                    FOREIGN KEY (tfn) REFERENCES Taxpayers(tfn)
                )
            ''')
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()


    def add_taxpayer(self, db_path, tfn, payroll_data):
        """Add a taxpayer to the database."""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            conn.execute('BEGIN')
            cursor.execute("INSERT INTO Taxpayers (tfn) VALUES (?)", (tfn,))

            payroll_data_with_tfn = [(tfn, *data) for data in payroll_data]
            cursor.executemany("INSERT INTO PayrollEntry (tfn, pay_period_number, taxable_wage, tax_witholdings, net_wage) VALUES (?, ?, ?, ?, ?)", payroll_data_with_tfn)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"An error occurred: {e}")
        finally:
            conn.close()


def main():
    # server = SimpleXMLRPCServer(("localhost", 8001))
    db_server = DatabaseServer()
    db_server.add_taxpayer(db_server.db_path, "12345678", db_server.taxpayer1)
    db_server.add_taxpayer(db_server.db_path, "87654321", db_server.taxpayer2)
    print("Taxpayers added successfully.")
    # server.register_instance(db_server)
    # print("Database Server is running on localhost, port 8001...")
    
    # try:
    #     server.serve_forever()
    # except KeyboardInterrupt:
    #     print("\nShutting down server...")
    #     server.server_close()

if __name__ == "__main__":
    main()