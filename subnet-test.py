import ipaddress

# Create a IPv4Network object for the subnet
subnet = ipaddress.IPv4Network('10.2.2.0/24')

# Check if a host belongs to the subnet
host = ipaddress.IPv4Address('10.2.2.10')
if host in subnet:
    print(f"{host} belongs to {subnet}")
else:
    print(f"{host} does not belong to {subnet}")
