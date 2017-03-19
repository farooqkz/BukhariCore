#!/usr/bin/python3

import sqlite3
import random

class BukhariCore:
    db = None
    dbc = None
    Nars = None
    Books = None
    TotalBooks = None
    
    def __init__(self, db_path="sahih_bukhari.db"):
        self.db = sqlite3.connect(db_path)
        self.dbc = self.db.cursor()

        self.dbc.execute("SELECT * FROM Nars")
        self.Nars = self.dbc.fetchall()
        for i, v in enumerate(self.Nars):
            self.Nars[i] = v[0]

        self.dbc.execute("SELECT * FROM Books")
        self.Books = self.dbc.fetchall()
        for i, v in enumerate(self.Books):
            self.Books[i] = v[0]
        
        self.TotalBooks = 0
        for b in self.Books:
            b = int(b.split()[0].replace('.', ''))
            if b > self.TotalBooks:
                self.TotalBooks = b



    def find_book_by_no(self, book_no):
        try:
            return [b for b in self.Books if b.startswith(str(book_no) + '.')][0]
        except IndexError:
            raise ValueError("Book Number " + str(book_no) + " does not"
                             + "exist.")


    def select_hadith(self, hadith_no, book_no = 0):
        if book_no != 0:
            book_name = self.find_book_by_no(book_no)
            self.dbc.execute("SELECT * FROM \"" + book_name + "\" WHERE info LIKE" +
                "'%Number " + str(hadith_no) + "%'")
            hadith = self.dbc.fetchall()
            if hadith == []:
                raise ValueError("Hadith Number "+ str(hadith_no) + " does not "
                    + "exist(in this book)")
            return hadith[0]
        else:
            result = []
            for b in self.Books:
                self.dbc.execute('SELECT * FROM "' + b + '" WHERE info LIKE' +
                '\'%Number ' + str(hadith_no) +' %\';')
                result += self.dbc.fetchall()
            if result != []:
                return result
            raise ValueError("Hadith Number " + str(hadith_no) + " does not"
                              + " exist")

    def randhadith(self, book_no = 0):
        if book_no == 0:
            book_name = random.choice(self.Books)
        else:
            book_name = self.find_book_by_no(book_no) 
        self.dbc.execute("SELECT * FROM \"" + book_name + "\";")
        return random.choice(self.dbc.fetchall())
    
    def search(self, pattern, book_no = 0, nar = ''):
        result = []
        if book_no == 0:
            for b in self.Books:
                self.dbc.execute("SELECT * FROM \"" + b + "\" WHERE text LIKE '%" +
                    pattern + "%' AND by LIKE '%" + nar + "%'")

                result += self.dbc.fetchall()

        else:
            book_name = self.find_book_by_no(book_no)
            self.dbc.execute("SELECT * FROM \"" + book_name + "\" WHERE text LIKE "
                + "'%" + pattern + "%' AND by LIKE '%" + nar + "%'")
            result += self.dbc.fetchall()

        
        return result

if __name__ == "__main__":
    import sys
    
    if "-h" in sys.argv:
        print("""bukharicore.py [Options] [Commands]
Options:
\t-db <database>\tUse this database instead of ./sahih_bukhari.db
\t-bk <book_no>\tUse this book instead of all books
\t-h\tShow this help message.

Commands:
\tsearch <pattern> \tSearches hadiths for <pattern>, if a book_no
\t\t\t\tusing -bk is mentioned, just searches in that
\t\t\t\tbook.

\trand\t\t\tSelects and shows a random hadith, if book_no
\t\t\t\tusing -bk is mentioned, it choices a random
\t\t\t\thadith from the the mentioned book.

\tselect <hadith_no>\tSelects and shows the hadith number <hadith_no>
\t\t\t\t,if book_no is not mentioned, it searches
\t\t\t\tall the database for the hadith.
        """)
        sys.exit()
    db_path = "sahih_bukhari.db"
    if "-db" in sys.argv:
        db_path = sys.argv[sys.argv.index("-db") + 1]
    b = BukhariCore(db_path)

    if "-bk" in sys.argv:
        book_no = int(sys.argv[sys.argv.index("-bk") + 1])
    else:
        book_no = 0

    if "search" in sys.argv:
        pattern = sys.argv[sys.argv.index("search") + 1]
        results = b.search(pattern, book_no)
        for r in results:
            print(r[0].replace(':', ''))
        sys.exit(0)

    if "select" in sys.argv:
        hadith_no = int(sys.argv[sys.argv.index("select") + 1])
        hadith = b.select_hadith(hadith_no, book_no)
        print(hadith)
        print(hadith[0] + '\n' + hadith[2] + '\n' + hadith[1])
        sys.exit(0)

    if "rand" in sys.argv:
        hadith = b.randhadith(book_no)
        print(hadith[0] + '\n' + hadith[2] + '\n' + hadith[1])
        sys.exit(0)
    
