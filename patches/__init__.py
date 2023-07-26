"""Patches"""
from flask import Blueprint, render_template

from patches.util import get_patch_pdfs, get_patch_pdf


# Flask Blueprint
patches_bp = Blueprint(
    'patches', __name__, url_prefix='/patches', template_folder='templates'
)


@patches_bp.route('/latest/', methods=['GET'])
def latest():
    """Embed most recent found static patch .pdf file"""
    return render_template(
        'latest.html.j2',
        pdf=get_patch_pdfs()[0]
    )


@patches_bp.route('/all/', methods=['GET'])
@patches_bp.route('/', methods=['GET'])
def index():
    """Page showing a dynamic list of patches (/patches)"""
    return render_template(
        'patches.html.j2',
        patches=get_patch_pdfs()
    )


@patches_bp.route('/text/', methods=['GET'])
def text():
    """Page showing text of the latest patch PDF (/patches/text)"""
    return render_template(
        'pdf.html.j2',
        pdf=get_patch_pdf()
    )
