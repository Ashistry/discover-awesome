import argparse
import logging
from api_calls import build_database_from_tag, fetch_database

def main():
    logging.basicConfig(level=logging.INFO)
    
    define_parser = argparse.ArgumentParser(description="Go through every repo (read: 1000 per Github API request sorting option) in the awesome-list GitHub topic from your terminal.")
    define_parser.add_argument('--database', '-d', type=str, default='most', choices=['most', 'least', 'newest','oldest'], help="Which local database to use. Default is most stars. This is different from --sortLocal in that the database type was requested by this stat from the API.")
    define_parser.add_argument('--sortLocal', '-s', type=str, default='most', choices=['most', 'least', 'newest','oldest'], help="Method of sorting chosen database. Default is most stars. This is different from --database in that this sorts your choice of requested-from-API-by-stat local database by the stat you've chosen.")
    define_parser.add_argument('--fetchDatabase','-f',action='store_true',help="Downloads databases from the discover-awesome repository.")
    define_parser.add_argument('--buildDatabase', '-b', type=str, required=True, help='Build all databases of repos directly from the Gihub API. Requires a personal access token to be passed wich does not need any special permissions.')

    args = define_parser.parse_args()        
        
    if args.buildDatabase:
        repositories = build_database_from_tag(args.buildDatabase)

    if args.fetchDatabase:
        fetch_database()
if __name__ == "__main__":
    main()
