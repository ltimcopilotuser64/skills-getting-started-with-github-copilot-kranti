# GitHub Copilot Skills Exercise Guide

## Current Status: Step 1 - Hello Copilot

This repository is set up for the GitHub Copilot Skills exercise. Follow the instructions below to complete Step 1.

## What You Need to Do

The automated workflow is waiting for you to create a branch named `accelerate-with-copilot`. Here's how to do it:

### Option 1: Using GitHub Codespace (Recommended)

1. Open your Codespace at: https://scaling-space-broccoli-r4vrvgrr449xhx6xp.github.dev/
2. Open the terminal in VS Code
3. Run these commands:
   ```bash
   git checkout -b accelerate-with-copilot
   git push -u origin accelerate-with-copilot
   ```

### Option 2: Using Copilot Terminal Inline Chat (As per Exercise Instructions)

1. In your Codespace, open a new terminal
2. Press `Ctrl + I` (Windows/Linux) or `Cmd + I` (Mac) to open Copilot's Terminal Inline Chat
3. Ask Copilot: "Hey copilot, how can I create and publish a new Git branch called 'accelerate-with-copilot'?"
4. Let Copilot generate the command and run it

### Option 3: Manual Command

Simply run this in your terminal:
```bash
git checkout -b accelerate-with-copilot && git push -u origin accelerate-with-copilot
```

## Verification

After pushing the branch, the automated workflow will:
- Check that the branch name is exactly `accelerate-with-copilot`
- Post feedback in issue #1
- Progress you to Step 2

## Current Repository Setup

✅ All dependencies are configured correctly:
- FastAPI application is ready
- Devcontainer is configured with Python 3.13
- GitHub Copilot extensions are pre-installed
- Launch configuration is set up for debugging

## Application Overview

This is the Mergington High School Activities application:
- **Backend**: FastAPI (Python)
- **Frontend**: Static HTML/CSS/JavaScript
- **Port**: 8000
- **Features**: View and sign up for extracurricular activities

### Running the Application

In your Codespace:
1. Click the "Run and Debug" icon in the left sidebar
2. Click "Start Debugging" (green play button)
3. Go to the "Ports" tab in the bottom panel
4. Click the "Open in Browser" icon next to port 8000

## Next Steps

After completing Step 1 (creating the `accelerate-with-copilot` branch), watch issue #1 for your next instructions from the automated exercise system.

## Troubleshooting

### Branch name must be exact
- ❌ `accelerate_with_copilot`
- ❌ `feature/accelerate-with-copilot`  
- ✅ `accelerate-with-copilot`

### Make sure the branch is pushed
Check with: `git branch -r | grep accelerate-with-copilot`

If you see `origin/accelerate-with-copilot`, you're all set!

## Reference

- Full exercise instructions: See issue #1
- GitHub Copilot Documentation: https://docs.github.com/en/copilot
