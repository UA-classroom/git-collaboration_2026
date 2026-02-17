# Collaborating with Git - A realistic demo

This demo simulates two developers (ua-tobias and Tobeyforce) collaborating on a FastAPI project using the feature branch workflow. You control both accounts to show students how real teamwork with git looks. You can just replace the users with your own usernames (but you’ll need two accounts to try it out properly)

## What This Covers

- Branch naming conventions
- Feature branches
- Pushing branches to GitHub
- Pull requests (creating, reviewing with requested changes, pushing fixes, merging)
- git pull (syncing changes from main and from colleague's branches)
- Pulling with uncommitted changes (commit vs stash)
- Merging with a dirty working directory (why you must commit first)
- Merge conflicts (why they happen, how to resolve them)
- git stash (saving work temporarily)
- Cleaning up old branches
- Squashing commits (GitHub squash merge + interactive rebase)
- Forking workflow (brief overview)

## Demo Setup

### Prerequisites

This exercise assumes **Windows** with the following installed:

- **Git for Windows** - download from https://git-scm.com
- **VS Code**
- A **GitHub** account (two accounts for the full demo)

All terminal commands in this exercise are run in **Git Bash**, which comes bundled with Git for Windows. Git Bash gives you a Linux-style terminal on Windows - it uses forward slashes (`/`) and `~` for your home directory, so all commands work identically on Windows, Linux, and Mac.

> **How to open Git Bash**: Right-click in any folder → "Open Git Bash here", or open it from the Start menu. You can also set Git Bash as the default terminal in VS Code: `Ctrl+Shift+P` → "Terminal: Select Default Profile" → "Git Bash".

### Accounts

| Developer | GitHub username | Email |
| --- | --- | --- |
| ua-tobias | ua-tobias | [tobias@utvecklarakademin.se](mailto:tobias@utvecklarakademin.se) |
| Tobeyforce | Tobeyforce | [tobias.fors.1993@gmail.com](mailto:tobias.fors.1993@gmail.com) |

### 1. Create the repo on GitHub

Create the repo under Tobeyforce's account. Push the starter code (main.py, models.py, schemas.py, database.py, seed.py, .gitignore) to main. Then add **ua-tobias** as a collaborator:

> GitHub repo → Settings → Collaborators → Add people → ua-tobias

Accept the invitation from ua-tobias's account.

### 2. Clone twice

Two separate folders, one per "developer":

```bash
# Tobeyforce's workspace
cd ~/projects/git-colab
# This folder already exists with the code - just make sure it's connected to the remote

# ua-tobias's workspace
git clone <REPO_URL> ~/projects/git-colab-ua
```

### 3. Configure git identity per folder

Each folder should commit as a different person:

```bash
# In Tobeyforce's folder
cd ~/projects/git-colab
git config user.name "Tobeyforce"
git config user.email "tobias.fors.1993@gmail.com"

# In ua-tobias's folder
cd ~/projects/git-colab-ua
git config user.name "ua-tobias"
git config user.email "tobias@utvecklarakademin.se"
```

Also configure line endings in both folders. Windows uses CRLF line endings while Linux/Mac use LF. This causes messy diffs if not handled. Run this in both folders:

```bash
git config core.autocrlf true
```

This tells git to convert line endings to LF when committing and back to CRLF when checking out - so the repo stays consistent regardless of OS.

### 4. Authentication

Each clone needs to push as its respective user. Easiest approach:

- **Tobeyforce's clone**: use SSH or `gh auth login` with the Tobeyforce account (repo owner)
- **ua-tobias's clone**: clone via HTTPS with a personal access token, or configure a second SSH key

Alternatively, clone ua-tobias's copy using a PAT in the URL:

```bash
git clone https://ua-tobias:<PAT>@github.com/Tobeyforce/git-colab.git ~/projects/git-colab-ua
```

### 5. Screen layout

- Two VS Code windows, one opened in each folder. Each uses Git Bash as the integrated terminal (`` Ctrl+` `` to toggle terminal). Alternatively, use VS Code for one user and Cursor for the other - makes it visually obvious which developer you're acting as.
- Two browser profiles logged into each GitHub account (use incognito or a different browser for the second)
- Label them clearly so students can follow who is who

### 6. Verify starting point

Both folders should be on the `main` branch with identical code:

```bash
# In both folders
git branch    # should show * main
git log --oneline -3   # should show same commits
```

## The Starting Project

A basic FastAPI product API. Students should already see these files on GitHub:

```
├── main.py           # GET /products, POST /products
├── models.py         # Product(id, name, price)
├── schemas.py        # Pydantic request/response schemas
├── database.py       # SQLAlchemy engine + session
├── seed.py           # Hardcoded seed data
├── requirements.txt
└── .gitignore
```

Walk through the code briefly so students understand what the project does before you start branching.

To seed the database, run:

```bash
python seed.py
```

> On some systems you may need to use `python3` instead of `python`.

## Branch Naming Conventions

Before we start, a quick note on branch names. Most teams follow a naming convention. The most common pattern is a prefix that describes the type of work:

| Prefix | Used for | Example |
|--------|----------|---------|
| `feature/` | New functionality | `feature/add-search-endpoint` |
| `bugfix/` | Fixing a bug | `bugfix/fix-null-price-crash` |
| `hotfix/` | Urgent production fix | `hotfix/patch-auth-bypass` |

Some teams also include ticket numbers: `feature/JIRA-42-add-search-endpoint`

The exact convention varies per team, but the principle is the same: anyone looking at the branch list should immediately understand what each branch is for. We'll use `feature/` throughout this demo.

## Part 1: The Happy Path (no conflicts)

> Goal: show the full cycle of branch → commit → push → PR → review → merge

### ua-tobias creates a feature branch

In ua-tobias's terminal:

```bash
git branch          # confirm you're on main
git switch -c feature/get-product-by-id
```

Explain to students: we're adding an endpoint to get a single product by its ID. Always check what branch you're on before starting work - this becomes second nature. Notice the branch name follows the `feature/` convention - it describes what the branch does.

Edit `main.py` - add this endpoint after the existing `create_product`:

```python
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

Also add the import at the top of `main.py`:

```python
from fastapi import Depends, FastAPI, HTTPException
```

Now, before committing, check what you've actually changed:

```bash
git status              # shows which files were modified
git diff                # shows the actual line-by-line changes
```

> Tell students: professionals run `git status` and `git diff` constantly. You want to know exactly what you're about to commit. No surprises.
> 

Stage and commit:

```bash
git add -A
git commit -m "Add GET /products/{id} endpoint"
```

Check the commit landed:

```bash
git log --oneline -3    # your new commit should be at the top
```

Push the branch:

```bash
git push -u origin feature/get-product-by-id
```

### ua-tobias opens a Pull Request

Switch to ua-tobias's browser:

1. Go to the repo on GitHub
2. You'll see a banner: "feature/get-product-by-id had recent pushes" → click **Compare & pull request**
3. Title: `Add GET /products/{id} endpoint`
4. Description: explain what the endpoint does
5. Click **Create pull request**

> Point out to students: the code is NOT in main yet. It's just a proposal.
> 

### Tobeyforce reviews the PR and requests changes

Switch to Tobeyforce's browser:

1. Open the same repo → Pull requests tab → click the PR
2. Click **Files changed** to see the diff
3. Click the `+` icon next to the line with `raise HTTPException(status_code=404, detail="Product not found")`
4. Leave a comment: "Can we also log a warning when someone requests a product that doesn't exist? Would help with debugging."
5. Click **Start a review** → **Submit review** → select **Request changes**

> Explain to students: "Request changes" is different from just leaving a comment. It blocks the merge until the author addresses the feedback. This is how most real code reviews work - the reviewer flags things that need fixing before the code can go into main.

### ua-tobias addresses the feedback with a new commit

Back in ua-tobias's terminal (still on the `feature/get-product-by-id` branch):

```bash
git branch    # confirm you're still on feature/get-product-by-id
```

Update the endpoint in `main.py` to add logging:

```python
import logging

logger = logging.getLogger(__name__)
```

And update the endpoint:

```python
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger.warning(f"Product with id {product_id} not found")
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

Commit and push - the PR updates automatically:

```bash
git status
git diff
git add -A
git commit -m "Add warning log for missing product lookups"
git push
```

> Point out to students: we didn't need `git push -u origin ...` again. The branch is already tracked. And the PR on GitHub now shows both commits automatically - no need to create a new PR.

Back on GitHub (ua-tobias's browser), reply to the review comment: "Added a warning log, check the new commit" and click **Resolve conversation**.

### Tobeyforce approves and merges

Back in Tobeyforce's browser:

1. Go to the PR → notice the new commit is visible in the conversation
2. Click **Files changed** to verify the logging was added
3. Click **Review changes** → select **Approve** → **Submit review**
4. Go back to the **Conversation** tab
5. Click **Merge pull request** → **Confirm merge**
6. Click **Delete branch** (recommended - keeps the repo clean)

> Point out: the code is now in main. Everyone can pull it. The PR has a full history of the conversation and all commits - this is valuable documentation of why decisions were made.
> 

## Part 2: Tobeyforce Works on a Feature

> Goal: show how the second developer stays in sync and creates their own feature
> 

### Tobeyforce pulls and starts working (with a realistic mistake)

In Tobeyforce's terminal:

```bash
git switch main
git pull
```

Check what new commits came in:

```bash
git log --oneline -5
```

> Point out to students: you can see ua-tobias's merged PR commit in the log now. `git log` is how you see what happened while you were away.
> 

Now, let's simulate a common mistake. Tobeyforce starts editing `main.py` directly on main - adding a delete endpoint. They write a few lines and then realize: "Wait, I should be on a feature branch."

This is where `git stash` saves you:

```bash
git stash
```

> Explain: `git stash` takes your uncommitted changes and puts them aside temporarily. Your working directory is now clean, as if you never made those changes.
> 

```bash
git switch -c feature/delete-product
git stash pop
```

> `git stash pop` brings the changes back onto the new branch. Crisis averted - this happens all the time in real development.
> 

Now continue editing `main.py` - add the delete endpoint after the get endpoint:

```python
@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
```

Add the import if not already there:

```python
from fastapi import Depends, FastAPI, HTTPException
```

Review and commit:

```bash
git status
git diff
git add -A
git commit -m "Add DELETE /products/{id} endpoint"
git push -u origin feature/delete-product
```

### Tobeyforce opens a PR, ua-tobias reviews and merges

Same flow as Part 1 but roles reversed:

1. Tobeyforce's browser: open PR
2. ua-tobias's browser: review, approve, merge

> This reinforces the pattern. Students see it works the same regardless of who does what.
> 

### ua-tobias pulls the latest main

In ua-tobias's terminal:

```bash
git switch main
git pull
git log --oneline -5
```

> Now both developers are up to date with main, which has both the GET and DELETE endpoints. Point out the log - students can see both merged PRs in the history.
> 

## Part 3: Pulling From a Colleague's Branch

> Goal: show that you can pull code from any branch, not just main. This happens constantly in real teams - "hey, push your branch, I need that code you wrote."
> 

### ua-tobias starts a new feature that depends on Tobeyforce's work

Scenario: ua-tobias needs to add a `PUT /products/{id}` endpoint (update a product). But Tobeyforce is working on adding an `updated_at` timestamp field to the Product model on a branch called `feature/add-updated-at`. ua-tobias needs that field to exist before the update endpoint makes sense.

In Tobeyforce's terminal, create the branch and make the change:

```bash
git switch main
git pull
git switch -c feature/add-updated-at
```

Edit [**models.py**](http://models.py/) - add the timestamp:

```python
from sqlalchemy import Integer, String, Float, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), default="")
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(100), default="general")
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
```

Commit and push the branch (but do NOT open a PR yet - this isn't ready for main):

```bash
git add -A
git commit -m "Add updated_at timestamp to Product model"
git push -u origin feature/add-updated-at
```

> Explain to students: Tobeyforce pushed the branch to GitHub but hasn't opened a PR. The code isn't in main. It's just on a remote branch.
> 

### ua-tobias pulls Tobeyforce's branch directly

In ua-tobias's terminal:

```bash
git switch main
git pull
git switch -c feature/update-product
```

Now pull Tobeyforce's branch into this one:

```bash
git pull origin feature/add-updated-at
```

> Explain: this is `git pull origin <branch-name>` - it fetches and merges that specific branch into whatever branch you're currently on. You're not pulling from main, you're pulling from a colleague's feature branch.
> 

Check that the `updated_at` field is now in ua-tobias's code:

```bash
git log --oneline -5
```

> Students should see Tobeyforce's commit in ua-tobias's branch history. This is how you share work-in-progress code between developers without going through main.
> 

Now ua-tobias can build the update endpoint in `main.py`:

```python
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.category = product.category
    db.commit()
    db.refresh(db_product)
    return db_product
