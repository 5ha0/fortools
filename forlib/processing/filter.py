import re
import datetime


def custom_filter(filter_list, json_list):
    __result = []
    if type(filter_list) is not list or len(filter_list) is not 3:
        print('\nPlz check your input. You need to input list.\nformat: [key_value,[filtering_values],type]\ntype 0 is normal filtering and 1 is regular expression')
        return -1
    elif filter_list[2] is 0 and type(filter_list[1]) is not list:
        print(
            '\nPlz check your input. You need to input list.\nformat: [key_value,[filtering_values],type]\ntype 0 is normal filtering and 1 is regular expression')
        return -1

    for i in range(0, len(json_list)):
        for j in range(0, len(filter_list), 3):
            if filter_list[j + 2] == 0:  # normal
                check = False
                for k in filter_list[j + 1]:
                    try:
                        if json_list[i][filter_list[j]] == k:
                            check = True
                            break
                        else:
                            pass
                    except KeyError:
                        print('It doesn\'t have that key. Plz check key one more time.')
                        return -1
                if check is True:
                    pass
                else:
                    break
            elif filter_list[j + 2] == 1:  # re
                try:
                    result_re = re.search(filter_list[j + 1], str(json_list[i][filter_list[j]]))
                except KeyError:
                    print('It doesn\'t have that key. Plz check key one more time.')
                    return -1
                except:
                    print('Error.\nYou need to check your input.')
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

def date_count(key, json_list):
    result = dict()
    for i in json_list:
        date_value = i[key].split(' ')[0]
        if result.get(date_value) is not None:
            result[date_value] = result[date_value] + 1
        else:
            result[date_value] = 1
    return result

def key_count(key, json_list):
    result = dict()
    for i in json_list:
        key_value = i[key]
        if result.get(key_value) is not None:
            result[key_value] = result[key_value] + 1
        else:
            result[key_value] = 1
    return result
