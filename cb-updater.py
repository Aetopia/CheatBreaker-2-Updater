from urllib.request import urlopen, urlretrieve
from tempfile import gettempdir
from shutil import unpack_archive, copytree, rmtree
from platform import system
from glob import glob
from json import load, dumps
from sys import exit
from pathlib import Path
from os import path
from ast import literal_eval
from sys import exit

url = 'https://api.github.com/repos/TellinqBreaker/CheatBreaker/releases'
profile_not_exist = True
temp = (f'{gettempdir()}/CheatBreaker.zip', f'{gettempdir()}/CheatBreaker')
if system() == 'Windows': mc_dir = f'{Path().home()}/AppData/Roaming/.minecraft'
else: mc_dir = f'{Path().home()}/.minecraft'  
json = load(urlopen(url))

print('Releases:')
for index, entry in enumerate(json):
    if entry['prerelease'] == True: type = 'Pre-Release'
    else: type = 'Release'
    print(f"{str(index+1).center(len(str(len(json)))).lstrip()} | {entry['name']} > {type}")

while True:
    try: entry = json[literal_eval(input('Select > '))-1]; break
    except KeyboardInterrupt: exit()

print(f"\nRelease Info > {entry['name']}:\n{entry['body']}".rstrip('\n'))
if len(entry['assets']) not in (0,1):
    print('\nFiles:')
    for index, asset in enumerate(entry['assets']):
        print(f"{str(index+1).center(len(str(len(entry['assets'])))).lstrip()} | {asset['name']}")
    while True:
        try:
            option = literal_eval(input('\nSelect > ').lower().strip())
            print(entry['assets'][option-1]['browser_download_url'])
            break
        except KeyboardInterrupt: exit() 
else: 
    while True:
        option = input('\nInstall? (Y/N) > ').lower().strip()
        if option in ('yes','y',''): file = entry['assets'][0]['browser_download_url']; break
        elif option in ('n','no'): exit() 

# Download and Install CheatBreaker 1.7.10
print(f'\nDownloading ({path.split(file)[1]})...')
urlretrieve(file, temp[0])
print('Extracting...')
if path.exists(temp[1]) and path.isdir(temp[1]): rmtree(temp[1]) 
unpack_archive(temp[0], temp[1])
folders = glob(f'{temp[1]}/*')
if len(folders) != 1:
    print('\nFolders:')
    for index, folder in enumerate(folders):
        if path.isdir(folder):
            print(f'{str(index+1).center(len(str(len(folders)))).lstrip()} | {path.split(folder)[1]}')
    while True:
        try:
            option = input('Select > ').lower().strip()
            folder = folders[literal_eval(option)-1]
            if path.isdir(folder) is False: continue
            with open(f'{glob(f"{folder}/*.json")[0]}') as version_json:
                version = load(version_json)['id']
                break
        except KeyboardInterrupt: exit()   
    print()    
else:
    folder = folders[0]
    for version_json_file in Path(temp[1]).rglob('*.json'):
        if path.isfile(version_json_file):
            with open(version_json_file) as version_json:
                version = load(version_json)['id']
                break
print(f"Copying ({version}) to (.minecraft)...")
copytree(folder, f'{mc_dir}/versions', dirs_exist_ok=True)

# Add a Cheatbreaker 1.7.10 Profile if it doesn't exist.
with open(f'{mc_dir}/launcher_profiles.json') as launcher_profiles:
    launcher_profiles = load(launcher_profiles)

for profile in tuple(launcher_profiles['profiles'].values()):
    if profile['lastVersionId'].lower() == version.lower(): profile_not_exist = False
if profile_not_exist:
    print(f'Making a Profile for ({version})...')
    launcher_profiles['profiles'][version] = {'created': '', 'icon': 'Furnace', 'lastUsed': '', 'lastVersionId': version, 'name': version, 'type': ''}
    with open(f'{mc_dir}/launcher_profiles.json', 'w') as file:
        file.write(dumps(launcher_profiles, indent=4))       
print('Installation Finished.')


