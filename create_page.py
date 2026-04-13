#! /usr/bin/python3

# Create the embeddable build status markdown page for repositories I track.

import subprocess
import os

from pathlib import Path

def get_git_upstream_info(repo_path):
    """
    Extracts the URL and default branch for the 'upstream' remote.
    """
    try:
        # 1. Get the URL of the 'upstream' remote
        url_cmd = ["git", "-C", repo_path, "remote", "get-url", "upstream"]
        upstream_url = subprocess.check_output(url_cmd, stderr=subprocess.STDOUT).decode().strip()
        if "git@github.com:" in upstream_url:
            upstream_url = upstream_url.replace("git@github.com:", "https://github.com/")
        if not upstream_url.endswith(".git"):
            upstream_url = upstream_url + ".git"

        # 2. Get the default branch (usually refs/remotes/upstream/HEAD)
        # We use 'remote show' to find what the remote considers the HEAD branch
        branch_cmd = ["git", "-C", repo_path, "remote", "show", "upstream"]
        show_output = subprocess.check_output(branch_cmd, stderr=subprocess.STDOUT).decode()

        # Look for the line: "  HEAD branch: main"
        default_branch = "Unknown"
        for line in show_output.splitlines():
            if "HEAD branch" in line:
                default_branch = line.split(":")[-1].strip()
                break

        return upstream_url, default_branch

    except subprocess.CalledProcessError:
        # This occurs if 'upstream' doesn't exist or the directory isn't a git repo
        return None, None

def list_directories(path_to_search, upper_bound = -1):
    p = Path(path_to_search)

    directories = [f.name for f in p.iterdir() if f.is_dir()]
    directories.sort()

    return [path_to_search + "/" + s for s in directories[:upper_bound]]

def process_directories(heading, classification, directories):
    print("")
    print(f"## {heading}")
    print("")

    for repo_path in directories:
        if not os.path.isdir(repo_path):
            continue
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            continue

        url, branch = get_git_upstream_info(repo_path)
        if not url:
            continue
        basedir = os.path.basename(repo_path)
        basedir_pluses = basedir.replace("-plugin", "").replace("_Plugin", "").replace("-", "+").replace("_", "+")
        if basedir == "bom":
            continue
        url = f"[![Build Status](https://ci.jenkins.io/buildStatus/icon?job={classification}%2F{basedir}%2F{branch}&subject={basedir_pluses})](https://ci.jenkins.io/job/{classification}/job/{basedir}/job/{branch}/)"

        print(f"{url}")

if __name__ == "__main__":
    process_directories("My Plugins",      "Plugins",             list_directories("/home/mwaite/hub/my-plugins", 3))
    process_directories("Core",            "Core",                list_directories("/home/mwaite/hub/core", 3))
    process_directories("Packaging",       "Packaging",           list_directories("/home/mwaite/hub/packaging", 3))
    process_directories("Tools",           "Tools",               list_directories("/home/mwaite/hub/tools", 3))
    process_directories("Orphan Plugins",  "Plugins",             list_directories("/home/mwaite/hub/orphans", 3))
    process_directories("Top 250 Plugins", "Plugins",             list_directories("/home/mwaite/all/popular-250", 3))
    process_directories("Maven Plugins",   "Plugins",             list_directories("/home/mwaite/hub/maven-plugins", 3))
    process_directories("Libraries",       "jenkinsci-libraries", list_directories("/home/mwaite/hub/libraries", 3))
