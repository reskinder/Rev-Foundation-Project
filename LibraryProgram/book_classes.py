#
# This file includes all book classes
#

# BOOK CLASS (PARENT)
class Book:
    def __init__(self, title, series, author, publishDate):
        self.title = title
        self.series = series
        self.author = author
        self.publishDate = publishDate

# EBOOK CLASS (Includes ASIN variable [PRIMARY KEY for bookID])
class Ebook(Book):
    def __init__(self, asin, title, series, author, publishDate):
        self.asin = asin
        super().__init__(title, series, author, publishDate)

# PHYSICAL CLASS (Includes ISBN variable [PRIMARY KEY for bookID])
class Physical(Book):
    def __init__(self, isbn, title, series, author, publishDate):
        self.isbn = isbn
        super().__init__(title, series, author, publishDate)

# READ CLASS (Includes bookID variable [references ASIN & ISBN])
class DoneReading(Book):
    def __init__(self, bookID, finishDate, rating, review, title, series, author, publishDate):
        self.bookID = bookID
        self.finishDate = finishDate
        self.rating = rating
        self.review = review
        super().__init__(title, series, author, publishDate)

# CURRENTLY READING CLASS (Includes bookID variable [references ASIN & ISBN])
class CurrReading(Book):
    def __init__(self, bookID, startDate, title, series, author, publishDate):
        self.bookID = bookID
        self.startDate = startDate
        super().__init__(title, series, author, publishDate)

# WANT TO READ CLASS (Includes bookID variable [references ASIN & ISBN])
class WantToRead(Book):
    def __init__(self, bookID, title, series, author, publishDate):
        self.bookID = bookID
        super().__init__(title, series, author, publishDate)

# CUSTOM SHELF CLASS (decide b/w making a 'custom' var here or in main program code)