```

Also update the `ProductResponse` schema in [**schemas.py**](http://schemas.py/) to include `updated_at`:

```python
from pydantic import BaseModel
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    category: str = "general"

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    updated_at: datetime
```

Update [**seed.py**](http://seed.py/) - since `updated_at` has a server default, no changes needed to the seed data.

Commit and push:

```bash
git status
git diff
git add -A
git commit -m "Add PUT /products/{id} endpoint"
git push -u origin feature/update-product
```

> At this point, Tobeyforce's branch should be merged first (since ua-tobias's work depends on it). Have Tobeyforce open a PR for `feature/add-updated-at`, get it reviewed and merged. Then ua-tobias opens a PR for `feature/update-product` - it should merge cleanly since it already includes Tobeyforce's changes.
> 

### Merge both PRs

1. Tobeyforce's browser: open PR for `feature/add-updated-at` → ua-tobias reviews, approves, merges
2. ua-tobias's browser: open PR for `feature/update-product` → Tobeyforce reviews, approves, merges

Both developers sync up:

```bash
# Both terminals
git switch main
git pull
git log --oneline -5
```

## Part 4: Git Pull With Uncommitted Changes

> Goal: answer the question every beginner asks: "do I have to commit before I can pull?"
> 

### What happens when you pull with uncommitted changes

In ua-tobias's terminal, make sure you're on main:

```bash
git switch main
```

Start editing a file - add a comment at the top of `main.py`:

```python
# Product API - v2
```

Do NOT commit. Now try to pull:

```bash
git pull
```

Two things can happen:

1. **If the pull changes different files** than what you edited → git will merge cleanly and your uncommitted changes stay intact
2. **If the pull changes the same file** you edited → git will refuse with: `error: Your local changes to the following files would be overwritten by merge`

> Explain to students: git is protecting you. It won't silently overwrite your work.
> 

### The two ways to handle it

**Option A: Commit first, then pull**

If your changes are ready to be committed:

```bash
git add -A
git commit -m "Add version comment to main.py"
git pull
```

> This is the cleanest option. Your work is saved as a commit. If the pull causes a conflict, you resolve it like any other merge conflict.
> 

**Option B: Stash, pull, then unstash**

If your changes aren't ready for a commit yet (half-finished work):

```bash
git stash
git pull
git stash pop
```

> Your changes are put aside, the pull runs cleanly, then your changes come back on top.
> 

### Clean up

Undo the comment change (we don't actually want it):

```bash
git checkout -- main.py
```

> Tell students: the rule is simple. **Git operates on commits.** Pulling and merging are operations between commits, not between random unsaved file states. Either commit or stash before you pull/merge.
> 

## Part 5: Merge Conflict

> Goal: show what happens when two developers modify the same code. This is the scary part for beginners - demystify it.
> 

### What happens if you merge with uncommitted changes?

Before we create the actual conflict, let's quickly show what happens if you try to merge while you have uncommitted work.

In ua-tobias's terminal:

```bash
git switch main
git pull
git switch -c feature/demo-dirty-merge
```

Edit `seed.py` - change a product name to anything. Do NOT stage or commit.

Now try to switch back to main:

```bash
git switch main
```

Git will either refuse (`error: Your local changes would be overwritten`) or carry the changes with you if there's no conflict. Either way, it's unpredictable.

> Explain: **always commit before switching branches or merging.** A merge is a combination of two sets of commits. If you have uncommitted changes floating around, git doesn't know what to do with them. Commit or stash first.
> 

Clean up:

```bash
git checkout -- seed.py
git switch main
git branch -d feature/demo-dirty-merge
```

### Both developers pull main and create branches

In ua-tobias's terminal:

```bash
git switch main
git pull
git switch -c feature/add-description-field
```

In Tobeyforce's terminal:

```bash
git switch main
git pull
git switch -c feature/add-category-field
```

> Explain: both developers are starting from the same code, but they're about to change the same files.
> 

### ua-tobias adds a `description` field

[**models.py**](http://models.py/) - add the field to the Product class:

```python
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), default="")
    price: Mapped[float] = mapped_column(Float)
