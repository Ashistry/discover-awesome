import argparse
import logging
from api_calls import build_database_from_tag, fetch_database
from appdirs import user_data_dir
import shutil       
import os

tool_name = 'discover-awesome' 
user_dir = user_data_dir(tool_name)
config_file = os.path.join(user_dir, "config.yaml")  

current_file_path = os.path.abspath(__file__)  # Get the absolute path of cli.py
project_root = os.path.dirname(current_file_path)  
database_subfolder  = os.path.join(project_root,"database")


def check_first_run():
    if os.path.exists(config_file):
        return True 
    else:
        create_first_run_files()

def create_first_run_files():
    os.makedirs(user_dir, exist_ok=False)
    with open(config_file, 'a') as f:
        f.write("run: 'true'")
            
    if args.fetchDatabase == False & args.buildDatabase == False:  
            for filename in os.listdir(database_subfolder):
                source_file = os.path.join(database_subfolder, filename)
                destination_file = os.path.join(user_dir, filename)
                shutil.copy(source_file, destination_file)
            logging.info(f"Since this is your first run, copied the repo's pre-made database files to {user_dir}. Please run your command again.")   

def default():
    if check_first_run() == True:
        database = args.database
        path = None
        
        database_paths = {
            "most_stars": 'user_dir/repositories_most_stars.json',
            "least_stars": 'user_dir/repositories_least_stars.json',
            "newest_created": 'user_dir/repositories_newest_created.json',
            "oldest_created": 'user_dir/repositories_oldest_created.json',
            "recently_updated": 'user_dir/repositories_recently_updated.json',
            "least_recently_updated": 'user_dir/repositories_least_recently_updated.json'
        }

        if database in database_paths:
            path = database_paths[database]
        else:
            raise ValueError("Not a valid database option.")



def main():    
    
    logging.basicConfig(level=logging.INFO)
    
    define_parser = argparse.ArgumentParser(description="Go through every repo (read: 1000 per Github API request sorting option) in the awesome-list GitHub topic from your terminal.")
    define_parser.add_argument('--database', '-d', type=str, default='most', choices=['most', 'least', 'newest','oldest'], help="Which local database to use. Default is most stars. This is different from --sortLocal in that the database type was requested by this stat from the API.")
    define_parser.add_argument('--sortLocal', '-s', type=str, default='most', choices=['most', 'least', 'newest','oldest'], help="Method of sorting chosen database. Default is most stars. This is different from --database in that this sorts your choice of requested-from-API-by-stat local database by the stat you've chosen.")
    define_parser.add_argument('--fetchDatabase','-f',action='store_true',help="Downloads databases from the discover-awesome repository.")
    define_parser.add_argument('--buildDatabase', '-b', type=str, required=False, help='Build all databases of repos directly from the Gihub API. Requires a personal access token to be passed wich does not need any special permissions.')

    args = define_parser.parse_args()        


if args.database:
    default()

    
if __name__ == "__main__":
    main()
