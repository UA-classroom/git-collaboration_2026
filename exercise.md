# Collaborating with Git

Collaborating using git can be done in many ways. In almost all strategies, even when working on a project alone, you should use branches. Branches allow us to copy our code and create another version of it, which we later can choose to discard, or to merge with our main branch.

Advanced usage of git usually involves:

- branches
- using forks (not necessary, but it is one of several strategies)
- pull requests (this is used for most strategies)
- merging one branch into another
- git pull (updating your local repository with the latest changes in the remote repository)

Creating branches is usually quite straightforward. The biggest challenge for beginners is usually merge conflicts, which occur when we attempt to merge branches or use git pull.

## Strategies

I suggest reading this article on the git feature branch workflow, a battle-tested way of working with git on bigger projects: https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow

A lot of companies and developers use this workflow, but there are other workflows such as the forking workflow, etc. I strongly recommend the feature workflow for beginners.

### Git Feature Branch Workflow Summarized / TLDR:

1. Create a repository
2. You generally have one or two "core" branches. The *main* branch will be your production branch, which means this is the most essential branch that should try not to introduce bugs. A lot of companies use a second branch called *staging* or *dev* - the idea is that dev/staging serves as a testing ground before finally merging the changes into main. For now, let's not use a staging branch and instead just use one main branch as our primary branch.
3. You create feature branches, or branches dedicated to a person (but mostly feature branches)
4. You perform changes on your branch, make a commit, and if needed push it to the cloud/GitHub. At that point, you can visit [github.com](http://github.com/) and create a pull request.
5. If needed, other people should review the pull request and the code submitted. Once ready, you will merge the pull request. At that point, you can choose if you want to delete the feature branch or keep it. You can always delete it later if you start amassing too many branches.

## Best Practices for Commits

Before we start the exercise, let's discuss some best practices for creating commits:

### Atomic Commits

An "atomic" commit means making a commit that includes changes related to a single feature, fix, or improvement. Benefits include:

- Easier to understand the purpose of each commit
- Simpler to revert specific changes if needed
- Makes code reviews more manageable
- Clearer project history

### Writing Good Commit Messages

A good commit message should:

- Be concise but descriptive (aim for 50 characters or less in the subject line)
- Use the imperative mood ("Add feature" not "Added feature")
- Include a more detailed explanation in the body if needed (separated from subject by a blank line)
- Reference issue numbers if applicable

Example:

```
Add user authentication feature

- Implement login/logout functionality
- Add password hashing
- Create session management
- Relates to issue #42

```

## Exercise

Collaborating means you need to be comfortable with branches and merging. Let's focus on that, and then continue with merging and pull requests.

You can use this repository to practice: https://github.com/UA-classroom/git-collaboration-1 - click on "use as template", and create a new repository - this will copy the repo and make it your own. You can also just create your own repository with some code.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2fb79146-c153-402e-a883-d44deb3c9cb1/ac6a5979-cc8b-4623-9e76-54256ed5a04f/Untitled.png)

### Creating a Branch

This will create a branch called *mynewbranch* (the -c means create) and switches to it:

```bash
git switch -c mynewbranch

```

Note: If you're using an older version of Git (before 2.23), use this command instead:

```bash
git checkout -b mynewbranch

```

Make it a habit to check what branch you are on before you start working:

```bash
git branch

```

Let's move back to the main branch:

```bash
git switch main

```

And then back to the new branch again:

```bash
git switch mynewbranch

```

Creating a branch means copying the current branch and creating a new version of it, with the exact same git history as the other branch.

### Using Git Stash

Sometimes you need to switch branches but aren't ready to commit your changes yet. This is where `git stash` becomes useful:

```bash
# Make some changes to your files...

# Stash your changes
git stash save "Work in progress on feature X"

# Now you can switch branches without committing
git switch main

# Do whatever you need on main...

# Switch back to your feature branch
git switch mynewbranch

# Apply your stashed changes
git stash apply

```

You can list all stashes with:

```bash
git stash list

```

And you can apply a specific stash with:

```bash
git stash apply stash@{0}

```

### Make Changes to a Branch

Make some changes to your code, then commit:

```bash
git add .
git commit -m "changes to my new branch"

```

At this point, your commit is still only local to your computer. Nothing has been pushed to GitHub yet. You can confirm this by going to GitHub and checking if any new branch has been created - the answer is no.

Let's merge the changes of this branch to our main branch:

1. We switch to the main branch
2. We merge the new branch INTO the main branch

```bash
git switch main
git merge mynewbranch

```

Good job, you merged commits made in the feature branch into your main branch, assuming you didn't have any conflicts (which you shouldn't have if you followed my steps).

