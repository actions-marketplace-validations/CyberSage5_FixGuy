#!/usr/bin/env python3
"""FixGuy: Automated code quality tool."""

import sys
import os
from fixguy.github.api import GitHubHandler
from fixguy.linters.python import PythonLinter
from fixguy.linters.javascript import JavaScriptLinter  # New
from fixguy.linters.java import JavaLinter  # New
from fixguy.linters.go import GoLinter  # New
from fixguy.utils.git import GitManager

class FixGuy:
    """Core FixGuy class to orchestrate linting and PR creation."""
    
    SUPPORTED_LANGUAGES = {
        ".py": PythonLinter,
        ".js": JavaScriptLinter,
        ".ts": JavaScriptLinter,  # TypeScript uses eslint too
        ".java": JavaLinter,
        ".go": GoLinter
    }
    
    def __init__(self, repo_url, github_token):
        self.repo_url = repo_url
        self.github_token = github_token
        self.github = GitHubHandler(repo_url, github_token)
        self.git = GitManager()
        self.linters = {ext: linter() for ext, linter in self.SUPPORTED_LANGUAGES.items()}

    def scan_files(self, repo_path):
        """Scan repo for supported file types."""
        files_by_lang = {ext: [] for ext in self.SUPPORTED_LANGUAGES}
        for root, _, files in os.walk(repo_path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in files_by_lang:
                    files_by_lang[ext].append(os.path.join(root, file))
        return files_by_lang

    def run(self):
        """Main execution flow."""
        print(f"Starting FixGuy for {self.repo_url}")
        
        # Clone the repo
        repo_path = self.github.clone_repo()
        
        # Scan for files
        files_by_lang = self.scan_files(repo_path)
        
        # Lint and fix each language
        all_issues = {}
        for ext, files in files_by_lang.items():
            if files:
                linter = self.linters[ext]
                issues = linter.lint_files(files)
                if issues:
                    linter.apply_fixes(files, issues)
                    all_issues[ext] = issues
                    print(f"Fixed {len(issues)} issues in {ext} files")
        
        # Commit and create PR if changes exist
        if self.git.has_changes(repo_path):
            branch_name = self.git.commit_changes(repo_path, "Fix code quality issues across languages")
            pr_url = self.github.create_pull_request(branch_name, "Automated fixes by FixGuy")
            print(f"PR created: {pr_url}")
        else:
            print("No changes to commit.")
        
        # Cleanup
        self.github.cleanup(repo_path)

def main():
    """Entry point for FixGuy."""
    if len(sys.argv) != 3:
        print("Usage: python -m fixguy.main <repo_url> <github_token>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    github_token = sys.argv[2]
    fixguy = FixGuy(repo_url, github_token)
    fixguy.run()

if __name__ == "__main__":
    main()