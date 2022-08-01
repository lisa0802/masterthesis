#this program imports a xml document, parses it and stores its content
#author: Lisa Kiss
#start date: 12.02.22

import os
from bs4 import BeautifulSoup
import csv
import re

#decision if mentions with flags should be counted
#if yes --> mentions with flags "rede", "in_rede" or "beschreibung" are also counted
#if no --> mentions with flags "rede", "in_rede" or "beschreibung" are not counted
decision = "no"

#open TEI documents
filenames= os.listdir(r'C:\Users\lisak\Documents\Uni\Master\Masterarbeit\Mären\Gesamtabenteuer Band 1\TEIs')
for file in filenames:
    print(file)
    g = os.path.join(r'C:\Users\lisak\Documents\Uni\Master\Masterarbeit\Mären\Gesamtabenteuer Band 1\TEIs',file)
    file_name_list = file.split('.') #to remove the .xml ending
    file_name = file_name_list[0]
    #opens first doc
    opened = open(g)
    content = opened.read()
    #open doc and store lines in list
    with open(g) as files:
        lines = files.readlines()
    #delete blank lines (because every second line is blank)
    lines_wo_blank_lines = []
    for item in lines:
        if item != '\n':
            lines_wo_blank_lines.append(item)
        else:
            continue

    #get reference names and flags to create a figure list
    ref_list_flags = []
    ref_list_names =[]
    soup = BeautifulSoup(content, 'html.parser')
    ref_list = soup.find_all('rs')
    #loop to get different references and check if flags are counted based on decision
    for ref in ref_list:
        name =ref.get('ref')
        if name == '#Got,NA,NA,NA,gott,nebenfigur':
            continue
        elif name == '#Erzaehler,NA,NA,NA,erzaehler,erzaehler' or name == '#Erzaehler,NA,NA,NA,erzaehler,erzaehler,' or name == '#Vrouwe-des-erzaehlers,weiblich,NA,NA,reale-person,reale-person' or name == '#Vrouwe-von-erzaehler,weiblich,NA,NA,reale-person,reale-person':
            continue
        elif name == '#Leser,NA,NA,NA,leser,leser':
            continue
        elif name == '#Tiuvel,NA,NA,NA,teufel,nebenfigur' or name == '#Lucifer,NA,NA,NA,teufel,nebenfigur' or name == '#Tiuvel,NA,NA,NA,teufel,hauptfigur' or name == '#Satana,NA,NA,NA,teufel,nebenfigur' or name == '#Lucifier,NA,NA,NA,teufel,nebenfigur':
            continue
        if decision == "no":
            flag = ref.get('ana')
            if flag == "rede":
                continue
            elif flag == "beschreibung":
                continue
            elif flag == "in_rede":
                continue
            else:
                ref_list_names.append(name)
        elif decision == "yes":
            ref_list_names.append(name)

    #create a list without duplicate figures to search for in list with all references of the window
    figure_list_wo_duplicates = []
    figure_list = []
    for item in ref_list_names:
        if item not in figure_list_wo_duplicates:
            regex = re.search('([^,]+).*?([^,]+).*?([^,]+).*?([^,]+).*?([^,]+).*?([^,]+)', item) #finds parts of reference name to get the different properties into different list items
            name_of_figure = regex.group(1)
            geschlecht = regex.group(2)
            stand = regex.group(3)
            alter = regex.group(4)
            if regex.group(5) == 'religioese-figur' or regex.group(5) == 'teufel':
                continue
            bezeichnung = regex.group(5)
            if regex.group(6) == 'autor' or regex.group(6) == 'autor2' or regex.group(6) == 'autor:tristan' or regex.group(6) == 'reale-person':
                continue
            rolle = regex.group(6)
            figure_list_wo_duplicates.append(item)
            figure_list.append([name_of_figure,geschlecht,stand,alter,bezeichnung,rolle])
        else:
            continue
    print(figure_list)

    #create node list
    header_nodes = ['name','geschlecht','stand','alter','bezeichnung','rolle']
    filename =file_name +'.csv'
    path_to_folder = os.path.join(r'C:\Users\lisak\Documents\Uni\Master\Masterarbeit\Mären\Gesamtabenteuer Band 1\CSVs\Nodes', filename)
    with open(path_to_folder, 'w', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file) 
        csvwriter.writerow(header_nodes)
        for row in figure_list:
            csvwriter.writerow(row)

    #find and get alls references in the window and check for figures from figurelist and create edges
    lines = []
    edgelist=[]
    lines_refs =[]
    #set window size
    window_size = 10
    start = 0
    end = start + window_size
    line_count = (len(lines_wo_blank_lines))//window_size
    rest = (len(lines_wo_blank_lines))%window_size
    list_list = []

    #words to help exclude the figures with the the tag 'autor', 'religioese_figur', 'reale-person' and 'teufel'
    word = 'autor'
    word2 = 'religioese'
    word3 = 'reale-person'
    word4 = 'teufel'

    #loop to go over the whole text
    for i in range(line_count):
        #loop to get refernces of lines of the window
        for h in range (start,end):                                         #start and end of the window
            soup = BeautifulSoup(lines_wo_blank_lines[h],'html.parser')     #gets references
            refs = soup.find_all('rs')
            #loop to append refernces of one line to list based on decision with or without mentions with flags
            for item in refs:
                name = item.get('ref')
                if name == '#Got,NA,NA,NA,gott,nebenfigur':
                    continue
                elif name == '#Erzaehler,NA,NA,NA,erzaehler,erzaehler' or name == '#Erzaehler,NA,NA,NA,erzaehler,erzaehler,' or name == '#Vrouwe-des-erzaehlers,weiblich,NA,NA,reale-person,reale-person' or name == '#Vrouwe-von-erzaehler,weiblich,NA,NA,reale-person,reale-person':
                    continue
                elif name == '#Leser,NA,NA,NA,leser,leser':
                    continue
                elif word in name:
                    continue
                elif word2 in name:
                    continue
                elif word3 in name:
                    continue
                elif word4 in name:
                    continue
                if decision == "no":
                    flag = item.get('ana')
                    if flag == "rede":
                        continue
                    elif flag == "beschreibung":
                        continue
                    elif flag == "in_rede":
                        continue
                    else:
                        lines_refs.append(name)
                elif decision == "yes":
                    lines_refs.append(name)

        #go over figures. If you find a figure in window create edges with figure and every other figure in window, append edges to edgelist
        #loop to go over figures
        for figure in figure_list_wo_duplicates:
            #loop to go over references of the lines of the window
            for item in lines_refs:
                working_list = []
                if figure in lines_refs:
                    if figure == item:                                      #to not create edges to itself
                        continue
                    else:
                        figure_new = re.search('^([^,])+',figure)
                        item_new = re.search('^([^,])+',item)
                        working_list.append(figure_new.group())
                        working_list.append(item_new.group())
                        edgelist.append(working_list)
                else:
                    continue

        #delete duplicates
        edgelist_final = []
        for f in range(len(edgelist)):
            if edgelist[f] not in edgelist_final:
                edgelist_final.append(edgelist[f])
            else:
                continue

        start = end
        end = end + window_size
        list_list.append(edgelist_final)
        lines_refs = []
        edgelist = []

    #remaining lines (rest of the division)
    for h in range((line_count*window_size),(((line_count*window_size)+rest))):
        soup = BeautifulSoup(lines_wo_blank_lines[h], 'html.parser')
        refs = soup.find_all('rs')
        for item in refs:
            name = item.get('ref')
            if name == '#Got,NA,NA,NA,gott,nebenfigur':
                continue
            elif name == '#Erzaehler,NA,NA,NA,erzaehler,erzaehler' or name == '#Erzaehler,NA,NA,NA,erzaehler,erzaehler,' or name == '#Vrouwe-des-erzaehlers,weiblich,NA,NA,reale-person,reale-person' or name == '#Vrouwe-von-erzaehler,weiblich,NA,NA,reale-person,reale-person':
                continue
            elif name == '#Leser,NA,NA,NA,leser,leser':
                continue
            elif word in name:
                continue
            elif word2 in name:
                continue
            elif word3 in name:
                continue
            elif word4 in name:
                continue
            flag = item.get('ana')
            if flag == "rede":
                continue  # [name,name2]
            elif flag == "beschreibung":
                continue
            elif flag == "in_rede":
                continue
            else:
                lines_refs.append(name)

    for figure in figure_list_wo_duplicates:
        for item in lines_refs:
            working_list = []
            if figure in lines_refs:
                if figure == item:
                    continue
                else:
                    figure_new = re.search('^([^,])+', figure)
                    item_new = re.search('^([^,])+', item)
                    working_list.append(figure_new.group())
                    working_list.append(item_new.group())
                    edgelist.append(working_list)
            else:
                continue

    # delete duplicates
    edgelist_final = []
    for f in range(len(edgelist)):
        if edgelist[f] not in edgelist_final:
            edgelist_final.append(edgelist[f])
        else:
            continue
    list_list.append(edgelist_final)
    lines_refs = []
    edgelist = []

    #add weight. Create a dictionary with edge as key and weight as value. If it is already in the dictionary add 1 to weight
    weight_dict = {}
    #loop to go over list with edges
    for i in range(len(list_list)):
        #loop to go over list of window in list with edges
        for h in range(len(list_list[i])):
                    if ((list_list[i][h][0],list_list[i][h][1])) not in weight_dict:                                                    #add edge to dictionary if its not already in it and set weight to 1
                        weight_dict[list_list[i][h][0],list_list[i][h][1]] = 1                                                          #append ('Lisa','Sarah'):0
                    else:                                                                                                               #if edge is already in dictionary change value of specific key to value plus one
                        weight_dict[list_list[i][h][0],list_list[i][h][1]] = weight_dict[(list_list[i][h][0],list_list[i][h][1])]+1     #weight_dict['Lisa','Sarah] = previous value +1
    #print(list_list) # list with lists with references in the window
    #print(weight_dict) # dictionaries with singular edges with weights

    #change dictionary back to a list
    a_list = []
    for item in weight_dict.keys():
        a_list.append([item[0],item[1],weight_dict[item]])

    #print to csv
    filename =file_name + '.csv'
    path_to_folder = os.path.join(r'C:\Users\lisak\Documents\Uni\Master\Masterarbeit\Mären\Gesamtabenteuer Band 1\CSVs\Edges',filename)
    header = ['from','to','weight']
    with open(path_to_folder, 'w', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(header)
        for row in a_list:
            csvwriter.writerow(row)