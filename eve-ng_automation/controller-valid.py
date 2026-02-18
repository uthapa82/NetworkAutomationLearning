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
            # -tt forces a pseudo-terminal so the device presents password change prompts
            # Legacy MACs, Ciphers, Kex, and HostKey algorithms are included to support
            # older network devices that don't support modern OpenSSH defaults
            command = [
                r'C:\Windows\System32\OpenSSH\ssh.exe',
                '-tt',
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=NUL',
                '-o', 'MACs=hmac-sha1,hmac-sha2-256,hmac-sha2-512,hmac-md5,hmac-sha1-96,hmac-md5-96',
                '-o', 'KexAlgorithms=diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,diffie-hellman-group-exchange-sha1,diffie-hellman-group-exchange-sha256',
                '-o', 'HostKeyAlgorithms=ssh-rsa,ssh-dss',
                '-o', 'Ciphers=aes128-cbc,aes192-cbc,aes256-cbc,3des-cbc,aes128-ctr,aes192-ctr,aes256-ctr',
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

            # On many network devices the session closes right after a password change
            # So both a shell prompt AND EOF are treated as success
            index = child.expect([r'[\$#]\s*$', pexpect.EOF], timeout=15)

            if index == 0:
                print(f"Success: Password updated for {hostname} (shell prompt received)")
            elif index == 1:
                print(f"Success: Password updated for {hostname} (session closed after change, this is normal)")

        except pexpect.TIMEOUT:
            print(f"Error: Timed out on {hostname}. It might not have prompted for a password change.")
            if child is not None:
                print(f"Last output seen: {child.before.strip()}")
                print(f"All output: {child.before}")
        except pexpect.EOF:
            print(f"Error: Connection closed unexpectedly on {hostname}.")
            if child is not None:
                print(f"Last output seen: {child.before.strip()}")
                print(f"All output: {child.before}")
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