```

[**schemas.py**](http://schemas.py/) - add description to the schemas:

```python
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
```

[**seed.py**](http://seed.py/) - update seed data:

```python
from database import Base, engine, SessionLocal
from models import Product

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.query(Product).delete()

db.add_all([
    Product(name="Laptop", description="14 inch development laptop", price=999.99),
    Product(name="Keyboard", description="Mechanical RGB keyboard", price=49.99),
    Product(name="Mouse", description="Wireless ergonomic mouse", price=29.99),
    Product(name="Monitor", description="27 inch 4K display", price=349.99),
    Product(name="Headphones", description="Noise cancelling headphones", price=79.99),
])

db.commit()
db.close()
print("Database seeded")
```

Review and commit:

```bash
git status
git diff
git add -A
git commit -m "Add description field to Product model"
git log --oneline -3
git push -u origin feature/add-description-field
```

### Tobeyforce adds a `category` field

> While ua-tobias was working, Tobeyforce was also working - they don't know about each other's changes yet.
> 

[**models.py**](http://models.py/) - add the field to the Product class:

```python
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(100), default="general")
```

[**schemas.py**](http://schemas.py/) - add category to the schemas:

```python
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    category: str = "general"

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
```

[**seed.py**](http://seed.py/) - update seed data:

```python
from database import Base, engine, SessionLocal
from models import Product

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.query(Product).delete()

