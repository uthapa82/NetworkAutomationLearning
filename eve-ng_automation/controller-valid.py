import sys
import getpass
import time
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def update_passwords(file_path, current_pw, new_pw):
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find the file '{file_path}'. Please check the name.")
        return

    for line in lines:
        try:
            hostname, ip = line.split(';')
            hostname = hostname.strip()
            ip = ip.strip()
        except ValueError:
            print(f"Skipping invalid line format: {line}")
            continue

        print(f"\n--- Processing {hostname} ({ip}) ---")

        try:
            device = {
                'device_type': 'linux',
                'host': ip,
                'username': 'root',
                'password': current_pw,
                'timeout': 30,
                'session_timeout': 60,
            }

            print(f"Connecting to {hostname}...")
            connection = ConnectHandler(**device)

            print(f"Sending password change command to {hostname}...")

            # Send passwd command and wait for "(current) UNIX password:" prompt
            output = connection.send_command_timing(
                'passwd',
                strip_prompt=False,
                strip_command=False,
                read_timeout=10
            )
            print(f"[DEBUG] After passwd: {output.strip()}")

            # Matches exactly: "(current) UNIX password:"
            if 'current' in output.lower():
                output = connection.send_command_timing(
                    current_pw,
                    strip_prompt=False,
                    strip_command=False,
                    read_timeout=10
                )
                print(f"[DEBUG] After current UNIX password: {output.strip()}")

            # Matches exactly: "New password:"
            if 'new password' in output.lower():
                output = connection.send_command_timing(
                    new_pw,
                    strip_prompt=False,
                    strip_command=False,
                    read_timeout=10
                )
                print(f"[DEBUG] After new password: {output.strip()}")

            # Matches exactly: "Retype new password:"
            if 'retype' in output.lower():
                output = connection.send_command_timing(
                    new_pw,
                    strip_prompt=False,
                    strip_command=False,
                    read_timeout=10
                )
                print(f"[DEBUG] After retype new password: {output.strip()}")

            # Wait for device to process the change
            print(f"Waiting for {hostname} to process the change...")
            time.sleep(10)

            # Check final output for success or failure
            if any(word in output.lower() for word in ['successfully', 'updated', 'changed']):
                print(f"Success: Password updated for {hostname}")
            elif any(word in output.lower() for word in ['failure', 'error', 'failed', 'denied', 'mistake']):
                print(f"Error: Password change failed for {hostname}")
                print(f"Device output: {output.strip()}")
            else:
                # Device likely closed session after change which is normal
                print(f"Success: Password change command sent to {hostname}")
                print(f"Device output: {output.strip()}")

            connection.disconnect()

        except NetmikoTimeoutException:
            print(f"Error: Timed out connecting to {hostname}. Check if the IP is reachable.")
        except NetmikoAuthenticationException:
            print(f"Error: Authentication failed on {hostname}. Check the current password.")
        except Exception as e:
            print(f"Error on {hostname}: {str(e)}")


if __name__ == '__main__':
    FILE_PATH = "hosts.txt"

    print("=== Secure Bulk Password Update ===")

    current_password = getpass.getpass("Enter Current (Expired) Password: ")
    new_password = getpass.getpass("Enter New Password: ")
    confirm_password = getpass.getpass("Retype New Password to confirm: ")

    if new_password != confirm_password:
        print("\nError: The new passwords you typed do not match. Exiting script.")
        sys.exit(1)

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
    