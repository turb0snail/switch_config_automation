import serial
import time
import getpass

def send_command(switch, command, wait_time=1):
    switch.write(command.encode() + b'\n')
    time.sleep(wait_time)


def expect_response(switch, expected_response, timeout=5):
    response = b""
    start_time = time.time()

    while time.time() - start_time < timeout:
        response += switch.read()
        if expected_response.encode() in response:
            return response.decode()
    
    return None

# def set_switch_password(switch):
#     response = expect_response(switch, "Enter Password:")
    
#     if response:
#         # Enter the new password directly in the script
#         new_password = "Admin12345@"  # Replace this with the actual new password
#         confirm_password = new_password

#         send_command(switch, new_password)

#         # Wait for the switch to process the first password entry
#         time.sleep(2)

#         # Send the confirmation password
#         send_command(switch, confirm_password)

#         # Wait for the switch to process the confirmation password
#         time.sleep(2)

#         # Check if the password change was successful
#         response = expect_response(switch, "Password is changed successfully")
#         if response:
#             print("Password changed successfully.")
#         else:
#             print("Failed to change the password.")
#     else:
#         print("Password is already set.")



def display_banner():
# Display a banner message
   banner = """
*****************************************************
*                                                   *                 
*   Huawei Switch S5735-L8P4X-QA-V2 Configuration   *
*                                                   *
*                                                   *
*****************************************************
"""
   print(banner)
   input("Press Enter to continue...")

def configure_switch():
    try:
        # Display the banner message
        display_banner()

        # Get user input for serial port
        serial_port = input("Enter the serial port (e.g., COM1 for Windows, /dev/ttyUSB0 for Linux): ") 

        # Open the serial connection to the switch
        switch = serial.Serial(serial_port, 9600, timeout=1)

        # Wait for the switch to initialize
        time.sleep(2)

        # Send commands to configure the switch
        send_command(switch, "")  # Press Enter to ensure you are in enable mode

        # Prompt for password securely
        password = getpass.getpass("Enter the switch password: ")
        send_command(switch, password)

        # Configure hostname
        hostname = input("Enter the hostname: ")
        send_command(switch, f"system-view")
        send_command(switch, f"sysname {hostname}")

        # Configure VLAN
        vlan_number = input("Enter VLAN number:")
        # vlan_name = input("Enter VLAN name: ")
        send_command(switch, f"vlan {vlan_number}")
        send_command(switch, f"name MANAGEMENT")
        send_command(switch, "quit")

        # User configuration commands
        send_command(switch, "telnet server enable")
        send_command(switch, "stelnet server enable")
        send_command(switch, "aaa")
        send_command(switch, f"local-user miaadmin password irreversible-cipher xxxx")
        send_command(switch, "local-user miaadmin privilege level 3")
        send_command(switch, "y")
        send_command(switch, "local-user miaadmin service-type telnet terminal ssh")
        send_command(switch, "quit")

        # Configure VLAN interface
        # vlan_interface = input("Enter VLAN interface:")
        vlan_ip = input("Enter VLAN interface IP (X.X.X.X): ")
        subnet_mask = input("Enter Subnet Mask (X.X.X.X): ")
        send_command(switch, f"interface Vlanif{vlan_number}")
        send_command(switch, f"ip address {vlan_ip} {subnet_mask}")
        send_command(switch, "quit")

        # Configure access ports
        send_command(switch, "port-group group-member GE 1/0/1 to GE 1/0/7")
        send_command(switch, f"port default vlan {vlan_number}")
        send_command(switch, "port link-type access")
        send_command(switch, "quit")

        # Configure trunk port
        # trunk_port = input("Enter trunk port (e.g., GigabitEthernet 0/0/8): ")
        send_command(switch, "interface 10GE 1/0/1")
        send_command(switch, "port link-type trunk")
        send_command(switch, f"port trunk allow-pass vlan {vlan_number}")
        send_command(switch, "quit")

        # Configure default route
        default_route = input("Enter default route (e.g., 0.0.0.0 0.0.0.0 x.x.x.x):")
        send_command(switch, f"ip route-static {default_route}")

        # Configure SSH settings
        send_command(switch, "user-interface vty 0 4")
        send_command(switch, "authentication-mode aaa")
        send_command(switch, "protocol inbound all")
        send_command(switch, "quit")

        # Additional settings
        send_command(switch, "user-interface console 0")
        send_command(switch, "authentication-mode aaa")
        send_command(switch, "protocol inbound all")
        send_command(switch, "quit")

        # Additional settings
        send_command(switch, f"ssh server-source -i Vlanif{vlan_number}")
        send_command(switch, "Y")
        send_command(switch, "ssh server-source all-interface")
        send_command(switch, "Y")
        send_command(switch, "ssh authorization-type default aaa")
        send_command(switch, "quit")
        send_command(switch, "quit")
        

        # # Save configuration
        # time.sleep(2)  # Delay to ensure previous commands are processed
        # send_command(switch, "save")
        # send_command(switch, "Y")

        # # Save to startup configuration
        # send_command(switch, "startup saved-configuration")

        # # Wait for 10 seconds
        # print("Waiting for 10 seconds after saving configuration...")
        # time.sleep(10)

        # Close the serial connection
        switch.close()

        print("Configuration completed.")

    except Exception as e:
        print(f"An error occurred: {e}")
        

if __name__ == "__main__":
    configure_switch()
