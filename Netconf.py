from ncclient import manager
import xmltodict
import xml.dom.minidom

#create filter to get specific part of configuration#
netconf_filter = """
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
    </interface>
    </interfaces>"""

#create XML interface description configuration#
config_interface ='''
                        <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                                <name>GigabitEthernet3</name>
                                <description>Test3</description>
                        </interface>
                        </interfaces>
                        </config>
'''

#create XML delete interface description#
delete_config ='''
                       <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                                <name>GigabitEthernet2</name>
                                <description operation="delete">Test3</description>
                        </interface>
                        </interfaces>
                        </config>

'''

#open netconf session to the server (device)
with manager.connect(host='sandbox-iosxe-latest-1.cisco.com',port=830,username='developer',password='C1sco12345',hostkey_verify=False) as session:
    #send RPC query to configure description for the interface on running datastore
    netconf_reply_config = session.edit_config(target = 'running', config =config_interface)
    #send RPC query to delet the interface description on running datastore
    netconf_reply_del_config = session.edit_config(target = 'running', config = delete_config)
    #send RPC to get interfaces configuration from running datastore 
    netconf_reply_interfaces = session.get_config(source = 'running', filter=("subtree", netconf_filter))
    #send RPC to get running configuration, using get operation always return configuration of running datastore
    netconf_reply_running = session.get_config(source = 'running')
    # netconf_reply = session.get(filter=("subtree", netconf_filter))
#change xml output of rpc_reply to pretty string format
# print(xml.dom.minidom.parseString(netconf_reply_interfaces.xml).toprettyxml())


#open tow files for running configuration and capabilities
with open('IOSXE_Netconf_capabilities.txt', 'w') as file:
    file.write('\n'.join(session.server_capabilities))
with open ('IOSXE_Netconf_Running_config.xml', 'w') as file:
    file.write(xml.dom.minidom.parseString(netconf_reply_running.xml).toprettyxml())


# Parse the returned XML to an Ordered Dictionary
netconf_data = xmltodict.parse(netconf_reply_interfaces.xml)["rpc-reply"]["data"]

# Create a list of interfaces
interfaces = netconf_data["interfaces"]["interface"]

# print(interfaces)

#Notes
################-----------------------------------------------#####################################

# rpc reply message for edit_config operation#
#<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:79fca487-0527-4e36-ad0c-c4a5e8713f11" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"><ok/></rpc-reply>

#Resources
# https://developer.cisco.com/learning/labs/intro-netconf/breaking-down-netconf-communications/
# https://devnetsandbox.cisco.com/RM/Topology
# https://aristanetworks.github.io/openmgmt/examples/netconf/ncclient/


