from github import Github

class GitHubHandler:
    """Handles GitHub API interactions."""
    
    def __init__(self, repo_url, token):
        self.repo_url = repo_url
        self.client = Github(token)
        self.repo_name = repo_url.split("github.com/")[-1]
        self.repo = self.client.get_repo(self.repo_name)
    
    def clone_repo(self):
        """Clone the repo (stub for now)."""
        print(f"Cloning {self.repo_url}")
        return "/tmp/fixguy_repo"  # Placeholder path
    
    def create_pull_request(self, branch_name, title):
        """Create a PR with fixes."""
        base = self.repo.default_branch
        pr = self.repo.create_pull(title=title, body="Automated code fixes", head=branch_name, base=base)
        return pr.html_url