db.add_all([
    Product(name="Laptop", price=999.99, category="computers"),
    Product(name="Keyboard", price=49.99, category="peripherals"),
    Product(name="Mouse", price=29.99, category="peripherals"),
    Product(name="Monitor", price=349.99, category="displays"),
    Product(name="Headphones", price=79.99, category="audio"),
])

db.commit()
db.close()
print("Database seeded")
```

Review and commit:

```bash
git status
git diff
git add -A
git commit -m "Add category field to Product model"
git push -u origin feature/add-category-field
```

### ua-tobias's PR gets merged first

1. ua-tobias's browser: open PR for `feature/add-description-field`, title: "Add description field to Product"
2. Tobeyforce's browser: review, approve, merge

> Main now has the description field.
> 

### Tobeyforce opens a PR - conflict!

1. Tobeyforce's browser: open PR for `feature/add-category-field`
2. GitHub will show: **This branch has conflicts that must be resolved**

> Stop here and explain to students: both developers changed the same files ([models.py](http://models.py/), [schemas.py](http://schemas.py/), [seed.py](http://seed.py/)). Git doesn't know how to combine them automatically. This is a merge conflict.
> 

### Tobeyforce resolves the conflict locally

In Tobeyforce's terminal, pull the latest main into the feature branch:

```bash
git pull origin main
```

Git will report conflicts. Open the files in VS Code - you'll see conflict markers like:

```
<<<<<<< HEAD
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(100), default="general")
=======
    description: Mapped[str] = mapped_column(String(500), default="")
    price: Mapped[float] = mapped_column(Float)
