import sqlite3

def books_info():
    books = []
    conn = sqlite3.connect('./instance/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book')
    books = cursor.fetchall()
    conn.close()
    return books

def find_book(title_or_author):
    print("title_or_author", title_or_author)
    conn = sqlite3.connect('./instance/database.db')
    cursor = conn.cursor()
    
    sql = "SELECT * FROM book WHERE title = ? OR author = ?"
    cursor.execute(sql, (title_or_author, title_or_author))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return result if result else None


def add_favorite(book_id, user_id):
    conn = sqlite3.connect('./instance/database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM favorite_book WHERE book_id = ? AND user_id = ?
    ''', (book_id, user_id))
    result = cursor.fetchone()

    if result is not None:
        print("Favorite already exists")
    else:
        try:
            cursor.execute('''
                INSERT INTO favorite_book (book_id, user_id)
                VALUES (?, ?)
            ''', (book_id, user_id))
            conn.commit()
            print("Favorite added successfully")
        except sqlite3.IntegrityError:
            cursor.execute('''
                UPDATE favorite_book
                SET book_id = ?
                WHERE user_id = ? 
            ''', (book_id, user_id))
            conn.commit()
            print("Favorite updated successfully")
        finally:
            conn.close()



def remove_from_favorite(book_id, user_id):
    conn = sqlite3.connect('./instance/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM favorite_book WHERE book_id = ? AND user_id = ?
    ''', (book_id, user_id))
    result = cursor.fetchone()

    if result is not None:
        try:
            cursor.execute('''
                DELETE FROM favorite_book WHERE book_id = ? AND user_id = ?
            ''', (book_id, user_id))
            conn.commit()
            print("Favorite removed successfully")
        except:
            print("Error removing favorite")
        finally:
            conn.close()
    else:
        print("Favorite doesn't exist")
        conn.close()


def get_favorite_books(user_id):
    conn = sqlite3.connect('./instance/database.db')
    print("user_id", user_id)
    c = conn.cursor()
    c.execute("SELECT book_id FROM favorite_book WHERE user_id=?", (user_id,))
    book_ids = c.fetchall()
    print("book_ids", book_ids)
    favorite_books = []
    for book_id in book_ids:
        c.execute("SELECT * FROM book WHERE id=?", (book_id[0],))
        book_info = c.fetchone()
        favorite_books.append(book_info)
    conn.close()
    print("favorite_books", favorite_books)
    return favorite_books
    