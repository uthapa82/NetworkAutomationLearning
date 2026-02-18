import sys
import getpass
import time
import pexpect
from pexpect.popen_spawn import PopenSpawn

def update_passwords(file_path, current_pw, new_pw):
    # 1. Read and parse the text file
    try:
        with open(file_path, 'r') as file:
            # Filters out empty lines
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find the file '{file_path}'. Please check the name.")
        return

    for line in lines:
        try:
            # Parse the format: HOSTNAME.domain.com;ipv6address
            hostname, ip = line.split(';')
            hostname = hostname.strip()
            ip = ip.strip()
        except ValueError:
            print(f"Skipping invalid line format: {line}")
            continue

        print(f"\n--- Processing {hostname} ({ip}) ---")

        child = None
        try:
            # 2. Spawn the SSH session using Windows built-in OpenSSH explicitly
            # StrictHostKeyChecking=no and UserKnownHostsFile=NUL together ensure
            # the host key popup never appears, even on first connection
            command = [
                r'C:\Windows\System32\OpenSSH\ssh.exe',
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=NUL',
                f'root@{ip}'
            ]

            # PopenSpawn is required for Windows. encoding='utf-8' allows us to match standard text.
            child = PopenSpawn(command, encoding='utf-8', timeout=15)

            # 3. Handle the login and password change sequence
            # Wait for "password:" prompt and send the expired password
            child.expect('(?i)password:')
            child.sendline(current_pw)

            # Matches "(current) UNIX password:" (we use a wildcard .* to handle the brackets safely)
            child.expect('(?i)current.*password:')
            child.sendline(current_pw)

            # Matches "New password:"
            child.expect('(?i)new password:')
            child.sendline(new_pw)

            # Matches "Retype new password:" — uses .* to handle variations across distros
            child.expect('(?i)retype.*password:')
            child.sendline(new_pw)

            # Wait 10 seconds for the device to process the password change
            print(f"Waiting for {hostname} to process the change...")
            time.sleep(10)

            # Wait for either a shell prompt or EOF after the password change
            # Timeout bumped to 15 to give extra breathing room on top of the sleep
            child.expect([r'[\$#]\s*$', pexpect.EOF], timeout=15)

            print(f"Success: Password updated for {hostname}")

        except pexpect.TIMEOUT:
            print(f"Error: Timed out on {hostname}. It might not have prompted for a password change.")
            if child is not None:
                print(f"Last output seen: {child.before.strip()}")
        except pexpect.EOF:
            print(f"Error: Connection closed unexpectedly on {hostname}. Check if the IP is reachable.")
        except Exception as e:
            print(f"Error on {hostname}: {str(e)}")


if __name__ == '__main__':
    # File containing your devices
    FILE_PATH = "hosts.txt"

    print("=== Secure Bulk Password Update ===")

    # Securely prompt for the passwords (characters will be hidden as you type)
    current_password = getpass.getpass("Enter Current (Expired) Password: ")
    new_password = getpass.getpass("Enter New Password: ")
    confirm_password = getpass.getpass("Retype New Password to confirm: ")

    if new_password != confirm_password:
        print("\nError: The new passwords you typed do not match. Exiting script.")
        sys.exit(1)

    # Show device count before proceeding as a safety check
    try:
        with open(FILE_PATH, 'r') as f:
            device_count = sum(1 for line in f if line.strip())
        print(f"\nFound {device_count} device(s) in '{FILE_PATH}'.")
    except FileNotFoundError:
        print(f"\nError: Could not find the file '{FILE_PATH}'. Exiting script.")
        sys.exit(1)

    confirm = input("Proceed with updating all devices? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Aborted by user.")
        sys.exit(0)

    print("\nStarting automated updates...")
    update_passwords(FILE_PATH, current_password, new_password)