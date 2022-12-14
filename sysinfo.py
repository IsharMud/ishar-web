
"""System Information page"""
from datetime import datetime
import os
import psutil
from flask import Blueprint, render_template

import delta


def get_proc(process_name='ishar'):
    """Get information about the 'ishar' MUD process"""

    # Loop through each process, getting its name, username, and create time
    pid_attrs = ['pid', 'name', 'username', 'create_time']

    # Return the process with the correct name owned by the same user
    for proc in psutil.process_iter(attrs=pid_attrs):
        if proc.info['name'] == process_name and \
            proc.info['username'] == os.getenv('USER'):
            return proc
    return None


# Flask Blueprint
sysinfo = Blueprint('sys', __name__)


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
    process = get_proc()
    uptime = None
    if process:
        uptime = delta.stringify(
            datetime.utcnow() - datetime.fromtimestamp(
                process.info['create_time']
            )
        )
    return render_template(
        'sys.html.j2',
        process=process,
        uptime=uptime
    )
