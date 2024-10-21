import mysql.connector
import os
import json

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",   # Your MySQL username
        password="",   # Your MySQL password
        database="mimo_clone"  # Create the database
    )

# Initialize the database (Create tables for users and progress)
def initialize_db():
    db = connect_to_db()
    cursor = db.cursor()

    # Create a users table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        progress JSON
    )
    """)
    
    # Create a progress table if it doesn't exist (to track user progress)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        lesson_completed INT,
        quiz_score INT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    db.commit()
    db.close()

# User Registration
def register():
    db = connect_to_db()
    cursor = db.cursor()
    
    username = input("Choose a username: ")
    password = input("Choose a password: ")

    try:
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password, progress) VALUES (%s, %s, %s)",
                       (username, password, json.dumps({"completed_lessons": [], "score": 0})))
        db.commit()
        print("Registration successful!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        db.close()

# User Login
def login():
    db = connect_to_db()
    cursor = db.cursor()
    
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    if user:
        print(f"Welcome back, {username}!")
        main_menu(user[0])  # Pass the user's ID to the main menu
    else:
        print("Invalid username or password!")
    db.close()

# Main Menu
def main_menu(user_id):
    while True:
        print("\n1. Start Learning\n2. Take Quiz\n3. Code Playground\n4. View Progress\n5. Logout")
        choice = input("\nChoose an option (1-5): ")

        if choice == '1':
            lessons_menu(user_id)
        elif choice == '2':
            take_quiz(user_id)
        elif choice == '3':
            code_playground()
        elif choice == '4':
            view_progress(user_id)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

# Lessons Menu
def lessons_menu(user_id):
    lessons = [
        {"title": "Lesson 1: Variables", "content": "Variables in Python store data..."},
        {"title": "Lesson 2: Loops", "content": "Loops in Python allow repeating tasks..."},
        # Add more lessons here...
    ]
    
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("SELECT progress FROM users WHERE id = %s", (user_id,))
    progress_data = json.loads(cursor.fetchone()[0])

    completed_lessons = progress_data["completed_lessons"]
    next_lesson = len(completed_lessons) + 1

    if next_lesson <= len(lessons):
        lesson = lessons[next_lesson - 1]
        print(f"\n{lesson['title']}\n{lesson['content']}")
        input("\nPress Enter to complete this lesson...")

        completed_lessons.append(next_lesson)
        progress_data["completed_lessons"] = completed_lessons

        cursor.execute("UPDATE users SET progress = %s WHERE id = %s", (json.dumps(progress_data), user_id))
        db.commit()
    else:
        print("You have completed all lessons!")
    
    db.close()

# Quiz Function
def take_quiz(user_id):
    quiz_questions = [
        {"question": "What is the output of print(2 + 3)?", "options": ["a) 5", "b) 6", "c) 7"], "answer": "a"},
        {"question": "Which keyword is used to define a function?", "options": ["a) func", "b) def", "c) method"], "answer": "b"},
        # Add more questions here...
    ]
    
    db = connect_to_db()
    cursor = db.cursor()

    score = 0

    for question in quiz_questions:
        print(f"\n{question['question']}")
        for option in question["options"]:
            print(option)
        answer = input("Choose the correct answer: ").lower()
        if answer == question["answer"]:
            score += 1
            print("Correct!")
        else:
            print("Incorrect!")

    print(f"\nYour score: {score}/{len(quiz_questions)}")

    cursor.execute("INSERT INTO progress (user_id, lesson_completed, quiz_score) VALUES (%s, %s, %s)",
                   (user_id, len(quiz_questions), score))
    db.commit()
    db.close()

# Code Playground
def code_playground():
    print("\nWelcome to the Code Playground!")
    print("Type your Python code below (type 'exit' to return to the main menu):\n")

    while True:
        code = input(">>> ")
        if code.lower() == "exit":
            break
        try:
            exec(code)
        except Exception as e:
            print(f"Error: {e}")

# View Progress
def view_progress(user_id):
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("SELECT progress FROM users WHERE id = %s", (user_id,))
    progress_data = json.loads(cursor.fetchone()[0])

    completed_lessons = len(progress_data["completed_lessons"])
    score = progress_data["score"]

    print(f"\nYou have completed {completed_lessons} lessons.")
    print(f"Your total quiz score is: {score}")

    db.close()

# Start the Application
def start_screen():
    print("Welcome to Mimo Clone (CLI)!")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    if choice == '1':
        login()
    elif choice == '2':
        register()
    elif choice == '3':
        print("Goodbye!")
        exit()
    else:
        print("Invalid option, please try again!")
        start_screen()

# Initialize the database when the app starts
initialize_db()

# Run the application
if __name__ == "__main__":
    start_screen()
