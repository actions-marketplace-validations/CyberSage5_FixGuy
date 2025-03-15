# FixGuy

Automated code quality fixes for Python, JavaScript, TypeScript, Java, and Go.

## Usage

Add this workflow to your repo in `.github/workflows/fixguy.yml`:

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
      - uses: username/fixguy@main  # Replace with your repo
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}