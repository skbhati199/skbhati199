#!/usr/bin/env python3
import os
import json
import subprocess
import matplotlib.pyplot as plt
from collections import Counter

def run_cmd(cmd):
    """Run shell command and return output as a string"""
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def categorize_repo(name, description="", topics=None):
    """Categorize a repository based on its name, description, and topics"""
    if topics is None:
        topics = []
    
    # Convert all to lowercase for easier matching
    name_lower = name.lower()
    desc_lower = description.lower() if description else ""
    topics_lower = [t.lower() for t in topics]
    
    # Define category keywords
    keywords = {
        "Web Development": ["web", "react", "next", "html", "css", "vue", "angular", "frontend"],
        "Mobile Apps": ["android", "ios", "mobile", "app", "react-native", "flutter", "kotlin", "swift"],
        "AI/ML Projects": ["ai", "ml", "model", "neural", "deep-learning", "machine-learning", "tensorflow", "pytorch", "openai"],
        "Chrome Extensions": ["chrome", "extension", "browser", "firefox", "addon"],
        "Backend Services": ["backend", "api", "server", "service", "node", "express", "django", "fastapi", "database"],
        "DevOps": ["devops", "docker", "kubernetes", "ci", "cd", "pipeline", "deploy", "aws", "cloud", "infra", "k8s", "workflow"],
    }
    
    # Check each category's keywords
    for category, kw_list in keywords.items():
        # Check in name
        if any(kw in name_lower for kw in kw_list):
            return category
        
        # Check in description
        if any(kw in desc_lower for kw in kw_list):
            return category
        
        # Check in topics
        if any(kw in topics_lower for kw in kw_list):
            return category
    
    # If no category matched, return "Other"
    return "Other"

def main():
    # Get repositories JSON from GitHub CLI
    repos_json = run_cmd('gh repo list --json name,description,topics,createdAt,pushedAt --limit 100')
    repos = json.loads(repos_json)
    
    # Categorize repositories
    categories = {}
    for repo in repos:
        category = categorize_repo(
            repo['name'], 
            repo.get('description', ''),
            repo.get('topics', [])
        )
        
        if category not in categories:
            categories[category] = []
        
        categories[category].append(repo['name'])
    
    # Count repositories in each category
    category_counts = {cat: len(repos) for cat, repos in categories.items()}
    
    # Output to markdown file
    with open('repo-categories.md', 'w') as f:
        f.write("# GitHub Repository Categories\n\n")
        
        # Create mermaid pie chart
        f.write("## Repository Distribution\n\n")
        f.write("```mermaid\n")
        f.write("pie\n")
        f.write("    title Repository Distribution by Category\n")
        for cat, count in category_counts.items():
            f.write(f'    "{cat}" : {count}\n')
        f.write("```\n\n")
        
        # List repositories by category
        f.write("## Repositories by Category\n\n")
        for cat, repos in categories.items():
            f.write(f"### {cat} ({len(repos)})\n\n")
            for repo in repos:
                f.write(f"- {repo}\n")
            f.write("\n")
    
    print(f"Categories have been written to repo-categories.md")

if __name__ == "__main__":
    main() 