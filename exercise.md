# Collaborating with Git - Teacher Demo

This demo simulates two developers (ua-tobias and Tobeyforce) collaborating on a FastAPI project using the feature branch workflow. You control both accounts to show students how real teamwork with git looks.

## What This Covers

- Feature branches
- Pushing branches to GitHub
- Pull requests (creating, reviewing, merging)
- git pull (syncing changes from main and from colleague's branches)
- Pulling with uncommitted changes (commit vs stash)
- Merging with a dirty working directory (why you must commit first)
- Merge conflicts (why they happen, how to resolve them)
- git stash (saving work temporarily)
- Forking workflow (brief overview)

## Demo Setup (do this before class)

### Accounts

| Developer | GitHub username | Email |
|-----------|----------------|-------|
| ua-tobias | ua-tobias | tobias@utvecklarakademin.se |
| Tobeyforce | Tobeyforce | tobias.fors.1993@gmail.com |

### 1. Create the repo on GitHub

Create the repo under ua-tobias's account. Push the starter code (main.py, models.py, schemas.py, database.py, seed.py, .gitignore) to main. Then add **Tobeyforce** as a collaborator:

> GitHub repo → Settings → Collaborators → Add people → Tobeyforce

Accept the invitation from Tobeyforce's account.

### 2. Clone twice

Two separate folders, one per "developer":

```bash
# ua-tobias's workspace
cd ~/projects
# This folder already exists with the code - just make sure it's connected to the remote

# Tobeyforce's workspace
git clone <REPO_URL> ~/projects/git-colab-tobey
```

### 3. Configure git identity per folder

Each folder should commit as a different person:

```bash
# In ua-tobias's folder
cd ~/projects/git-colab
git config user.name "ua-tobias"
git config user.email "tobias@utvecklarakademin.se"

# In Tobeyforce's folder
cd ~/projects/git-colab-tobey
git config user.name "Tobeyforce"
git config user.email "tobias.fors.1993@gmail.com"
```

### 4. Authentication

Each clone needs to push as its respective user. Easiest approach:

- **ua-tobias's clone**: use SSH or `gh auth login` with the ua-tobias account
- **Tobeyforce's clone**: clone via HTTPS with a personal access token, or configure a second SSH key

Alternatively, clone Tobeyforce's copy using a PAT in the URL:

```bash
git clone https://Tobeyforce:<PAT>@github.com/ua-tobias/git-colab.git ~/projects/git-colab-tobey
```

### 5. Screen layout

- Two terminal windows side by side (or two VS Code windows)
- Two browser profiles logged into each GitHub account (use incognito for the second)
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

## Part 1: The Happy Path (no conflicts)

> Goal: show the full cycle of branch → commit → push → PR → review → merge

### ua-tobias creates a feature branch

In ua-tobias's terminal:

```bash
git branch          # confirm you're on main
git switch -c feature/get-product-by-id
```

Explain to students: we're adding an endpoint to get a single product by its ID. Always check what branch you're on before starting work - this becomes second nature.

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

### Tobeyforce reviews the PR

Switch to Tobeyforce's browser:

1. Open the same repo → Pull requests tab → click the PR
2. Click **Files changed** to see the diff
3. Click the `+` icon next to the `raise HTTPException` line
4. Leave a comment: "Good, but could we also add a message in the response for the 404?"
5. Click **Start a review** → **Submit review** → select **Comment**

> Explain to students: in real teams, you'd have actual feedback. This is where discussions happen.

### ua-tobias addresses the feedback

Back in ua-tobias's terminal. The endpoint already has `detail="Product not found"` so let's say ua-tobias responds on GitHub:

1. Reply to the comment: "It's already there - the `detail` parameter in HTTPException gets returned in the response body"
2. Click **Resolve conversation**

> Show students that PRs are a conversation, not just a rubber stamp.

### Tobeyforce approves and merges

Back in Tobeyforce's browser:

1. Go to the PR → **Files changed**
2. Click **Review changes** → select **Approve** → **Submit review**
3. Go back to the **Conversation** tab
4. Click **Merge pull request** → **Confirm merge**
5. Click **Delete branch** (optional but recommended)

> Point out: the code is now in main. Everyone can pull it.

## Part 2: Tobeyforce Works on a Feature

> Goal: show how the second developer stays in sync and creates their own feature

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

Now, let's simulate a common mistake. Tobeyforce starts editing `main.py` directly on main - adding a delete endpoint. They write a few lines and then realize: "Wait, I should be on a feature branch."

This is where `git stash` saves you:

```bash
git stash
```

> Explain: `git stash` takes your uncommitted changes and puts them aside temporarily. Your working directory is now clean, as if you never made those changes.

```bash
git switch -c feature/delete-product
git stash pop
```

> `git stash pop` brings the changes back onto the new branch. Crisis averted - this happens all the time in real development.

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

### ua-tobias pulls the latest main

In ua-tobias's terminal:

```bash
git switch main
git pull
git log --oneline -5
```

> Now both developers are up to date with main, which has both the GET and DELETE endpoints. Point out the log - students can see both merged PRs in the history.

## Part 3: Pulling From a Colleague's Branch

> Goal: show that you can pull code from any branch, not just main. This happens constantly in real teams - "hey, push your branch, I need that code you wrote."

### ua-tobias starts a new feature that depends on Tobeyforce's work

Scenario: ua-tobias needs to add a `PUT /products/{id}` endpoint (update a product). But Tobeyforce is working on adding an `updated_at` timestamp field to the Product model on a branch called `feature/add-updated-at`. ua-tobias needs that field to exist before the update endpoint makes sense.

In Tobeyforce's terminal, create the branch and make the change:

```bash
git switch main
git pull
git switch -c feature/add-updated-at
```

Edit **models.py** - add the timestamp:

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

Check that the `updated_at` field is now in ua-tobias's code:

```bash
git log --oneline -5
```

> Students should see Tobeyforce's commit in ua-tobias's branch history. This is how you share work-in-progress code between developers without going through main.

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

Also update the `ProductResponse` schema in **schemas.py** to include `updated_at`:

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

Update **seed.py** - since `updated_at` has a server default, no changes needed to the seed data.

Commit and push:

```bash
git status
git diff
git add -A
git commit -m "Add PUT /products/{id} endpoint"
git push -u origin feature/update-product
```

> At this point, Tobeyforce's branch should be merged first (since ua-tobias's work depends on it). Have Tobeyforce open a PR for `feature/add-updated-at`, get it reviewed and merged. Then ua-tobias opens a PR for `feature/update-product` - it should merge cleanly since it already includes Tobeyforce's changes.

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