>>>>>>> main
```

> Walk through what these markers mean:
> 
> - Everything between `<<<<<<< HEAD` and `=======` is Tobeyforce's version (current branch)
> - Everything between `=======` and `>>>>>>> main` is what's on main (ua-tobias's merged work)
> - We want BOTH fields, so we keep both

Resolve each file. The final versions should have both `description` and `category`:

[**models.py**](http://models.py/) after resolving:

```python
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), default="")
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(100), default="general")
```

[**schemas.py**](http://schemas.py/) after resolving:

```python
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    category: str = "general"

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
```

[**seed.py**](http://seed.py/) after resolving:

```python
from database import Base, engine, SessionLocal
from models import Product

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.query(Product).delete()

db.add_all([
    Product(name="Laptop", description="14 inch development laptop", price=999.99, category="computers"),
    Product(name="Keyboard", description="Mechanical RGB keyboard", price=49.99, category="peripherals"),
    Product(name="Mouse", description="Wireless ergonomic mouse", price=29.99, category="peripherals"),
    Product(name="Monitor", description="27 inch 4K display", price=349.99, category="displays"),
    Product(name="Headphones", description="Noise cancelling headphones", price=79.99, category="audio"),
])

db.commit()
db.close()
print("Database seeded")
```

After resolving all conflicts, commit and push:

```bash
git add -A
git commit -m "Resolve merge conflicts - combine description and category fields"
git push
```

### Merge the PR

Back in Tobeyforce's browser (or ua-tobias reviews):

1. The PR now shows no conflicts
2. Review, approve, merge

> Final takeaway for students: merge conflicts aren't errors. They're git asking "I see two changes to the same code, which one do you want?" - and often the answer is "both".
> 

## Part 6: Sync Up and Clean Up

Both developers pull the latest main:

```bash
# ua-tobias's terminal
git switch main
git pull

