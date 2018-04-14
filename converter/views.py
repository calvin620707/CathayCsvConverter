import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from converter.forms import UploadFileForm


logger = logging.getLogger(__name__)


def upload_file(request):
    logger.info("Test")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info(request.FILES['file'].read())
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'converter/index.html', {'form': form})

