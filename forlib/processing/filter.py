import re
import datetime


def custom_filter(filter_list, json_list):
    __result = []

    for i in range(0, len(json_list)):
        for j in range(0, len(filter_list), 3):
            if filter_list[j + 2] == 0:  # normal
                check = False
                for k in filter_list[j + 1]:
                    if json_list[i][filter_list[j]] == k:
                        check = True
                        break
                    else:
                        pass
                if check is True:
                    pass
                else:
                    break
            elif filter_list[j + 2] == 1:  # re
                result_re = re.search(filter_list[j + 1], str(json_list[i][filter_list[j]]))
                if result_re is not None:
                    pass
                else:
                    break
            if j == len(filter_list) - 3:
                __result.append(json_list[i])
    return __result


def date_filter(key, filter_list, json_list):
    __result = []
    for i in range(0, len(json_list)):
        c_date = json_list[i][key].split('.')[0]
        if datetime.datetime.strptime(filter_list[0], "%Y-%m-%d") <= datetime.datetime.strptime(c_date, "%Y-%m-%d %H:%M:%S") \
                <= datetime.datetime.strptime(filter_list[1], "%Y-%m-%d") + datetime.timedelta(1):
            __result.append(json_list[i])
    return __result


def time_filter(key, filter_list, json_list):
    __result = []
    for i in range(0, len(json_list)):
        c_date = json_list[i][key].split('.')[0].split(' ')[1]
        if datetime.datetime.strptime(filter_list[0], "%H:%M:%S") <= datetime.datetime.strptime(c_date, "%H:%M:%S") \
                <= datetime.datetime.strptime(filter_list[1], "%H:%M:%S"):
            __result.append(json_list[i])
    return __result


def day_filter(key, filter_list, json_list):
    __result = []
    for i in range(0, len(json_list)):
        c_date = json_list[i][key].split('.')[0]
        if datetime.datetime.strptime(filter_list[0], "%Y-%m-%d %H:%M:%S") <= \
                datetime.datetime.strptime(c_date, "%Y-%m-%d %H:%M:%S") \
                <= datetime.datetime.strptime(filter_list[1], "%Y-%m-%d %H:%M:%S"):
            __result.append(json_list[i])
    return __result


def time_sort(key, json_list):
    json_list = sorted(json_list, key=lambda list_info: (list_info[key]))
    return json_list
