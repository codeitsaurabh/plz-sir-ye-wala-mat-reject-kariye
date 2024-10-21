import json
import os

# Global variables
user_data = {}  # Stores user information such as username, password, progress, and score
current_user = None  # Keeps track of the currently logged-in user

# Check if the user data file exists; if not, create it
if not os.path.exists("user_data.json"):
    with open("user_data.json", "w") as f:
        json.dump({}, f)  # Initialize an empty JSON file

# Load existing user data from the JSON file
with open("user_data.json", "r") as f:
    user_data = json.load(f)

# Function to save user data to the JSON file (to store progress and scores)
def save_user_data():
    with open("user_data.json", "w") as f:
        json.dump(user_data, f)  # Write the updated user data to the JSON file

# Lesson content, stored as a list of dictionaries (Each lesson has a title and content)
lessons = [
    {"title": "Lesson 1: Variables", "content": "Variables in Python are used to store data. Example: x = 5"},
    {"title": "Lesson 2: Loops", "content": "Loops allow you to execute a block of code repeatedly. Example: for i in range(5): print(i)"},
    {"title": "Lesson 3: Functions", "content": "Functions are blocks of code that perform a task. Example: def my_function(): print('Hello')"},
]

# Quiz questions with multiple-choice options (Each question has options and a correct answer)
quiz_questions = [
    {"question": "How do you declare a variable in Python?", "options": ["a) int x = 5", "b) x = 5", "c) var x = 5"], "answer": "b"},
    {"question": "Which keyword is used to define a loop in Python?", "options": ["a) loop", "b) while", "c) for"], "answer": "c"},
]

# Utility function to clear the console (to improve user interface)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears console on Windows (cls) and Linux/macOS (clear)

# Authentication Functions
# User Login
def login():
    global current_user
    username = input("Enter your username: ")  # Ask for the username
    password = input("Enter your password: ")  # Ask for the password
    
    # Check if the username exists and if the password matches
    if username in user_data and user_data[username]["password"] == password:
        current_user = username  # Set the current user
        print(f"\nWelcome back, {current_user}!\n")
        main_menu()  # Navigate to the main menu
    else:
        print("Incorrect username or password!\n")
        start_screen()  # Redirect back to start screen

# User Registration
def register():
    global current_user
    username = input("Choose a username: ")  # Ask for a new username
    password = input("Choose a password: ")  # Ask for a new password
    
    # Check if the username is already taken
    if username not in user_data:
        # Create a new entry for the user
        user_data[username] = {"password": password, "progress": 0, "score": 0}
        current_user = username  # Set the current user to the newly registered user
        save_user_data()  # Save the updated user data
        print("\nRegistration successful!\n")
        main_menu()  # Navigate to the main menu
    else:
        print("Username already exists!\n")
        start_screen()  # Redirect back to start screen

# Main Menu (navigation menu for users after login)
def main_menu():
    clear_console()  # Clear the console for a clean display
    print(f"Welcome to the Python Learning App, {current_user}!")
    print("1. Start Learning")  # Lesson option
    print("2. Take Quiz")  # Quiz option
    print("3. Code Playground")  # Code execution environment
    print("4. View Progress")  # Check progress and quiz score
    print("5. Logout")  # Logout option
    
    choice = input("\nChoose an option (1-5): ")  # Ask the user to choose an option
    
    # Redirect the user based on the chosen option
    if choice == '1':
        lessons_menu()  # Start learning lessons
    elif choice == '2':
        take_quiz()  # Take the quiz
    elif choice == '3':
        code_playground()  # Code playground to execute custom code
    elif choice == '4':
        view_progress()  # View progress and quiz scores
    elif choice == '5':
        logout()  # Logout and return to the login screen
    else:
        print("Invalid choice, please try again.")  # Handle invalid input
        main_menu()  # Show the main menu again

