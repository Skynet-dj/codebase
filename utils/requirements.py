import subprocess
import sys
import os

ENABLE_PROGRESS_BAR = True  # Default is False, no logging unless run directly

# Function to check if a package is already installed
def is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

# Function to print the progress bar
def print_progress_bar(completed, total, bar_length=30):
    os.system("cls" if os.name == "nt" else "clear")
    percent = (completed / total) * 100
    filled_length = int(bar_length * completed // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f"\nInstalling dependencies..")
    print(f"[{bar}] {percent:.1f}%")

# Function to read the requirements.txt file and install the necessary packages
def install_requirements(requirements_file="requirements.txt"):
    os.system("cls" if os.name == "nt" else "clear")

    try:
        print(f"Reading requirements from {requirements_file}...")
        with open(requirements_file, 'r') as file:
            packages = file.readlines()

        total_packages = len(packages)
        for i, package in enumerate(packages):

            #printing----------
            if ENABLE_PROGRESS_BAR:
                print_progress_bar(i, total_packages)


            package = package.strip()
            if not package:
                print("Skipping empty line in requirements file.")
                continue

            package_name = package.split('==')[0].split('>=')[0].split('<=')[0]

            # Print the progress bar at the start of each iteration
            

            # Check if the package is already installed
            if is_package_installed(package_name):
                print(f"Skipping installation for {package_name}, already installed.")
                continue  # Skip to the next package
            
            print(f"Attempting to install {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

        print("Installation Complete!")

    except FileNotFoundError:
        print(f"Error: {requirements_file} not found.")
    except Exception as e:
        print(f"An error occurred while processing requirements: {e}")
    


# Test the program by running this section directly
if __name__ == "__main__":
    ENABLE_PROGRESS_BAR = False  # Set to True if you want to see logs
    requirements_file = 'requirements.txt'  # Adjust the path as needed
    install_requirements(requirements_file)
