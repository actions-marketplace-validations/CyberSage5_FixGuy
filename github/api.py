import os
import shutil
import git
from PyGithub import Github  # Changed from 'github' to 'PyGithub'

class GitHubHandler:
    """Handles GitHub API interactions."""
    
    def __init__(self, repo_url, token):
        self.repo_url = repo_url
        self.client = Github(token)
        self.repo_name = repo_url.split("github.com/")[-1].replace(".git", "")
        self.repo = self.client.get_repo(self.repo_name)
        self.token = token
    
    def clone_repo(self):
        """Clone the repo to a temporary directory."""
        clone_path = f"/tmp/fixguy_{self.repo_name.replace('/', '_')}"
        
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)
        
        auth_url = f"https://{self.token}:x-oauth-basic@github.com/{self.repo_name}.git"
        print(f"Cloning {self.repo_url} to {clone_path}")
        git.Repo.clone_from(auth_url, clone_path)
        
        return clone_path
    
    def create_pull_request(self, branch_name, title):
        """Create a PR with fixes."""
        base = self.repo.default_branch
        pr = self.repo.create_pull(title=title, body="Automated code fixes by FixGuy", head=branch_name, base=base)
        return pr.html_url
    
    def cleanup(self, clone_path):
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)