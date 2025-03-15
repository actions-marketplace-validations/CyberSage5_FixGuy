# FixGuy

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Build Status](https://github.com/CyberSage5/fixguy/actions/workflows/fixguy.yml/badge.svg)](https://github.com/CyberSage5/fixguy/actions/workflows/fixguy.yml)
[![GitHub release](https://img.shields.io/github/release/username/fixguy.svg)](https://github.com/CyberSage5/fixguy/releases)

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
      - uses: CyberSage5/fixguy@v1.0.1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
