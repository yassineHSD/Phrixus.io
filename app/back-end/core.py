import requests
import json
from tabulate import tabulate
from colorama import Fore, Back, Style

def single_port_scan(target,scanner,port):
    port=int(port)
    res = scanner.scan(target,str(port))
    status = res['scan'][target]['tcp'][port]['state']
    if(status=="open"):
        name = res['scan'][target]['tcp'][port]['name']
        product = res['scan'][target]['tcp'][port]['product']
        version = res['scan'][target]['tcp'][port]['version']
        extrainfo = res['scan'][target]['tcp'][port]['extrainfo']
        conf = res['scan'][target]['tcp'][port]['conf']
        cpe = res['scan'][target]['tcp'][port]['cpe']
        response = requests.get("https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString="+cpe)
        cve_data=json.loads(response.text)
        cve_abstract_list=[]
        cve_abstract_list_colored=[]

        if(cve_data["result"]["CVE_Items"]):
            cve_list=cve_data["result"]["CVE_Items"]
            for cve in cve_list:
                if("baseMetricV3" in cve['impact']):
                    if(cve['impact']['baseMetricV3']['impactScore']>9.0):
                        color=Fore.RED
                        Impact="Critical"
                    if(7.0<cve['impact']['baseMetricV3']['impactScore']<=8.9):
                        color=Fore.ORANGE
                        Impact="High"
                    if(4.0<cve['impact']['baseMetricV3']['impactScore']<=6.9):
                        color=Fore.YELLOW
                        Impact="Medium"
                    if(0.1<cve['impact']['baseMetricV3']['impactScore']<=3.9):
                        color=Fore.GREEN
                        Impact="Low"
                    elif(cve['impact']['baseMetricV3']['impactScore']<0.1):
                        color=Fore.WHITE
                        Impact="None"
                    tmp_cve_score_colored=color+str(cve['impact']['baseMetricV3']['impactScore'])+" "+Impact+Style.RESET_ALL
                    tmp_cve_colored=[color+cve['cve']['CVE_data_meta']['ID'],tmp_cve_score_colored]
                    tmp_cve=[cve['cve']['CVE_data_meta']['ID'],cve['impact']['baseMetricV3']['impactScore'],Impact]
                    cve_abstract_list.append(tmp_cve)
                    cve_abstract_list_colored.append(tmp_cve_colored)
            table_headers=['\033[1m'+'CVE', 'Impact Score'+'\033[0m']
            output_str=f'''
Port: {port}
Protocol: {name}
Product: {product}
Version: {version}
Status: {status}
CPE: {cpe}

{tabulate(cve_abstract_list_colored, headers=table_headers)}
{Style.RESET_ALL}
=====================================================================
'''

        else:
            output_str=f'''
Port: {port}
Protocol: {name}
Product: {product}
Version: {version}
Status: {status}
CPE: {cpe}
=====================================================================
'''
        print(output_str)
        return {
        "port":port,
        "protocol": name,
        "product":product,
        "version":version,
        "cpe":cpe,
        "CVE":cve_abstract_list
        }
        #print(output_str)
