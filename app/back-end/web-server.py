from flask import Flask,jsonify,request,send_from_directory
import nmap
from core import single_port_scan
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
static_files_dir="../web-client/"
def scan_host(target,begin,end):
    scanner = nmap.PortScanner()
    processes = []
    scan_result_list=[]
    with ThreadPoolExecutor(max_workers=None) as executor:
        for i in range(begin,end+1):
            x=executor.submit(single_port_scan, target,scanner,i)
            scan_port_result=x.result()
            if(scan_port_result!=None):
                scan_result_list.append(scan_port_result)
    print(jsonify(scan_result_list))
    return jsonify(scan_result_list)
"""
for i in range(begin,end+1):
    #processes.append(executor.submit(single_port_scan, target,scanner,i))
    single_port_scan(target,scanner,str(i))

"""

@app.route('/scanhost', methods = ['GET'])
@cross_origin()
def ReturnJSON():
    if(request.method == 'GET'):
            target = request.args['target']
            start = int(request.args['start_port'])
            end = int(request.args['end_port'])
            return scan_host(target,start,end)

@app.route('/dashboard/<path:filename>')
def send_static_dashboard(filename):
    return send_from_directory(static_files_dir, filename)

if __name__=='__main__':
	app.run(debug=False)
