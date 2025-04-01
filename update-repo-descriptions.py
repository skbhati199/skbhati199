#!/usr/bin/env python3
import json
import subprocess
import os
import time

def run_cmd(cmd):
    """Run shell command and return output as a string"""
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_recommended_description(repo_name):
    """Generate a recommended description based on the repository name"""
    words = repo_name.replace('-', ' ').replace('_', ' ').split()
    
    # Common prefixes to handle
    prefixes = {
        'ai': 'Artificial Intelligence',
        'ml': 'Machine Learning',
        'api': 'API',
        'app': 'Application',
        'web': 'Web',
        'mobile': 'Mobile',
        'ios': 'iOS',
        'android': 'Android',
        'react': 'React',
        'node': 'Node.js',
        'py': 'Python',
        'next': 'Next.js',
        'chrome': 'Chrome Extension',
        'wordpress': 'WordPress',
        'wp': 'WordPress',
    }
    
    # Replace words with expanded versions
    for i, word in enumerate(words):
        if word.lower() in prefixes:
            words[i] = prefixes[word.lower()]
    
    # Capitalize words
    words = [word.capitalize() for word in words]
    
    # Generate description
    description = ' '.join(words)
    
    # Add common suffixes based on repository type
    if any(tech in repo_name.lower() for tech in ['web', 'react', 'next', 'vue', 'angular']):
        description += ' - Web Application'
    elif any(tech in repo_name.lower() for tech in ['android', 'ios', 'mobile', 'app']):
        description += ' - Mobile Application'
    elif any(tech in repo_name.lower() for tech in ['api', 'server', 'backend']):
        description += ' - Backend Service'
    elif any(tech in repo_name.lower() for tech in ['ai', 'ml', 'chat', 'gpt']):
        description += ' - AI/ML Project'
    elif any(tech in repo_name.lower() for tech in ['chrome', 'extension', 'addon']):
        description += ' - Browser Extension'
    
    return description

def main():
    """Main function to update repository descriptions"""
    # Get repositories JSON from GitHub CLI
    print("Fetching repository data...")
    repos_json = run_cmd('gh repo list --json name,description,url --limit 100')
    repos = json.loads(repos_json)
    
    # Filter repositories without descriptions
    empty_desc_repos = [repo for repo in repos if not repo.get('description')]
    
    if not empty_desc_repos:
        print("All repositories already have descriptions!")
        return
    
    print(f"Found {len(empty_desc_repos)} repositories without descriptions.")
    
    # Process each repository
    for i, repo in enumerate(empty_desc_repos):
        repo_name = repo['name']
        recommended_desc = get_recommended_description(repo_name)
        
        print(f"\n{i+1}/{len(empty_desc_repos)}: {repo_name}")
        print(f"Recommended description: {recommended_desc}")
        
        choice = input("Use this description? [Y]es/[N]o/[S]kip/[C]ustom: ").lower()
        
        if choice == 'y':
            description = recommended_desc
        elif choice == 'n':
            continue  # Skip this repository
        elif choice == 's':
            print(f"Skipping {repo_name}")
            continue
        elif choice == 'c':
            description = input("Enter custom description: ")
        else:
            print("Invalid choice, skipping")
            continue
        
        # Update the repository description
        print(f"Updating description for {repo_name}...")
        cmd = f'gh repo edit {repo_name} --description "{description}"'
        try:
            run_cmd(cmd)
            print("Description updated successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error updating description: {e}")
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)
    
    print("\nAll done! Repository descriptions have been updated.")

if __name__ == "__main__":
    main() 