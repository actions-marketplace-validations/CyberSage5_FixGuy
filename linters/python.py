import subprocess
import os

class PythonLinter:
    """Lints and fixes Python code."""
    
    def lint_directory(self, repo_path):
        """Run flake8 and return issues."""
        try:
            result = subprocess.run(
                ["flake8", repo_path, "--exit-zero", "--select=F841"],  # Only unused variables
                capture_output=True,
                text=True
            )
            return self.parse_flake8_output(result.stdout)
        except Exception as e:
            print(f"Linting failed: {e}")
            return []
    
    def parse_flake8_output(self, output):
        """Parse flake8 output into a list of issues."""
        issues = []
        for line in output.splitlines():
            if "F841" in line:  # Unused variable
                parts = line.split(":")
                file_path = parts[0]
                line_num = int(parts[1])
                message = ":".join(parts[3:]).strip()
                issues.append({"file": file_path, "line": line_num, "message": message})
        return issues
    
    def apply_fixes(self, repo_path, issues):
        """Remove unused variables from Python files."""
        if not issues:
            return
        
        for issue in issues:
            file_path = issue["file"]
            line_num = issue["line"] - 1  # Convert to 0-based index
            
            # Read the file
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            # Remove the line with the unused variable (basic approach)
            if 0 <= line_num < len(lines):
                lines.pop(line_num)
                print(f"Removed unused variable at {file_path}:{line_num + 1}")
            
            # Write back
            with open(file_path, "w") as f:
                f.writelines(lines)