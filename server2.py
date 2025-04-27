from xmlrpc.server import SimpleXMLRPCServer
import sqlite3


class DatabaseServer:
    def __init__(self):
        self.db_path = "PITD_database.db"

    def get_taxpayer(self, tfn):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PayrollEntry WHERE tfn = ?", (tfn,))
            result = cursor.fetchall()
            conn.close()
            if result:
                income_data = []
                for row in result:
                    income_data.append((row[3], row[4]))            
                return {
                    "tfn": tfn,
                    "income_data": income_data,
                }
            return None
        except sqlite3.Error as e:
            print(f"Error fetching taxpayer data: {e}")
            return None
        
    def ping(self):
        return "Pong"

def main():
    server = SimpleXMLRPCServer(("localhost", 8001))
    print("Database Server is running on localhost, port 8001...")
    db_server = DatabaseServer()
    server.register_instance(db_server)
    # print(db_server.get_taxpayer("12345678"))  # Example TFN for testing
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

if __name__ == "__main__":
    main()