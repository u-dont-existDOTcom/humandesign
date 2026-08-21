# Push this project to your `humandesign` GitHub repo

From a terminal with GitHub credentials configured:

```bash
unzip humandesign_repo_ready.zip
cd humandesign_repo_ready
git init
git add .
git commit -m "Add Human Design reverse-matching research plan"
git branch -M main
git remote add origin <YOUR_HUMANDESIGN_REPO_URL>
git push -u origin main
```

If the repo already contains files, clone it first, copy the contents of `humandesign_repo_ready/` into the clone, then commit and push normally rather than force-pushing.

Do not commit secret blind-test answer keys. `.gitignore` is already configured to exclude common answer-key and secret paths.
