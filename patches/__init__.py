"""Patches"""
from flask import Blueprint, redirect, render_template, url_for

from patches.util import get_patch_pdfs

# Flask Blueprint
patches = Blueprint('patches', __name__, template_folder='templates')


@patches.route('/patches/latest/', methods=['GET'])
@patches.route('/patches/latest', methods=['GET'])
@patches.route('/patch/latest/', methods=['GET'])
@patches.route('/patch/latest', methods=['GET'])
@patches.route('/latestpatch/', methods=['GET'])
@patches.route('/latestpatch', methods=['GET'])
@patches.route('/latest_patch/', methods=['GET'])
@patches.route('/latest_patch', methods=['GET'])
def latest():
    """Redirect to most recent found static patch .pdf file"""
    return redirect(
        url_for(
            'static',
            filename=f"patches/{get_patch_pdfs()[0]['name']}"
        )
    )


@patches.route('/patches/all/', methods=['GET'])
@patches.route('/patches/all', methods=['GET'])
@patches.route('/patches/', methods=['GET'])
@patches.route('/patches', methods=['GET'])
def index():
    """Page showing a dynamic list of patches (/patches)"""
    return render_template(
        'patches.html.j2',
        patches=get_patch_pdfs()
    )
