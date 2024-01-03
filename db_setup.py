import sqlite3

def database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            Id INTEGER PRIMARY KEY,
            Name TEXT,
            Author TEXT,
            Year_Published INTEGER,
            Type INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            Id INTEGER PRIMARY KEY,
            Name TEXT,
            City TEXT,
            Age INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Loans (
            CustID INTEGER,
            BookID INTEGER,
            Loandate TEXT,
            Returndate TEXT,
            FOREIGN KEY (CustID) REFERENCES Customers(Id),
            FOREIGN KEY (BookID) REFERENCES Books(Id)
        )
    ''')

    conn.commit()
    conn.close()