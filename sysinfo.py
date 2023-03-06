
"""System Information page"""
from datetime import datetime
import os
import psutil
from flask import Blueprint, render_template

from sentry import sentry_sdk


def get_proc(process_name='ishar'):
    """Get information about the (usually 'ishar') MUD process"""

    # Loop through each process, getting its name, username, and create time
    pid_attrs = ['pid', 'name', 'username', 'create_time']
    for proc in psutil.process_iter(attrs=pid_attrs):

        # Return the process with the correct name owned by the same user
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


def get_connections(process=get_proc()):
    """Create dictionary of unique IP addresses connected to the MUD,
        and the count of times """

    # Only continue if the process exists
    ips = {}
    if process:

        # Loop through each connection
        try:
            for conn in process.connections(kind='inet'):

                # Only process established connections to port 9999
                if conn.status == 'ESTABLISHED' and \
                 conn.laddr.port == 9999 and conn.raddr.ip:

                    # Increment existing, or set fresh count
                    if conn.raddr.ip in ips:
                        ips[conn.raddr.ip] += 1
                    else:
                        ips[conn.raddr.ip] = 1

        except (PermissionError, psutil.AccessDenied) as cerr:
            sentry_sdk.capture_exception(cerr)

    # Return the dictionary of IP addresses and their count
    return ips


# Flask Blueprint
sysinfo_bp = Blueprint('sysinfo', __name__)


@sysinfo_bp.route('/connections/', methods=['GET'])
@sysinfo_bp.route('/connections', methods=['GET'])
@sysinfo_bp.route('/conns/', methods=['GET'])
@sysinfo_bp.route('/conns', methods=['GET'])
@sysinfo_bp.route('/who/', methods=['GET'])
@sysinfo_bp.route('/who', methods=['GET'])
@sysinfo_bp.route('/online/', methods=['GET'])
@sysinfo_bp.route('/online', methods=['GET'])
@sysinfo_bp.route('/uptime/', methods=['GET'])
@sysinfo_bp.route('/uptime', methods=['GET'])
@sysinfo_bp.route('/systeminfo/', methods=['GET'])
@sysinfo_bp.route('/systeminfo', methods=['GET'])
@sysinfo_bp.route('/system_info/', methods=['GET'])
@sysinfo_bp.route('/system_info', methods=['GET'])
@sysinfo_bp.route('/sys/', methods=['GET'])
@sysinfo_bp.route('/sys', methods=['GET'])
@sysinfo_bp.route('/sys_info/', methods=['GET'])
@sysinfo_bp.route('/sys_info', methods=['GET'])
@sysinfo_bp.route('/sysinfo/', methods=['GET'])
@sysinfo_bp.route('/sysinfo', methods=['GET'])
def index():
    """System information"""
    proc = get_proc()
    ret = None
    if proc and proc.info:
        ret = {
            'connections':   len(get_connections(process=proc)),
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
