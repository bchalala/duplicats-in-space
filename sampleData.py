#!/usr/bin/env python

import csv
import unidecode

dataDir = "dataRev2"
sampleDataDir = "sampleData"

'''
Creates sample data from PaperAuthor, Paper, Author csv files and saves to sampleDataDir

USAGE:
    mkdir sampleData
    python3 sampleData.py
'''
def buildSampleData(numPapers, inputDir, outputDir):
    papers = set()
    authors = set()

    with open(dataDir + "/PaperAuthor.csv") as csvfile:
        reader = csv.DictReader(csvfile)

        with open(sampleDataDir + "/PaperAuthor.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)

            writer.writeheader()
            for row in reader:
                # make sure to stop after numPapers
                if len(papers) >= numPapers:
                    break

                papers.add(row["PaperId"])
                authors.add(row["AuthorId"])
                writer.writerow(row)

    copyFile("Author.csv", authors, inputDir, outputDir)
    copyFile("Paper.csv", papers, inputDir, outputDir)
    return papers, authors

def copyFile(filename, Ids, inputDir, outputDir):
    with open(inputDir + "/" + filename) as csvfile:
        reader = csv.DictReader(csvfile)

        with open(outputDir + "/" + filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)

            writer.writeheader()
            for row in reader:
                # make sure to include rows matching Ids (or all if None)
                if Ids is None or row["Id"] in Ids:
                    writer.writerow(row)


papers, authors = buildSampleData(70000, dataDir, sampleDataDir)
print("number of papers copied: %d" % len(papers))
print("number of authors copied: %d" % len(authors))
