import csv
import logging
from io import TextIOWrapper

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from converter.forms import UploadFileForm

logger = logging.getLogger(__name__)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            __convert_csv(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'converter/index.html', {'form': form})


def __convert_csv(in_f):
    f = TextIOWrapper(in_f, encoding='big5')

    # skip first 2 lines for account info and headers
    for _ in range(2):
        f.readline()

    reader = csv.reader(f)
    for row in reader:
        logging.info(row)
