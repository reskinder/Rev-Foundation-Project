## Possible Changes
- Might do 4 tables instead (ebook, physical, read, currently reading) since all timeline tables basically have the same columns
  - Ask Jacob to see what he thinks

## Project Summary Info
Project: A library of books I've read and am currently reading using Python & MySQL

- Tables
  - Ebook -- 51 books
  - Physical -- 217 books
  - Currently Reading -- 2 books (might add more later)
  - Child (6 - 9) -- 97 books
  - Tweens-Teens (10 - 17) -- 57 books
  - Adult (18+) -- 114 books

- Columns
  - Ebook
    - ASIN (book ID for ebooks) -- PRIMARY KEY
    - Title
    - Author
  - Physical
    - ISBN (book ID for physical books) -- PRIMARY KEY
    - Title
    - Author
  - Currently Reading
    - book ID -- FOREIGN KEY (references Ebooks & Physical)
    - Title
    - Author
  - Childhood
    - book ID -- FOREIGN KEY (references Ebooks & Physical)
    - Title
    - Author
    - Publish Date
    - Finished Reading Date
    - Genre
    - Rating (1 - 5)
  - Tweens-Teens
    - book ID -- FOREIGN KEY (references Ebooks & Physical)
    - Title
    - Author
    - Publish Date
    - Finished Reading Date
    - Genre
    - Rating (1 - 5)
  - Adult
    - book ID -- FOREIGN KEY (references Ebooks & Physical)
    - Title
    - Author
    - Publish Date
    - Finished Reading Date
    - Genre
    - Rating (1 - 5)
