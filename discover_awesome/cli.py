import argparse
import logging
from api_call import build_database_from_tag

def main():
    logging.basicConfig(level=logging.INFO)
    
    define_parser = argparse.ArgumentParser(description="Go through every repo (read: 1000 per Github API request sorting option) in the awesome-list GitHub topic from your terminal.")
    define_parser.add_argument('--database', '-d', type=str, default='most', choices=['most', 'least', 'newest','oldest'], help="Which local database to use. Default is most stars. This is different from --sortLocal in that the database type was requested by this stat from the API.")
    define_parser.add_argument('--sortLocal', '-s', type=str, default='most', choices=['most', 'least', 'newest','oldest'], help="Method of sorting chosen database. Default is most stars. This is different from --database in that this sorts your choice of local database by the stat you've chosen.")
    define_parser.add_argument('--fetchDatabase','-f',action='store_true',help="Checks for a newer copy of the databases in the discover-awesome repo. If found, they are downloaded.")
    define_parser.add_argument('--buildDatabase', '-b', type=str, required=True, help='Build all databases of repos directly from the Gihub API. Requires a personal access token to be passed wich does not need any special permissions.')

    args = define_parser.parse_args()

    def buildDatabase(args):
        repositories = build_database_from_tag(args.buildDatabase)
        
        
    if args.buildDatabase:
        buildDatabase(args)

    
if __name__ == "__main__":
    main()
