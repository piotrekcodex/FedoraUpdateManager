import subprocess
import getpass
import time


# Check for root privileges and ask for the password if need
def check_for_root():
    # Check for root subprocess (return a string)
    root_check = subprocess.run(["id", "-u"], capture_output=True, text=True).stdout.strip()

    # Check for root subprocess
    sudo_check = subprocess.run(["sudo", "-n", "true"], capture_output=True).returncode

    # Check for root access or if password is cached (if cache timestamp has not expired yet)
    try:
        # Check for root user or privileges by sudo
        if root_check == "0" or sudo_check == 0:
            return 0
        else:
            print("[ NOTICE! ] -> Please, run me as root!")
            password = getpass.getpass("[ Trusted ] -> Specify the root password:")

            if subprocess.run(["sudo", "-S", "true"], input=password, capture_output=True, text=True).returncode == 0:
                return 0
            else:
                time.sleep(3)
                print("[ ERROR!! ] -> Incorrect password!")
                return 1
    except subprocess.CalledProcessError as error:
        print(error.output)


# Perform a packages update
def check_packages_updates():
    check_for_root()

    updates_execution = subprocess.run(["sudo", "dnf", "-y", "upgrade", "--refresh"], capture_output=True, text=True)

    try:
        print("Checking for package updates...")

        # Try to execute user-selected packages installation
        if updates_execution.returncode == 0:
            print(">>>   All packages are up to date!   <<<")
            print(updates_execution.stdout)
            return 0
        else:
            print(">>>   ERROR: System update failed   <<<")
            print(updates_execution.stderr)
            return 1
    except subprocess.CalledProcessError as error:
        print(error.output)


check_packages_updates()