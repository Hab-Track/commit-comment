import sys
import os
from github import Github

# Typing stuff
from github.Repository import Repository
from github.Commit import Commit
from typing import Optional, Dict, List

# Utils stuff
from utils import status


def get_latest_commit(repo: Repository) -> Commit:
    return repo.get_commits()[0]

def get_previous_commit(commit: Commit) -> Optional[Commit]:
    return commit.parents[0] if commit.parents else None

def get_previous_files_dict(previous_commit: Optional[Commit]) -> Dict[str, any]:
    if previous_commit:
        return {file.filename: file for file in previous_commit.files}
    else:
        return {}   


@status.print_status("comparing")
def comment_on_diffs(repo: Repository, latest_commit: Commit, previous_commit: Optional[Commit], folder: Optional[str] = None) -> None:
    print("[DEBUG] Inside comment_on_diffs function")
    diff = repo.compare(previous_commit.sha, latest_commit.sha)
    print("[DEBUG] Diff retrieved")
    for file in diff.files:
        if not folder or file.filename.startswith(folder):
            print(f"[DEBUG] Processing file: {file.filename}")
            filtered_diff_lines = [line for line in file.patch.split('\n') if line.startswith('+') or line.startswith('-')]
            print("[DEBUG] Diff lines filtered")
            if filtered_diff_lines:
                comment_text = f"Modifications in {file.filename}:\n"
                comment_text += '\n'.join(filtered_diff_lines)
                latest_commit.create_comment(body=comment_text)
                print(f"Commented diff for {file.filename}")
            else:
                print(f"No diff lines found for {file.filename}")


def main() -> None:
    github_token: str = os.environ['GITHUB_TOKEN']
    repository_name: str = os.environ['GITHUB_REPOSITORY']

    g: Github = Github(github_token)
    repo: Repository = g.get_repo(repository_name)

    latest_commit: Commit = get_latest_commit(repo)
    previous_commit: Optional[Commit] = get_previous_commit(latest_commit)

    folder: Optional[str] = sys.argv[1] if len(sys.argv) > 1 else None

    comment_on_diffs(repo, latest_commit, previous_commit, folder)

if __name__ == "__main__":
    main()
