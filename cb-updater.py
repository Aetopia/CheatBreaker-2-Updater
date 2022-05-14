from urllib.request import urlopen, urlretrieve
from tempfile import gettempdir
from shutil import unpack_archive, copytree
from platform import system
from glob import glob
from json import load, dumps
from sys import exit
from pathlib import Path
from os import path
from getpass import getpass

url = 'https://api.github.com/repos/TellinqBreaker/CheatBreaker/releases'
file = load(urlopen(url))[0]['assets'][0]['browser_download_url']
temp = (f'{gettempdir()}/CheatBreaker.zip', f'{gettempdir()}/CheatBreaker')
if '1.7.10' not in file:
    exit()
if system() == 'Windows': mc_dir = f'{Path().home()}/AppData/Roaming/.minecraft'
else: mc_dir = f'{Path().home()}/.minecraft'  

# Download and Install CheatBreaker 1.7.10
print('Downloading the latest CheatBreaker 2 Release...')
urlretrieve(file, temp[0])
print('Unpacking Release...')
unpack_archive(temp[0], temp[1])
print("Copying CheatBreaker 2's files to .minecraft's versions folder...")
copytree(path.dirname(tuple(Path(glob(temp[1])[0]).rglob('*'))[0]), f'{mc_dir}/versions', dirs_exist_ok=True)

# Add a Cheatbreaker 1.7.10 Profile if it doesn't exist.
with open(f'{mc_dir}/launcher_profiles.json') as launcher_profiles:
    launcher_profiles = load(launcher_profiles)
    profile_not_exist = False    
for profile in tuple(launcher_profiles['profiles'].values()):
    if 'cheatbreaker-1.7.10' != profile['lastVersionId'].lower(): profile_not_exist = True
    else: profile_not_exist = False;break
if profile_not_exist:
    print('Making a Profile for Cheatbreaker 2...')
    launcher_profiles['profiles']['CheatBreaker 1.7.10'] = {'created': '', 'icon': 'Furnace', 'lastUsed': '', 'lastVersionId': 'CheatBreaker-1.7.10', 'name': 'CheatBreaker 1.7.10', 'type': ''}
    with open(f'{mc_dir}/launcher_profiles.json', 'w') as file:
        file.write(dumps(launcher_profiles, indent=4))   
print('Installation finished.')
getpass('\nPress Enter to exit.')


