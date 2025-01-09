import os
from path import Path

class SosPods:
    def __init__(self, sosarchive):
        # Path to the pod directory inside sosreport
        self.pod_dirs = Path(sosarchive).glob('sos_commands/metalk8s/by-namespaces/*/pod')

    def list_pods(self):
        print("=======================  PODS  =======================")
        for pod_dir in self.pod_dirs:
            pod_list_file = os.path.join(pod_dir, "list.txt")
            if os.path.exists(pod_list_file):
                print(f"\nNamespace: {pod_dir.parent.basename()}")
                with open(pod_list_file, 'r') as file:
                    print(file.read().strip())
            else:
                print(f"No pod list found in {pod_dir}")
