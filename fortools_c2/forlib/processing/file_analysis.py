import xmltodict
import json
from collections import OrderedDict

class log_analysis():
    def __init__(self, file):
        self.file = file
        self.evtx_json = self.make_json()

    def make_json(self):
        num = 0
        json_record = OrderedDict()
        with self.file as log:
            for record in log.records():
                num = num+1
                dict_type = json.dumps(xmltodict.parse(record.xml()))
                json_record[num] = dict_type
                print(json.dumps(json_record, ensure_ascii=False, indent="\t"))
                #print(json.loads(self.dict_type))
                #json_record.append(json.loads(self.dict_type))
            return json_record

    #def get_event_ID(self):
        #for i in self.evtx_json:
            #print(i["Event"]["System"]["EventID"]["@Qualifiers"])
