import os
from tabulate import tabulate
import sys
import time

def retrievePasswords(profile):
    individual_interface_ouput = os.popen(f'netsh wlan show profiles "{profile}" key=clear').read().split("\n")
    datastructure = {}
    for i in range(len(individual_interface_ouput)):
        if "Security key" in individual_interface_ouput[i]:
            j = individual_interface_ouput[i].index(":") + 2
            if individual_interface_ouput[i][j::] == "Absent":
                datastructure["Has Security Key"] = False
                datastructure["Security Key"] = None
                break
            elif individual_interface_ouput[i][j::] == "Present":
                datastructure["Has Security Key"] = True
                x = individual_interface_ouput[i+1].index(":") + 2
                datastructure["Security Key"] = individual_interface_ouput[i+1][x::]
    return datastructure

def screenFormatter():
    time.sleep(0.7)
    os.system("cls")




print("Initializing...")
screenFormatter()
print("Retrieving Passwords...")
interfaces_output = os.popen("netsh wlan show profiles").read().split("\n")

useless_values_at_start = 9
useless_values_at_end = 2

for i in range(useless_values_at_start):
    interfaces_output.pop(0)

for j in range(useless_values_at_end):
    interfaces_output.pop()

if len(interfaces_output) > 0:
    profiles_on_interface = []
    for i in range(len(interfaces_output)):
        for j in range(len(interfaces_output[i])):
            if interfaces_output[i][j] == ":":
                j += 2
                passwords = retrievePasswords(interfaces_output[i][j::])
                profiles_on_interface.append([interfaces_output[i][j::], passwords["Has Security Key"], passwords["Security Key"]])
    
    screenFormatter()
    print(tabulate(profiles_on_interface, headers=["SSID", "Has Security Key", "Security Key"], tablefmt="pretty"))

try:
    print("Press CTRL-C to exit the program")
    while True:
        pass
except KeyboardInterrupt:
    sys.exit()