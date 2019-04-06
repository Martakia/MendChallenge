import unittest
import unittest.mock as MagicMock
from xml.etree import ElementTree as ET
import sys
sys.path.append("..")
from Converters.SenatorChartConverter import SenatorChartConverter

class SenatorChartTests(unittest.TestCase):
    # TODO: move this resource to a file
    mockDataResult = ET.fromstring("<contact_information> <member> <member_full>Alexander (R-TN)</member_full> <last_name>Alexander</last_name> <first_name>Lamar</first_name> <party>R</party> <state>TN</state> <address> 455 Dirksen Senate Office Building Washington DC 20510 </address> <phone>(202) 224-4944</phone> <email> http://www.alexander.senate.gov/public/index.cfm?p=Email </email> <website>http://www.alexander.senate.gov/</website> <class>Class II</class> <bioguide_id>A000360</bioguide_id> </member> <member> <member_full>Young (R-IN)</member_full> <last_name>Young</last_name> <first_name>Todd</first_name> <party>R</party> <state>IN</state> <address> 185 Dirksen Senate Office Building Washington DC 20510 </address> <phone>(202) 224-5623</phone> <email>https://www.young.senate.gov/contact</email> <website>http://www.young.senate.gov</website> <class>Class III</class> <bioguide_id>Y000064</bioguide_id> </member> <last_updated>Monday, April 1, 2019: 10:51 AM EST</last_updated> </contact_information>")
    mockAPI = "mockAPI.com"

    def testInitChartConverter(self):
        chartConverter = SenatorChartConverter(self.mockAPI)
        self.assertIsNotNone(chartConverter)
        self.assertEqual(chartConverter.dataEndpoint, self.mockAPI)

    # TODO: GetXMLData
    def testGetXMLData(self):
        chartConverter = SenatorChartConverter(self.mockAPI)
        # chartConverter.GetXMLData = MagicMock(return_value = self.mockDataResult)
        # chartConverter.GetXMLData()

        # self.assertEqual(chartConverter.xmlData, self.mockDataResult)
    
    # TODO: ConvertDataToJson

    # TODO: PrintJsonData

if __name__ == "__main__":
    unittest.main()