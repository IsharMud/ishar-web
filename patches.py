"""Patches Pages"""
import glob
import os

from flask import Blueprint, redirect, render_template

patches = Blueprint('patches', __name__)


@patches.route('/latest_patch/', methods=['GET'])
@patches.route('/latest_patch', methods=['GET'])
def latest():
    """Redirect /latest_patch to latest found static patch .pdf file"""
    return redirect(
        '/' + max(
                glob.glob('static/patches/*.pdf'),
                key=os.path.getmtime
            )
    )


@patches.route('/patches/', methods=['GET'])
@patches.route('/patches', methods=['GET'])
def index():
    """Page showing a dynamic list of patches (/patches)"""
    return render_template(
        'patches.html.j2',
        patches=sorted(
            os.listdir('static/patches'),
            reverse=True
        )
    )
