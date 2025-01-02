import psycopg2
import psycopg2.extras
import datetime
import os 
import cbor2
created_at = datetime.datetime.strptime('13-10-2022', '%d-%m-%Y')
conn= None
cur = None

#Office DB
# hostname = '10.113.130.51'
# port = '5432'
# username = 'hermesci'
# password = 'BlauGrot5@'
# database= 'test-db'


#My local DB
hostname = 'localhost'
port = '5432'
username = 'postgres'
password = 'postgres'
database= 'postgres'

# CHANGE_ID='2291' #HARDCODING
# pr_number = 'PR-'+'2292' 
created_at= '2024-01-01'

def create_connection():
    try:
        conn= psycopg2.connect(
             host=hostname,
             dbname=database,
             user=username,
             password=password,
             port=port
             )
        return conn
    except Exception as e:
       print(f"Error: {e}")
       return None
    
def create_tables(cursor):
    create_script = ''' 
                CREATE TABLE IF NOT EXISTS pr (
                    id serial primary key,
                    pr_number   varchar,
                    branch  varchar,
                    is_passed   bool,
                    created_at  DATE NOT NULL);

                CREATE TABLE IF NOT EXISTS test_c (
                    id serial primary key,
                    pr_number varchar,
                    folder_name_1 varchar,
                    folder_name_2 varchar,
                    file_name varchar,
                    created_at  DATE NOT NULL,
                    file_content text
                );
                CREATE TABLE IF NOT EXISTS test_python (
                    id serial primary key,
                    pr_number varchar,
                    folder_name_1 varchar,
                    folder_name_2 varchar,
                    file_name varchar,
                    created_at  DATE NOT NULL,
                    file_content text
                );
                    CREATE TABLE IF NOT EXISTS aft (
                    id serial primary key,
                    pr_number varchar,
                    device_name varchar,
                    part varchar,
                    folder_name varchar,
                    file_name varchar,
                    created_at DATE NOT NULL,
                    file_content text
                );

                    '''
    # Execute table creation
    cursor.execute(create_script)


# Function to insert Harcoded pr data to pr table
def insert_pr_data(cursor):
     insert_script_pr = 'INSERT INTO pr (pr_number, branch, is_passed, created_at) VALUES(%s,%s,%s,%s) '
     insert_values_pr = [('PR-2291','B1.36.6_Candidate', False, '2022-01-01' ),
                        ('PR-2292','B1.40.2_Candidate', False, '2024-01-01' ),
                        ('PR-3200','B1.40.2_Candidate', False, '2024-01-01' )
    ]
     for record in insert_values_pr:
         cursor.execute(insert_script_pr, record)



# Unified function to insert data fot test_c and test_python into the database
def insert_data(directory, pr_number, table_name,created_at, cursor):
    """
    Insert data into the specified table based on the folder structure.
    This function can be used for `insert_onto target_and_simulator_data`, `insert_into_test_c_table`, and `insert_into_test_python_table`.
    """
    # Get the files (either .txt, .xml, .js, .html, etc.)
    all_files = []

    # Special handling for test_c and test_python: search across all levels of subfolders for files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'stdout.txt': # exclude this file
                continue
            if file.endswith(('.txt', '.xml', '.js', '.html' , 'css')):
                all_files.append(os.path.join(root, file))

    if not all_files:
        raise FileNotFoundError(f"No appropriate files found in the folder: {directory}")
    
    excluded_folders = ['CppUTestProj-prefix', 'Testing', 'src', 'temp', 'CppUTestProj-build']

    # Insert each file into the database
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        
        if 'cache' in file_name.lower():
            continue
        
        # Read file content and encode it
        with open(file_path, 'r') as file:
            file_text = file.read()


            file_content = cbor2.dumps(file_text)


        folder_name_1 = os.path.basename(os.path.dirname(file_path))  # Parent folder
        dir_path=os.path.dirname(file_path)
        test_name=os.path.basename(directory)



        if folder_name_1 == 'coverage' or folder_name_1 == 'html_coverage' or folder_name_1 == 'html_pytest':
            folder_name_2=''

        else:
            dir_path=os.path.dirname(file_path)
            build_dir=os.path.dirname(dir_path)
            get_dir_folder=os.path.basename(build_dir)

            folder_name_1=os.path.basename(build_dir) #'build' folder
            folder_name_2=os.path.basename(dir_path)  # Subfolder or file name
            # Exclude 'CppUTestProj-prefix' and 'Testing' folders
            # Skip files in excluded folders
            if folder_name_1 in excluded_folders or folder_name_2 in excluded_folders or get_dir_folder in excluded_folders :
                continue  # Skip this file

        if folder_name_1== test_name or folder_name_2 == test_name:
            folder_name_1=''
            folder_name_2=''
        

        # Prepare insert statement
        insert_script = f'''INSERT INTO {table_name} (pr_number, folder_name_1, folder_name_2, file_name, created_at, file_content)
                            VALUES (%s, %s, %s, %s, %s, %s)'''
        insert_values = (pr_number, folder_name_1, folder_name_2, file_name, created_at, file_content)
        
        # Execute the insert
        cursor.execute(insert_script, insert_values)

# Consistent function to insert test_c & test_python data
def insert_into_test_c_and_test_python_table(directory, pr_number, created_at, cursor, table_name):
    insert_data(directory, pr_number, table_name, created_at, cursor)


# insert AFT data into the database
def insert_data_aft(directory, pr_number,device_name, created_at, cursor):
    """
    Insert data into the specified table based on the folder structure.
    """
    DEVICE=device_name # in static_check.jenkinsfile
    # Get the files (either .txt, .xml, .js, .html, etc.)
    all_files = []



    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.txt', '.xml', '.json', 'pkl','log', '.html')):  # You can adjust the file types here
                 all_files.append(os.path.join(root, file))

    if not all_files:
        raise FileNotFoundError(f"No appropriate files found in the folder: {directory}")


    # Insert each file into the database
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        
        # Read file content and encode it
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # If it opens in text mode, read the file as text
                file_text = file.read()
                file_content = cbor2.dumps(file_text)
        except UnicodeDecodeError:
            # If there is a Unicode error, treat the file as binary
            with open(file_path, 'rb') as file:
                file_binary = file.read()
                file_content = cbor2.dumps(file_binary)

        if device_name == 'obd2' or device_name == 'advanced_getway_iap':
            part=''
        else:
            part='1' #hardcode for now
            part= part # it is a parameter in executeAft function in hermes.groovy



        # Determine folder names from path
        folder_name = os.path.basename(os.path.dirname(file_path))  # Parent folder
        if folder_name == 'aft':
            folder_name='' #to save .log file in main aft folder not in aft/aft


        # Prepare insert statement
        insert_script = f'''INSERT INTO aft (pr_number, device_name, part, folder_name, file_name, created_at, file_content)
                            VALUES (%s, %s, %s, %s, %s, %s,%s)'''
        insert_values = (pr_number,device_name,part, folder_name, file_name, created_at, file_content)
        
        # Execute the insert
        cursor.execute(insert_script, insert_values)

# Consistent function to insert test_c data
def insert_into_aft_table(directory, pr_number,device_name, created_at, cursor):
    insert_data_aft(directory, pr_number,device_name,created_at , cursor)


