import json
import psycopg2
import os

def lambda_handler(event, context):
    print(f"Event collected: {event}")
    
    try:
        for record in event['Records']:
            s3_bucket = record['s3']['bucket']['name']
            print(f"Bucket name: {s3_bucket}")
            s3_key = record['s3']['object']['key']
            print(f"Bucket key: s3_key{}")
            from_path = f"s3://{s3_bucket}/{s3_bucket}")
            print(f"From path: {from_path}")
            
            Access_key = os.getenv('AWS_ACCESS_KEYID')
            Access_Secret = os.getenv('AWS_SECRET_ACCESSKEY')
            dbname = os.getenv('DBNAME')
            host = os.getenv('HOST')
            user = os.getenv('USER')
            password = os.getenv('PASSWORD')
            tablename = os.getenv('TABLENAME')
            port = os.getenv('PORT')
            region = os.getenv('REGION')
            
            connection = psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=password)
            print('Connected to the database...')
            
            curs = connection.cursor()
            print('Cursor created...')
            
            query = """
            COPY {} FROM '{}' CREDENTIALS 'aws_access_key_id={};aws_secret_access_key={}' FORMAT AS CSV DELIMITER ',' QUOTE '"' IGNOREHEADER 1 REGION AS '{}';
            """.format(tablename, from_path, Access_key, Access_Secret, region)
            print(f"Query: {query}")
            
            curs.execute(query)
            connection.commit()
            print('Query executed and committed...')
            
            curs.close()
            print('Cursor closed...')
            
            connection.close()
            print('Connection closed...')
        
        print('Function executed successfully...')
    
    except Exception as e:
        print(f"Error: {e}")
       raise e  
