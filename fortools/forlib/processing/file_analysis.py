class log_analysis():
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

class file_analysis():
    def __init__(self, file):
        self.file = file
