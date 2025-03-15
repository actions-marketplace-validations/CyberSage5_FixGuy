import subprocess

class GoLinter:
    """Lints and fixes Go code with staticcheck."""
    
    def lint_files(self, files):
        """Run staticcheck on Go files."""
        try:
            result = subprocess.run(
                ["staticcheck"] + files,
                capture_output=True,
                text=True
            )
            return self.parse_staticcheck_output(result.stdout)
        except Exception as e:
            print(f"Staticcheck failed: {e}")
            return []
    
    def parse_staticcheck_output(self, output):
        """Parse staticcheck output."""
        issues = []
        for line in output.splitlines():
            if "unused" in line.lower():
                parts = line.split(":")
                issues.append({"file": parts[0], "line": int(parts[1]), "message": line})
        return issues
    
    def apply_fixes(self, files, issues):
        """Stub for Go fixes."""
        for issue in issues:
            file_path = issue["file"]
            line_num = issue["line"] - 1
            with open(file_path, "r") as f:
                lines = f.readlines()
            if 0 <= line_num < len(lines):
                lines.pop(line_num)
            with open(file_path, "w") as f:
                f.writelines(lines)