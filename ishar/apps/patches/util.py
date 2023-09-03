"""
isharmud.com patches utilities.
"""
import glob
import os

from datetime import date
from django.conf import settings
from pypdf import PdfReader


def sizeof_fmt(num=None, suffix='B'):
    """Convert bytes to human-readable file size"""
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'


def get_patch_pdfs(patch_directory=settings.PATCH_DIR):
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


def get_patch_pdf(patch_name=None):
    """
    Get patch PDF information and text.
    """
    count = 0
    text = str()

    # Default patch name is latest
    if patch_name is None:
        patch_name = get_patch_pdfs()[0]['name']

    # Open the PDF patch file
    with open(file=f'{settings.PATCH_DIR}/{patch_name}', mode='rb') as pdf_fh:

        # Parse the PDF, then get the number of pages and metadata
        pdf = PdfReader(pdf_fh)
        page_count = len(pdf.pages)
        meta = pdf.metadata

        # Loop through each page of the PDF extracting the text
        for page in pdf.pages:
            count += 1
            text += f'\nPage {count} of {page_count}\n'
            text += page.extract_text()

    # Return the PDF name, metadata, page count, and text
    return {
        'name': patch_name,
        'meta': meta,
        'page_count': page_count,
        'text': text
    }
