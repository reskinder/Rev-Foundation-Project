## Project Proposal
#### Note: Final project will be a little different based on changes made during development; for updated info see file "Project Summary Info"

For my project, I will be using Python & MySQL and will make a library of books I've read that will be separated into five tables: 
ebook, physical, child, tweens-teens, and adult. Ebook will contain 51 books, physical will contain 217 books, child (age 6 - 9) will 
contain 97 books, tweens-teens (age 10 - 17) will contain 57 books, and adult (age 18+) will contain 114 books for a total of 268 books. 
The first two tables (ebook & physical) will have the main primary keys (ASIN/ISBN respectively) and will be referenced by the other tables 
with foreign keys.  

The columns will include book ID (ASIN/ISBN), title, author, publish date, read date, genre, and rating (out of five stars). 
The ebook and physical tables will only include book ID, title, and author. I will be able to create records of new books I’ve read, 
update any records (e.g. rating), and delete any records if need be.
