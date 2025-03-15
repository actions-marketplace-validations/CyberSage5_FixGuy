import subprocess
import os

class JavaScriptLinter:
    """Lints and fixes JavaScript/TypeScript code with eslint."""
    
    def lint_files(self, files):
        """Run eslint on JS/TS files."""
        try:
            result = subprocess.run(
                ["npx", "eslint", "--fix-dry-run", "--format", "json"] + files,
                capture_output=True,
                text=True
            )
            return self.parse_eslint_output(result.stdout)
        except Exception as e:
            print(f"ESLint failed: {e}")
            return []
    
    def parse_eslint_output(self, output):
        """Parse eslint JSON output."""
        import json
        issues = []
        try:
            data = json.loads(output)
            for file_data in data:
                for msg in file_data["messages"]:
                    if msg["ruleId"] == "no-unused-vars":
                        issues.append({
                            "file": file_data["filePath"],
                            "line": msg["line"],
                            "message": msg["message"]
                        })
        except json.JSONDecodeError:
            pass
        return issues
    
    def apply_fixes(self, files, issues):
        """Apply eslint fixes."""
        if issues:
            subprocess.run(["npx", "eslint", "--fix"] + [i["file"] for i in issues])