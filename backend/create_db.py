#!/usr/bin/env python
"""
Script to create the mahila_udyam database automatically
"""
import pymysql
import sys

def create_database():
    try:
        # Connect to MySQL server without specifying a database
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='prathap@0210',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS mahila_udyam CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("✅ Database 'mahila_udyam' created successfully!")
        
        cursor.close()
        connection.commit()
        connection.close()
        
        return True
    except pymysql.MySQLError as e:
        print(f"❌ MySQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = create_database()
    sys.exit(0 if success else 1)
