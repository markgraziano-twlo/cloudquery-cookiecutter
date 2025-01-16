import os
import subprocess
import shutil
from pathlib import Path

# ANSI color codes for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Function to run shell commands
def run_command(command, capture_output=False):
    result = subprocess.run(command, shell=True, text=True, capture_output=capture_output)
    if result.returncode != 0:
        print(RED + f"Error executing command: {command}\n{result.stderr}" + RESET)
        exit(1)
    return result.stdout.strip() if capture_output else None

# Step 1: Prompt for project folder
print(YELLOW + "Please navigate to your preferred projects folder." + RESET)
project_folder = input(YELLOW + "Enter the full path to your projects folder: " + RESET).strip()
if not Path(project_folder).is_dir():
    print(RED + "Invalid directory. Please ensure the path exists." + RESET)
    exit(1)
os.chdir(project_folder)

# Step 2: Clone the repository
repo_url = "git@github.com:twilio-internal/cloudquery-plugins.git"
print(CYAN + f"Cloning repository: {repo_url}" + RESET)
run_command(f"git clone {repo_url}")

# Step 2.1: Create a feature branch
project_name = "cloudquery-plugins"
os.chdir(project_name)
print(GREEN + f"Changed directory to: {os.getcwd()}" + RESET)
plugin_name = input(YELLOW + "Enter the snake_case identifier for your plugin (e.g., proofpoint_psat): " + RESET).strip()
if not plugin_name:
    print(RED + "Plugin name is required." + RESET)
    exit(1)
branch_name = f"feature/{plugin_name}-init"
print(CYAN + f"Creating feature branch: {branch_name}" + RESET)
run_command(f"git checkout -b {branch_name}")
print(GREEN + f"Created and switched to branch: {branch_name}" + RESET)

# Step 3: Navigate into the plugins folder
os.chdir("plugins")
print(GREEN + f"Changed directory to: {os.getcwd()}" + RESET)

# Step 4: Sparse checkout cookiecutter template
cookiecutter_repo_url = "https://github.com/markgraziano-twlo/cloudquery-cookiecutter.git"
temp_repo_dir = "../temp_cookiecutter_repo"
cookiecutter_folder = "cookiecutter_template"

print(CYAN + f"Fetching {cookiecutter_folder} from {cookiecutter_repo_url}..." + RESET)

# Clone the repo sparsely with only the required folder
run_command(f"git clone --depth 1 --filter=blob:none --sparse {cookiecutter_repo_url} {temp_repo_dir}")
os.chdir(temp_repo_dir)
run_command(f"git sparse-checkout set {cookiecutter_folder}")

# Copy the cookiecutter template folder to the plugins directory
os.chdir("../cloudquery-plugins/plugins")
shutil.copytree(os.path.join(temp_repo_dir, cookiecutter_folder), os.path.join(os.getcwd(), plugin_name))
print(GREEN + f"Copied {cookiecutter_folder} to {plugin_name}" + RESET)

# Cleanup the temporary directory
shutil.rmtree(temp_repo_dir)
print(GREEN + "Cleaned up temporary files." + RESET)

# Step 5: Navigate to the new folder
os.chdir(plugin_name)
print(GREEN + f"Changed directory to: {os.getcwd()}" + RESET)

# Step 6: Prompt for cookiecutter variables
plugin_camel_case = input(YELLOW + "Enter the CamelCase identifier for your plugin (e.g., ProofpointPsat): " + RESET).strip()
record_type = input(YELLOW + "Enter the snake_case name for the record type (e.g., events, user_ids): " + RESET).strip()
api_base_url = input(YELLOW + "Enter the base URL for the API: " + RESET).strip()
team_name_email = input(YELLOW + "Enter your Full Name, Team Name: " + RESET).strip()

# Generate RecordTypeClass from record_type
record_type_class = ''.join(word.capitalize() for word in record_type.split('_'))

cookiecutter_json = {
    "plugin_name": plugin_name,
    "PluginName": plugin_camel_case,
    "record_type": record_type,
    "RecordTypeClass": record_type_class,
    "APIBaseURL": api_base_url,
    "TeamNameTeamEmail": team_name_email
}

# Save cookiecutter.json
import json
with open("cookiecutter.json", "w") as f:
    json.dump(cookiecutter_json, f, indent=4)
print(GREEN + "Generated cookiecutter.json" + RESET)

# Step 7: Check for OpenAPI support
openapi_support = input(YELLOW + "Does the source support OpenAPI (y/n)? " + RESET).strip().lower()
if openapi_support == 'n':
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:
            if "oapi" in name:
                os.remove(os.path.join(root, name))
        for name in dirs:
            if "oapi" in name:
                shutil.rmtree(os.path.join(root, name))
    print(GREEN + "Deleted OpenAPI-related files and folders." + RESET)

# Step 8: Perform cookiecutter variable refactoring
try:
    print(CYAN + "Installing pipx for cookiecutter management..." + RESET)
    run_command("pip install pipx")
    print(CYAN + "Installing cookiecutter using pipx..." + RESET)
    run_command("pipx install cookiecutter")
    print(CYAN + "Running cookiecutter refactoring..." + RESET)
    run_command(f"pipx run cookiecutter . --no-input")
    print(GREEN + "Performed cookiecutter refactoring." + RESET)
except Exception as e:
    print(RED + f"Error performing cookiecutter refactoring: {e}" + RESET)
    exit(1)

# Step 9: Delete cookiecutter.json if user confirms
delete_json = input(YELLOW + "Do you want to delete the cookiecutter.json file (y/n)? " + RESET).strip().lower()
if delete_json == 'y':
    os.remove("cookiecutter.json")
    print(GREEN + "Deleted cookiecutter.json." + RESET)

# Step 10: Prompt to open project in IDE
input(CYAN + "You are now ready to start modifying the project files in your preferred IDE. Hit Enter to close the terminal." + RESET)
