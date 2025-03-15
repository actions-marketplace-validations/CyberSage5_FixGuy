import subprocess
import os

class JavaLinter:
    """Lints and fixes Java code with checkstyle."""
    
    def lint_files(self, files):
        """Run checkstyle on Java files."""
        try:
            checkstyle_jar = "/usr/local/lib/checkstyle-10.17.0-all.jar"  # Assume installed
            result = subprocess.run(
                ["java", "-jar", checkstyle_jar, "-c", "/google_checks.xml"] + files,
                capture_output=True,
                text=True
            )
            return self.parse_checkstyle_output(result.stdout)
        except Exception as e:
            print(f"Checkstyle failed: {e}")
            return []
    
    def parse_checkstyle_output(self, output):
        """Parse checkstyle output (basic)."""
        issues = []
        for line in output.splitlines():
            if "UnusedLocalVariable" in line:
                parts = line.split(":")
                issues.append({"file": parts[0], "line": int(parts[1]), "message": line})
        return issues
    
    def apply_fixes(self, files, issues):
        """Stub for Java fixes (manual removal for now)."""
        for issue in issues:
            file_path = issue["file"]
            line_num = issue["line"] - 1
            with open(file_path, "r") as f:
                lines = f.readlines()
            if 0 <= line_num < len(lines):
                lines.pop(line_num)
            with open(file_path, "w") as f:
                f.writelines(lines)