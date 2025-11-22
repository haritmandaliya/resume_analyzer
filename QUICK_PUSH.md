# Quick Push Instructions

## Current Status ✅
- ✅ develop branch created and ready
- ✅ main branch ready
- ✅ All files committed
- ❌ Need authentication to push

## Fastest Method: Personal Access Token

### Step 1: Get Your Token (2 minutes)

1. Visit: **https://github.com/settings/tokens**
2. Click **"Generate new token (classic)"**
3. Name it: `Resume Analyzer`
4. Select scope: **✅ repo** (Full control of private repositories)
5. Click **"Generate token"**
6. **COPY THE TOKEN** immediately (you won't see it again!)

### Step 2: Push Branches

Open terminal in the project directory and run:

```bash
cd /home/harit/resume_analyzer

# Push develop branch
git checkout develop
git push -u origin develop
# When prompted for password, paste your TOKEN (not your GitHub password)

# Merge develop into main
git checkout main
git merge develop

# Push main branch
git push -u origin main
# When prompted for password, paste your TOKEN again
```

### Alternative: Use the Helper Script

```bash
./push_to_github.sh
```

Then follow the authentication prompts.

## Verify Success

After pushing, visit:
**https://github.com/haritmandaliya/resume_analyzer**

You should see:
- ✅ `main` branch
- ✅ `develop` branch
- ✅ All files present

## Troubleshooting

**If you get "403 Forbidden":**
- Make sure you copied the token correctly
- Ensure token has `repo` scope
- Try using the token in the URL: `git remote set-url origin https://YOUR_TOKEN@github.com/haritmandaliya/resume_analyzer.git`

**If you get "Permission denied":**
- Check that the token hasn't expired
- Regenerate a new token if needed

