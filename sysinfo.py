
"""System Information page"""
from datetime import datetime
import os
import psutil
from flask import Blueprint, render_template


def get_proc(process_name='ishar'):
    """Get information about the (usually 'ishar') MUD process"""

    # Loop through each process, getting its name, username, and create time
    pid_attrs = ['pid', 'name', 'username', 'create_time']

    # Return the process with the correct name owned by the same user
    for proc in psutil.process_iter(attrs=pid_attrs):
        if proc.info['name'] == process_name:
            if proc.info['username'] == os.getenv('USER'):
                return proc
    return None


def get_uptime(process=get_proc()):
    """Format uptime of the MUD process"""
    if process:
        return datetime.utcnow() - datetime.fromtimestamp(
            process.info['create_time']
        )
    return None


# Flask Blueprint
sysinfo = Blueprint('sysinfo', __name__)


@sysinfo.route('/online/', methods=['GET'])
@sysinfo.route('/online', methods=['GET'])
@sysinfo.route('/uptime/', methods=['GET'])
@sysinfo.route('/uptime', methods=['GET'])
@sysinfo.route('/systeminfo/', methods=['GET'])
@sysinfo.route('/systeminfo', methods=['GET'])
@sysinfo.route('/system_info/', methods=['GET'])
@sysinfo.route('/system_info', methods=['GET'])
@sysinfo.route('/sys/', methods=['GET'])
@sysinfo.route('/sys', methods=['GET'])
@sysinfo.route('/sys_info/', methods=['GET'])
@sysinfo.route('/sys_info', methods=['GET'])
@sysinfo.route('/sysinfo/', methods=['GET'])
@sysinfo.route('/sysinfo', methods=['GET'])
def index():
    """System information"""
    proc = get_proc()
    ret = None
    if proc and proc.info:
        ret = {
            'cpu_percent':  proc.cpu_percent(),
            'cpu_times':    proc.cpu_times(),
            'ctx_switches': proc.num_ctx_switches(),
            'memory':       proc.memory_info(),
            'uptime':       get_uptime(process=proc)
        }

    return render_template(
        'sysinfo.html.j2',
        sysinfo=ret
    )
