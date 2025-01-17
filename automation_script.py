import os
import sys
import json
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
        sys.exit(1)
    return result.stdout.strip() if capture_output else None

# Function to prompt for a valid directory
def prompt_for_directory(prompt_message):
    while True:
        directory = input(YELLOW + prompt_message + RESET).strip()
        directory = os.path.abspath(os.path.expanduser(directory))
        if Path(directory).is_dir():
            return directory
        print(RED + f"Invalid directory: {directory}. Please ensure the path exists." + RESET)

# Ensure the filesystem is fully updated before running cookiecutter
def force_sync():
    print(CYAN + "Forcing filesystem sync to ensure no stale state." + RESET)
    try:
        run_command("sync")  # Runs the sync command to flush filesystem buffers
        print(GREEN + "Filesystem synced successfully." + RESET)
    except Exception as e:
        print(RED + f"Error syncing filesystem: {e}" + RESET)
        sys.exit(1)

# Step 1: Prompt for project folder
print(YELLOW + "Please navigate to your preferred projects folder." + RESET)
print(RED + "Note: The folder must already exist." + RESET)
project_folder = prompt_for_directory("Enter the full path to your projects folder: ")
project_folder = Path(project_folder)

# Step 2: Clone the repository
repo_url = "git@github.com:twilio-internal/cloudquery-plugins.git"
print(CYAN + f"Cloning repository: {repo_url}" + RESET)
run_command(f"git clone {repo_url} {project_folder / 'cloudquery-plugins'}")

# Step 2.1: Create a feature branch
repo_path = project_folder / "cloudquery-plugins"
os.chdir(repo_path)
print(GREEN + f"Changed directory to: {repo_path}" + RESET)
plugin_name = input(YELLOW + "Enter the snake_case identifier for your plugin (e.g., proofpoint_psat): " + RESET).strip()
if not plugin_name:
    print(RED + "Plugin name is required." + RESET)
    sys.exit(1)
branch_name = f"feature/{plugin_name}-init"
print(CYAN + f"Creating feature branch: {branch_name}" + RESET)
run_command(f"git checkout -b {branch_name}")
print(GREEN + f"Created and switched to branch: {branch_name}" + RESET)

# Step 3: Verify and navigate into the plugins folder
plugins_dir = repo_path / "plugins"
if not plugins_dir.is_dir():
    print(RED + f"The expected plugins directory '{plugins_dir}' does not exist. Please check the repository structure." + RESET)
    sys.exit(1)

# Step 4: Sparse checkout cookiecutter template
cookiecutter_repo_url = "https://github.com/markgraziano-twlo/cloudquery-cookiecutter.git"
temp_repo_dir = project_folder / "temp_cookiecutter_repo"
cookiecutter_folder = "{{cookiecutter.plugin_name}}"

print(CYAN + f"Fetching {cookiecutter_folder} from {cookiecutter_repo_url}..." + RESET)

# Clone the repo sparsely with only the required folder
run_command(f"git clone --depth 1 --filter=blob:none --sparse {cookiecutter_repo_url} {temp_repo_dir}")
os.chdir(temp_repo_dir)
run_command(f"git sparse-checkout set {cookiecutter_folder}")

# Copy the cookiecutter template folder to the plugins directory
shutil.copytree(
    temp_repo_dir / cookiecutter_folder,
    plugins_dir / cookiecutter_folder  # Keep the placeholder format
)
print(GREEN + f"Copied {cookiecutter_folder} to {plugins_dir / cookiecutter_folder}" + RESET)

# Cleanup the temporary repository directory
shutil.rmtree(temp_repo_dir)
print(GREEN + "Temporary cookiecutter repository cleaned up." + RESET)

# Step 5: Prompt for cookiecutter variables
plugin_path = plugins_dir / cookiecutter_folder
print(GREEN + f"Changed directory to template: {plugin_path}" + RESET)

plugin_camel_case = input(YELLOW + "Enter the CamelCase identifier for your plugin (e.g., ProofpointPsat): " + RESET).strip()
record_type = input(YELLOW + "Enter the snake_case name for the record type (e.g., events, user_ids): " + RESET).strip()
api_base_url = input(YELLOW + "Enter the base URL for the API: " + RESET).strip()
team_name_email = input(YELLOW + "Enter your Full Name, Team Name: " + RESET).strip()

record_type_class = ''.join(word.capitalize() for word in record_type.split('_'))

cookiecutter_json = {
    "plugin_name": plugin_name,
    "PluginName": plugin_camel_case,
    "record_type": record_type,
    "RecordTypeClass": record_type_class,
    "APIBaseURL": api_base_url,
    "TeamNameTeamEmail": team_name_email
}

# Save cookiecutter.json in the plugins directory
with open(plugins_dir / "cookiecutter.json", "w") as f:
    json.dump(cookiecutter_json, f, indent=4)
print(GREEN + f"Generated cookiecutter.json at {plugins_dir}" + RESET)

# Ensure the filesystem is fully updated before running cookiecutter
force_sync()

# Step 6: Run cookiecutter refactoring
try:
    # Ensure we are in the correct working directory
    print(CYAN + "Ensuring correct working directory for cookiecutter execution..." + RESET)
    os.chdir(plugins_dir)
    print(GREEN + f"Current working directory: {os.getcwd()}" + RESET)

    # Run the cookiecutter command
    print(CYAN + "Running cookiecutter refactoring..." + RESET)
    run_command(f"pipx run cookiecutter . --no-input")  # Use `.` to indicate the current directory
    print(GREEN + "Performed cookiecutter refactoring." + RESET)

    # Validate the expected plugin folder
    plugin_path = plugins_dir / plugin_name
    if not plugin_path.is_dir():
        print(RED + f"Error: Plugin directory '{plugin_path}' not found after refactoring." + RESET)
        sys.exit(1)
    print(GREEN + f"Plugin directory after refactoring: {plugin_path}" + RESET)

except Exception as e:
    print(RED + f"Error during cookiecutter refactoring: {e}" + RESET)
    sys.exit(1)

finally:
    # Restore the original working directory
    os.chdir(repo_path)
    print(GREEN + f"Restored working directory to: {os.getcwd()}" + RESET)

# Step 7: OpenAPI cleanup
openapi_support = input(YELLOW + "Does the source support OpenAPI (y/n)? " + RESET).strip().lower()
if openapi_support == 'n':
    for root, dirs, files in os.walk(plugin_path, topdown=False):
        for name in files:
            if "oapi" in name:
                os.remove(Path(root) / name)
        for name in dirs:
            if "oapi" in name:
                shutil.rmtree(Path(root) / name)
    print(GREEN + "Deleted OpenAPI-related files and folders." + RESET)

# Step 8: Completion message
input(CYAN + "You are now ready to start modifying the project files in your preferred IDE. Hit Enter to close the terminal." + RESET)
