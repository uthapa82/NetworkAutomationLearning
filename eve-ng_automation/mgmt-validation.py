import openpyxl
import getpass
import paramiko
import socket

def ssh_connect(ip_address, old_password, new_password):
    """
    Attempt to connect via SSH using old password, then new password.
    Returns: (result_status, password_in_use)
    """
    passwords = [old_password, new_password]
    pwd_names = ['old password', 'new password']
    
    for pwd, pwd_name in zip(passwords, pwd_names):
        ssh = None
        try:
            print(f"  Trying {pwd_name}...")
            
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Try to connect
            ssh.connect(
                hostname=ip_address,
                username='root',
                password=pwd,
                timeout=10,
                look_for_keys=False,
                allow_agent=False
            )
            
            # If we get here, connection was successful
            print(f"  ✓ Login successful with {pwd_name}")
            ssh.close()
            return ("Login Successful", pwd_name)
            
        except paramiko.AuthenticationException:
            print(f"  ✗ Authentication failed with {pwd_name}")
            if ssh:
                ssh.close()
        except socket.timeout:
            print(f"  ✗ Connection timeout")
            if ssh:
                ssh.close()
        except Exception as e:
            print(f"  ✗ Connection error: {str(e)}")
            if ssh:
                ssh.close()
    
    # Both passwords failed
    print(f"  ✗ Both passwords failed")
    return ("Login Failed", "Login Failed")


def process_excel():
    """Main function to process Excel file"""
    
    # Ask for two passwords
    print("Enter old password:")
    old_password = getpass.getpass()
    print("Enter new password:")
    new_password = getpass.getpass()
    
    # Excel file path
    file_path = "C:\\path\\to\\your_file.xlsx"
    
    # Load workbook and sheet
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    
    # Find column indices
    header_map = {}
    for cell in sheet[1]:
        if cell.value:
            header_map[cell.value.lower().strip().replace('-', ' ')] = cell.column_letter
    
    # Look for the required columns
    results_col = header_map.get('results')
    password_col = header_map.get('password in use') or header_map.get('passwordinuse')
    
    if not all([results_col, password_col]):
        print("\nERROR: Required columns not found.")
        print(f"Found columns: {list(header_map.keys())}")
        print("Need: 'Results' and 'password-in-use' columns")
        return
    
    print(f"\n✓ Using columns: Results={results_col}, Password-in-use={password_col}\n")
    
    # Process each row
    success_count = 0
    fail_count = 0
    
    for row in range(2, sheet.max_row + 1):
        ip_address = sheet[f'B{row}'].value
        
        if not ip_address:
            continue
        
        print(f"\n{'='*60}")
        print(f"Row {row}: {ip_address}")
        print(f"{'='*60}")
        
        # Attempt SSH connection
        result_status, password_in_use = ssh_connect(ip_address, old_password, new_password)
        
        # Write results
        sheet[f'{results_col}{row}'] = result_status
        sheet[f'{password_col}{row}'] = password_in_use
        
        if result_status == "Login Successful":
            success_count += 1
            print(f"✓ Row {row} completed\n")
        else:
            fail_count += 1
            print(f"✗ Row {row} failed\n")
    
    # Save workbook
    wb.save(file_path)
    
    print("\n" + "="*60)
    print(f"✅ Completed!")
    print(f"   Successful: {success_count}")
    print(f"   Failed: {fail_count}")
    print(f"   Results saved to: {file_path}")
    print("="*60)


if __name__ == "__main__":
    process_excel()