import re
import datetime

class Filter():
    def keys(key_list, json_list):
        __result = []
        for i in json_list:
            info = dict()
            try:
                for j in key_list:
                    info[j] = i[j]
                __result.append(info)
            except KeyError:
                print("Plz check your key.")
                return -1
        return __result

    def same(filter_list, json_list):
        result = []
        for i in json_list:
            for j in filter_list.items():
                result_re = None
                if type(j[1]) == list:
                    for k in j[1]:
                        p = re.compile(str(k))
                        try:
                            result_re = p.match(str(i[j[0]]))
                            if result_re is not None:
                                break;
                        except KeyError:
                            print('Key Error: '+str(j[0]))
                            return -1
                else:
                    p = re.compile('^'+str(j[1])+'$')
                    try:
                        result_re = p.search(str(i[j[0]]))
                    except KeyError:
                        print('Key Error: ' + str(j[0]))
                        return -1
                if result_re is not None:
                    result.append(i)
        return result

    def keywords(filter_list, json_list):
        result = []
        for i in json_list:
            for j in filter_list.items():
                result_re = None
                if type(j[1]) == list:
                    for k in j[1]:
                        p = re.compile(str(k))
                        try:
                            result_re = p.search(str(i[j[0]]))
                            if result_re is not None:
                                break;
                        except KeyError:
                            print('Key Error: '+str(j[0]))
                            return -1
                else:
                    p = re.compile(str(j[1]))
                    try:
                        result_re = p.search(str(i[j[0]]))
                    except KeyError:
                        print('Key Error: ' + str(j[0]))
                        return -1
                if result_re is not None:
                    result.append(i)
        return result


    def date(key, filter_list, json_list):
        __result = []
        for i in range(0, len(json_list)):
            try:
                c_date = json_list[i][key]
            except KeyError:
                print('Key Error. You need to check your key.')
                return -1
            try:
                if datetime.datetime.strptime(filter_list[0], "%Y-%m-%d") <= datetime.datetime.strptime(c_date, "%Y-%m-%d %H:%M:%S") \
                        <= datetime.datetime.strptime(filter_list[1], "%Y-%m-%d") + datetime.timedelta(1):
                    __result.append(json_list[i])
            except TypeError:
                print('Plz check your input format. You need to input date type')
                return -1
            except ValueError:
                pass
        return __result


    def time(key, filter_list, json_list):
        __result = []
        for i in range(0, len(json_list)):
            try:
                c_date = json_list[i][key].split(' ')[1]
            except KeyError:
                print('Key Error. You need to check your key.')
            try:
                if datetime.datetime.strptime(filter_list[0], "%H:%M:%S") <= datetime.datetime.strptime(c_date, "%H:%M:%S") \
                        <= datetime.datetime.strptime(filter_list[1], "%H:%M:%S"):
                    __result.append(json_list[i])
            except TypeError:
                print('Plz check your input format. You need to input time type')
                return -1
            except ValueError:
                pass
        return __result


    def day(key, filter_list, json_list):
        __result = []
        for i in range(0, len(json_list)):
            c_date = json_list[i][key]
            try:
                if datetime.datetime.strptime(filter_list[0], "%Y-%m-%d %H:%M:%S") <= \
                        datetime.datetime.strptime(c_date, "%Y-%m-%d %H:%M:%S") \
                        <= datetime.datetime.strptime(filter_list[1], "%Y-%m-%d %H:%M:%S"):
                    __result.append(json_list[i])
            except TypeError:
                print('Plz check your input format. You need to input time type')
                return -1
            except ValueError:
                pass
        return __result


    def sorting(type, key, json_list):
        json_list = sorted(json_list, key=lambda list_info: (list_info[key]), reverse=type)
        return json_list


    def date_count(key, json_list):
        result = dict()
        for i in json_list:
            try:
                date_value = i[key].split(' ')[0]
            except KeyError:
                print('Check your key.')
                return -1
            if result.get(date_value) is not None:
                result[date_value] = result[date_value] + 1
            else:
                result[date_value] = 1
        return result


    def key_count(key, json_list):
        result = dict()
        for i in json_list:
            try:
                key_value = i[key]
            except KeyError:
                print('Check your key.')
                return -1
            if result.get(key_value) is not None:
                result[key_value] = result[key_value] + 1
            else:
                result[key_value] = 1
        return result

class Show:
    def data(json_list):
        for i in json_list:
            print(i)

    def keys(json_list):
        print(list(json_list[0].keys()))

