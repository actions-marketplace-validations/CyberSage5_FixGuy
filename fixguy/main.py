#!/usr/bin/env python3
"""FixGuy: Automated code quality tool."""

import sys
from fixguy.github.api import GitHubHandler  # Corrected: use fixguy.github.api
from fixguy.linters.python import PythonLinter  # Already correct
from fixguy.utils.git import GitManager  # Already correct

class FixGuy:
    """Core FixGuy class to orchestrate linting and PR creation."""
    
    def __init__(self, repo_url, github_token):
        self.repo_url = repo_url
        self.github_token = github_token
        self.github = GitHubHandler(repo_url, github_token)
        self.git = GitManager()
        self.linter = PythonLinter()

    def run(self):
        """Main execution flow."""
        print(f"Starting FixGuy for {self.repo_url}")
        
        # Step 1: Clone or fetch the repo
        repo_path = self.github.clone_repo()
        
        # Step 2: Lint Python files
        issues = self.linter.lint_directory(repo_path)
        
        # Step 3: Apply fixes
        if issues:
            self.linter.apply_fixes(repo_path, issues)
            print(f"Fixed {len(issues)} issues")
        
        # Step 4: Commit and create PR
        if self.git.has_changes(repo_path):
            branch_name = self.git.commit_changes(repo_path, "Fix code quality issues")
            pr_url = self.github.create_pull_request(branch_name, "Automated fixes by FixGuy")
            print(f"PR created: {pr_url}")
        else:
            print("No changes to commit.")

def main():
    """Entry point for FixGuy."""
    if len(sys.argv) != 3:
        print("Usage: python -m fixguy.main <repo_url> <github_token>")
        sys.exit(1)
    
    repo_url = sys.argv[1]  # e.g., https://github.com/username/repo
    github_token = sys.argv[2]
    fixguy = FixGuy(repo_url, github_token)
    fixguy.run()

if __name__ == "__main__":
    main()