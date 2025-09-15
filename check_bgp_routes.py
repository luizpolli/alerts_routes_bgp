from ctypes import util
import os, netmiko, random
import time
import utility

def check_bgp_routes():
  

  devices = {
    "ip": "10.224.80.56",
    "device_type": "cisco_xr",
    "username": "username",
    "password": "***********"
  }

  # Connecting to device
  print(f"Connecting to device {devices['ip']}...")
  conn = netmiko.ConnectHandler(**devices)

  # Running the command
  command = "show bgp vpnv4 unicast all summary" # Variable for the command
  print(f"Executing command {command}")
  outputbgp = conn.send_command(command)
  outputbgp = outputbgp.strip().splitlines()[16:]

  # Getting the number of routes and including in a list
  routes=[]
  for value in outputbgp:
    routes.append(value.split(" ")[-1])

  # Summing both bgp neighbors routes received
  sumbgproutes = int(routes[0])+int(routes[1])

  # Variable for Java Syslog Command Path
  javapathsyslog = "/opt/CSCOlumos/jre/bin/java -jar /localdisk/sftp/syslog/syslogGenerator.jar"
  

  # Running the SQL query in ORACLE
  # Sending CRITICAL syslog
  if (sumbgproutes > 20000):
    print("Generating CRITICAL syslog. Please wait a few seconds...")
    time.sleep(2)
    print(f"%BGPVPNv4ROUTE-2-BPGVPNv4ROUTEEXCEEDED : Route exceeded the amount of 20000. Value is {sumbgproutes} -destinationip 127.0.0.1 -destinationport 514 -sourceip {devices['ip']}")
    #os.system(f"{javapathsyslog} \"%BGPVPNv4ROUTE-2-BPGVPNv4ROUTEEXCEEDED : Route exceeded the amount of 20000. Value is {sumbgproutes}\" -destinationip 127.0.0.1 -destinationport 514 -sourceip {devices['ip']}")
  
  # Sending MAJOR syslog
  if (18000 <= sumbgproutes <= 20000):
    print("Generating MAJOR syslog. Please wait a few seconds...")
    time.sleep(2)
    print(f"%BGPVPNv4ROUTE-3-BPGVPNv4ROUTEEXCEEDED : Route exceeded the amount of 20000. Value is {sumbgproutes} -destinationip 127.0.0.1 -destinationport 514 -sourceip {devices['ip']}")
    #os.system(f"{javapathsyslog} \"%BGPVPNv4ROUTE-3-BPGVPNv4ROUTEEXCEEDED : Route exceeded the amount of 20000. Value is {sumbgproutes}\" -destinationip 127.0.0.1 -destinationport 514 -sourceip {devices['ip']}")
  
  # Sending MINOR syslog
  if (16000 <= sumbgproutes < 18000):
    print("Generating MINOR syslog. Please wait a few seconds...")
    time.sleep(2)
    print(f"%BGPVPNv4ROUTE-4-BPGVPNv4ROUTEEXCEEDED : Route exceeded the amount of 20000. Value is {sumbgproutes} -destinationip 127.0.0.1 -destinationport 514 -sourceip {devices['ip']}")
    #os.system(f"{javapathsyslog} \"%BGPVPNv4ROUTE-4-BPGVPNv4ROUTEEXCEEDED : Route exceeded the amount of 20000. Value is {sumbgproutes}\" -destinationip 127.0.0.1 -destinationport 514 -sourceip {devices['ip']}")

check_bgp_routes()



