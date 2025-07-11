import requests
import json
import os
import logging

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
                
                # Check if we have reached the maximum number of repositories or if there are no more pages
                if len(repositories) < request_params['per_page'] or len(all_repos) >= 1000:
                    break
                request_params['page'] += 1
            else:
                print(f"Error: {response.status_code} - {response.json().get('message')}")
                return []

        filtered_repos = [
            {
                'name': repo['name'],
                'description': repo.get('description'),
                'url': repo['html_url'],
                'author': repo['owner']['login'],
                'stars': repo['stargazers_count'],
                'updated_at': repo['updated_at'], 
                'created_at': repo['created_at'],
                'tags': repo.get('topics', []) 
            }
            for repo in all_repos[:1000] 
        ]
        
        save_to_file(filtered_repos, sort_by)

def save_to_file(data, sort_by):
    if sort_by == "most_stars":
        sorted_data = sorted(data, key=lambda x: x['stars'], reverse=True)
    elif sort_by == "least_stars":
        sorted_data = sorted(data, key=lambda x: x['stars'])
    elif sort_by == "newest":
        sorted_data = sorted(data, key=lambda x: x['created_at'], reverse=True)
    elif sort_by == "oldest":
        sorted_data = sorted(data, key=lambda x: x['created_at'])
    elif sort_by == "recently_updated":
        sorted_data = sorted(data, key=lambda x: x['updated_at'], reverse=True)
    elif sort_by == "least_recently_updated":
        sorted_data = sorted(data, key=lambda x: x['updated_at'])
    else:
        sorted_data = data  

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    filename = f'repositories_{sort_by}.json'
    file_path = os.path.join(script_dir, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)
    
    logging.info(f"repositories_{sort_by}.json created.")

if __name__ == "__main__":
    token = "" 
    build_database_from_tag(token)
