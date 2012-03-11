import sys, os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
import json
import xlwt

def convert2excel(l, outfile, tab_name, mode, wb_object):
    # TODO: Allow multiple lists of data to be passed to this
    # function and add each one to a separate worksheet in the
    # excel sheet
    # TODO: Add a mode so that the excel sheet can be left open

    # Mode: 'open'      - Setup Excel file
    #       'update'    - Add sheet to file
    #       'save'      - [Default] Update and Close Excel file

    if mode == '':
        # set mode default to 'save'
        mode = 'save'

    print "mode: " + mode

    # Setup excel file name
    excelfilename ="%s.xls" % (outfile)
    if mode == 'open':

        # setup Sheet
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 2
        font0.bold = True

        style0 = xlwt.XFStyle()
        style0.font = font0

        style1 = xlwt.XFStyle()
        style1.num_format_str = 'D-MMM-YY'

        #initialize workbook
        wb = xlwt.Workbook()
        print "Workbook:"
        print wb

    else:
        wb = wb_object



    # Now do the create a worksheet with contents of list
    l=json.dumps(l)
    l=json.loads(l)
    print "convert to excel received:"
    # print l

    cdcsheet= wb.add_sheet(tab_name)
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

    if mode == 'save':
        # Close excel file and exit
        excelpath = os.path.join(settings.MEDIA_ROOT, excelfilename)
        wb.save(excelpath)
        return excelfilename

    else:
        return wb



def simpler_parse(inPath, OutPath):
    outfile =open(OutPath, 'w')
    line=[]
    items=[]
    generic_dict={}
    with open(inPath, 'r') as f:
        for i, l in enumerate(f):
            generic_dict={}
            line=l.split(":")
            if len(line)>1:
                k=line[0]
                v=line[1]
                if v[0]==" ":
                    v=v.lstrip()
                if len(line)>2 and k=="Time":
                    v="%s:%s" % (line[1], line[2])
                v=v.rstrip()
                generic_dict[k]=v
                items.append(generic_dict)
            outfile.write(l)
    outfile.close()

    f.close()
    return items