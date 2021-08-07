#Importing the sqllite library
import sqlite3
from sqlite3.dbapi2 import Cursor

#Creating a connection to database
def connect():
  conn = sqlite3.connect('passwords.db') #Connecting to database
  cursor = conn.cursor() #Initiating a cursor
  return conn,cursor

#Kills the connection to the database after commiting the transaction
def disconnect(conn):
  conn.commit()
  conn.close()

#Creates a database with tables users and passwords(Called when database doesn't exist in the system)
def create_database():
  conn , cursor = connect()
  #User table
  cursor.execute('''
        CREATE TABLE "users" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "username" TEXT NOT NULL,
        "master_password" BLOB NOT NULL,
        "key" BLOB NOT NULL
        );
    ''')
 #Services table
  cursor.execute('''
        CREATE TABLE "services" (
        "service_name" TEXT NOT NULL,
        "username" TEXT NOT NULL,
        "password" BLOB NOT NULL,
        "user_id" INT NOT NULL,
        CONSTRAINT fk_users
        FOREIGN KEY ("user_id")
        REFERENCES users(id)
        );
    ''')

  disconnect(conn)

# SQL query to retrieve the list of usernames
def get_usernames_list():
  conn , cursor = connect()
  cursor.execute('SELECT username FROM users')
  users_list = cursor.fetchall()
  disconnect (conn)
  return users_list

#Adding new users (master_hashed - hash of the password of new user | key - key to encrpt and decrypt the new user passwords)
def add_user(username , master_hashed , key):
  conn , cursor = connect()
  cursor.execute(f'''INSERT INTO users ("username", "master_password", "key")
                    VALUES ("{username}", "{master_hashed}", "{key}")''')
  disconnect (conn)

#Gets the hashed master password for a given username. (master_password_hashed[0] (bytestring): hash of the user's master password)
def get_master_hashed(username):
  conn,cursor = connect()
  cursor.execute(f'SELECT master_password FROM users WHERE username="{username}"')
  master_password_hashed = cursor.fetchone()
  disconnect(conn)
  return master_password_hashed[0]

#Gets the user id for a given username
def get_user_id(username):
  conn , cursor = connect()
  cursor.execute(f'SELECT id FROM USERS WHERE username="{username}"')
  user_id = cursor.fetchone()[0]
  disconnect(conn)
  return user_id 

#Deletes a given user.
def delete_user(user_id):
  conn , cursor = connect()
  cursor.execute(f'DELETE FROM users WHERE id={user_id}')
  cursor.execute(f'DELETE FROM services WHERE user_id={user_id}')
  disconnect(conn)

#Retrieves all the saved services for the given user from services table
def list_saved_services(user_id):
 conn , cursor = connect()
 cursor.execute(f'SELECT service_name FROM services WHERE user_id="{user_id}"')
 services = cursor.fetchall()
 disconnect(conn)
 return services

#Gets the encryption key for the given user 
def get_key(user_id):
  conn , cursor = connect()
  cursor.execute(f'SELECT key FROM users where id="{user_id}"')
  key = cursor.fetchone()[0]
  key = key[2:]
  disconnect(conn)
  return key.encode()

#Adds a service to the database
def add_service(service_name , username , encrypted_password , user_id):
  conn , cursor = connect()
  cursor.execute(f'''
                    INSERT INTO services (service_name, username, password, user_id)
                    VALUES ("{service_name}", "{username}", "{encrypted_password}", "{user_id}")''')
  disconnect(conn)

#Retrieve data aka username and the encrypted password of a service from the services table | results[0] - username | results[1][2:] - encrypted password of the given service
def check_data_from_service(user_id , service_name):
  conn , cursor = connect()
  cursor.execute(f'''
                    SELECT username, password
                    FROM services
                    WHERE user_id="{user_id}"
                    AND service_name="{service_name}"
                    ''')
  results = cursor.fetchone()
  disconnect(conn)
  return results[0] , results[1][2:]

#Updates the username of a service in the services table
def update_service_username(user_id , username , service):
  conn , cursor = connect()
  cursor.execute(f'''
                    UPDATE services
                    SET username="{username}"
                    WHERE user_id="{user_id}"
                    AND service_name="{service}"''')
  disconnect(conn)

#Updates the password of a service in the services table
def update_service_password(user_id , service , password):
  conn , cursor = connect()
  cursor.execute(f'''
                    UPDATE services
                    SET password="{password}"
                    WHERE user_id="{user_id}"
                    AND service_name="{service}"''')
  disconnect(conn)

#Deletes the given service from the services table
def delete_service(user_id , service):
  conn , cursor = connect()
  cursor.execute(f'DELETE FROM services WHERE user_id="{user_id}" AND service_name="{service}"')
  disconnect(conn)