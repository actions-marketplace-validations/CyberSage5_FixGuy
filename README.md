# FixGuy

Automated code quality fixes for Python, JavaScript, TypeScript, Java, and Go.

## Usage

Add this to your `.github/workflows/fixguy.yml`:
```yaml
name: Run FixGuy
on:
  schedule:
    - cron: "0 0 * * 0"  # Weekly on Sunday
  workflow_dispatch:
jobs:
  fixguy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: username/fixguy@v1.0.0  # Repo stays username/fixguy
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}