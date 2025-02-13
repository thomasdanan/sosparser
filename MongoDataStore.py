import json
import os

class MongoDataStore:
    def __init__(self, sos_path):
        """
        Initialize the parser with the SOS report path.
        :param sos_path: Path to the extracted SOS report directory
        """
        self.sos_path = sos_path
        self.rs_status_file = self.find_rs_status_file()

    def find_rs_status_file(self):
        """
        Locate the MongoDB `rs.status()` output in the SOS report.
        """
        sos_commands_path = os.path.join(self.sos_path, "sos_commands/artesca")
        for root, _, files in os.walk(sos_commands_path):
            for file in files:
                if "rs.status" in file:
                    return os.path.join(root, file)
        return None

    def parse_rs_status(self):
        """
        Parse the `rs.status()` output and extract key replication details.
        """
        if not self.rs_status_file:
            return {"error": "rs.status() output not found in SOS report"}

        with open(self.rs_status_file, "r") as file:
            data = file.read()
        
        try:
            rs_status = json.loads(data)
        except json.JSONDecodeError:
            return {"error": "Failed to parse rs.status() JSON data"}

        result = {
            "set": rs_status.get("set", "Unknown"),
            "primary": None,
            "secondaries": [],
            "replication_lag": {},
            "node_health": {}
        }
        
        for member in rs_status.get("members", []):
            state = member.get("stateStr", "Unknown")
            name = member.get("name", "Unknown")
            health = "Healthy" if member.get("health", 0) == 1 else "Unhealthy"
            optime_date = member.get("optimeDate", "N/A")
            
            if state == "PRIMARY":
                result["primary"] = name
            elif state == "SECONDARY":
                result["secondaries"].append(name)
                if "optimeDate" in member and "lastHeartbeat" in member:
                    lag = member["lastHeartbeat"] - member["optimeDate"]
                    result["replication_lag"][name] = lag
            
            result["node_health"][name] = health
        
        return result

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse SOS Report for MongoDB details")
    parser.add_argument("sos_path", help="Path to the extracted SOS report")
    parser.add_argument("--stat", choices=["USAGE", "TOPO", "ALERTS", "PODS", "RS_STATUS"], help="Specify the statistic to extract")
    
    args = parser.parse_args()

    if args.stat == "RS_STATUS":
        mongo_parser = MongoDataStore(args.sos_path)
        rs_status_data = mongo_parser.parse_rs_status()
        print(json.dumps(rs_status_data, indent=4))
    else:
        print(f"Statistic type {args.stat} not implemented for this script.")
