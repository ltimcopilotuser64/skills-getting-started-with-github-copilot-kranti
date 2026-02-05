#!/bin/bash

# Script to create and push the accelerate-with-copilot branch
# This completes Step 1 of the GitHub Copilot Skills exercise

echo "Creating and pushing accelerate-with-copilot branch..."

# Create the branch
git checkout -b accelerate-with-copilot

# Push the branch to origin
git push -u origin accelerate-with-copilot

echo "✅ Branch accelerate-with-copilot has been created and pushed!"
echo "Check issue #1 for feedback from the automated workflow."
