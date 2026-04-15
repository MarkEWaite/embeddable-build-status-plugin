#! /usr/bin/python3

# Create the embeddable build status markdown page for repositories I track.
#
# File content is based on my repository structure
#
# Use python create_page.py to update README.md
# Use python create_page.py PLUGINS.md to update PLUGINS.md
# Use python create_page.py TOP-250.md to update TOP-250.md

import subprocess
import os
import sys

from pathlib import Path
from urllib.parse import quote_plus

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

def process_directories(heading, classification, f, directories):
    print("", file=f)
    print(f"## {heading}", file=f)
    print("", file=f)

    for repo_path in directories:
        if not os.path.isdir(repo_path):
            continue
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            continue
        basedir = os.path.basename(repo_path)
        if basedir in [ "bom", "jenkins-core-changelog-generator", "release"]:
            continue
        basedir_quoted = quote_plus(basedir.replace("-plugin", "").replace("_Plugin", "").replace("-", " ").replace("_", " "))

        url, branch = get_git_upstream_info(repo_path)
        if not url:
            continue
        branch_quoted = quote_plus(quote_plus(branch)) # Must be double encoded per build status plugin docs
        print("url is " +  url + ", quoted branch is " + branch_quoted)
        print(f"[![Status](https://ci.jenkins.io/buildStatus/icon?job={classification}%2F{basedir}%2F{branch_quoted}&subject={basedir_quoted})](https://ci.jenkins.io/job/{classification}/job/{basedir}/job/{branch_quoted}/)", file=f)

if __name__ == "__main__":
    dest = "README.md"
    if len(sys.argv) > 1:
        dest = sys.argv[1]
    with open(dest, "w") as f:
        if dest == "README.md":
            process_directories("Core",            "Core",                f, list_directories("/home/mwaite/hub/core"))
            process_directories("Packaging",       "Packaging",           f, list_directories("/home/mwaite/hub/packaging"))
            process_directories("Tools",           "Tools",               f, list_directories("/home/mwaite/hub/tools"))
            process_directories("Maven Plugins",   "Plugins",             f, list_directories("/home/mwaite/hub/maven-plugins"))
            process_directories("Libraries",       "jenkinsci-libraries", f, list_directories("/home/mwaite/hub/libraries"))
        elif dest == "PLUGINS.md":
            process_directories("My Plugins",      "Plugins",             f, list_directories("/home/mwaite/hub/my-plugins"))
            process_directories("Orphan Plugins",  "Plugins",             f, list_directories("/home/mwaite/hub/orphans"))
        else:
            process_directories("Top 250 Plugins", "Plugins",             f, list_directories("/home/mwaite/all/popular-250"))
