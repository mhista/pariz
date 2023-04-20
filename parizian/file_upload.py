from django.conf import settings
import uuid
"""
the form returns a string part of the media to be uploaded, which is checked against the list
of allowed media access
import 'the upload_file_to' function if you wish to control user uploads.
"""
def check_file_type(file):
    '''checks the type of file being used'''
    extensions = {
        'images' : ('jpeg', 'jpg', 'png', 'gif'),
        'videos' : ('mp4', 'webm', 'ogg'),
        'music' : ('mp4', 'mp3', 'ogg', 'wav')
    }

    file = file.split('.')[1]
    file = str(file)
    for x in extensions:
        if file in extensions[x]:
            return x
    return None

file_type = check_file_type


def check_file_extension(file):
    """
        checks the extension being used
        1.can be imported in the view function to check the file type before validating form
        2. if uploading multiple files, override the post method to, loop through the files to check the file type
    
    """

    extensions = {
        'images' : ('jpeg', 'jpg', 'png', 'gif'),
        'videos' : ('mp4', 'webm', 'ogg'),
        'music' : ('mp4', 'mp3', 'ogg', 'wav')
    }
    file = str(file)
    fil = file.split('.')[1]
    for x in extensions.values():
        if fil in x:
            return file
        return None
file_ext = check_file_extension


def uploaded_files_directory(instance,filename, file_func=file_type):
    """used by the model to create a directory for the file being used 
    """
    file = file_func(filename)
    return f'{instance.user}/{file}/{filename}'


# upload_file_to = uploaded_files_directory
profile_upload = uploaded_files_directory
def item_files_directory(instance,filename):
   
    return f'{instance.name}/{filename}'
item_uploads = item_files_directory

def company_files_directory(instance,filename):
       
    return f'{instance.company_name}/{filename}'
company_upload = company_files_directory



def generate_ref_code():
    code = str(uuid.uuid4()).replace('-','')[:12]
    return code



