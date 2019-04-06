from Converters.BaseConverterAbs import BaseConverter
from xml.etree import ElementTree as ET
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from collections import OrderedDict
import json


class SenatorChartConverter(BaseConverter):
    cityKeyWords = ["NEW", "LOS", "SAN", "FORT", "FT.", "FT", "EL", "LONG", "SANTA", "SAINT", "ST.", "ST", "SAN", "CITY", "BEACH", "SPRINGS", "ROUGE", "VISTA"]

    def __init__(self, dataEndpoint):
        BaseConverter.__init__(self, dataEndpoint)


    def GetXMLData(self):
        # Set up the request and set the user agent in order to have the request complete
        request = Request(url = self.dataEndpoint)
        request.add_header("User-Agent", "MendTest-/0.1")
        
        # Send the request and then convert the result to an XML
        try:
            reqResult = urlopen(request)
            self.xmlData = ET.fromstring(reqResult.read())
        
        except HTTPError as err:
            print("Unable to get response from dataEndpoint.")
            print(err.reason)

        except ET.ParseError:
            print("Unable to parse XML data.")
            reqResult.close()
        
        else:
            # Close the request since we are done with it
            reqResult.close()


    def ConvertDataToJson(self):
        """Converts class xmlData att to json format and places it into
           a list of json objects called jsonData. Expected format of each object
           is as follows:
           {
                “firstName”: “First”,
                “lastName”: “Last”,
                “fullName”: “First Last”,
                “chartId”: “:Contents of bioguide_id:”,
                “mobile”: “Phone”,
                “address”: [
                    {
                        “street”: “123 Main Street”,
                        “city”: “Orlando”,
                        “state”: “FL”,
                        “postal”: 32825
                    }
                ]
            }
        """
        if not hasattr(self, "xmlData"):
            print("Unable to convert data, xml data is missing.")
            pass
        
        xml = self.xmlData
        self.jsonData = []

        # Traverse each node in the root of the xml where the tag is member
        for member in list(xml.iter(tag = "member")):

            memberObject = OrderedDict()

            # Get each expected property and convert it into the json
            # NOTE: If no property of the tag returns in the list, then an empty string will be placed
            
            # NOTE: For first and last name, currently if a person has two last names, both are put
            # into the same xml node. If that changes, then this will need to be updated

            # firstName, lastName, fullName
            self.__convertMemberName(memberNode = member, memberObject = memberObject)

            # chartID
            self.__convertMemberValue(memberNode = member, memberObject = memberObject, xmlTag = "bioguide_id", jsonTag = "chartId")

            # mobile
            self.__convertMemberValue(memberNode = member, memberObject = memberObject, xmlTag = "phone", jsonTag = "mobile")

            # address
            self.__convertMemberAddress(memberNode = member, memberObject = memberObject)
            
            # Add the member data to the collection
            self.jsonData.append(memberObject)


    def PrintJsonData(self):
        if not hasattr(self, "jsonData"):
            print("Unable to print json data, json data is missing.")
            pass
        
        for member in self.jsonData:
            print(json.dumps(member, indent=4))
            print()


    def __convertMemberValue(self, memberNode, memberObject, xmlTag, jsonTag):
        """ Given a member node from an XML, this method converts that to a json property
            memberNode: The xml node to be searched
            memberObject: The json object to have the converted value insterted into
            xmlTag: The tag to search the xml node for.
            jsonTag: By default the same value as the xmlTag, but if a different name for the json property
                     is desired, this value can be passed in.
        """
        # TODO: insert type checking for parameters

        properties = list( memberNode.iter(tag = xmlTag) )

        value = ""
        if len(properties) != 0:
            value = properties[0].text
            
        memberObject.update( {jsonTag : value} )


    def __convertMemberName(self, memberNode, memberObject):
        """ Given the memberNode and memberObject to insert into this method will
            convert the first, last and full name of the member
            memberNode: The xml node to be searched
            memberObject: The json object to have the converted value insterted into
        """
        # TODO: insert type checking for parameters

        # firstName
        properties = list( memberNode.iter(tag = "first_name") )

        firstNameValue = ""
        if len(properties) != 0:
            firstNameValue = properties[0].text

        memberObject.update( {"firstName" : firstNameValue} )
         
        # lastName
        properties = list(memberNode.iter(tag = "last_name"))

        lastNameValue = ""
        if len(properties) != 0:
            lastNameValue = properties[0].text
            
        memberObject.update( {"lastName" : lastNameValue} )

        # fullName
        memberObject.update( {"fullName" : firstNameValue + " " + lastNameValue} )


    def __convertMemberAddress(self, memberNode, memberObject):
        """ Given the memberNode and memberObject to insert into, this method will
            convert and parse out the address information. This method assumes the address has already
            been validated and that the state will be the 2 character representation.
            memberNode: The xml node to be searched
            memberObject: The json object to have the converted value insterted into
        """
        # Sample address to parse: 717 Hart Senate Office Building Washington DC 20510
        # Expected result:
        #   street : 717 Hart Senate Office Building
        #   city : Washington DC
        #   state : 
        #   postal : 30510
        
        addressList = []
        addressVal = {}
        streetVal = ""
        cityVal = ""
        stateVal = ""
        postalVal = ""

        # TODO?: Validate address, but for now assume the data handed to it is valid
        properties = list(memberNode.iter(tag = "address"))
        propertiesLen = len(properties)

        if propertiesLen >= 1:
            # We use a list of key word to determine if cities have two words in their name. This will effect the address parsing. 

            for address in properties:
                splitAddress = address.text.split()
                splitAddressLen = len(splitAddress)

                # Washington DC has no state
                if splitAddress[splitAddressLen - 2] == "DC":
                    streetVal = splitAddress[0]
                    for i in range(1, splitAddressLen - 3):
                        streetVal += " " + splitAddress[i]

                    cityVal = splitAddress[splitAddressLen - 3] + " " + splitAddress[splitAddressLen - 2]
                    stateVal = ""
                    
                # 2 word city
                elif splitAddress[splitAddressLen - 3].upper() in self.cityKeyWords or splitAddress[splitAddressLen - 4].upper() in self.cityKeyWords:
                    streetVal = splitAddress[0]
                    for i in range(1, splitAddressLen - 5):
                        streetVal += " " + splitAddress[i]

                    cityVal = splitAddress[splitAddressLen - 4] + " " + splitAddress[splitAddressLen - 3]
                    stateVal = splitAddress[splitAddressLen - 2]

                # Else default to 1 state city
                else:
                    streetVal = splitAddress[0]
                    for i in range(1, splitAddressLen - 4):
                        streetVal += " " + splitAddress[i]

                    cityVal = splitAddress[splitAddressLen - 3]
                    stateVal = splitAddress[splitAddressLen - 2]
                
                postalVal = splitAddress[splitAddressLen - 1]

                addressVal.update( {"street" : streetVal} )
                addressVal.update( {"city" : cityVal} )
                addressVal.update( {"state" : stateVal} )
                addressVal.update( {"postal" : postalVal} )

                addressList.append(addressVal)

                memberObject.update( { "address" : addressList} )
                
                # Reset the values before moving on to the next address
                streetVal = ""
                cityVal = ""
                stateVal = ""
                postalVal = ""
                addressList = []
                addressVal = {}

        elif propertiesLen == 0:        

            addressVal.update( {"street" : streetVal} )
            addressVal.update( {"city" : cityVal} )
            addressVal.update( {"state" : stateVal} )
            addressVal.update( {"postal" : postalVal} )

            addressList.append(addressVal)

            memberObject.update( { "address" : addressList} )