# Tobeyforce's terminal
git switch main
git pull
```

> Both now have identical code with both the description and category fields, plus the GET and DELETE endpoints. This is the normal rhythm of teamwork with git.

### Cleaning up old branches

After several PRs, both developers have accumulated local branches that are already merged. Check:

```bash
git branch
```

You'll see something like:

```
  feature/add-category-field
  feature/add-description-field
  feature/delete-product
  feature/get-product-by-id
  feature/update-product
* main
```

These branches served their purpose - they've all been merged via PRs. Delete them:

```bash
git branch -d feature/get-product-by-id
git branch -d feature/delete-product
git branch -d feature/add-description-field
git branch -d feature/update-product
# etc.
```

> The `-d` flag only deletes branches that have already been merged. Git will refuse if the branch has unmerged work, protecting you from accidentally losing code.

To also clean up references to remote branches that were deleted on GitHub (e.g. after clicking "Delete branch" on a merged PR):

```bash
git fetch --prune
```

> Tell students: do this regularly. In a real project, you'll create dozens of branches over time. If you never clean up, `git branch` becomes a wall of noise and you can't tell what's current.
> 

## Alternative: The Forking Workflow

The demo above uses the **feature branch workflow** - everyone pushes branches to the same repo. This is the most common approach in companies where all developers have write access.

There's another strategy called the **forking workflow**, mostly used in open source. Here's how it differs:

### How it works

1. There's one "upstream" repo that you do NOT have write access to (e.g. `facebook/react`)
2. You **fork** it - this creates a full copy under your own GitHub account (e.g. `tobeyforce/react`)
3. You clone YOUR fork, not the original
4. You create feature branches on your fork, push to your fork
5. You open a PR from your fork's branch → into the upstream repo's main branch
6. The maintainers of the upstream repo review and merge (or reject) your PR

### Setting it up

```bash
# Clone your fork
git clone <https://github.com/Tobeyforce/some-project.git>
cd some-project

# Add the original repo as "upstream" so you can pull updates from it
git remote add upstream <https://github.com/original-owner/some-project.git>

