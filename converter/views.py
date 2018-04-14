import csv
import logging
from collections import defaultdict, OrderedDict
from datetime import datetime
from io import TextIOWrapper

from django.conf import settings
from django.shortcuts import render

# Create your views here.
from converter.forms import UploadFileForm

logger = logging.getLogger(__name__)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            ret = __convert_csv(request.FILES['file'])

            # TODO: try to find a way to show data on web page which can be copied past on google sheet
            ret_list = []
            for row_date, values in ret.items():
                ret_list.append((
                    row_date,
                    settings.HOUSE_RENT,
                    values.get('電費'),
                    values.get('水費'),
                    values.get('瓦斯'),
                    values.get('中華電信'),
                    values.get('koko卡費')
                ))

            row_count = len(ret_list)
            ret_str = ""
            for row in ret_list:
                for value in row:
                    if value:
                        ret_str += str(value)
                    ret_str += "\t"
                ret_str += "\n"

            return render(request, 'converter/results.html', {'ret': ret_str, 'row_count': row_count})
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
        key = row_date.strftime("%Y/%m")

        if ret.get(key, {}).get(category):
            ret[key][category] += spent
            continue

        ret[key].update({category: spent})

    ret = OrderedDict(sorted(ret.items(), key=lambda t: t[0]))

    logging.info(ret)
    return ret
