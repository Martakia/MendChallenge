from Converters.SenatorChartConverter import SenatorChartConverter


def main():
    base = "https://www.senate.gov"
    endpoint = "/general/contact_information/senators_cfm.xml"

    senatorConverter = SenatorChartConverter(dataEndpoint = base + endpoint)

    # Get the XML from the link
    senatorConverter.GetXMLData()

    # Convert the data to the desired format
    senatorConverter.ConvertDataToJson()

    # Print each converted member node
    senatorConverter.PrintJsonData()


if __name__ == "__main__":
    
    main()