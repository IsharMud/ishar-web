"""Patches Pages"""
import glob
import os
from datetime import date
from flask import Blueprint, redirect, render_template, url_for

from mud_secret import PATCH_DIR


def get_patch_pdfs(patch_directory=PATCH_DIR):
    """Return all patch PDF information"""
    pdfs = sorted(
        glob.glob(
            f'{patch_directory}/*.pdf'
        ),
        reverse=True
    )

    all_patches = []
    for patch in pdfs:
        all_patches.append({
            'name': os.path.basename(patch),
            'created': date.fromtimestamp(os.path.getctime(patch)),
            'modified': date.fromtimestamp(os.path.getmtime(patch)),
            'size': os.path.getsize(patch)
        })
    return all_patches


# Flask Blueprint
patches = Blueprint('patches', __name__)


@patches.route('/latest_patch/', methods=['GET'])
@patches.route('/latest_patch', methods=['GET'])
def latest():
    """Redirect /latest_patch to latest found static patch .pdf file"""
    latest_pdf = get_patch_pdfs()[0]
    return redirect(
        url_for(
            'static',
            filename=f'patches/{latest_pdf.name}'
        )
    )


@patches.route('/patches/', methods=['GET'])
@patches.route('/patches', methods=['GET'])
def index():
    """Page showing a dynamic list of patches (/patches)"""
    return render_template(
        'patches.html.j2',
        patches=get_patch_pdfs()
    )
