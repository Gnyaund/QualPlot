from lib.dataplot import DataPlot
import json

if __name__ == "__main__":
    jopen = open(".\\config.json", "r")
    config = json.load(jopen)
    QUALNET_PATH = config["qualnet_path"]

    print("SEED START Number ->")
    start = int(input())
    print("SEED END Number ->")
    end = int(input())
    print("MAX NODE Number ->")
    node = int(input())


    c = DataPlot(start, end, node, QUALNET_PATH)
    
    c.nameResolver()
    c.qualFilesCopy()
    c.executeQualnet()
    
    c.makeCsvFolder()
    c.extractSendingPacket()

    c.makeAnalysisFolder()
    c.executePlot()

    c.makeCombinegraphFolder()
    c.combinePlot()

    c.deleteCopyFiles()
    c.moveArchives()