# Lesson Functions
# Displays the lesson content based on user progress
def lessons_menu():
    progress = user_data[current_user]["progress"]  # Retrieve user's progress
    lesson_index = int(progress / (100 / len(lessons)))  # Calculate which lesson the user is on

    if lesson_index >= len(lessons):  # If all lessons are complete
        print("You have completed all lessons!\n")
        main_menu()  # Go back to the main menu
    else:
        lesson = lessons[lesson_index]  # Fetch the current lesson
        print(f"\n{lesson['title']}")  # Display the lesson title
        print(lesson['content'])  # Display the lesson content
        input("\nPress Enter to continue...")  # Wait for user input to proceed

        # Mark lesson as complete by updating user progress
        user_data[current_user]["progress"] += (100 / len(lessons))
        save_user_data()  # Save progress to the JSON file

        main_menu()  # Return to the main menu after lesson completion

# Quiz Function
# Function to administer a quiz
def take_quiz():
    current_score = 0  # Initialize the score for the current quiz session

    # Loop through each quiz question
    for question in quiz_questions:
        print("\n" + question["question"])  # Display the quiz question
        for option in question["options"]:  # Display each option
            print(option)

        # Ask the user to select an option
        answer = input("\nChoose the correct answer (a, b, c): ").lower()
        if answer == question["answer"]:  # If the answer is correct
            current_score += 1  # Increment the score
            print("Correct!")  # Inform the user that they answered correctly
        else:
            print("Incorrect!")  # Inform the user that they answered incorrectly

    # Update the user's overall score
    user_data[current_user]["score"] += current_score  # Update the total score
    save_user_data()  # Save the score to the JSON file

    # Display the final score for the current quiz
    print(f"\nYour final score: {current_score}/{len(quiz_questions)}\n")
    main_menu()  # Return to the main menu after completing the quiz

# Code Playground
# A space for users to try out their Python code
def code_playground():
    print("\nWelcome to the Code Playground!")
    print("Type your Python code below (type 'exit' to return to the main menu):\n")

    # Continuously allow users to input and run code until they type 'exit'
    while True:
        code = input(">>> ")  # Prompt the user for code input
        if code.lower() == "exit":  # Exit the playground when the user types 'exit'
            break
        try:
            exec(code)  # Try to execute the input code
        except Exception as e:  # Handle any errors that occur during code execution
            print(f"Error: {e}")  # Print the error message

    main_menu()  # Return to the main menu after the playground session

# View Progress
# Function to display the user's progress and quiz score
def view_progress():
    progress = user_data[current_user]["progress"]  # Get the user's progress percentage
    score = user_data[current_user]["score"]  # Get the user's quiz score

    # Display the user's progress and score
    print(f"\nYour Progress: {progress:.2f}% Complete")
    print(f"Quiz Score: {score} Points\n")

    main_menu()  # Return to the main menu

# Logout
# Function to log the user out and return to the login screen
def logout():
    global current_user
    current_user = None  # Reset the current user to None
    start_screen()  # Go back to the start screen

# Start Screen (shown at the very beginning of the application)
def start_screen():
    clear_console()  # Clear the console for a clean display
    print("Welcome to the Python Learning App!")
    print("1. Login")  # Option to login
    print("2. Register")  # Option to register a new account
    print("3. Help")  # Option to view help
    print("4. Exit")  # Option to exit the application
    
    choice = input("\nChoose an option (1-4): ")  # Ask the user to choose an option
    
    # Redirect the user based on the chosen option
    if choice == '1':
        login()  # Go to the login screen
    elif choice == '2':
        register()  # Go to the registration screen
    elif choice == '3':
        help_menu()  # Show the help menu
    elif choice == '4':
        print("Goodbye!")  # Exit the application
        exit()
    else:
        print("Invalid choice, please try again.")  # Handle invalid input
        start_screen()  # Show the start screen again

# Help Menu
# Function to display instructions for the user
def help_menu():
    print("\nHelp Section:")
    print("1. Login: Use your username and password to login if you've already registered.")
    print("2. Register: Create a new account if you're a new user.")
    print("3. Start Learning: Follow the lessons step-by-step and track your progress.")
    print("4. Take Quiz: Test your knowledge by answering multiple-choice questions.")
    print("5. Code Playground: Experiment with Python code in a free coding environment.")
    print("6. View Progress: Check your learning progress and quiz scores.")
    input("\nPress Enter to return to the main menu...")  # Wait for user input to return to the main menu
    start_screen()  # Show the start screen again

# Start the Application
if __name__ == "__main__":
    start_screen()  # Start the application by showing the start screen
