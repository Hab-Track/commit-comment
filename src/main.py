import sys
from github import Github
import os

github_token = os.environ['GITHUB_TOKEN']
repository_name = os.environ['GITHUB_REPOSITORY']

g = Github(github_token)

repo = g.get_repo(repository_name)

latest_commit = repo.get_commits()[0]

files = latest_commit.files

previous_commit = latest_commit.parents[0] if latest_commit.parents else None

previous_files_dict = {file.filename: file for file in previous_commit.files} if previous_commit else {}

folder = sys.argv[1] if len(sys.argv) > 1 else None

for file in files:
    if not folder or file.filename.startswith(folder):
        if previous_file := previous_files_dict.get(file.filename):
            diff = repo.compare(previous_commit.sha, latest_commit.sha)
            filtered_diff_lines = [line for line in diff.diff.split('\n') if line.startswith('+') or line.startswith('-')]
            
            comment_text = f"Modifications in {file.filename} :\n"
            comment_text += '\n'.join(filtered_diff_lines)
            comment = latest_commit.create_comment(body=comment_text)
