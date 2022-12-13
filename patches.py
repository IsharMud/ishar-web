"""Patches Pages"""
import glob
import os
from datetime import date
from flask import Blueprint, redirect, render_template, url_for

from mud_secret import PATCH_DIR


def sizeof_fmt(num=None, suffix='B'):
    """Convert bytes to human-readable file size"""
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'


def get_patch_pdfs(patch_directory=PATCH_DIR):
    """Find and return all PDF file information from the patch directory"""

    # Find all .pdf files in the patch directory,
    #   and sort by most recent modified time first
    pdfs = sorted(
        glob.glob(
            f'{patch_directory}/*.pdf'
        ),
        key=os.path.getmtime,
        reverse=True
    )

    # Loop through each file that was found,
    #   creating a list containing a dictionary for each file
    ret = []
    for pdf in pdfs:

        # Append a dictionary to the list to return
        ret.append({

            # Patch PDF file base name
            #   (such as "Patch_#.#.pdf")
            'name': os.path.basename(pdf),

            # File modified time (mtime) datetime object
            'modified': date.fromtimestamp(
                os.path.getmtime(pdf)
            ),

            # Human-readable file size
            #   (such as 1.2MiB or 11.5KiB)
            'size': sizeof_fmt(
                num=os.path.getsize(pdf)
            )
        })

    # Return the list of dictionaries
    return ret


# Flask Blueprint
patches = Blueprint('patches', __name__)


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
