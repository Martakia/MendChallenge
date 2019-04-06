
# Createing an abstract that should function as the requirements for any XML to JSON converter
class BaseConverter:
    
    def __init__(self, dataEndpoint):
        self.dataEndpoint = dataEndpoint

    def GetXMLData(self):
        raise NotImplementedError("The method has not been implemented. This class is meant to act as an abstract class to extend.")

    def ConvertDataToJson(self):
        raise NotImplementedError("The method has not been implemented. This class is meant to act as an abstract class to extend.")

    def PrintJsonData(self):
        raise NotImplementedError("The method has not been implemented. This class is meant to act as an abstract class to extend.")