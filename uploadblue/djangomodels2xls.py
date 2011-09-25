import sys, os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
import json
import xlwt

def convert2excel(l):
    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 2
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.num_format_str = 'D-MMM-YY'
    
    wb = xlwt.Workbook()
    cdcsheet= wb.add_sheet('CDCSheet')
    keys= l[0].keys()
    cdc_list=l
    j=0
    for i in keys:
        cdcsheet.write(0,j, i)
        j+=1
    row=1
    column=0
    j=0
    for i in cdc_list[0:]:
       values=i.values()
       for j in i.values():
            cdcsheet.write(row,column, str(j))
            column+=1
       column=0 
       row+=1
    excelfilename ="%s.xls"   
    excelpath = os.path.join(settings.MEDIA_ROOT, excelfilename)
    wb.save(excelpath)
    return excelfilename