import uuid, os
from django.conf import settings

def handle_uploaded_file(f, myuuid=str(uuid.uuid4())):
    dest_dir=settings.MEDIA_ROOT
    dest_filename="%s.bb" % (myuuid)
    dest_path=os.path.join(dest_dir, dest_filename)
    destination = open(dest_path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return dest_filename


def de_duplicate_list(list_source):
    list_target = []
    for item in list_source:
        if item not in list_target:
            list_target.append(item)

    return list_target
# Mark Scrimshire:
# Remove duplicate items from a list
