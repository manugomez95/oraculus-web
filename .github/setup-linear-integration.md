# Setup Linear Integration

Follow these steps to enable automatic Linear + GitHub synchronization:

## 1. Create Linear API Key

1. Go to [Linear Settings](https://linear.app/settings/api)
2. Click "Create new key" 
3. Name it: `GitHub Actions - Oraculus`
4. Copy the generated API key

## 2. Add GitHub Secret

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `LINEAR_API_KEY`
5. Value: Paste your Linear API key from step 1
6. Click "Add secret"

## 3. Test the Integration

Create a test PR to verify everything works:

```bash
# Create test branch
git checkout -b test/man-33-integration-test

# Make a small change
echo "# Integration Test" >> test.md
git add test.md
git commit -m "test: Verify Linear integration (MAN-33)"

# Push and create PR
git push -u origin test/man-33-integration-test
gh pr create --title "test: Verify Linear Integration (MAN-33)" --body "Testing automated Linear sync"
```

## 4. Verify Results

Check that:
- ✅ PR has a comment linking to Linear issue
- ✅ Linear issue MAN-33 status changed to "In Review"
- ✅ When you merge the PR, Linear issue becomes "Done"

## 5. Clean Up Test

After verification:
```bash
gh pr close test/man-33-integration-test
git checkout main
git branch -D test/man-33-integration-test
```

## Security Notes

- API key is stored securely in GitHub secrets
- Workflow only runs on your repository
- Linear API access is limited to your workspace

## Support

If you encounter issues:
1. Check GitHub Actions logs
2. Verify Linear API key permissions
3. Ensure Linear issue IDs follow MAN-XX format