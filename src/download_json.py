import requests
import concurrent.futures
import json
import util


config = json.loads(open(util.get_rel_path('conf'), 'r').read())
util.create_dir(util.get_rel_path(config["data_path"]))
util.create_dir(util.get_rel_path(config["json_path"]))
util.create_dir(util.get_rel_path(config["db_path"]))


# Function to download a file
def download_file(uri, file_name):
    try:
        response = requests.get(uri)
        # Only create file if response content is not empty
        if response.status_code == 200 and response.content:
            with open(util.get_rel_path(util.get_rel_path(config["json_path"])) + file_name, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {file_name}")
        else:
            print(f"No content or error for {file_name}")
    except Exception as e:
        # Print the error message and return
        print(f"Error while downloading {file_name}: {e}")

names = config["file_list"].split(',')

# Create a thread pool executor
with concurrent.futures.ThreadPoolExecutor(max_workers=config["max_workers"]) as executor:
    # Iterate through each name and year-month combination
    for name in names:
        for year in range(2020, 2024):
            for month in range(1, 13):
                # Format the URI and file name
                uri = f"https://oss.x-lab.info/open_digger/github/{name}/project_openrank_detail/{year}-{month:02d}.json"
                file_name = f"{name}.{year}-{month}.json".replace('/', '-')

                # Submit the download task to the thread pool
                executor.submit(download_file, uri, file_name)