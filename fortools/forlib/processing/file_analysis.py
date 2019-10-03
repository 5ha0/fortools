import json


class evtx_analysis():
    def __init__(self, file):
        self.file = file
        self.evtx_xml = self.make_xml()

    def make_xml(self):
        xml_object = []
        with self.file as log:
            for record in log.records():
                xml_object.append(record.xml())
        return xml_object

    def get_event_ID(self, num):
        for i in self.evtx_xml:
            print(i)


class log_nalysis():
    def __init__(self, file):
        self.file = file

    def make_json(self):
        line = self.file.readline()
        log_line = line.split()
        log_obj = dict()
        log_obj["host"] = log_line[0]
        log_obj["indent"] = log_line[1]
        log_obj["AuthUser"] = log_line[2]
        log_obj["Date"] = log_line[3]
        log_obj["Request"] = log_line[4]
        log_obj["Status"] = log_line[5]
        log_obj["Bytes"] = log_line[6]
        return json.dumps(log_obj, ensure_ascii=False, indent='\t')


class file_analysis():
    def __init__(self, file):
        self.file = file
