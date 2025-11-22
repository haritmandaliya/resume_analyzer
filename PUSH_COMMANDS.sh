#!/bin/bash
# Copy and paste these commands after getting your GitHub Personal Access Token

echo "🚀 Pushing Resume Analyzer to GitHub"
echo ""
echo "Step 1: Pushing develop branch..."
git checkout develop
git push -u origin develop

echo ""
echo "Step 2: Merging develop into main..."
git checkout main
git merge develop

echo ""
echo "Step 3: Pushing main branch..."
git push -u origin main

echo ""
echo "✅ Done! Check: https://github.com/haritmandaliya/resume_analyzer"
