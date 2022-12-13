"""Patches Pages"""
import glob
import os
from datetime import date
from flask import Blueprint, redirect, render_template, url_for

from mud_secret import PATCH_DIR


def sizeof_fmt(num=None, suffix='B'):
    """Format file size to human-readable"""
    units = ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']
    for unit in units:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'


def get_patch_pdfs(patch_directory=PATCH_DIR):
    """Find and return all PDF file information from the patch directory"""

    # Find all .pdf files in the patch directory,
    #   and reverse sort them by mtime
    pdfs = sorted(
        glob.glob(
            f'{patch_directory}/*.pdf'
        ),
        key=os.path.getmtime,
        reverse=True
    )

    # Loop through each pdf file that was found,
    #   creating a list containing a dictionary for each file
    ret = []
    for pdf in pdfs:

        # Include the PDF file base name, modified time (mtime) datetime object,
        #   and human-readable file size
        ret.append({
            'name': os.path.basename(
                p=pdf
            ),
            'modified': date.fromtimestamp(
                os.path.getmtime(
                    filename=pdf
                )
            ),
            'size': sizeof_fmt(
                num=os.path.getsize(pdf))
        })

    # Return the list of dictionaries
    return ret


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
