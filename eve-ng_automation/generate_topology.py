from evengsdk.client import EvengClient
import yaml
import getpass

# --- 1 Connect to EVE-NG server ---
username = input("Username: ")
password = getpass.getpass("Password: ")

host = input("EVE-NG Host (IP or URL): ")
eve = EvengClient(host, ssl_verify=False, protocol="http", port=80)
eve.disable_insecure_warnings()
eve.login(username=username, password=password)

print(f"\u2714 Connected to EVE-NG successfully")

# --- 2 Load lab topology YAML ---
with open("lab_topology.yml") as f:
    lab_data = yaml.safe_load(f)

lab_name = lab_data["lab"]["name"]
lab_path = lab_data["lab"].get("path", "/")

# Get default values
defaults = lab_data["lab"].get("defaults", {})
default_template = defaults.get("template", "vios")
default_image = defaults.get("image", "vios-adventerprisek9-m.SPA.159-3.M6")
default_node_type = defaults.get("node_type", "qemu")

# --- 3 Create a new lab ---
print(f"\nCreating lab '{lab_name}'...")
lab_config = {
    "name": lab_name,
    "description": lab_data["lab"].get("description", "Auto-generated lab"),
    "path": lab_path,
}
resp = eve.api.create_lab(**lab_config)

if resp.get("status") == "success":
    print(f"\u2714 Lab '{lab_name}' created successfully")

full_lab_path = f"{lab_path}{lab_name}.unl"

# --- 4 Create nodes ---
nodes = lab_data["lab"]["nodes"]
print(f"\nCreating {len(nodes)} nodes...")

# Auto-position parameters
start_x = 100   # starting horizontal position
start_y = 100   # starting vertical position
x_step = 250    # horizontal spacing between nodes
y_step = 200    # vertical spacing between rows
nodes_per_row = 3  # nodes per row

for i, node in enumerate(nodes):
    router_name = node["name"]

    node_template = node.get("template", default_template)
    node_image = node.get("image", default_image)
    node_type = node.get("node_type", default_node_type)

    # Calculate positions automatically
    left = start_x + (i % nodes_per_row) * x_step
    top = start_y + (i // nodes_per_row) * y_step

    node_config = {
        "name": router_name,
        "template": node_template,
        "image": node_image,
        "node_type": node_type,
        "left": left,
        "top": top
    }

    eve.api.add_node(full_lab_path, **node_config)
    print(f"\u2714 Node {router_name} created")


# --- 5 Create links ---
if "links" in lab_data["lab"]:
    print(f"\nCreating {len(lab_data['lab']['links'])} links...")
    for link in lab_data["lab"]["links"]:
        endpoints = link["endpoints"]
        node_a, intf_a = endpoints[0].split(":")
        node_b, intf_b = endpoints[1].split(":")

        link_config = {
            "src": node_a,
            "src_label": intf_a,
            "dst": node_b,
            "dst_label": intf_b,
        }

        eve.api.connect_node_to_node(full_lab_path, **link_config)
        print(f"\u2714 Link {node_a}:{intf_a} ↔ {node_b}:{intf_b} created")

# --- 6 Start all nodes ---
print(f"\nStarting all nodes in lab '{lab_name}'...")
eve.api.start_all_nodes(full_lab_path)
print(f"\u2714 All nodes started")

# --- 7 Final instructions ---
print("\n" + "=" * 70)
print(f"\u2714 Lab Creation Complete!")
print("=" * 70)
print(f"\nLab Name: {lab_name}")
print(f"Lab Path: {full_lab_path}")
print(f"Nodes Created: {len(nodes)}")
print(f"Links Created: {len(lab_data['lab'].get('links', []))}")


# Logout
# eve.logout()
# print("\nDisconnected from EVE-NG")
