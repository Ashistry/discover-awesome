import argparse
import logging
from api_calls import build_database_from_tag, fetch_database
from appdirs import user_data_dir
import shutil       
import os

class DiscoverAwesome:
    def __init__(self):
        self.app_name = 'discover-awesome' 
        self.user_dir = user_data_dir(self.app_name)
        self.config_file = os.path.join(self.user_dir, "config.yaml")  
        self.current_file_path = os.path.abspath(__file__)  # Get the absolute path of cli.py
        self.project_root = os.path.dirname(self.current_file_path)  
        self.database_subfolder  = os.path.join(self.project_root, "database")
        self.args = self.parse_args() 
        
    def parse_args(self):
        define_parser = argparse.ArgumentParser(description="Go through every repo (read: 1000 per Github API request sorting option) in the awesome-list GitHub topic from your terminal.")
        define_parser.add_argument('--database', '-d', type=str, default='most', choices=['most', 'least', 'newest', 'oldest'], help="Which local database to use. Default is most stars.")
        define_parser.add_argument('--sortLocal', '-s', type=str, default='most', choices=['most', 'least', 'newest', 'oldest'], help="Method of sorting chosen database. Default is most stars.")
        define_parser.add_argument('--fetchDatabase', '-f', action='store_true', help="Downloads databases from the discover-awesome repository.")
        define_parser.add_argument('--buildDatabase', '-b', action='store_true', help='Build all databases of repos directly from the GitHub API.')

        return define_parser.parse_args() 

    def check_first_run(self):
        if os.path.exists(self.config_file):
            return True 
        else:
            self.create_first_run_files()

    def create_first_run_files(self):
        os.makedirs(self.user_dir, exist_ok=False)
        with open(self.config_file, 'a') as f:
            f.write("run: 'true'")

        for filename in os.listdir(self.database_subfolder):
            source_file = os.path.join(self.database_subfolder, filename)
            destination_file = os.path.join(self.user_dir, filename)
            shutil.copy(source_file, destination_file)
        logging.info(f"Since this is your first run, copied the repo's pre-made database files to {self.user_dir}. Please run your command again.")   

    def default(self):
        if self.check_first_run():
            database = self.args.database
            path = None
            
            database_paths = {
                "most": os.path.join(self.user_dir, 'repositories_most_stars.json'),
                "least": os.path.join(self.user_dir, 'repositories_least_stars.json'),
                "newest": os.path.join(self.user_dir, 'repositories_newest_created.json'),
                "oldest": os.path.join(self.user_dir, 'repositories_oldest_created.json'),
                "recently": os.path.join(self.user_dir, 'repositories_recently_updated.json'),
                "least_recently": os.path.join(self.user_dir, 'repositories_least_recently_updated.json')
            }

            if database in database_paths:
                path = database_paths[database]
            else:
                raise ValueError("Not a valid database option.")


    def run(self):
        logging.basicConfig(level=logging.INFO)
        
        if self.args.buildDatabase:
            self.default()

if __name__ == "__main__":
    app = DiscoverAwesome()
    app.run()  
