import sys
import getpass
import time
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

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

        try:
            # 2. Define the device connection parameters
            # device_type 'linux' works for most Unix/Linux based network devices
            # If your device is a Cisco, Juniper, etc. change device_type accordingly
            device = {
                'device_type': 'linux',
                'host': ip,
                'username': 'root',
                'password': current_pw,
                'timeout': 30,
                'session_timeout': 60,
                # These allow Netmiko to handle expired password prompts
                'handling_password_change': True,
                'secret': current_pw,
            }

            # 3. Connect to the device
            print(f"Connecting to {hostname}...")
            connection = ConnectHandler(**device)

            # 4. Send the passwd command and handle the prompts
            print(f"Sending password change command to {hostname}...")

            # Send passwd command and wait for current password prompt
            output = connection.send_command_timing(
                'passwd',
                strip_prompt=False,
                strip_command=False,
                read_timeout=10
            )

            # Handle current password prompt
            if 'current' in output.lower() or 'password' in output.lower():
                output += connection.send_command_timing(
                    current_pw,
                    strip_prompt=False,
                    strip_command=False,
                    read_timeout=10
                )

            # Handle new password prompt
            if 'new' in output.lower() or 'password' in output.lower():
                output += connection.send_command_timing(
                    new_pw,
                    strip_prompt=False,
                    strip_command=False,
                    read_timeout=10
                )

            # Handle retype/confirm password prompt
            if 'retype' in output.lower() or 'confirm' in output.lower() or 'new' in output.lower():
                output += connection.send_command_timing(
                    new_pw,
                    strip_prompt=False,
                    strip_command=False,
                    read_timeout=10
                )

            # Wait for device to process
            print(f"Waiting for {hostname} to process the change...")
            time.sleep(10)

            # Check the output for success or failure indicators
            if any(word in output.lower() for word in ['successfully', 'updated', 'changed']):
                print(f"Success: Password updated for {hostname}")
            elif any(word in output.lower() for word in ['failure', 'error', 'failed', 'denied']):
                print(f"Error: Password change may have failed for {hostname}")
                print(f"Device output: {output.strip()}")
            else:
                # If no clear success/failure message, assume success and show output
                print(f"Success: Password change command sent to {hostname}")
                print(f"Device output: {output.strip()}")

            # 5. Disconnect cleanly
            connection.disconnect()

        except NetmikoTimeoutException:
            print(f"Error: Timed out connecting to {hostname}. Check if the IP is reachable.")
        except NetmikoAuthenticationException:
            print(f"Error: Authentication failed on {hostname}. Check the current password.")
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