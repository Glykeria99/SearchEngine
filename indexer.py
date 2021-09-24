import os
import csv
import numpy
import copy

def myInvertedIndexer():
    list = []
    num_of_words_in_doc = []
    num = 0
    columns = ['word', 'document', 'frequency']
    # getting each word from each file
    # creating a csv file to save the data
    with open('.\\indexer\\indexer.csv', 'w', newline='', encoding='utf-8') as csv_file:

        for file in os.listdir(".\\files\\"):  # for each txt file created by crawler
            words_count = 0
            if not file.endswith(".txt"):
                continue
                # reading each line
            with open(".\\files\\" + file, 'r',  encoding='utf-8') as f:
                for line in f:
                    # reading each word
                    for word in line.split():
                        punc = '''!()|-[]{};:'", <>./?@#$%^&*_~©®™¨¨«»'''
                        if word in punc:
                            continue
                        words_count = words_count+1
                        flag = 0
                        for index, array in enumerate(list):
                            if word in array[0] and str(file) == str(array[1]):
                                list[index][2] = int(list[index][2]) + 1
                                flag = 1
                        if flag == 0:
                            list.append(numpy.array([str(word), str(file), 1]))
                        else:
                            continue
            num_of_words_in_doc.append([file, words_count])
        # sorting the csv in alphabetic order by the 'word' value
        list.sort(key=get_word)
        # print(numpy.array(list).tolist())
        # calculating the number of documents that each word appears in.
        print("all words in list: ", len(list))
        count = []
        frequency = 0
        previous_word = list[0][0]
        for array in list:
            current_word = array[0]
            if current_word == previous_word:
                frequency = frequency + 1
                previous_word = current_word
            else:
                count.append([previous_word, frequency])
                frequency = 1
                previous_word = current_word
    print("all different words: ", len(count))
    #print(count)
    # creating a csv file to save the data
    indexer_copy = []
    with open('.\\indexer\\indexer.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['word', 'documents', 'data']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        temp = []
        for data in count:
            temp.clear()
            for array in list:
                if array[0] == data[0]:
                    temp.append([str(array[1]), int(array[2])])
            temp2 = copy.deepcopy(temp)
            indexer_copy.append([data[0], data[1], temp2]) # Icorrectly add the temp (always adds the last temp data for some reason)
            # writer.writerow({'word': data[0], 'documents': data[1], 'data': temp})
    print(*indexer_copy, sep='\n')

    print("counter for words in each doc: ", num_of_words_in_doc)
    return count, num_of_words_in_doc, indexer_copy


def get_word(array):
    return array[0]

