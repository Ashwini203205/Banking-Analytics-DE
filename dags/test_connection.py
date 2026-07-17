import pandas as pd
from sqlalchemy import create_engine

# Database connection URI
# format: postgresql://username:password@host:port/database_name
DATABASE_URL = "postgresql://admin:password123@localhost:5432/banking_db"

try:
    # 1. Create the database engine
    engine = create_engine(DATABASE_URL)
    
    # 2. Create a dummy dataframe representing mock transactions
    df = pd.DataFrame({
        'transaction_id': [101, 102, 103],
        'customer_id': [9901, 9902, 9903],
        'amount': [250.50, 1000.00, 45.25],
        'type': ['deposit', 'transfer', 'withdrawal']
    })
    
    # 3. Write data to PostgreSQL
    df.to_sql('mock_transactions', engine, if_exists='replace', index=False)
    print("✅ Successfully connected to DB and created 'mock_transactions' table!")
    
    # 4. Read it back to verify
    query_df = pd.read_sql('SELECT * FROM mock_transactions', engine)
    print("\nData retrieved from Database:")
    print(query_df)

except Exception as e:
    print(f"❌ Connection failed: {e}")