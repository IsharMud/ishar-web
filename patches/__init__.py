"""Patches"""
from flask import Blueprint, redirect, render_template, url_for

from patches.util import get_patch_pdfs


# Flask Blueprint
patches_bp = Blueprint(
    'patches',
    __name__,
    url_prefix='/',
    template_folder='templates'
)


@patches_bp.route('/patches/latest/', methods=['GET'])
@patches_bp.route('/patches/latest', methods=['GET'])
@patches_bp.route('/patch/latest/', methods=['GET'])
@patches_bp.route('/patch/latest', methods=['GET'])
@patches_bp.route('/latestpatch/', methods=['GET'])
@patches_bp.route('/latestpatch', methods=['GET'])
@patches_bp.route('/latest_patch/', methods=['GET'])
@patches_bp.route('/latest_patch', methods=['GET'])
def latest():
    """Redirect to most recent found static patch .pdf file"""
    return redirect(
        url_for('static', filename=f"patches/{get_patch_pdfs()[0]['name']}")
    )


@patches_bp.route('/patches/all/', methods=['GET'])
@patches_bp.route('/patches/all', methods=['GET'])
@patches_bp.route('/patches/', methods=['GET'])
@patches_bp.route('/patches', methods=['GET'])
def index():
    """Page showing a dynamic list of patches (/patches)"""
    return render_template(
        'patches.html.j2',
        all_patches=get_patch_pdfs(),
        patches=get_patch_pdfs()
    )
