import pandas as pd

# Define the functions
def extract_mgmt_prefix(ip):
    return ip.split('::')[0]

def normalize_assigned_prefix(ip):
    return ip.rstrip('::')

# Load the files
mgmt_ip_df = pd.read_csv('mgmt-ip.csv')
assigned_ipv6_df = pd.read_csv('assignment-ipv6.csv')

# Clean Column Names
mgmt_ip_df.columns = mgmt_ip_df.columns.str.strip()
assigned_ipv6_df.columns = assigned_ipv6_df.columns.str.strip()

# Prepare mgmt_ip_df
mgmt_ip_df.dropna(subset=['Management IPs'], inplace=True)
mgmt_ip_df['Sites'] = mgmt_ip_df['Sites'].ffill()
mgmt_ip_df['Mgmt_Prefix'] = mgmt_ip_df['Management IPs'].apply(extract_mgmt_prefix)
mgmt_prefix_df = mgmt_ip_df.groupby('Sites')['Mgmt_Prefix'].first().reset_index()
mgmt_prefix_df.rename(columns={'Mgmt_Prefix': 'Actual_Prefix'}, inplace=True)

# Prepare assigned_ipv6_df
assigned_ipv6_df['Assigned_Prefix'] = assigned_ipv6_df['Management IPs'].apply(normalize_assigned_prefix)
assigned_prefix_df = assigned_ipv6_df[['Sites', 'Assigned_Prefix']]

# Merge and Compare
comparison_df = pd.merge(mgmt_prefix_df, assigned_prefix_df, on='Sites', how='inner')
comparison_df['Match'] = comparison_df['Actual_Prefix'] == comparison_df['Assigned_Prefix']



# Select and rename final columns for a clean output file
final_output = comparison_df[['Sites', 'Actual_Prefix', 'Assigned_Prefix', 'Match']]
final_output.rename(columns={
    'Actual_Prefix': 'Mgmt_IP_Prefix',
    'Assigned_Prefix': 'Assigned_IPv6_Prefix'
}, inplace=True)

# Save the final output to an Excel file
final_output.to_excel('ipv6_prefix_match_results.xlsx', index=False)

