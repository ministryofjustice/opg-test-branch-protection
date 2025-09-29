import os
import random
import string
import subprocess

BASE_BRANCH = "main"
BRANCH_PREFIX = "testing"

rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
branch_name = f"{BRANCH_PREFIX}-{rand}"
file_path = f"test_folder/file_{rand}.txt"

subprocess.run(["git", "checkout", BASE_BRANCH], check=True)
subprocess.run(["git", "pull", "origin", BASE_BRANCH], check=True)
subprocess.run(["git", "checkout", "-b", branch_name], check=True)

os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, "w") as f:
    f.write("this is a test file for test branch: " + rand + "\n")

subprocess.run(["git", "add", file_path], check=True)
subprocess.run(["git", "commit", "-m", "add test file"], check=True)
subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

subprocess.run([
    "gh", "pr", "create",
    "--base", BASE_BRANCH,
    "--head", branch_name,
    "--title", f"Add {file_path}",
    "--body", "automated test"
], check=True)
