import sqlite3

class PostDB:
    def __init__(self, db_name="humbleB.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """게시글 테이블 생성"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            content TEXT,
            date TEXT,
            password TEXT
        )
        """)
        self.conn.commit()

    def add_post(self, title, author, content, date, password):
        """게시글 추가"""
        self.cursor.execute("INSERT INTO posts (title, author, content, date, password) VALUES (?, ?, ?, ?, ?)",
                            (title, author, content, date, password))
        self.conn.commit()

    def get_posts(self):
        """모든 게시글 조회"""
        self.cursor.execute("SELECT id, title, author, content, date FROM posts")
        return self.cursor.fetchall()

    def get_post_by_id(self, post_id):
        """특정 게시글 조회"""
        self.cursor.execute("SELECT id, title, author, content, date FROM posts WHERE id = ?", (post_id,))
        return self.cursor.fetchone()

    def update_post(self, post_id, title, author, content, date, password):
        """게시글 수정 (비밀번호 확인)"""
        self.cursor.execute("SELECT password FROM posts WHERE id = ?", (post_id,))
        stored_password = self.cursor.fetchone()
        
        if stored_password and stored_password[0] == password:
            self.cursor.execute("UPDATE posts SET title=?, author=?, content=?, date=? WHERE id=?",
                                (title, author, content, date, post_id))
            self.conn.commit()
            return True
        return False

    def delete_post(self, post_id, password):
        """게시글 삭제 (비밀번호 확인)"""
        self.cursor.execute("SELECT password FROM posts WHERE id = ?", (post_id,))
        stored_password = self.cursor.fetchone()
        
        if stored_password and stored_password[0] == password:
            self.cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
            self.conn.commit()
            return True
        return False
