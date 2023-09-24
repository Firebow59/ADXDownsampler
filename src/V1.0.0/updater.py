import requests
import webbrowser
from tkinter import messagebox
import tkinter as tk
import sys

def print_github_error():
    print(f"Error: GitHub page unable to be reached.")
    sys.exit(0)

def check_for_new_version(owner, repo, current_version):
       try:
        repo_url = f"https://github.com/{owner}/{repo}"
        repo_response = requests.head(repo_url)
        if repo_response.status_code != 200:
            print(f"Error: GitHub repository not found, program cannot update.")
            sys.exit(0)
       except Exception as e:
        print_github_error()
       else:
         try:
          url = f"https://github.com/{owner}/{repo}/releases/latest"
          response = requests.get(url)
          response.raise_for_status()
         except requests.exceptions.RequestException as e:
          print_github_error()

         try:
          api_url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
          response = requests.get(api_url)
          if response.status_code == 200:
           release_info = response.json()
           latest_program_version = ''
           latest_program_version = release_info['tag_name']
         except requests.exceptions.RequestException as e:
          print_github_error()

         if f"/{current_version}" not in response.text:
          if current_version < latest_program_version:
           programupdate = tk.messagebox.askyesno(title='Program Update', message="A new update is available. Would you like to visit the GitHub page to download it?")
           if programupdate:
            webbrowser.open_new_tab(url)
         else:
          print("Program is at latest version")
          sys.exit(0)

def main():
    owner = "Firebow59"
    repo = "ADXDownsampler"
    current_version = "1.0.0"

    check_for_new_version(owner, repo, current_version)

if __name__ == "__main__":
    main()