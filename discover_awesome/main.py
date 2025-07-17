import argparse
import logging
import os
import shutil
import yaml 
from api_calls import build_database_from_tag, fetch_database
from appdirs import user_data_dir
import json
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem
import curses

class DiscoverAwesome:
    def __init__(self):
        self.app_name = "discover-awesome" 
        self.user_dir = user_data_dir(self.app_name)
        self.config_file = os.path.join(self.user_dir, "config.yaml")  
        self.current_file_path = os.path.abspath(__file__)  # Get the absolute path of cli.py
        self.project_root = os.path.dirname(self.current_file_path)  
        self.database_subfolder  = os.path.join(self.project_root, "database")
        self.args = self.parse_args() 

        logging.basicConfig(level=logging.INFO) 

        self.check_first_run()

    def parse_args(self):
        define_parser = argparse.ArgumentParser(description="Go through a bunch of repos in the awesome-list GitHub topic from your terminal!")
        define_parser.add_argument("--token", "-t", type=str, help="Save a RESTRICTIVELY SCOPED GitHub personal access token to your local config. Required so you can make API requests for specific repos.")     
        define_parser.add_argument("--database", "-d", type=str, default="most", choices=["most", "least", "newest", "oldest", "recently-updated", "least-recently-updated"], help="Which local database to use. Due to the GitHub API's limit of 1,000 results per request, multiple databases are retrieved by making separate requests based on different statistics (e.g., stars, forks) to ensure accurately sorted results across various categories.")
        define_parser.add_argument("--fetchDatabase", "-f", action="store_true", help="Downloads databases from the discover-awesome repository.")
        define_parser.add_argument("--buildDatabase", "-b", action="store_true", help="Build databases directly from the GitHub API.")
        
        return define_parser.parse_args() 

        
    def check_config_field(self, field, value):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f)
            return config.get(field, False) == value
        return False

    def check_first_run(self):
        if os.path.exists(self.config_file):
            return True
        else:
            self.create_first_run_files()
            return False

    def create_first_run_files(self):
        os.makedirs(self.user_dir, exist_ok=True)

        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f) or {} 
        else:
            config = {}  

        with open(self.config_file, "w") as f:
            yaml.dump(config, f) 

        for filename in os.listdir(self.database_subfolder):
            source_file = os.path.join(self.database_subfolder, filename)
            destination_file = os.path.join(self.user_dir, filename)
            shutil.copy(source_file, destination_file)

        logging.info(f"First run detected. Copied the repo's pre-made database files to {self.user_dir}.")

    def check_token(self):
        with open(self.config_file, "r") as f:
            config = yaml.safe_load(f)
        if config.get("token", False):  # 2nd argument is else
            return True
        else:
            logging.error("No token found in config. Please provide it with --token")      
            exit()
        
    def supply_token(self):

        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f) or {} 
        else:
            config = {} 


        config["token"] = self.args.token

    
        with open(self.config_file, "w") as f:  
            yaml.dump(config, f) 
  
    def choose_database(self):
        database_paths = {
            "most": os.path.join(self.user_dir, "repositories_most_stars.json"),
            "least": os.path.join(self.user_dir, "repositories_least_stars.json"),
            "newest": os.path.join(self.user_dir, "repositories_newest_created.json"),
            "oldest": os.path.join(self.user_dir, "repositories_oldest_created.json"),
            "recently-updated": os.path.join(self.user_dir, "repositories_recently_updated.json"),
            "least-recently-updated": os.path.join(self.user_dir, "repositories_least_recently_updated.json")
        }

        if self.args.database in database_paths:
            self.path = database_paths[self.args.database]
            self.showResults(self.path)
        else:
            raise ValueError('Somehow, an invalid database arg got through!')
   
    def showResults(self, path, limit=10):
        with open(path, 'r') as file:
            data = json.load(file)
        
        limit = 10
        
        menu = CursesMenu(path)
        terminalsize = shutil.get_terminal_size()
        terminalwidth = terminalsize.columns - 7
        
        for entry in data[:limit]:
            name = entry.get('name', 'Unknown')
            description = entry.get('description', 'No description')
            url = entry.get('url', 'No URL')
        
            item_text = f"{name} - {description}"
        
            # Truncate item_text to fit within the terminal width
            if len(item_text) > terminalwidth:
                item_text = item_text[:terminalwidth - 10] 
        
            command_item = CommandItem(
                item_text,
                f"echo {name} selected",
            )
            menu.items.append(command_item)
        
        menu.show()


    def run(self):
        if self.args.buildDatabase:
            build_database_from_tag(self.args.buildDatabase)
        if self.args.token:
            self.supply_token()
        if self.args.fetchDatabase:
            self.fetch_database()
        if self.args.database:
            self.choose_database()
        else:
            self.choose_database()


if __name__ == "__main__":
    app = DiscoverAwesome()
    app.run()