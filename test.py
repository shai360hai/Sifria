import unittest
from library import LibraryDAL
from book import Book
from customer import Customer
from loan import Loan

class TestLibraryDAL(unittest.TestCase):
    def setUp(self):
        self.dal = LibraryDAL(':memory:')  

    def test_add_book(self):
        book = Book('Book1', 'Author1', 2021, 1)
        self.dal.add_book(book)

    def test_add_customer(self):
        customer = Customer('John Doe', 'City1', 30)
        self.dal.add_customer(customer)

    def test_loan_book(self):
        loan = Loan(1, 1, '2023-01-01', '2023-01-10')
        self.dal.loan_book(loan.cust_id, loan.book_id, loan.loandate, loan.returndate)

    def tearDown(self):
        self.dal.close_connection()

if __name__ == '__main__':
    unittest.main()