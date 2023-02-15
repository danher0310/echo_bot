import mysql.connector
import os 
from dotenv import load_dotenv

load_dotenv()

def connectionDb():
  try:
    mydb = mysql.connector.connect(
      host = os.getenv('dbhost'),
      user= os.getenv('userdb'),
      password= os.getenv('passdb'),
      database= os.getenv('dbname'),
      auth_plugin="mysql_native_password"      
    )
    return mydb
  except OSError:
    return OSError
  
def register_employe(tlgid, user_firstN, username, charge):
  
  mydb = connectionDb()
  mycursor = mydb.cursor()
  try:
    queryString = "INSERT INTO attendence (tlg_id, name, currentDate, currentTime, role, user) VALUES (%s,%s,current_date(),current_time(),%s,%s);"
    values = (tlgid, user_firstN, charge, username,)
    mycursor.execute(queryString, values)
    mydb.commit()
    mydb.close()
    return None
  except :
    return "We have a error register you in the system"
  
def remove_user(tlgid):
  mydb = connectionDb()
  mycursor = mydb.cursor()
  try:
    print("entre en el try")
    queryString = "DELETE FROM attendence WHERE ('tlg_id'= %s);"
    value = tlgid
    mycursor.execute(queryString, (value,))
    mydb.commit()
    mydb.close()
    return None
  except OSError:    
    return "We have a error remove the user in the system"
  
   
    