### The two ways to handle it

**Option A: Commit first, then pull**

If your changes are ready to be committed:

```bash
git add -A
git commit -m "Add version comment to main.py"
git pull
```

> This is the cleanest option. Your work is saved as a commit. If the pull causes a conflict, you resolve it like any other merge conflict.

**Option B: Stash, pull, then unstash**

If your changes aren't ready for a commit yet (half-finished work):

```bash
git stash
git pull
git stash pop
```

> Your changes are put aside, the pull runs cleanly, then your changes come back on top.

### Clean up

Undo the comment change (we don't actually want it):

```bash
git checkout -- main.py
```

> Tell students: the rule is simple. **Git operates on commits.** Pulling and merging are operations between commits, not between random unsaved file states. Either commit or stash before you pull/merge.

## Part 5: Merge Conflict

> Goal: show what happens when two developers modify the same code. This is the scary part for beginners - demystify it.

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

### ua-tobias adds a `description` field

**models.py** - add the field to the Product class:

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

**schemas.py** - add description to the schemas:

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

**seed.py** - update seed data:

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

**models.py** - add the field to the Product class:

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

**schemas.py** - add category to the schemas:

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

**seed.py** - update seed data:

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

### Tobeyforce opens a PR - conflict!

1. Tobeyforce's browser: open PR for `feature/add-category-field`
2. GitHub will show: **This branch has conflicts that must be resolved**

> Stop here and explain to students: both developers changed the same files (models.py, schemas.py, seed.py). Git doesn't know how to combine them automatically. This is a merge conflict.

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
> - Everything between `<<<<<<< HEAD` and `=======` is Tobeyforce's version (current branch)
> - Everything between `=======` and `>>>>>>> main` is what's on main (ua-tobias's merged work)
> - We want BOTH fields, so we keep both

Resolve each file. The final versions should have both `description` and `category`:

**models.py** after resolving:

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

**schemas.py** after resolving:

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

**seed.py** after resolving:

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

## Part 6: Both Developers Sync Up

Both developers should end the demo with the latest code:

```bash
# ua-tobias's terminal
git switch main
git pull

# Tobeyforce's terminal
git switch main
git pull
```

> Both now have identical code with both the description and category fields, plus the GET and DELETE endpoints. This is the normal rhythm of teamwork with git.

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
git clone https://github.com/Tobeyforce/some-project.git
cd some-project

# Add the original repo as "upstream" so you can pull updates from it
git remote add upstream https://github.com/original-owner/some-project.git

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
|----------|----------|
| **Feature branch** | You're on a team with shared repo access. Most companies use this. |
| **Forking** | You're contributing to a project you don't own. Open source contributions, or organizations that want stricter access control. |

> The core git skills (branches, PRs, merge conflicts) are the same in both workflows. The only difference is where you push: same repo (branch workflow) vs your own copy (forking workflow).

## Quick Reference

### Commands you'll use every day

These are the commands professional developers run constantly - not just occasionally:

| Command | When you use it | How often |
|---------|----------------|-----------|
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
