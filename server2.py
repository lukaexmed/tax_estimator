from xmlrpc.server import SimpleXMLRPCServer
import sqlite3


class DatabaseServer:
    def __init__(self):
        self.db_path = "PITD_database.db"

    #query the database for tax info
    def get_taxpayer(self, tfn):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            #query based on tfn
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
            print(f"No tax records found for the person with TFN = {tfn}.")
            return f"No tax records found for the person with TFN = {tfn}."
        except sqlite3.Error as e:
            print(f"Error fetching taxpayer data: {e}")
            return "Error fetching taxpayer data: {e}"
        
    def ping(self):
        return "Pong"
    #register user into the database 
    def register_user(self, person_id, tfn, first_name, last_name, email, has_phic, password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (person_id, tfn, first_name, last_name, email, has_phic, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (person_id, tfn, first_name, last_name, email, has_phic, password))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            print(f"Error registering user: {e}")
            return False
        
    def login_user(self, person_id, password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE person_id = ? AND password = ?", (person_id, password))
            result = cursor.fetchone()
            conn.close()
            if result:
                return result
            else:
                return "User not found or incorrect password."
        except sqlite3.Error as e:
            print(f"Error logging in user: {e}")
            return f"Error logging in user: {e}"

def main():
    server = SimpleXMLRPCServer(("localhost", 8001))
    print("Database server is running on localhost, port 8001...")
    db_server = DatabaseServer()
    server.register_instance(db_server)
    # print(db_server.get_taxpayer("12345678")) #test
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down database server...")
        server.server_close()

if __name__ == "__main__":
    main()