# main.py
from src import generate_keyword_ideas
from src.config import load_config
from src.models import Base, Session
from src.db_operations import load_data_to_db, get_unique_keywords_from_db
import os
from sqlalchemy import create_engine


config = load_config()
DATABASE_URL = config['DATABASE_URL']

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check your .env file.")

# Run Scripts
if __name__ == "__main__":
    
    engine = create_engine(DATABASE_URL)
    print("Engine created")
    
    Base.metadata.create_all(bind=engine)  # Create tables in the database if they don't exist
    session = Session(bind=engine)  # Create a Session instance
    print("Session created")

    while True:  # Main loop presenting the user with options
        print("Select an option:")
        print("a) Generate Keywords and Search Volume")
        print("b) Upload Keywords with Search Volume to Database")
        print("e) Exit")
        
        user_input = input("Enter your choice: ").strip().lower()
        
        if user_input == 'a':
            print("Generating keyword ideas defined in seed_keywords.txt - 1 seed keyword per row")
            generate_keyword_ideas.run()
            print("Ideas are exhausted")
        
        elif user_input == 'b':
            csv_path = "data/keyword_ideas.csv"
            if os.path.exists(csv_path):
                print(f"{csv_path} exists")
            else:
                print(f"Error: {csv_path} does not exist")
                continue  # Go back to the start of the loop
            
            load_data_to_db(csv_path, engine, session)
            print("Data loaded to db")
        
        elif user_input == 'e':
            print("Exiting the program.")
            break  # Exit the loop and end the program
        
        else:
            print("Invalid input. Please enter a, b, c, d or e.")
