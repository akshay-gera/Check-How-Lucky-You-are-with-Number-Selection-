import pyodbc
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                    'Server=LAPTOP-R24KKR36;'
                    'Database=AkshayGeraGuessingStats;'
                    'Trusted_Connection=yes;')

cursor = conn.cursor()

print('Connected to database')

cursor.execute('''
        CREATE TABLE GuessStats(
            GameSessionNumber int,
            GamePlayNumber int,
            Guess int,
            SeekNumber int,
            Match int,
            PointsScored int
            PRIMARY KEY(GameSessionNumber,GamePlayNumber)
        )
            ''')

conn.commit()
print('GuessStats Table Created')