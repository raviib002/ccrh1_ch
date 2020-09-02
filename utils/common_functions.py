import datetime
import urllib.parse
import random
import requests
import binascii
import json
import calendar
import re
from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags, format_html
from django.db.models.functions import Lower
from django.db.models import Q
from django.shortcuts import render
# from case_history.models import CaseStatusHistory,CaseStatus


"""
While Creating a user username is spliting form email and
if username is already exist a random number is appending to username
due to username is unique so we are making making the username is unique"""
def make_unique_username(email):
    user_name = email.split('@', 1)[0]
    if User.objects.filter(username=user_name).exists():
        postfix = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3))
        return str(user_name+postfix)
    else:
        return user_name


'''For medicine prescription mapping --Starts Here '''
def data_as_list(data):
    """data is request.POST"""
    data_list = []
    if data:
        label_keys = [key.split('_')[3] for key in data.keys() if re.match(r'addon_thrpy_mas_\d+', key)]
        for i in label_keys:
            data_list.append(
                    [data.get("addon_thrpy_mas_%s" % i, None),
                     data.get("medicine_name_%s" % i, None),
                     data.get("medicine_dosage_%s" % i, None),
                     data.get("duration_other_therapy_%s" % i, None),
                     data.get("duration_after_which_other_therapy_%s" % i, None),
                     data.get("addon_order_%s" % i, None),
                    ]
                )
        return data_list
    else:
        return data_list
    
'''For medicine prescription mapping --Ends Here '''

def data_as_past_supression_list(data):
    """data is request.POST"""
    data_list = []
    if data:
        label_keys = [key.split('_')[3] for key in data.keys() if re.match(r'past_hisry_supression_\d+', key)]
        for i in label_keys:
            if data.get("type_of_suppression_%s" % i) or data.get("year_of_suppression_%s" % i) or data.get("age_of_suppression_%s" % i) or data.get("aetiology_%s" % i) or data.get("other_information_%s" % i) or data.get("past_supression_idex_%s" % i):
                data_list.append(
                        [data.get("type_of_suppression_%s" % i, None),
                         data.get("year_of_suppression_%s" % i, None),
                         data.get("age_of_suppression_%s" % i, None),
                         data.get("aetiology_%s" % i, None),
                         data.get("other_information_%s" % i, None),
                         data.get("past_supression_idex_%s" % i, None),
    
                        ]
                    )
        return data_list     
    else:
        return data_list    
""" To keep the history status of cases """
# def keep_case_status_history(case_id, case_status=None):
#     if case_status == "Submitted":
#         save_status = CaseStatus.objects.get(cstatus_name = 'Submitted')
#     else:
#         save_status = CaseStatus.objects.get(cstatus_name = 'Saved')
#     CaseStatusHistory.objects.create(case_id = case_id,
#                                     case_status_id = save_status.id,
#                                     )