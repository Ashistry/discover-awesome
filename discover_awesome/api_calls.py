import requests
import json
import os
import logging
from appdirs import user_data_dir
import base64

logging.basicConfig(level=logging.INFO)


def build_database_from_tag(token):
    url = "https://api.github.com/search/repositories"
    query = "topic:awesome-list"
    
    sort_options = {
        "most_stars": {'sort': 'stars', 'order': 'desc'},
        "least_stars": {'sort': 'stars', 'order': 'asc'},
        "newest_created": {'sort': 'created', 'order': 'desc'},
        "oldest_created": {'sort': 'created', 'order': 'asc'},
        "recently_updated": {'sort': 'updated', 'order': 'desc'},
        "least_recently_updated": {'sort': 'updated', 'order': 'asc'}
    }

    for sort_by, params in sort_options.items():
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'

        request_params = {
            'q': query,
            'sort': params['sort'],
            'order': params['order'],
            'per_page': 100,
            'page': 1
        }

        all_repos = [] 

        while True:
            response = requests.get(url, params=request_params, headers=headers)
            
            if response.status_code == 200:
                repositories = response.json().get('items', [])
                all_repos.extend(repositories) 
                
                # check if we have reached the maximum number of repositories or if there are no more pages
                if len(repositories) < request_params['per_page'] or len(all_repos) >= 1000:
                    break
                request_params['page'] += 1
            else:
                print(f"Error: {response.status_code} - {response.json().get('message')}")
                return []

        filtered_repos = []
        
        for repo in all_repos[:1000]:
            default_branch = repo.get('default_branch', 'main')  # fallback to 'main' if not found
            raw_url = f"https://raw.githubusercontent.com/{repo['owner']['login']}/{repo['name']}/{default_branch}"
            filtered_repos.append({
                'name': repo['name'],
                'description': repo.get('description'),
                'url': repo['html_url'],
                'raw_url': raw_url,  
                'author': repo['owner']['login'],
                'stars': repo['stargazers_count'],
                'updated_at': repo['updated_at'], 
                'created_at': repo['created_at'],
                'tags': repo.get('topics', []),
                'default_branch': default_branch 
            })

        save_to_file(filtered_repos, sort_by)

def save_to_file(data, sort_by):
    if sort_by == "most_stars":
        sorted_data = sorted(data, key=lambda x: x['stars'], reverse=True)
    elif sort_by == "least_stars":
        sorted_data = sorted(data, key=lambda x: x['stars'])
    elif sort_by == "newest_created":
        sorted_data = sorted(data, key=lambda x: x['created_at'], reverse=True)
    elif sort_by == "oldest_created":
        sorted_data = sorted(data, key=lambda x: x['created_at'])
    elif sort_by == "recently_updated":
        sorted_data = sorted(data, key=lambda x: x['updated_at'], reverse=True)
    elif sort_by == "least_recently_updated":
        sorted_data = sorted(data, key=lambda x: x['updated_at'])
    else:
        sorted_data = data  

    app_name = 'discover-awesome' 
    target_dir = user_data_dir(app_name)

    os.makedirs(target_dir, exist_ok=True)

    filename = f'repositories_{sort_by}.json'
    file_path = os.path.join(target_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)
    
    logging.info(f"{filename} created in {target_dir}.")
    
    

def fetch_database(folder_path, token):
    os.makedirs(folder_path, exist_ok=True)

    file_names = [
        "repositories_least_recently_updated.json",
        "repositories_least_stars.json",
        "repositories_most_stars.json",
        "repositories_newest_created.json",
        "repositories_oldest_created.json",
        "repositories_recently_updated.json"
    ]


    url_dict = {
        file_name: f'https://raw.githubusercontent.com/Ashistry/discover-awesome/main/discover_awesome/database/{file_name}'
        for file_name in file_names
    }

    headers = {
        'Authorization': f'token {token}' 
    }
    
    # Loop through the dictionary and download each file
    for file_name, file_url in url_dict.items():
        file_path = os.path.join(folder_path, file_name)

        # Download the file with headers
        response = requests.get(file_url, headers=headers)
        print(file_ur)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded: {file_name} and moved it to: {folder_path}')
        else:
            print(f'Failed to download {file_name}: {response.status_code}')
        

        
def get_readme(url, token):
    
    #logging.basicConfig(level=logging.debug)

    readme_options = [
        os.path.join(url, "README"),
        os.path.join(url, "readme"),
        os.path.join(url, "README.MD"),
        os.path.join(url, "README.md"),
        os.path.join(url, "readme.md"),
    ]

    headers = {'Authorization': f'token {token}'}
    print(url)

    for url in readme_options:
        response = requests.get(url, headers=headers)  


        if response.status_code == 200:
            logging.debug(f"Successfully retrieved README from: {url}")
            target_dir = user_data_dir('discover-awesome')
            os.makedirs(target_dir, exist_ok=True)
            file_path = os.path.join(target_dir, 'cache.md')

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)  
            return file_path  
            
        else:
            logging.debug(f"Failed to retrieve from {url}. Status code: {response.status_code}")
    
    return None  

