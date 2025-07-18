import argparse
import json
import logging
import os
import shutil
import yaml

from appdirs import user_data_dir
from api_calls import build_database_from_tag, fetch_database, get_readme
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

class DiscoverAwesome:
    def __init__(self):
        self.app_name = "discover-awesome" 
        self.user_dir = user_data_dir(self.app_name)
        self.config_file = os.path.join(self.user_dir, "config.yaml")  
        self.current_file_path = os.path.abspath(__file__) 
        self.project_root = os.path.dirname(self.current_file_path)  
        self.database_subfolder  = os.path.join(self.project_root, "database")
        self.args = self.parse_args() 
        self.current_page = 0
        self.token = self.check_token()

        logging.basicConfig(level=logging.INFO) 

        self.check_first_run()

    def parse_args(self):
        define_parser = argparse.ArgumentParser(description="Go through a bunch of repos in the awesome-list GitHub topic from your terminal!")
        define_parser.add_argument("--token", "-t", type=str, help="Save a RESTRICTIVELY SCOPED GitHub personal access token to your local config. Required so you can make API requests for specific repos.")     
        define_parser.add_argument("--database", "-d", type=str, default="most", choices=["most", "least", "newest", "oldest", "recently-updated", "least-recently-updated"], help="Which local database to use. Due to the GitHub API's limit of 1,000 results per request, multiple databases are retrieved by making separate requests based on different statistics (e.g., stars, forks) to ensure accurately sorted results across various categories.")
        define_parser.add_argument("--fetchDatabase", "-f", action="store_true", help="Downloads databases from the discover-awesome repository.")
        define_parser.add_argument("--buildDatabase", "-b", action="store_true", help="Build databases directly from the GitHub API.")
        
        return define_parser.parse_args() 

        
    def check_token(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f)

            # Check if config is None
            if config is None:
                logging.info("Config file is empty or invalid. Creating default configuration files.")
                self.create_first_run_files()  # Call the method to create default files
                return False  # Return False or handle as needed

            # Check if the token field exists and return its value
            if "token" in config:
                return config["token"]
            else:
                return False
        else:
            logging.error(f"Config file not found: {self.config_file}")
            self.create_first_run_files()  # Call the method to create default files
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
                config = yaml.safe_load(f) or {}  # Use an empty dict if None
        else:
            config = {"run": True}  

        if not isinstance(config, dict):
            logging.error("Config file is invalid. Resetting to default configuration.")
            config = {"run": True}  

        with open(self.config_file, "w") as f:
            yaml.dump(config, f)  # Dump the dictionary 

        for filename in os.listdir(self.database_subfolder):
            source_file = os.path.join(self.database_subfolder, filename)
            destination_file = os.path.join(self.user_dir, filename)
            shutil.copy(source_file, destination_file)

        logging.info(f"First run detected. Copied the pre-made database files to {self.user_dir}.")

    def supply_token(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f) or {}  # Load config or use an empty dict if None
        else:
            self.create_first_run_files()
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f) or {}  # Load config after creating files

        # Ensure config is a dictionary
        if not isinstance(config, dict):
            logging.error("Config file is invalid. Resetting to empty dictionary.")
            config = {}  # Reset to an empty dictionary if invalid
            
            
        if "token" not in config:
            config["token"] = self.args.token
        if "token" in config:
            config["token"] = self.args.token

        with open(self.config_file, "w") as f:
            yaml.dump(config, f)

        logging.info(f"Token written to {self.config_file}")

  
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
            self.showResults(self.path,0)
        else:
            raise ValueError('Somehow, an invalid database arg got through!')
    


    def showResults(self, path, page=0):
        with open(path, 'r') as file:
            data = json.load(file)

        limit = 10
        console = Console()
        total_entries = len(data)
        self.current_page = page
        total_pages = (total_entries + limit - 1) // limit  

        while True:
            start_index = self.current_page * limit
            end_index = start_index + limit

            # don't go out of bounds
            entries_to_display = data[start_index:end_index]

            table = Table(title="Discover Awesome", show_lines=True)
            table.add_column("Index", justify="right", style="bold cyan")
            table.add_column("Name", style="bold magenta")
            table.add_column("Description", style="green")  
            table.add_column("URL", style="cyan")


            for index, entry in enumerate(entries_to_display, start=start_index):
                name_display = entry.get('name', 'Unknown') 
                description_display = entry.get('description', 'No description') or 'No description'  # Handle None
                url_display = entry.get("url","no url")

                table.add_row(str(index + 1), name_display, description_display, url_display)

            console.clear()
            console.print(table)

            console.print(f"\nNavigation:  (q)uit | (n)ext | (p)revious")
            choice = Prompt.ask("Choose an option or index")

            if choice.lower() == 'q':
                break
            elif choice.lower() == 'n':
                if self.current_page < total_pages - 1:
                    self.current_page += 1
                else:
                    console.print("You are already on the last page.")
            elif choice.lower() == 'p':
                if self.current_page > 0:
                    self.current_page -= 1
                else:
                    console.print("You are already on the first page.")
            else:
                try:
                    selection = int(choice) - 1  # adjust for zero-based index
                    if 0 <= selection < total_entries:
                        selected_entry = data[selection]
                        entry_url = selected_entry.get("url", "no url")  # avoid KeyError
                        self.repository_picked(entry_url) 
                        break
                    else:
                        console.print("Invalid index. Please try again.")
                except RuntimeError:
                    console.print("Invalid input. Please enter a valid index or option.")

    def repository_picked(self,entryurl):

        url = entryurl
        get_readme(url,self.token)

        
    def modify_markdown(self,markdown_file):
        print("hi")
        
    def display_markdown(modified_markdown):
        print('hello')
        
    def run(self):
       if self.check_token():
           if self.args.buildDatabase:
               build_database_from_tag(self.args.buildDatabase)
           
           if self.args.token:
               self.supply_token()
               return  
           
           if self.args.fetchDatabase:
               self.fetch_database()
           
           self.choose_database()  
       else:
           if self.args.token:
               self.supply_token()
               return  
           else:
               logging.error("No token found in config. Please provide it with --token")

                    

if __name__ == "__main__":
    app = DiscoverAwesome()
    app.run()