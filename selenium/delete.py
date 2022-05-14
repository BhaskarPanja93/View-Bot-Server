import sqlite3
from os import getcwd
read_only_location = '../read only'



db_connection = sqlite3.connect(getcwd()+f'/{read_only_location}/user_data.db', check_same_thread=False)
print([row[0] for row in db_connection.cursor().execute("SELECT total_views from user_data where u_name = 'bhaskar'")][0])

