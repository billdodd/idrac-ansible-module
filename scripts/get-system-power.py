import rfutils
import json
import requests
import sys
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
rf = rfutils.rfutils()

def get_power(idrac, base_uri, rf_uri):
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if response.status_code == 400:
        rf.print_red("Something went wrong.")
        exit(1)

    data = response.json()
    # print(json.dumps(data, separators=(',', ':')))
    print("Power Monitoring - Historical Trends - Last Hour")
    print("Average Usage: %s" % data[u'PowerMetrics'][u'AverageConsumedWatts'])
    print("Max Peak:      %s" % data[u'PowerMetrics'][u'MaxConsumedWatts'])
    print("Min Peak:      %s" % data[u'PowerMetrics'][u'MinConsumedWatts'])

    return

def main():
    idrac = rf.check_args(sys)

    # Disable insecure-certificate-warning message
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Chassis/System.Embedded.1/Power/PowerControl"

    # Get system inventory
    get_power(idrac, base_uri, rf_uri)

if __name__ == '__main__':
    main()
