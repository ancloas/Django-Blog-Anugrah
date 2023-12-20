# utils.py
from account.models import Account

def get_filename(filename, request):
    # Customize the filename generation logic here
    # For example, you can return the uppercase version of the original filename
    
    # Validate if the author_id is correct
    try:
        author = Account.objects.get(id=request.user.id)
    except Account.DoesNotExist:
        return None
    return     f'{author.id}/{filename.upper()}'
