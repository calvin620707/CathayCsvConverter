import csv
import logging
from collections import defaultdict
from io import TextIOWrapper
from datetime import date, datetime

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
    ret = defaultdict(dict)
    for row in reader:
        category = None
        if 'Y177748' in row[5]:
            category = '中華電信'

        if '北市水費' in row[4]:
            category = '水費'

        if '台電電費' in row[4]:
            category = '電費'

        if '信用卡款' in row[4] and '國泰世華卡' in row[5]:
            category = 'koko卡費'

        if '604056495' in row[5]:
            category = '瓦斯'

        if not category:
            logging.info("{} no category".format(row))
            continue

        row_date = datetime.strptime(row[0], '%Y%m%d').date()
        spent = int(row[1])
        ret[row_date.strftime("%Y%m")].update({category: spent})
    print(ret)
