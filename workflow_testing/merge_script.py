import os
import random
import string
import subprocess
import sys

BASE_BRANCH = "main"
BRANCH_PREFIX = "testing"


def random_string(length=6):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def create_branch(branch_name):
    subprocess.run(["git", "checkout", BASE_BRANCH], check=True)
    subprocess.run(["git", "pull", "origin", BASE_BRANCH], check=True)
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)


def push_and_pr(branch_name, file_paths):
    subprocess.run(["git", "add"] + file_paths, check=True)
    subprocess.run(["git", "commit", "-m", "add test files"], check=True)
    subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

    subprocess.run([
        "gh", "pr", "create",
        "--base", BASE_BRANCH,
        "--head", branch_name,
        "--title", f"Add files for {branch_name}",
        "--body", "automated test"
    ], check=True)


def normal_mode(count):
    for _ in range(count):
        rand = random_string()
        branch_name = f"{BRANCH_PREFIX}-{rand}"
        file_path = f"test_folder/file_{rand}.txt"

        create_branch(branch_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(f"this is a test file for test branch: {rand}\n")

        push_and_pr(branch_name, [file_path])


def number_mode():
    rand = random_string()
    branch_name = f"number-{rand}"
    file_path = f"example_file/number_{rand}.txt"

    create_branch(branch_name)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write("120\n")

    push_and_pr(branch_name, [file_path])


def break_mode():
    rand = random_string()
    branch_name = f"break-{rand}"

    create_branch(branch_name)

    os.makedirs("example_file", exist_ok=True)
    file_paths = []
    for i in range(2):
        file_path = f"example_file/number_{rand}_{i}.txt"
        with open(file_path, "w") as f:
            f.write("120\n")
        file_paths.append(file_path)

    push_and_pr(branch_name, file_paths)


mode = sys.argv[1] if len(sys.argv) > 1 else "normal"
count = int(sys.argv[2]) if len(sys.argv) > 2 and mode == "normal" else 1

if mode == "normal":
    normal_mode(count)
elif mode == "number":
    number_mode()
elif mode == "break":
    break_mode()
else:
    print("Usage:")
    print("python3 merge_script.py normal [count]")
    print("python3 merge_script.py number")
    print("python3 merge_script.py break")
