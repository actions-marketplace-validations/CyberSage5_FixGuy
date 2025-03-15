import git

class GitManager:
    """Handles Git operations."""
    
    def __init__(self):
        self.repo = None
    
    def has_changes(self, repo_path):
        """Check if there are uncommitted changes."""
        self.repo = git.Repo(repo_path)
        return self.repo.is_dirty()
    
    def commit_changes(self, repo_path, message):
        """Commit changes to a new branch."""
        self.repo = git.Repo(repo_path)
        branch_name = f"fixguy-{int(__import__('time').time())}"
        self.repo.git.checkout("-b", branch_name)
        self.repo.git.add(".")
        self.repo.git.commit(m=message)
        self.repo.git.push("origin", branch_name)
        return branch_name