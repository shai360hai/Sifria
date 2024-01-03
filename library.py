from datetime import timedelta, datetime
import sqlite3
from book import Book
from customer import Customer
from loan import Loan

class LibraryDAL:
    def __init__(self, db_path='library.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.db_file = db_path
        
    def add_book(self, book):
        self.cursor.execute('''
            INSERT INTO Books (Name, Author, Year_Published, Type)
            VALUES (?, ?, ?, ?)
        ''', (book.name, book.author, book.year_published, book.type))
        self.conn.commit()

    def add_customer(self, customer):
        self.cursor.execute('''
            INSERT INTO Customers (Name, City, Age)
            VALUES (?, ?, ?)
        ''', (customer.name, customer.city, customer.age))
        self.conn.commit()
        
    def get_book_type_by_id(self, book_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT type FROM Books WHERE id=?", (book_id,))
            book_type_data = cursor.fetchone()
            if book_type_data:
                return book_type_data[0]  
            else:
                return None
            
    def loan_book(self, cust_id, book_id, loandate, return_date=None):
            if self.is_book_rented(book_id):
                return "Book is already rented."

            book_type = self.get_book_type_by_id(book_id)
            if book_type:
                if book_type == 1:
                    return_date = loandate + timedelta(days=10)
                elif book_type == 2:
                    return_date = loandate + timedelta(days=5)
                elif book_type == 3:
                    return_date = loandate + timedelta(days=2)
                print(f"return date is :{return_date}")
                self.cursor.execute('''
                    INSERT INTO Loans (CustID, BookID, Loandate, Returndate)
                    VALUES (?, ?, ?, ?)
                ''', (cust_id, book_id, loandate, return_date))
                self.conn.commit()
                return f"Book with ID {book_id} has been loaned. Return date: {return_date}"
            return "Book type not found."

    def is_book_rented(self, book_id):
            self.cursor.execute("SELECT COUNT(*) FROM Loans WHERE BookID=? ", (book_id,))
            result = self.cursor.fetchone()[0]
            return result > 0
  
    def return_book(self, cust_id, book_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Loans WHERE CustID=? AND BookID=? ", (cust_id, book_id))
            loan_data = cursor.fetchone()
            if loan_data:
                book_type = self.get_book_type_by_id(book_id)
                if book_type is not None:
                    if book_type == 1:
                        max_loan_days = 10
                    elif book_type == 2:
                        max_loan_days = 5
                    elif book_type == 3:
                        max_loan_days = 2
                    else:
                        raise ValueError("Invalid book type.")

                    return_date = (datetime.now() + timedelta(days=max_loan_days)).strftime("%Y-%m-%d")

                    cursor.execute("DELETE FROM Loans WHERE CustID=? AND BookID=?", (cust_id, book_id))
                    conn.commit()
                    return f"Book with ID {book_id} has been returned. Actual return date: {return_date}"
                else:
                    return f"Book with ID {book_id} not found."
            return f"Loan not found for customer with ID {cust_id} and book with ID {book_id}."
    
    def get_all_books(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, author, year_published, type FROM Books")
            books_data = cursor.fetchall()
        return books_data
    
    def get_all_customers(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, city, age FROM Customers")
            customers_data = cursor.fetchall()
        return customers_data

    def get_all_loans(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Loans")
            loans_data = cursor.fetchall()
            loans = [Loan(*row) for row in loans_data]
        return loans    

    def find_books_by_name(self, book_name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, author, year_published, type FROM Books WHERE name LIKE ?", ('%' + book_name + '%',))
            books_data = cursor.fetchall()
            # books = [Book(*row) for row in books_data]
        return books_data

    def find_customers_by_name(self, customer_name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, city, age FROM Customers WHERE name LIKE ?", ('%' + customer_name + '%',))
            customers_data = cursor.fetchall()
            # customers = [Customer(*row) for row in customers_data]
        return customers_data

    def remove_book(self, book_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Books WHERE id=?", (book_id,))
            book_data = cursor.fetchone()
            if book_data:
                cursor.execute("DELETE FROM Books WHERE id=?", (book_id,))
                conn.commit()
                return True  
            else:
                return False  
            
    def remove_customer(self, customer_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Customers WHERE id=?", (customer_id,))
            customer_data = cursor.fetchone()
            if customer_data:
                cursor.execute("DELETE FROM Customers WHERE id=?", (customer_id,))
                conn.commit()
                return True  
            else:
                return False  
            
    def close_connection(self):
            self.conn.close()