import os
from path import Path

class SosPods:
    def __init__(self, sosarchive):
        # Path to the pod directory inside sosreport
        self.pod_dirs = Path(sosarchive).glob('sos_commands/metalk8s/by-namespaces/*/pod')

    def list_pods(self):
        print("==============================  PODS  ==============================")
        print("### Display pods showing restarts or not being in Running state  ###")
        for pod_dir in self.pod_dirs:
            pod_list_file = os.path.join(pod_dir, "list.txt")
            if os.path.exists(pod_list_file):
                print(f"Namespace: {pod_dir.parent.basename()}")
                with open(pod_list_file, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        trimmedLine = ' '.join(line.split())
                        if(trimmedLine.startswith("NAME")):
                            continue
                        parts = trimmedLine.split(' ')
                        if(parts[2] == "Completed"):
                            continue
                        #parts[3] = nbr of restarts, parts[2] is pod status parts[1] is nbr of container Running
                        if(int(parts[3]) > 0 or (parts[2] != "Running") or (parts[1] != "1/1" and parts[1] != "2/2" and parts[1] != "3/3")):
                            print(line.strip())
            else:
                print(f"No pod list found in {pod_dir}")
