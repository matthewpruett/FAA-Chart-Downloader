import os
import urllib
import xml.etree.ElementTree as ET
import zipfile
import progressbar # progressbar2
import time

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
    print "Downloading " + chartName
    bar.begin()
    urllib.urlretrieve(fileUrl, "downloads/temp.zip", reporthook=updateProgress)
    bar.finish()

    # Extract chart from zip file
    print "\nExtracting file..."
    zipRef = zipfile.ZipFile("downloads/temp.zip", 'r')
    zipRef.extract(chartName, "downloads")
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

    fileName = cityName + " SEC " + editionNum + ".tif"

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

    fileName = cityName + " TAC " + editionNum + ".tif"

    downloadFile(productUrl, fileName)

    return

#getVfrSectional(vfrSectionalCities[20], "current")
getTac(tacCities[8])