Now let's actually push these changes to GitHub.

While you are on the main branch, do this:

```bash
git push

```

Let's create another branch, let's call it secondbranch:

```bash
git switch -c secondbranch

```

Make some changes to it, e.g., adding some code.

```bash
git add .
git commit -m "changes to second branch"

```

Now, let's actually push these changes to GitHub - meaning we will actually create this branch in the cloud.

The recommended approach for pushing a new branch is:

```bash
git push -u origin secondbranch

```

The `-u` (or `--set-upstream`) flag sets up tracking, so next time you can simply run `git push` without specifying the branch.

If you run just `git push` without parameters for a new branch, Git will show an error message with the full command you need to use:

```bash
git push --set-upstream origin secondbranch

```

Good! Now the branch exists in the cloud/on GitHub.

### Understanding Git Pull vs Git Fetch + Git Merge

Before we move on to pull requests, it's important to understand the difference between:

1. `git pull`: This is a combination of two commands in one - it does a `git fetch` followed by a `git merge`.
2. `git fetch`: Downloads commits, files, and refs from a remote repository into your local repo, but it doesn't automatically merge any changes into your working files.
3. `git merge`: Integrates changes from another branch into your current branch.

When you run `git pull`, you're doing both operations at once, which can be convenient but sometimes less clear about what's happening. For more control, you can run:

```bash
git fetch origin  # Get the latest changes from remote without merging
git status        # See how your branch relates to the remote branch
git merge origin/main  # Merge the fetched changes into your branch

```

This approach gives you a chance to see what's changed before you merge.

### Pull Request: Complete Process

A pull request is a formal way of merging a set of commits from one branch to another. It enables code reviews and discussions before changes are merged into the main codebase.

Let's go through the complete pull request workflow:

### 1. Create a Pull Request on GitHub

After pushing your branch to GitHub:

1. Go to your repository on GitHub
2. You'll often see a notification about your recently pushed branch with a "Compare & pull request" button. Click it.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2fb79146-c153-402e-a883-d44deb3c9cb1/3204f585-01af-4338-a081-72c7781c9355/Untitled.png)

1. Alternatively, you can go to the "Pull requests" tab and click "New pull request"
2. Select the base branch (where you want to merge to, usually "main") and the compare branch (your feature branch, e.g., "secondbranch")
3. Click "Create pull request"
4. Add a descriptive title and detailed description of your changes
5. Include any relevant information for reviewers, such as:
    - What the changes do
    - Why they're needed
    - How to test them
    - Any related issues or tickets
6. Click "Create pull request" again to finalize

### 2. Code Review Process

Once the pull request is created:

1. Assigned reviewers will receive notifications (you can manually add reviewers in the right sidebar)
2. Reviewers can:
    - Comment on specific lines of code
    - Suggest changes
    - Approve the pull request
    - Request changes
3. You can respond to comments and make additional commits to address feedback
4. New commits pushed to the same branch will automatically appear in the pull request
5. Discussions can continue until all concerns are addressed

### 3. Merging the Pull Request

When the pull request is approved and ready to merge:

1. Click the "Merge pull request" button
2. Choose a merge method:
    - **Create a merge commit**: Preserves all commits from your branch as separate commits in the history
    - **Squash and merge**: Combines all your changes into a single commit
    - **Rebase and merge**: Applies your changes as if they were made directly on the base branch
3. Confirm the merge
4. You'll be given the option to delete the branch after merging (recommended for feature branches)

### 4. Post-Merge Cleanup

After merging the pull request:

1. If you didn't delete the branch on GitHub, consider doing so now
2. Back in your local repository, update your main branch:
    
    ```bash
    git switch main
    git pull
    
    ```
    
3. Delete the local feature branch when no longer needed:
    
    ```bash
    git branch -d secondbranch
    
    ```
    

### Merge Conflicts

A merge conflict occurs when the branch you're currently on tries to merge commits from another branch, and it turns out that both branches have modified the same lines of code or the same locations. In this situation, Git doesn't know which change should apply - the change in the commit made on main, or in this case, the commit made on secondbranch.

