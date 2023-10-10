import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from .models import SearchVolumeKeywordGenerator
from .models import Base
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert



# Load environment variables
Base = declarative_base()
load_dotenv('../keyword_generator_env/.env')  # Adjust the path to your .env file if needed
DATABASE_URL = os.getenv("DATABASE_URL")
Session = sessionmaker()


def load_data_to_db(csv_path, engine, session): 
    print("Starting data loading process...")
    
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows from {csv_path}.")
        df['month'] = pd.to_datetime(df['month'] + '-01')        
        df.drop_duplicates(subset=['seed_keyword', 'keyword', 'month'], keep='first', inplace=True)
        
        batch_size = 1000  # Adjust batch size according to your system's capability
        batch = []  # Initiate the batch list
        
        with session.begin():
            print("Starting to insert rows into the database...")
            for index, row in df.iterrows():
                batch.append(
                    {
                        "seed_keyword": row['seed_keyword'],
                        "keyword": row['keyword'],
                        "avg_monthly_searches": row['avg_monthly_searches'],
                        "competition": row['competition'],
                        "competition_index": row['competition_index'],
                        "month": row['month'],
                        "monthly_searches": row['monthly_searches'],
                        "cpc": row['cpc'],
                        "low_range_bid": row['low_range_bid'],
                        "high_range_bid": row['high_range_bid'],
                        "keyword_annotation": row['keyword_annotation'],
                        "brand_bool": row['brand_bool'],
                        "concept_group": row['concept_group'],
                        "concept_name": row['concept_name'],
                        "language_id": row['language_id'],
                        "location_id": row['location_id']
                    }
                )
                
                if (index + 1) % batch_size == 0:
                    insert_stmt = insert(SearchVolumeKeywordGenerator).values(batch)
                    do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['seed_keyword', 'keyword', 'month'])
                    session.execute(do_nothing_stmt)
                    batch = []  # Reset the batch list
                    print(f"Processed {index + 1} rows...")
            
            # Don't forget to process the last batch if it exists
            if batch:
                insert_stmt = insert(SearchVolumeKeywordGenerator).values(batch)
                do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['seed_keyword', 'keyword', 'month'])
                session.execute(do_nothing_stmt)
                print(f"Processed remaining {len(batch)} rows...")
                
            print("All rows processed. Committing to the database...")
        
    except Exception as e:
        print(f"Error occurred: {e}")


def get_unique_keywords_from_db(session, seed_keyword=None):  # seed_keyword is optional and defaults to None
    print("Starting to retrieve unique keywords from the database...")
    unique_keywords = []
    
    try:
        query = session.query(SearchVolumeKeywordGenerator.keyword).distinct()
        
        # Apply the filter only if seed_keyword is provided
        if seed_keyword is not None:
            query = query.filter(SearchVolumeKeywordGenerator.seed_keyword == seed_keyword)
        
        unique_keywords = [row.keyword for row in query.all()]
        
        if seed_keyword:
            print(f"Retrieved {len(unique_keywords)} unique keywords from the database for seed_keyword: {seed_keyword}.")
        else:
            print(f"Retrieved {len(unique_keywords)} unique keywords from the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return unique_keywords

