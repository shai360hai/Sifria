
import datetime 
from datetime import date
from library import LibraryDAL
from book import Book
from customer import Customer
from loan import Loan
from db_setup import database

def display_menu():
    print("\n--- Library Management System Menu ---")
    print("1. Add a new customer")
    print("2. Add a new book")
    print("3. Loan a book")
    print("4. Return a book")
    print("5. Display all books")
    print("6. Display all customers")
    print("7. Display all loans")
    print("8. Display late loans")
    print("9. Find book by name")
    print("10. Find customer by name")
    print("11. Remove book")
    print("12. Remove customer")
    print("q. Quit")
    
def main():
    dal = LibraryDAL()
    database()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
#1. Add a new customer
        if choice == '1':
            name = input("Enter customer name: ")
            city = input("Enter customer city: ")
            age = int(input("Enter customer age: "))
            customer = Customer(name, city, age)
            dal.add_customer(customer)
            print("Customer added successfully.")
#2. Add a new book
        elif choice == '2':
            name = input("Enter book name: ")
            author = input("Enter book author: ")
            year_published = int(input("Enter year published: "))
            book_type = int(input("Enter book type (1/2/3): "))
            book = Book(name, author, year_published, book_type)
            dal.add_book(book)
            print("Book added successfully.")
# 3. Loan a book
        elif choice == '3':
            cust_id = int(input("Enter customer ID: "))
            book_id = int(input("Enter book ID: "))
            loandate = date.today()
            print(dal.loan_book(cust_id, book_id, loandate))
#    4. Return a book
        elif choice == '4':
            cust_id = int(input("Enter customer ID: "))
            book_id = int(input("Enter book ID: "))
            print(dal.return_book(cust_id, book_id))
# 5. Display all books
        elif choice == '5':
            all_books = dal.get_all_books()
            if all_books:
                print("\n--- All Books ---")
                for book in all_books:
                        formatted_string = "ID: {}, Name: {}, Author: {}, Year: {}, Book Type: {}".format(*book)
                        print(formatted_string)
            else:
                print("No books available in the library.")
# 6. Display all customers
        elif choice == '6':
            all_customers = dal.get_all_customers()
            if all_customers:
                print("\n--- All Customers ---")
                for customer in all_customers:
                        formatted_string = "ID: {}, Name: {}, city: {}, age: {}".format(*customer)
                        print(formatted_string)
            else:
                print("No customers available in the library.")
# 7. Display all loans
        elif choice == '7':
            all_loans = dal.get_all_loans()
            if all_loans:
                print("\n--- All Loans ---")
                for loan in all_loans:
                    print(f"CustID: {loan.cust_id}, BookID: {loan.book_id}, Loan Date: {loan.loandate}, Return Date: {loan.returndate}")
            else:
                print("No loans available in the library.")
#8. Display late loans
        elif choice == '8':
            all_loans = dal.get_all_loans()
            current_date = date.today()
            late = False
            if all_loans:
                print("\n--- Late Loans ---")
                for loan in all_loans:
                    if (datetime.datetime.strptime(loan.returndate, "%Y-%m-%d").date()) < current_date:
                        print(f"CustID: {loan.cust_id}, BookID: {loan.book_id}, Loan Date: {loan.loandate}, Return Date: {loan.returndate}")
                        late = True
            else:
                print("No loans available in the library.")
            if late is False:
                print("There are no LATE loans in my library")    
            
#9. Find book by name
        elif choice == '9':
            book_name_to_find = input("Enter the name of the book to find: ")
            found_books = dal.find_books_by_name(book_name_to_find)
            if found_books:
                print(f"\n--- Books Found with Name '{book_name_to_find}' ---")
                for book in found_books:
                    formatted_string = "ID: {}, Name: {}, Author: {}, Year: {}, Book Type: {}".format(*book)
                    print(formatted_string)
            else:
                print(f"No books found with the name '{book_name_to_find}'.")
#10. Find customer by name
        elif choice == '10':
            customer_name_to_find = input("Enter the name of the customer to find: ")
            found_customers = dal.find_customers_by_name(customer_name_to_find)
            if found_customers:
                print(f"\n--- Customers Found with Name '{customer_name_to_find}' ---")
                for customer in found_customers:
                        formatted_string = "ID: {}, Name: {}, city: {}, age: {}".format(*customer)
                        print(formatted_string)
            else:
                print(f"No customers found with the name '{customer_name_to_find}'.")
#11. Remove book
        elif choice == '11':
            book_id_to_remove = int(input("Enter the ID of the book to remove: "))
            removed_book = dal.remove_book(book_id_to_remove)
            if removed_book:
                print(f"Book with ID {book_id_to_remove} has been removed.")
            else:
                print(f"No book found with the ID {book_id_to_remove}.")
#12. Remove customer
        elif choice == '12':
            customer_id_to_remove = int(input("Enter the ID of the customer to remove: "))
            removed_customer = dal.remove_customer(customer_id_to_remove)
            if removed_customer:
                print(f"Customer with ID {customer_id_to_remove} has been removed.")
            else:
                print(f"No customer found with the ID {customer_id_to_remove}.")

        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please try again.")
    dal.close_connection()

if __name__ == '__main__':
    main()