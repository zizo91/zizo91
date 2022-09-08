import re
lldp_run = '''result
Capability codes:
    (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
    (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other

Device ID           Local Intf     Hold-time  Capability      Port ID
XRV4                Gi4            120        R               Gi0/0/0/1
CSR3.cisco.com      Gi2            120        R               Gi2
vIOS1.cisco.com     Gi3            120        R               Gi0/1

Total entries displayed: 3

CSR2#'''

lldp = lldp_run.split('\n')

for neigh in range(6,len(lldp)-4):
    # print(lldp[neigh].split())
    hostname_ID = re.findall('\d+',lldp[neigh].split()[0])[0]
    Local_port = lldp[neigh].split()[1]
    print(hostname_ID, Local_port)

# https://www.regextutorial.org/regex-for-numbers-and-ranges.php