Let's say you create a feature branch - in this case, we already have our secondbranch.

When you created the secondbranch, the code in the first file looked like this:

first.py

```python
def myfirstfunc():
    print("hello")

```

Make a change so it looks like this:

```python
def myfirstfunc():
    print("newnewnewsecond")
    print("hello")
    print("newnewnewsecond")

```

Then make a commit:

```bash
git add .
git commit -m "change firstfunc in second branch"

```

Don't push the change yet. Instead, switch back to main and change the code in the same function, but with something different:

```bash
git switch main

```

Change the code in first.py:

```python
def myfirstfunc():
    print("mainmainmain")
    print("hello")
    print("mainmainmain")

```

Make a commit (i.e., now we're modifying the main branch before we've had a chance to merge what's coming from secondbranch):

```bash
git add .
git commit -m "update main branch first func"

```

### Triggering a Merge Conflict

Now that both branches have changed the same lines of code, a merge conflict will occur.

While you're in the main branch (double-check by running git branch):

```bash
git branch # looks ok
git merge secondbranch

```

A merge conflict has now occurred.

You have several options, but generally you'll be interested in:

1. **Accept incoming change** (i.e., accept the changes made in the branch you're trying to merge FROM, in this case we're merging from secondbranch, so we want to use the code from the commit made on secondbranch)
2. **Accept current change** (i.e., accept the commit/changes made on your current branch, in this case main)
3. **Accept both changes** (keep changes from both branches)
4. **Compare changes** (see side-by-side differences)

### Resolving with Visual Tools

Most modern code editors like VSCode offer visual tools for resolving merge conflicts:

1. In VSCode, you'll see conflict markers in the file
2. Above the conflict, you'll see buttons for the different resolution options
3. Click the option you want, or manually edit the file to resolve the conflict
4. Save the file once you're satisfied with the resolution

You can see on the right side if you have multiple merge conflicts and scroll down to them, or you can click on source control in VSCode's left panel.

Once you've handled all merge conflicts in all files, you can make a commit and push it:

```bash
git add .
git commit -m "resolve conflicts"
git push

```

Now it's visible on GitHub - you've merged the changes!

### Git Pull Origin - Getting Changes from Another Branch

Sometimes you might be working on a feature branch, and your colleague decides to update the main branch. You realize you want to incorporate the changes from main into your branch, so you can work from that code instead of the old code from when you created the branch with switch -c.

Given that you're on secondbranch, for example, you can run:

```bash
git pull origin main

```

This command does two things:

- Git will fetch the latest changes from the main branch on the remote repository
- Git will try to merge those changes into your current branch (secondbranch)

If there are conflicts, you'll need to resolve them as described above.

This is a very useful command when you know someone has pushed changes to a certain branch remotely / to the cloud / to GitHub, and you want to work with these changes in your own branch.

## Additional Git Commands and Tips

### Setting Up a .gitignore File

A `.gitignore` file specifies files that Git should ignore. This is crucial for collaboration to avoid committing:

- Build artifacts
- Dependencies
- Local configuration files
- Log files
- Personal IDE settings

Create a `.gitignore` file in your repository root with patterns like:

```
# Build artifacts
/build/
/dist/

# Dependencies
/node_modules/
/venv/

# Local config
.env
config.local.js

# Logs
*.log

# IDE files
.idea/
.vscode/
*.sublime-project

```

### Troubleshooting Common Git Issues

### "Your local changes would be overwritten by merge"

```bash
# Option 1: Stash your changes
git stash
git pull
git stash pop

# Option 2: Commit your changes
git commit -m "Work in progress"
git pull

```

### "Cannot pull with rebase: You have unstaged changes"

```bash
git stash
git pull --rebase
git stash pop

```

### "Failed to push some refs"

```bash
git pull
# Resolve any conflicts
git push

```

### Accidentally committed to the wrong branch

```bash
# Get the commit hash
git log -1

# Checkout the correct branch
git switch correct-branch

# Apply the commit to the current branch
git cherry-pick <commit-hash>

# Go back to the wrong branch and remove the commit
git switch wrong-branch
git reset --hard HEAD~1

```

### Want to undo the last commit but keep the changes

```bash
git reset --soft HEAD~1

```