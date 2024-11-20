import sqlite3

# Database setup
def setup_database():
    """Create required tables in the database."""
    conn = sqlite3.connect('quizapp.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    # Create scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            username TEXT,
            score INTEGER,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    """)

    # Create quiz questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)

    # Add sample questions (if not already present)
    cursor.execute("SELECT COUNT(*) FROM questions")
    if cursor.fetchone()[0] == 0:  # Add only if empty
        sample_questions = [
            ("Which SQL keyword is used to retrieve unique values from a column?", "A. DISTINCT", "B. UNIQUE", "C. FILTER", "D. EXCLUSIVE", "A"),
            ("What is the purpose of the SQL GROUP BY clause?", "A. To arrange records in ascending order", "B. To filter records by criteria", "C. To group rows with the same values", "D. To delete duplicate rows", "C"),
        ]
        cursor.executemany("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_questions)

    conn.commit()
    conn.close()

# Functionality
def register():
    """Register a new user."""
    conn = sqlite3.connect('quizapp.db')
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please try a different one.")
    finally:
        conn.close()

def login():
    """Log in an existing user."""
    conn = sqlite3.connect('quizapp.db')
    cursor = conn.cursor()

    username = input("Enter Username: ")
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        for _ in range(3):
            password = input("Enter Password: ")
            if password == result[0]:
                print("Login successful!")
                conn.close()
                return username
            else:
                print("Incorrect password. Try again.")
        print("Maximum attempts exceeded.")
    else:
        print("Username not found. Please register first.")
    conn.close()
    return None

def attempt_quiz(username):
    """Attempt the quiz and save the score."""
    conn = sqlite3.connect('quizapp.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    if not questions:
        print("No quiz questions available.")
        conn.close()
        return

    score = 0
    for q in questions:
        print(f"\n{q[1]}")
        print(f"A. {q[2]}")
        print(f"B. {q[3]}")
        print(f"C. {q[4]}")
        print(f"D. {q[5]}")

        answer = input("Enter your answer (A-D): ").upper()
        if answer == q[6]:
            print("Correct!")
            score += 10
        else:
            print("Incorrect.")

    cursor.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    print(f"Quiz complete! Your score: {score}")
    conn.close()

def view_results(username):
    """View the logged-in user's results."""
    conn = sqlite3.connect('quizapp.db')
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM scores WHERE username = ?", (username,))
    results = cursor.fetchall()

    if results:
        print(f"{username}'s Scores:")
        for i, score in enumerate(results, 1):
            print(f"Attempt {i}: {score[0]} points")
    else:
        print("No scores found. Please attempt the quiz first.")
    conn.close()

# Main program
def main():
    """Main function to run the quiz application."""
    setup_database()

    username = None
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Attempt Quiz")
        print("4. View Results")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            register()
        elif choice == "2":
            username = login()
        elif choice == "3":
            if username:
                attempt_quiz(username)
            else:
                print("Please log in first.")
        elif choice == "4":
            if username:
                view_results(username)
            else:
                print("Please log in first.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the application
main()
