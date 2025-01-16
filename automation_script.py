import os
import subprocess
import shutil
from pathlib import Path
from termcolor import colored

# Function to run shell commands
def run_command(command, capture_output=False):
    result = subprocess.run(command, shell=True, text=True, capture_output=capture_output)
    if result.returncode != 0:
        print(colored(f"Error executing command: {command}\n{result.stderr}", "red"))
        exit(1)
    return result.stdout.strip() if capture_output else None

# Step 1: Prompt for project folder
print(colored("Please navigate to your preferred projects folder.", "cyan"))
project_folder = input(colored("Enter the full path to your projects folder: ", "yellow")).strip()
if not Path(project_folder).is_dir():
    print(colored("Invalid directory. Please ensure the path exists.", "red"))
    exit(1)
os.chdir(project_folder)

# Step 2: Clone the repository
repo_url = "git@github.com:twilio-internal/cloudquery-plugins.git"
print(colored(f"Cloning repository: {repo_url}", "cyan"))
run_command(f"git clone {repo_url}")

# Step 2.1: Create a feature branch
project_name = "cloudquery-plugins"
os.chdir(project_name)
print(colored(f"Changed directory to: {os.getcwd()}", "green"))
plugin_name = input(colored("Enter the snake_case identifier for your plugin (e.g., proofpoint_psat): ", "yellow")).strip()
if not plugin_name:
    print(colored("Plugin name is required.", "red"))
    exit(1)
branch_name = f"feature/{plugin_name}-init"
print(colored(f"Creating feature branch: {branch_name}", "cyan"))
run_command(f"git checkout -b {branch_name}")
print(colored(f"Created and switched to branch: {branch_name}", "green"))

# Step 3: Navigate into the plugins folder
os.chdir("plugins")
print(colored(f"Changed directory to: {os.getcwd()}", "green"))

# Step 4: Sparse checkout cookiecutter template
cookiecutter_repo_url = "https://github.com/markgraziano-twlo/cloudquery-cookiecutter.git"
temp_repo_dir = "../temp_cookiecutter_repo"
cookiecutter_folder = "cookiecutter_template"

print(colored(f"Fetching {cookiecutter_folder} from {cookiecutter_repo_url}...", "cyan"))

# Clone the repo sparsely with only the required folder
run_command(f"git clone --depth 1 --filter=blob:none --sparse {cookiecutter_repo_url} {temp_repo_dir}")
os.chdir(temp_repo_dir)
run_command(f"git sparse-checkout set {cookiecutter_folder}")

# Copy the cookiecutter template folder to the plugins directory
os.chdir("../cloudquery-plugins/plugins")
shutil.copytree(os.path.join(temp_repo_dir, cookiecutter_folder), os.path.join(os.getcwd(), plugin_name))
print(colored(f"Copied {cookiecutter_folder} to {plugin_name}", "green"))

# Cleanup the temporary directory
shutil.rmtree(temp_repo_dir)
print(colored("Cleaned up temporary files.", "green"))

# Step 5: Navigate to the new folder
os.chdir(plugin_name)
print(colored(f"Changed directory to: {os.getcwd()}", "green"))

# Step 6: Prompt for cookiecutter variables
plugin_camel_case = input(colored("Enter the CamelCase identifier for your plugin (e.g., ProofpointPsat): ", "yellow")).strip()
record_type = input(colored("Enter the snake_case name for the record type (e.g., events, user_ids): ", "yellow")).strip()
api_base_url = input(colored("Enter the base URL for the API: ", "yellow")).strip()
team_name_email = input(colored("Enter your Full Name, Team Name: ", "yellow")).strip()

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
print(colored("Generated cookiecutter.json", "green"))

# Step 7: Check for OpenAPI support
openapi_support = input(colored("Does the source support OpenAPI (y/n)? ", "yellow")).strip().lower()
if openapi_support == 'n':
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:
            if "oapi" in name:
                os.remove(os.path.join(root, name))
        for name in dirs:
            if "oapi" in name:
                shutil.rmtree(os.path.join(root, name))
    print(colored("Deleted OpenAPI-related files and folders.", "green"))

# Step 8: Perform cookiecutter variable refactoring
try:
    print(colored("Installing pipx for cookiecutter management...", "cyan"))
    run_command("pip install pipx")
    print(colored("Installing cookiecutter using pipx...", "cyan"))
    run_command("pipx install cookiecutter")
    print(colored("Running cookiecutter refactoring...", "cyan"))
    run_command(f"pipx run cookiecutter . --no-input")
    print(colored("Performed cookiecutter refactoring.", "green"))
except Exception as e:
    print(colored(f"Error performing cookiecutter refactoring: {e}", "red"))
    exit(1)

# Step 9: Delete cookiecutter.json if user confirms
delete_json = input(colored("Do you want to delete the cookiecutter.json file (y/n)? ", "yellow")).strip().lower()
if delete_json == 'y':
    os.remove("cookiecutter.json")
    print(colored("Deleted cookiecutter.json.", "green"))

# Step 10: Prompt to open project in IDE
input(colored("You are now ready to start modifying the project files in your preferred IDE. Hit Enter to close the terminal.", "cyan"))
