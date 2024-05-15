import sys
from github import Github
import os

from utils import status


def get_latest_commit(repo):
    return repo.get_commits()[0]


def get_previous_commit(commit):
    return commit.parents[0] if commit.parents else None


def get_previous_files_dict(previous_commit):
    if previous_commit:
        return {file.filename: file for file in previous_commit.files}
    else:
        return {}


@status.print_status("comparing")
def comment_on_diffs(repo, latest_commit, previous_commit, folder=None):
    files = latest_commit.files
    for file in files:
        if not folder or file.filename.startswith(folder):
            diff = repo.compare(previous_commit.sha, latest_commit.sha)
            filtered_diff_lines = [line for line in diff.diff.split('\n') if line.startswith('+') or line.startswith('-')]
            if filtered_diff_lines:
                comment_text = f"Modifications in {file.filename}:\n"
                comment_text += '\n'.join(filtered_diff_lines)
                latest_commit.create_comment(body=comment_text)
                print(f"Commented diff for {file.filename}")


def main():
    github_token = os.environ['GITHUB_TOKEN']
    repository_name = os.environ['GITHUB_REPOSITORY']

    g = Github(github_token)
    repo = g.get_repo(repository_name)

    latest_commit = get_latest_commit(repo)
    previous_commit = get_previous_commit(latest_commit)

    folder = sys.argv[1] if len(sys.argv) > 1 else None

    comment_on_diffs(repo, latest_commit, previous_commit, folder)


if __name__ == "__main__":
    main()
