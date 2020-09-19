#!/usr/bin/env bash
find ./ -not -path "./data/*" -not -path "./__pycache__/*" -not -path "./output/*" -not -path "./resourses/images/*" -not -path "./README.md" -not -path "./LICENSE" -not -path "./.git/*" -not -path "./.vscode/*" -type f | xargs wc -l
