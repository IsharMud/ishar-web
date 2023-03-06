"""Admin Patches"""
import os

from flask import abort, Blueprint, flash, render_template, url_for
from werkzeug.utils import secure_filename

from mud_secret import PATCH_DIR
from forms import PatchAddForm
from patches.util import get_patch_pdfs


# Flask Blueprint
admin_patches_bp = Blueprint(
    'admin_patches',
    __name__,
    url_prefix='patches',
    template_folder='templates/patches'
)


@admin_patches_bp.route('/', methods=['GET', 'POST'])
def index():
    """Administration portal to allow Gods to manage patch PDFs
        /admin/patches"""

    # Get patch add form and check if submitted
    patch_add_form = PatchAddForm()
    if patch_add_form.validate_on_submit():

        # Get the name in the format we want, and title-case it
        patch_name = secure_filename(patch_add_form.name.data.title())
        if patch_name.endswith('.Pdf'):
            patch_name = patch_name.replace('.Pdf', '')
        patch_name_pdf = f'{patch_name}.pdf'

        # Get the uploaded file, and set upload path
        patch_file = patch_add_form.file.data
        upload_file = f'{PATCH_DIR}/{patch_name_pdf}'

        # Limit upload file size to 50MB
        if patch_file.content_length > 52428800:
            flash('Sorry, stick to 50 megabytes or less!', 'error')

        # Limit to PDF files only
        if not patch_file.content_type == 'application/pdf':
            flash('Sorry, but only PDF files are supported!', 'error')

        # Make sure the file does not already exist
        elif os.path.exists(upload_file):
            flash(f'Sorry, that patch file exists ({patch_name})!', 'error')

        # Proceed in possibly uploading the file
        else:
            patch_file.save(dst=upload_file)
            patch_url = url_for(
                'static',
                filename=f'patches/{patch_name_pdf}',
                _external=True
            )
            patch_link = f'<a href="{patch_url}" target="_blank" ' \
                         f'title="{patch_name}">{patch_url}</a>'
            flash(f'Uploaded: <code>{patch_link}</code>', 'success')

    # Show the form to manage patches in the administration portal
    return render_template(
        'manage_patches.html.j2',
        all_patches=get_patch_pdfs(),
        patch_add_form=patch_add_form
    )


@admin_patches_bp.route('/delete/<string:delete_patch_name>/', methods=['GET'])
@admin_patches_bp.route('/delete/<string:delete_patch_name>', methods=['GET'])
def delete(delete_patch_name=None):
    """Administration portal to allow Gods to delete patch files
        /admin/patches/delete"""
    patch_names = [patch['name'] for patch in get_patch_pdfs()]
    if delete_patch_name not in patch_names:
        flash('Invalid patch file.', 'error')
        abort(400)

    # Delete the patch file PDF
    delete_path = f'{PATCH_DIR}/{delete_patch_name}'
    if os.path.exists(delete_path):
        os.remove(delete_path)
        flash(f'Deleted <code>{delete_patch_name}</code>.', 'success')

    # Show the form to manage patches in the administration portal
    return index()
