def add_router_connections(self, ws_fiber, site_data, start_row):
    """Add router interconnect connections to FIBER with X-CONNECT tab."""
    clli = site_data.get('CLLI', '')
    additional_blade = site_data.get('Additional_blade', 0)
    existing_blade = site_data.get('Existing_blade', 0)
    router_ports_str = site_data.get('router_ports', '')
    
    # Convert to integers if they're strings or floats
    try:
        additional_blade = int(additional_blade) if pd.notna(additional_blade) else 0
        existing_blade = int(existing_blade) if pd.notna(existing_blade) else 0
    except (ValueError, TypeError):
        print(f"  Warning: Invalid blade values. Skipping router connections.")
        return
    
    if additional_blade == 0:
        print(f"  No additional blades to add. Skipping router connections.")
        return
    
    # Parse router ports - handle both string and already-parsed formats
    if not router_ports_str or pd.isna(router_ports_str):
        print(f"  Warning: No router ports specified. Skipping router connections.")
        return
    
    # Convert to string and clean up any extra spaces
    router_ports_str = str(router_ports_str).strip()
    
    # Split by comma and clean each port
    router_ports = [port.strip() for port in router_ports_str.split(',') if port.strip()]
    
    print(f"  Parsed {len(router_ports)} router ports: {router_ports}")
    
    if len(router_ports) < additional_blade:
        print(f"  Warning: Not enough router ports ({len(router_ports)}) for {additional_blade} connections. Using available ports.")
    
    # Calculate per-device blade counts
    additional_per_device = additional_blade // 2
    existing_per_device = existing_blade // 2
    
    # Starting slot number (after existing blades)
    start_slot_index = existing_per_device
    
    # Firewall and Router hostnames
    firewall_01 = f"{clli}Firewall-01"
    firewall_02 = f"{clli}Firewall-02"
    router_07 = f"{clli}Router-07"
    router_06 = f"{clli}Router-06"
    
    print(f"  Adding {additional_blade} router connections ({additional_per_device} per firewall)")
    
    current_row = start_row
    
    # Add black separator row before router connections
    self.fill_row_black(ws_fiber, current_row)
    current_row += 1
    
    # Add connections for Firewall-01 to Router-07
    for i in range(additional_per_device):
        # Calculate slot number (odd numbers: 1, 3, 5, 7...)
        slot_number = (start_slot_index + i) * 2 + 1
        
        # Get router port and extract slot number
        router_port = router_ports[i] if i < len(router_ports) else ""
        
        # Extract slot number (first part before first slash)
        if router_port and '/' in router_port:
            router_slot = router_port.split('/')[0]
        else:
            router_slot = router_port  # Fallback if no slash found
        
        print(f"    FW-01 Connection {i+1}: Slot {slot_number} -> Router Port: {router_port}, Router Slot: {router_slot}")
        
        # Column D: TYPE
        ws_fiber[f'D{current_row}'] = "SM DUP"
        
        # Column E: COLOR
        ws_fiber[f'E{current_row}'] = "YL"
        
        # Column I: DEVICE NAME (Firewall-01)
        ws_fiber[f'I{current_row}'] = firewall_01
        
        # Column J: SLOT
        ws_fiber[f'J{current_row}'] = slot_number
        
        # Column K: PORT (TX/RX) - always 2 for router connections
        ws_fiber[f'K{current_row}'] = 2
        
        # Column L: CON TYPE
        ws_fiber[f'L{current_row}'] = "LC"
        
        # Column BF: DEVICE NAME (Router-07)
        ws_fiber[f'BF{current_row}'] = router_07
        
        # Column BG: SLOT (first number from router port)
        ws_fiber[f'BG{current_row}'] = router_slot
        
        # Column BH: PORT (full router port)
        ws_fiber[f'BH{current_row}'] = router_port
        
        # Column BI: CON TYPE
        ws_fiber[f'BI{current_row}'] = "LC"
        
        current_row += 1
    
    print(f"  Added {additional_per_device} connections: {firewall_01} to {router_07}")
    
    # Add black separator row between Firewall-01 and Firewall-02 connections
    self.fill_row_black(ws_fiber, current_row)
    current_row += 1
    
    # Add connections for Firewall-02 to Router-06
    for i in range(additional_per_device):
        # Calculate slot number (odd numbers: 1, 3, 5, 7...)
        slot_number = (start_slot_index + i) * 2 + 1
        
        # Get router port from the second half of the list
        port_index = additional_per_device + i
        router_port = router_ports[port_index] if port_index < len(router_ports) else ""
        
        # Extract slot number (first part before first slash)
        if router_port and '/' in router_port:
            router_slot = router_port.split('/')[0]
        else:
            router_slot = router_port  # Fallback if no slash found
        
        print(f"    FW-02 Connection {i+1}: Slot {slot_number} -> Router Port: {router_port}, Router Slot: {router_slot}")
        
        # Column D: TYPE
        ws_fiber[f'D{current_row}'] = "SM DUP"
        
        # Column E: COLOR
        ws_fiber[f'E{current_row}'] = "YL"
        
        # Column I: DEVICE NAME (Firewall-02)
        ws_fiber[f'I{current_row}'] = firewall_02
        
        # Column J: SLOT
        ws_fiber[f'J{current_row}'] = slot_number
        
        # Column K: PORT (TX/RX) - always 2 for router connections
        ws_fiber[f'K{current_row}'] = 2
        
        # Column L: CON TYPE
        ws_fiber[f'L{current_row}'] = "LC"
        
        # Column BF: DEVICE NAME (Router-06)
        ws_fiber[f'BF{current_row}'] = router_06
        
        # Column BG: SLOT (first number from router port)
        ws_fiber[f'BG{current_row}'] = router_slot
        
        # Column BH: PORT (full router port)
        ws_fiber[f'BH{current_row}'] = router_port
        
        # Column BI: CON TYPE
        ws_fiber[f'BI{current_row}'] = "LC"
        
        current_row += 1
    
    print(f"  Added {additional_per_device} connections: {firewall_02} to {router_06}")
    print(f"  Successfully added all router connections")
    
    return current_row
```

**Key improvements:**

1. **Better port parsing**: Added `if port.strip()` to filter out empty strings after splitting
2. **Debugging output**: Added print statements to show what ports are being parsed and used
3. **Better slot extraction**: Improved the logic to extract the slot number from the port string
4. **Fallback handling**: If no slash is found in the port string, it uses the entire string as the slot

**Your data format `"4/1/c23/1,4/1/c29/1,5/1/c23/1"` should work fine now.**

Make sure in your Excel data sheet:
- There are **no extra spaces** before or after the commas
- The format is exactly: `4/1/c23/1,4/1/c29/1,5/1/c23/1` (no spaces)
- Or with spaces: `4/1/c23/1, 4/1/c29/1, 5/1/c23/1` (both work)

If you still have issues, check the console output when running the script - it will now print:
```
  Parsed X router ports: ['4/1/c23/1', '4/1/c29/1', '5/1/c23/1']
    FW-01 Connection 1: Slot 17 -> Router Port: 4/1/c23/1, Router Slot: 4