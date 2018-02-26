import os
import urllib
import xml.etree.ElementTree as ET
import zipfile
import progressbar # progressbar2
import math

vfrSectionalCities = ["Albuquerque", "Anchorage", "Atlanta", "Bethel",
             "Billings", "Brownsville", "Cape Lisburne", "Charlotte",
             "Cheyenne", "Chicago", "Cincinnati", "Cold Bay",
             "Dallas-Ft Worth", "Dawson", "Denver", "Detroit",
             "Dutch Harbor", "El Paso", "Fairbanks", "Great Falls",
             "Green Bay", "Halifax", "Hawaiian Islands", "Houston",
             "Jacksonville", "Juneau", "Kansas City", "Ketchikan",
             "Klamath Falls", "Kodiak", "Lake Huron", "Las Vegas",
             "Los Angeles", "McGrath", "Memphis", "Miami",
             "Montreal", "New Orleans", "New York", "Nome", "Omaha",
             "Phoenix", "Point Barrow", "Salt Lake City",
             "San Antonio", "San Francisco", "Seattle", "Seward",
             "St Louis", "Twin Cities", "Washington",
             "Western Aleutian Islands", "Whitehorse", "Wichita"]

tacCities = ["Anchorage-Fairbanks", "Atlanta", "Baltimore-Washington",
             "Boston", "Charlotte", "Chicago", "Cincinnati", "Cleveland",
             "Dallas-Ft Worth", "Denver-Colorado Springs", "Detroit",
             "Houston", "Kansas City", "Las Vegas", "Los Angeles",
             "Memphis", "Miami", "Minneapolis-St Paul", "New Orleans",
             "New York", "Philadelphia", "Phoenix", "Pittsburgh",
             "Puerto Rico-VI", "St Louis", "Salt Lake City", "San Diego",
             "San Francisco", "Seattle", "Tampa-Orlando"]

bar = progressbar.ProgressBar(max_value=100)

def updateProgress(current, chunk, total):
    percent = current * chunk * 100 / total
    bar.update(percent)

def downloadFile(fileUrl, chartName):
    # Create downloads directory if it does not exist
    try:
        os.mkdir("downloads")
        print "Creating directory 'downloads'"
    except:
        print "Directory 'downloads' already exists"

    # Download chart
    downloadMessage = "Downloading "
    for name in chartName:
        downloadMessage += name
        if name != chartName[len(chartName)-1]:
            downloadMessage += ", "
    print downloadMessage
    urllib.urlretrieve(fileUrl, "downloads/temp.zip", reporthook=updateProgress)

    # Extract chart from zip file
    if len(chartName) == 1:
        print "\nExtracting file..."
    else:
        print "\nExtracting files..."
    zipRef = zipfile.ZipFile("downloads/temp.zip", 'r')
    for name in chartName:
        zipRef.extract(name, "downloads")
    zipRef.close()

    # Remove zip file
    os.remove("downloads/temp.zip")

    return

def getVfrSectional(cityName, edition = "current", format = "tiff"):
    # VFR Sectionals valid 6 months 15 days

    # Create API URL
    vfrApi = "https://soa.smext.faa.gov/apra/vfr/sectional/chart?geoname="
    vfrApi += cityName
    vfrApi += "&edition="
    vfrApi += edition
    vfrApi += "&format="
    vfrApi += format

    print(vfrApi)

    # Get API response
    resp = urllib.urlopen(vfrApi)
    xmlStr = resp.read()
    print(xmlStr)

    # Parse XML response
    root = ET.fromstring(xmlStr)

    editionInfo = root.findall("{http://arpa.ait.faa.gov/arpa_response}edition")[0]
    editionDate = editionInfo.find("{http://arpa.ait.faa.gov/arpa_response}editionDate").text
    editionNum = editionInfo.find("{http://arpa.ait.faa.gov/arpa_response}editionNumber").text
    productUrl = editionInfo.find("{http://arpa.ait.faa.gov/arpa_response}product").get("url")

    print editionDate
    print productUrl

    fileName = [cityName + " SEC " + editionNum + ".tif"]

    downloadFile(productUrl, fileName)

    return

def getTac(cityName, edition = "current", format = "tiff"):
    # VFR Sectionals valid 6 months 15 days

    # Create API URL
    tacApi = "https://soa.smext.faa.gov/apra/vfr/tac/chart?geoname="
    tacApi += cityName
    tacApi += "&edition="
    tacApi += edition
    tacApi += "&format="
    tacApi += format

    print(tacApi)

    # Get API response
    resp = urllib.urlopen(tacApi)
    xmlStr = resp.read()
    print(xmlStr)

    # Parse XML response
    root = ET.fromstring(xmlStr)

    editionInfo = root.findall("{http://arpa.ait.faa.gov/arpa_response}edition")[0]
    editionDate = editionInfo.find("{http://arpa.ait.faa.gov/arpa_response}editionDate").text
    editionNum = editionInfo.find("{http://arpa.ait.faa.gov/arpa_response}editionNumber").text
    productUrl = editionInfo.find("{http://arpa.ait.faa.gov/arpa_response}product").get("url")

    print editionDate
    print productUrl

    if cityName == "Tampa-Orlando":
        fileName = ["Tampa" + " TAC " + editionNum + ".tif",
                    "Orlando" + " TAC " + editionNum + ".tif",
                    "Orlando" + " FLY " + editionNum + ".tif"]
    elif cityName == "Denver-Colorado Springs":
        fileName = ["Denver" + " TAC " + editionNum + ".tif",
                    "Denver" + " FLY " + editionNum + ".tif",
                    "Colorado Springs" + " TAC " + editionNum + ".tif"]
    else:
        fileName = [cityName + " TAC " + editionNum + ".tif",
                    cityName + " FLY " + editionNum + ".tif"]

    downloadFile(productUrl, fileName)

    return

def getIfr(chartNum, type = "low", edition = "current", format = "tiff"):

    # Create API URL
    ifrApi = "https://soa.smext.faa.gov/apra/enroute/chart?"
    ifrApi += "edition="
    ifrApi += edition
    ifrApi += "&format="
    ifrApi += format
    ifrApi += "&geoname=US&seriesType="
    ifrApi += type

    print(ifrApi)

    # Get API response
    resp = urllib.urlopen(ifrApi)
    xmlStr = resp.read()
    print(xmlStr)

    # Parse XML response
    root = ET.fromstring(xmlStr)

    editionInfo = root.findall("{http://arpa.ait.faa.gov/arpa_response}edition")[0]
    editionDate = editionInfo.find("{http://arpa.ait.faa.gov/arpa_response}editionDate").text
    editionNum = editionInfo.find("{http://arpa.ait.faa.gov/arpa_response}editionNumber").text
    productUrl = editionInfo.find("{http://arpa.ait.faa.gov/arpa_response}product").get("url")

    # Change URL for desired chart number
    urlLen = len(productUrl)
    tens = math.modf(chartNum / 10)[1]
    newUrl = productUrl[:(urlLen-6)] + ("%i" % tens) + ("%i" % (chartNum - (tens * 10))) + ".zip"

    print editionDate
    print newUrl

    if type == "high":
        typeCode = "H"
    else:
        typeCode = "L"

    if chartNum < 10:
        fileName = ["ENR_" + typeCode + "0" + ("%i" % chartNum) + ".tif"]
    else:
        fileName = ["ENR_" + typeCode + ("%i" % chartNum) + ".tif"]

    downloadFile(newUrl, fileName)

    return

#getVfrSectional("Cold Bay", "current")
#getTac("Denver-Colorado Springs")
getIfr(7, "high")
