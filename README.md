# sosparser
Sosparser is a Python-based tool designed to parse and analyze ARTESCA sosreports.
It extracts detailed information such as usage statistics, topology configurations, 
active alerts, and pod details, providing insights into the health and performance of the environment.

# Set up the environment:
  
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt

## Usage
Run the main script `parse-sos.py` to analyze a sosreport.

### Full Analysis
Run a comprehensive analysis of all available statistics:
```bash
python parse-sos.py /path/to/extracted/sosreport --stat ALL
```

### Specific Analysis
Run the script with the following flags to extract specific data:
- **Usage Statistics**:
  ```bash
  python parse-sos.py /path/to/extracted/sosreport --stat USAGE
  ```
- **Topology Information**:
  ```bash
  python parse-sos.py /path/to/extracted/sosreport --stat TOPO
  ```
- **Alerts**:
  ```bash
  python parse-sos.py /path/to/extracted/sosreport --stat ALERTS
  ```
- **Pod Details**:
  ```bash
  python parse-sos.py /path/to/extracted/sosreport --stat PODS
  ```
