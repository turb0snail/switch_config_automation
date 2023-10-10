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
*                    AVICOM                         *                 
*                                                   *
*     HP ARUBA Switch 6000 R8N89A Configuration     *
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
        switch = serial.Serial(serial_port, 115200, timeout=1)

        # Wait for the switch to initialize
        time.sleep(2)

        # Send commands to configure the switch
        send_command(switch, "")  # Press Enter to ensure you are in enable mode

        # Prompt for password securely
        password = getpass.getpass("Enter the switch password: ")
        send_command(switch, password)

        # Configure hostname
        hostname = input("Enter the hostname: ")
        send_command(switch, f"configure terminal")
        send_command(switch, f"hostname {hostname}")
        send_command(switch, "ssh server vrf default")

        # Configure VLAN
        vlan_number = input("Enter VLAN number:")
        send_command(switch, f"vlan {vlan_number}")
        send_command(switch, "name MANAGEMENT")
        send_command(switch, "exit")

        # Spanning-tree configuration commands
        send_command(switch, "spanning-tree")
        
        # Configure access ports
        send_command(switch, "interface 1/1/1-1/1/11")
        send_command(switch, f"vlan access {vlan_number}")
        send_command(switch, "description CAMERA")
        send_command(switch, "exit")
        send_command(switch, "interface 1/1/12-1/1/14")
        send_command(switch, "shutdown")
        send_command(switch, "exit")

        # Configure trunk ports
        send_command(switch, "interface 1/1/15-1/1/16")
        send_command(switch, "no shutdown")
        send_command(switch, f"vlan trunk allowed {vlan_number}")
        send_command(switch, "exit")

        # VLAN 1 shutdown
        send_command(switch, "interface vlan 1")
        send_command(switch, "shutdown")
        send_command(switch, "exit")

        # Configure VLAN interface
        # vlan_interface = input("VLAN interface nömrəsini qeyd et:")
        vlan_ip = input("VLAN interface İP-sini qeyd et (X.X.X.X): ")
        subnet_mask = input("Subnet Maskı qeyd et (X.X.X.X): ")
        send_command(switch, f"interface vlan {vlan_number}")
        send_command(switch, f"ip address {vlan_ip} {subnet_mask}")
        send_command(switch, "exit")

        # Configure default route
        default_route = input("Enter default route (e.g., 0.0.0.0 0.0.0.0 10.205.46.254):")
        send_command(switch, f"ip route {default_route}")
        
        
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
