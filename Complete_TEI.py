#this program imports a unfinished TEI document and completes it to a standardized TEI document
#author: Lisa Kiss
#start date: 28.02.22

import os
import xml.etree.ElementTree as ET
import pandas as pd

#open excel with meta data of Mären and put content into data frame
data = pd.read_excel (r'C:\Users\lisak\Documents\Uni\Master\Masterarbeit\Märenkorpus.xlsx')
df = pd.DataFrame(data, columns= ['Titel','Autor','Original_Titel','Entstehungsjahr','Quelle'])

#get header info
file_list = df.to_dict(orient='record')            #list with one dictionary per excel row (one dictionary per file)
print(file_list)
#loop to go over dictionarys in file list
for element in file_list:
    #Title
    title = element['Titel']
    #Original Title in middle high german
    original_titel = element['Original_Titel']
    #author
    if str(element['Autor']) == "nan":             #Attention: typ of nan not string but float
        autor = "unbekannt"
    else:
        autor = element['Autor']
    #source
    if str(element['Quelle']) == "Gesammtabenteuer Band 1":
        pubplace = "Stuttgart; Tuebingen"
        quelle = element['Quelle']
        jahr = "1850"
    elif str(element['Quelle']) == "Gesammtabenteuer Band 2":
        pubplace = "Stuttgart; Tuebingen"
        quelle = element['Quelle']
        jahr = "1850"
    elif str(element['Quelle']) == "Gesammtabenteuer Band 3":
        pubplace = "Stuttgart; Tuebingen"
        quelle = element['Quelle']
        jahr = "1850"
    elif str(element['Quelle']) == "MHDBDB":
        pubplace = "NA"
        quelle = element['Quelle']
        jahr = "1850"
    else:
        pubplace = "NA"
        quelle = element['Quelle']
        jahr = "NA"

    #build new TEI
    TEI_root = ET.Element("TEI" ,xmlns='http://www.tei-c.org/ns/1.0')

    #header
    header = ET.SubElement(TEI_root, "teiHeader")
    #file description
    file_desc = ET.SubElement(header, "fileDesc")
    #title statement
    title_stm = ET.SubElement(file_desc, "titleStmt")
    ET.SubElement(title_stm, "title").text = title

    #file_desc close

    #source description
    source_desc = ET.SubElement(header, "sourceDesc")
    #bibl_full
    bibl_full = ET.SubElement(source_desc, "biblFull")
    #title statement
    title_stm_bib = ET.SubElement(bibl_full, "titleStmt")
    ET.SubElement(title_stm_bib, "title").text = title
    ET.SubElement(title_stm_bib, r'title type = "alt"').text = str(original_titel)
    ET.SubElement(title_stm_bib, "author").text = str(autor)
    #publication statement bib
    publication_stm_bib = ET.SubElement(bibl_full, "publicationStmt")
    ET.SubElement(publication_stm_bib, "publisher").text = str(quelle)
    ET.SubElement(publication_stm_bib, "pubPlace").text = pubplace
    ET.SubElement(publication_stm_bib, "date").text = str(jahr)

    #sourceDesc close
    #header close

    #open tei
    filename = element['Titel'] + '.xml'
    path = os.path.join(r'C:\Users\lisak\Documents\Uni\Master\Masterarbeit\Mären\Gesamtabenteuer Band 1\TEIs', filename)
    if filename ==  filename == "Crescentia.xml" or filename == "Der_Busant.xml" or filename == "Der_Jungherr_und_der_treue_Heinrich.xml" or filename == "Die_Eule_und_der_Habicht.xml" or filename == "Die_Rebhuehner.xml"  or filename == "Gegen_Gleichgeschlechtlichkeit.xml" or filename == "Helmbrecht.xml" or filename == "Meister_Irregang.xml" or filename == "Die_treue_Magd.xml" :
        continue
    opened = open(path)
    content = opened.read()

    #body
    body = ET.SubElement(TEI_root, "Text")
    ET.SubElement(body, "p").text = content

    #print into new xml file
    tree = ET.ElementTree(TEI_root)
    ET.indent(tree, space="\t", level=0)
    tree.write(filename, encoding="UTF-8")



