#
# This file includes all shelf classes
#

# SHELF CLASS (PARENT)
class Shelf:
    def __init__(self, title, series, author, publishDate):
        self.title = title
        self.series = series
        self.author = author
        self.publishDate = publishDate

# EBOOK CLASS (Includes ASIN variable [PRIMARY KEY for bookID])
class Ebook(Shelf):
    def __init__(self, asin, title, series, author, publishDate):
        self.asin = asin
        super().__init__(title, series, author, publishDate)

# PHYSICAL CLASS (Includes ISBN variable [PRIMARY KEY for bookID])
class Physical(Shelf):
    def __init__(self, isbn, title, series, author, publishDate):
        self.isbn = isbn
        super().__init__(title, series, author, publishDate)

# READ CLASS (Includes bookID variable [references ASIN & ISBN])
class Read(Shelf):
    def __init__(self, bookID, finishDate, rating, review, title, series, author, publishDate):
        self.bookID = bookID
        self.finishDate = finishDate
        self.rating = rating
        self.review = review
        super().__init__(title, series, author, publishDate)

# CURRENTLY READING CLASS (Includes bookID variable [references ASIN & ISBN])
class CurrReading(Shelf):
    def __init__(self, bookID, startDate, title, series, author, publishDate):
        self.bookID = bookID
        self.startDate = startDate
        super().__init__(title, series, author, publishDate)

# WANT TO READ CLASS (Includes bookID variable [references ASIN & ISBN])
class WantToRead(Shelf):
    def __init__(self, bookID, title, series, author, publishDate):
        self.bookID = bookID
        super().__init__(title, series, author, publishDate)

# CUSTOM SHELF CLASS (decide b/w making a 'custom' var here or in main program code)