# Now you have two remotes:
git remote -v
# origin    → your fork (you push here)
# upstream  → the original repo (you pull from here)
```

### Staying in sync with the original

```bash
git fetch upstream
git switch main
git merge upstream/main
git push origin main        # update your fork's main
```

### When to use which

| Workflow | Use when |
| --- | --- |
| **Feature branch** | You're on a team with shared repo access. Most companies use this. |
| **Forking** | You're contributing to a project you don't own. Open source contributions, or organizations that want stricter access control. |

> The core git skills (branches, PRs, merge conflicts) are the same in both workflows. The only difference is where you push: same repo (branch workflow) vs your own copy (forking workflow).
> 

## Keeping a Clean History: Squashing

During the demo, you may have noticed that some PRs had multiple commits (e.g. the first PR had "Add GET /products/{id} endpoint" and then "Add warning log for missing product lookups"). When merged normally, all those commits appear individually in main's history.

On a small project this is fine. On a larger project with multiple developers making several commits per feature, main's history can become noisy and hard to read.

### Squash and merge (on GitHub)

When merging a PR on GitHub, you can choose **Squash and merge** instead of the regular **Merge pull request**. This combines all commits from the branch into a single commit on main.

Example - a PR with these commits:

```
feat: Add GET /products/{id} endpoint
fix: Add warning log for missing product lookups
fix: Typo in log message
```

With **Squash and merge**, main gets one clean commit: `Add GET /products/{id} endpoint (#1)`

Many teams set this as the default (or only) merge strategy in the repo settings:

> GitHub repo → Settings → General → Pull Requests → select "Allow squash merging" and optionally disable the other options.

### Squashing locally with `git rebase -i`

You can also squash commits before pushing, without relying on GitHub's squash merge. This is useful when you want to clean up your branch before opening a PR.

Say you're on a feature branch and made 3 commits:

```bash
git log --oneline -3
# a1b2c3d Fix typo in log message
# d4e5f6g Add warning log for missing product lookups
# h7i8j9k Add GET /products/{id} endpoint
```

You can squash them into one:

```bash
git rebase -i HEAD~3
```

This opens an editor showing your 3 commits. Change `pick` to `squash` (or `s`) for the commits you want to combine:

```
pick h7i8j9k Add GET /products/{id} endpoint
squash d4e5f6g Add warning log for missing product lookups
squash a1b2c3d Fix typo in log message
```

Save and close. Git will open another editor where you can write one combined commit message. Now your branch has one clean commit instead of three.

> **Warning**: Only squash commits that haven't been pushed yet, or commits on a branch that only you are working on. Squashing rewrites history - if someone else has already pulled your branch, this will cause problems for them.

### When to squash

| Approach | When to use |
|----------|-------------|
| **Squash and merge** (GitHub) | Team wants a clean main history. Each PR = one commit. Most common approach. |
| **Regular merge** | Team wants full commit history preserved. Useful for detailed audit trails. |
| **Interactive rebase** | You want to clean up your own branch before opening a PR. More advanced. |

> A lot of teams use squash merge as their default. It keeps `git log` on main readable - each entry is one feature or fix, not dozens of "WIP" and "fix typo" commits.

## Quick Reference

### Commands you'll use every day

These are the commands professional developers run constantly - not just occasionally:

| Command | When you use it | How often |
| --- | --- | --- |
| `git status` | Before staging, before committing, when confused | 20+ times a day |
| `git diff` | Before `git add`, to review what you're about to stage | Before every commit |
| `git branch` | Check what branch you're on before starting work | Start of every task |
| `git log --oneline -5` | After pulling, after merging, to see what happened | Several times a day |
| `git pull` | Start of the day, before creating a new branch | Every time you touch main |
| `git stash` / `git stash pop` | When you need to switch branches with uncommitted work | A few times a week |

### Feature branch workflow cheat sheet

```bash
git switch main                    # start from main
git pull                           # get latest changes
git switch -c feature/my-feature   # create feature branch
# ... make changes ...
git status                         # see what changed
git diff                           # review the actual changes
git add -A                         # stage changes
git commit -m "description"        # commit
git log --oneline -3               # verify commit
git push -u origin feature/my-feature  # push branch
# ... open PR on GitHub, get review, merge ...
git switch main                    # back to main
git pull                           # get the merged changes
```

### When you hit a merge conflict

```bash
git pull origin main               # pull main into your branch
# ... resolve conflicts in VS Code ...
git add -A
git commit -m "Resolve merge conflicts"
git push
```