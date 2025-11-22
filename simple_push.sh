#!/bin/bash
# Simple script to push all files to GitHub

echo "🚀 Pushing Resume Analyzer to GitHub..."
echo ""
echo "📋 What will be pushed:"
echo "   - 39 files (all source code, configs, docs)"
echo "   - 7 commits (full project history)"
echo "   - Both 'develop' and 'main' branches"
echo ""
echo "⚠️  You'll need your GitHub Personal Access Token"
echo "   Get it from: https://github.com/settings/tokens"
echo ""
read -p "Press Enter when you have your token ready..."

# Push develop
echo ""
echo "📤 Pushing develop branch..."
git checkout develop
git push -u origin develop

if [ $? -eq 0 ]; then
    echo "✅ develop branch pushed!"
    
    # Push main
    echo ""
    echo "📤 Pushing main branch..."
    git checkout main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 SUCCESS! All files pushed to GitHub!"
        echo ""
        echo "🌐 View your repo: https://github.com/haritmandaliya/resume_analyzer"
    else
        echo "❌ Failed to push main branch"
    fi
else
    echo "❌ Failed to push develop branch"
    echo "💡 Make sure you used your TOKEN as password (not GitHub password)"
fi
