import nmap
from core import single_port_scan
from concurrent.futures import ThreadPoolExecutor, as_completed
begin,end = 22,24
target = '10.0.2.6'
target = '127.0.0.1'
scanner = nmap.PortScanner()

processes = []
scan_result_list=[]
with ThreadPoolExecutor(max_workers=None) as executor:
    for i in range(begin,end+1):

        #processes.append(executor.submit(single_port_scan, target,scanner,i))
        x=executor.submit(single_port_scan, target,scanner,i)
        scan_port_result=x.result()
        if(scan_port_result!=None):
            scan_result_list.append(scan_port_result)

print(scan_result_list)
"""
for i in range(begin,end+1):
    #processes.append(executor.submit(single_port_scan, target,scanner,i))
    single_port_scan(target,scanner,str(i))

"""
