import pyodbc
from datetime import date

class BookingManager:
    def __init__(self):

        # connect to  DB
        self.server = "ldaijiw-micro.cdix33vx1qyf.eu-west-2.rds.amazonaws.com"
        self.database = "test_database"
        self.username = "ldaijiw"
        self.password = "DreamJLMSU743"

        self.start_connection()


    def start_connection(self):
        # server name, DB name, username, and password are required to connect with pyodbc
        try:
            self.db_connection = pyodbc.connect(
                f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
            )
            self.cursor = self.db_connection.cursor()
        except (ConnectionError, pyodbc.OperationalError, pyodbc.DatabaseError):
            return "Connection Unsuccessful"
        
        else:
            return "Connection Successful"

        



    
    # TABLES: TICKET DETAILS, FLIGHT TRIP, PASSENGERS
    # INPUT: FLIGHT TRIP ID, LIST OF PASSENGER ID
    def make_booking(self, flight_trip_id, passenger_id_list):

        # Check flight_trip_id is valid
        flight_trip_exists = True if self.cursor.execute(f"SELECT COUNT(*) FROM FlightTrip WHERE FlightTrip_id = {flight_trip_id}").fetchone()[0] == 1 else False
        if not flight_trip_exists:
            return "INVALID FLIGHT TRIP ID"

        # Check passenger_id is valid
        for passenger_id in passenger_id_list:
            passenger_id_exists = True if self.cursor.execute(f"SELECT COUNT(*) FROM Passengers WHERE Passenger_id = {passenger_id}").fetchone()[0] == 1 else False
            if not passenger_id_exists:
                return "INVALID PASSENGER ID"


        # CHECK HOW MANY SEATS THEY WILL NEED (BABY?)
        passenger_discounts = []
        passengers_need_seat = []
        for passenger_id in passenger_id_list:
            passenger_dob = self.cursor.execute(f'''
            SELECT
            DateOfBirth
            FROM Passengers
            WHERE Passenger_id = {passenger_id}
            ''').fetchone()[0]

            passenger_age = (date.today() - passenger_dob).days // 365

            # CHECK IF THEY'RE ELIGIBLE FOR DISCOUNT
            passenger_discounts.append(1 if passenger_age < 18 else 0)
            # Check if they need a seat
            passengers_need_seat.append(True if passenger_age > 1 else False)

        # Calculate total seats required
        seats_required = sum(passengers_need_seat)
        
        # CHECK THAT SEATS ARE AVAILABLE
        seats_available = self.cursor.execute(f'''
        SELECT AvailableSeats
        FROM FlightTrip
        WHERE FlightTrip_id = {flight_trip_id}
        ''').fetchone()[0]

        # IF SEATS ARE NOT AVAILABLE THEN RETURN: NOT AVAILABLE
        if seats_available < seats_required:
            return "NOT AVAILABLE"
        
        # OTHERWISE UPDATE NUMBER OF SEATS AVAILABLE
        self.cursor.execute(f'''
        UPDATE FlightTrip
        SET AvailableSeats = {seats_available - seats_required}
        WHERE FlightTrip_id = {flight_trip_id}
        ''')
        self.db_connection.commit()
        
        # FOR EACH PASSENGER
        # ADD COST OF TICKET TO TICKET DETAILS
        # retrieve ticket price and ticket discount from flight trip table
        ticket_price = self.cursor.execute(f'''
        SELECT TicketPrice
        FROM FlightTrip
        WHERE FlightTrip_id = {flight_trip_id}
        ''').fetchone()[0]

        ticket_discount = self.cursor.execute(f'''
        SELECT TicketDiscount
        FROM FlightTrip
        WHERE FlightTrip_id = {flight_trip_id}
        ''').fetchone()[0]

        # calculate passenger prices to pay after considering if they're eligible for discount
        passenger_prices = [ticket_price - (ticket_price * ticket_discount * passenger_discount) for passenger_discount in passenger_discounts]

        # ADD FLIGHT TRIP ID/PASSENGER ID TO TICKET DETAILS TABLE
        ticket_id_list = []
        for i, passenger_id in enumerate(passenger_id_list):
            self.cursor.execute(f'''
            INSERT INTO TicketDetails (Passenger_id, FlightTrip_id, PricePaid)
            VALUES({passenger_id}, {flight_trip_id}, {passenger_prices[i]})
            ''')
            self.db_connection.commit()

            # retrieve ticket id and append to list
            ticket_id = self.cursor.execute(f'''
            SELECT Ticket_id
            FROM TicketDetails
            WHERE Passenger_id = {passenger_id}
            ''').fetchone()[0]

            ticket_id_list.append(ticket_id)

        # RETURN: TICKET ID, COST OF TICKET (ANY DISCOUNT APPLIED), EXTRA FLIGHT DETAILS

        ticket_info_dict = {ticket_id: passenger_prices[i] for i, ticket_id in enumerate(ticket_id_list)}

        return ticket_info_dict


    def test(self):
        # self.cursor.execute('''
        # CREATE TABLE [Passengers] (
        # [Passenger_id] INT IDENTITY(1,1) NOT NULL,
        # [PassportNumber] VARCHAR(9) NOT NULL,
        # [FirstName] VARCHAR(32) NOT NULL,
        # [LastName] VARCHAR(32) NOT NULL,
        # [DateOfBirth] DATE NOT NULL,
        # PRIMARY KEY ([Passenger_id]) 
        # );
        # ''')
        # self.db_connection.commit()

        # table_info = self.cursor.execute('''
        # SELECT
        # TABLE_NAME,
        # COLUMN_NAME
        # FROM INFORMATION_SCHEMA.COLUMNS
        # WHERE TABLE_NAME = 'Passengers';
        # ''').fetchall()
        # print(table_info)

        # insert_data_query = "INSERT INTO Passengers\n(PassportNumber, FirstName, LastName, DateOfBirth)\nVALUES('ABC123456', 'Leo', 'Waltmann', '1999-07-13');"

        # self.cursor.execute(insert_data_query)
        
        # insert_data_query = "INSERT INTO Passengers\n(PassportNumber, FirstName, LastName, DateOfBirth)\nVALUES('ABC123456', 'Oscar', 'Olive', '2010-01-12');"

        # self.cursor.execute(insert_data_query)
        
        # insert_data_query = "INSERT INTO Passengers\n(PassportNumber, FirstName, LastName, DateOfBirth)\nVALUES('ABC123456', 'Ben', 'Button', '2019-10-13');"

        # self.cursor.execute(insert_data_query)
        # print(list(self.cursor.execute('''
        # SELECT sp.name, sp.default_database_name
        # FROM sys.server_principals sp
        # WHERE sp.name = SUSER_SNAME();
        # ''')))
        #self.cursor.execute("USE test_db;")
        print(self.cursor.execute("SELECT * FROM FlightTrip;").fetchall())
        #self.db_connection.commit()

if __name__ == "__main__":
    new_bm = BookingManager()
    new_bm.test()
    #new_bm.make_booking(1, [1, 2, 3])