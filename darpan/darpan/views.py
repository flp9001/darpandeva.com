from django.shortcuts import redirect

from .models import LinkAccess

def linkView(request, target):
    url = request.GET['url']
    link_access = LinkAccess(url=url)
    link_access.save()
    print("Redirecting to", url)
    return redirect(url)
