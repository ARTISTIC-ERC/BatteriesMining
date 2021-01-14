#!/usr/bin/env python
# -*- coding: utf-8 -*-


import string
import re
import os

__all__ = ['Filtring_Function', 'Filtring_Classify']


def Clean_text(text):
    """
    :param file: text to clean
    :return: clean text
    """
    stop = [item for item in string.punctuation if (item != ':' and item != '/' and item != '.' and item != '-' and item != ',')]
    stop.remove('%')
    liste = ['', '', '', '', '', '', '', '', '', '', '', '', '', '�']
    stop = stop + liste
    text.translate(str.maketrans('', '', str(stop)))
    text = re.sub("\s\s+", " ", text)

    return text


def Devide_Title_Abstract_Key(text, sub_text, keywords, abstract, No_Intro):
    """
    :param text: the text of interest
    :param sub_text: text before "introduction"
    :param keywords: list of "keywords" and its synonyms
    :param abstract: list of "abstract" and its synonyms
    :param No_Intro: if there is introduction or not
    :return: the title, the keywords and the abstract parts
    """
    No_Keywords = True
    No_Abstract = True
    if No_Intro == False:
        if any(item in sub_text for item in keywords):
            for key in keywords:
                if key in sub_text:
                    words_text = sub_text.split(key)[1]
                    words = words_text.split()
                    wanted_words = words[0:15]
                    keywords_part = ' '.join(wanted_words)
                    No_Keywords = False

        elif not any(item in sub_text for item in keywords):
            keywords_part = ''
        if any(item in sub_text for item in abstract):
            for key in abstract:
                if key in sub_text:
                    abstract_part = sub_text.split(key)[1]
                    title_part = sub_text.split(key)[0]
                    No_Abstract = False
            if No_Abstract == False and No_Keywords == False:
                if any(item in title_part for item in keywords):
                    for key in keywords:
                        if key in title_part:
                            title_part_yes = title_part.split(key)[0]
                    title_part = title_part_yes
                if any(item in abstract_part for item in keywords):
                    for key in keywords:
                        if key in abstract_part:
                            abstract_part_yes = abstract_part.split(key)[0]
                    abstract_part = abstract_part_yes
        else:
            words = sub_text.split()
            title_list = []
            abstract_list = []
            for i in range(0, int(len(words) * 0.33)):
                title_list.append(words[i])
            title_part = ' '.join(item for item in title_list)
            for i in range(int(len(words) * 0.33), len(words)):
                abstract_list.append(words[i])
            abstract_part = ' '.join(item for item in abstract_list)
    else:
        if any(item in text for item in keywords):
            for key in keywords:
                if key in text:
                    words_text = text.split(key)[1]
                    words = words_text.split()
                    wanted_words = words[0:15]
                    keywords_part = ' '.join(wanted_words)
        else:
            keywords_part = ''
        if any(item in text for item in abstract):
            for key in abstract:
                if key in text:
                    abstract_part = ''
                    title_part = text.split(key)[0]
        else:
            title_part = ''
            abstract_part = ''
    if keywords_part == '':
        if any(item in text for item in keywords):
            for key in keywords:
                if key in text:
                    words_text = text.split(key)[1]
                    words = words_text.split()
                    wanted_words = words[0:15]
                    keywords_part = ' '.join(wanted_words)

    return title_part, keywords_part, abstract_part


def Filtring_Classify(file):
    """
    :param file: path of the file of interest
    :return: the title, keywords and abstract
    """
    introduction = ['INTRODUCTION', 'Introduction', 'introduction']
    abstract = ['ABSTRACT', 'Abstract', 'abstract', 'a b s t r a c t', 'A B S T R A C T', 'A b s t r a c t']
    keywords = ['KEYWORDS', 'Keywords', 'keywords']
    text = open(file, 'r', encoding='utf8').read()
    text = Clean_text(text)

    text = text.replace('\n', ' ')
    part_22 = []
    if any(item in text for item in introduction):
        for intro in introduction:
            if intro in text:
                part_2 = text.split(intro)[0]
                part_22.append(part_2)
    try:
        part_2 = part_22[0]
    except:
        part_2 = []
    No_Intro = False
    if part_2 != []:
        sub_text = part_2
    else:
        No_Intro = True

    if No_Intro == False:
        title_part, keywords_part, abstract_part = Devide_Title_Abstract_Key(text, sub_text, keywords, abstract, No_Intro)
    else:
        words = text.split()
        sub_text = []
        for i in range(0, int(len(words)*0.25)):
            sub_text.append(words[i])
        sub_text = ' '.join(item for item in sub_text)
        title_part, keywords_part, abstract_part = Devide_Title_Abstract_Key(text, sub_text, keywords, abstract, No_Intro)

    return title_part, keywords_part, abstract_part


def copy_paste_text(file, path):
    """
    :param file: path to text file
    :param path: the path where to paste the file
    """
    name = file.split('/')[-1][:-4]
    path = path + '/' + name + '.txt'
    f = open(file, 'r', encoding='utf8')
    try:
        with open(path, 'a', encoding='utf8') as f1:
            for x in f.readlines():
                f1.write(x)
            f.close()
            f1.close()
    except:
        try:
            path = '//?/' + path
            with open(path, 'a', encoding='utf8') as f1:
                for x in f.readlines():
                    f1.write(x)
                f.close()
                f1.close()
        except:
            pass


def Remove_Duplicat(seq):
    """
    :param seq: list of interest
    :return: the same entry list removing duplicate elements
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def Capitalize_Liste(liste):
    """
    :param liste: list of string
    :return: the same input list of string in lowercase, in capital letters and earache tring written letter by letter separately
    """
    new_liste = []
    new_liste1 = []
    first = liste[0]
    listes = [item.replace('-', '−') for item in liste if '-' in item]
    liste = liste + listes
    for item in liste:
        new_liste.append(item.capitalize())
        new_liste.append(item.upper())
        new_liste.append(item.title())
    for item in new_liste:
        word = ' '.join(i for i in item)
        new_liste1.append(word)
    liste = liste + new_liste + new_liste1
    liste.insert(0, first)
    liste = Remove_Duplicat(liste)
    return liste


Batteries_plomb = ['lead–acid battery', 'plomb-battery', 'plomb battery', 'battery plomb', 'batteries plomb',
                   'plomb batteries',
                   'battery-plomb', 'batteries-plomb', 'plomb-batteries',
                   'plomb cell', 'plomb battery cell', 'plomb batteries cell', 'plomb cell',
                   'plomb-cell', 'plomb battery-cell', 'plomb batteries-cell', 'plomb-cell',

                   'lead–acid-battery', 'lead–acid battery', 'battery lead–acid', 'batteries lead–acid',
                   'lead–acid batteries',
                   'battery-lead–acid', 'batteries-lead–acid', 'lead–acid-batteries',
                   'lead–acid cell', 'lead–acid battery cell', 'batteries cell lead–acid', 'lead–acid cell',
                   'lead–acid-cell', 'lead–acid battery-cell', 'lead–acid batteries-cell', 'lead–acid-cell',
                   'battery-cell lead–acid', 'batteries-cell lead–acid', 'cell-lead–acid', 'batteries-cell lead–acid',

                   'lead acid-battery', 'lead acid battery', 'battery lead acid', 'batteries lead acid',
                   'lead acid batteries',
                   'battery-lead acid', 'batteries-lead acid', 'lead acid-batteries',
                   'lead acid cell', 'lead acid battery cell', 'batteries cell lead–acid', 'lead acid cell',
                   'lead acid-cell', 'lead acid battery-cell', 'lead acid batteries-cell', 'lead acid-cell',
                   'battery-cell lead acid', 'batteries-cell lead acid', 'cell-lead acid', 'batteries-cell lead acid',

                   'lead/acid-battery', 'lead/acid battery', 'battery lead/acid', 'batteries lead/acid',
                   'lead/acid batteries',
                   'battery-lead/acid', 'batteries-lead/acid', 'lead/acid-batteries',
                   'lead/acid cell', 'lead/acid battery cell', 'batteries cell lead/acid', 'lead/acid cell',
                   'lead/acid-cell', 'lead/acid battery-cell', 'lead/acid batteries-cell', 'lead/acid-cell',
                   'battery-cell lead/acid', 'batteries-cell lead/acid', 'cell-lead/acid', 'batteries-cell lead/acid',

                   'lead-acid-battery', 'lead-acid battery', 'battery lead-acid', 'batteries lead-acid',
                   'lead-acid batteries',
                   'battery-lead-acid', 'batteries-lead-acid', 'lead-acid-batteries',
                   'lead-acid cell', 'lead-acid battery cell', 'batteries cell lead-acid', 'lead-acid cell',
                   'lead-acid-cell', 'lead-acid battery-cell', 'lead-acid batteries-cell', 'lead-acid-cell',
                   'battery-cell lead-acid', 'batteries-cell lead-acid', 'cell-lead-acid', 'batteries-cell lead-acid',

                   ' sla-battery', 'sla battery', 'battery sla', 'batteries sla', 'sla batteries',
                   'battery-sla', 'batteries-sla', 'sla-batteries',
                   'sla cell', 'sla battery cell', 'batteries cell sla', 'sla cell',
                   'sla-cell', 'sla battery-cell', 'sla batteries-cell', 'sla-cell',
                   'battery-cell sla', 'batteries-cell sla', 'cell-sla', 'batteries-cell sla',

                   ' vrla-battery', 'vrla battery', 'battery vrla', 'batteries vrla', 'vrla batteries',
                   'battery-vrla', 'batteries-vrla', 'vrla-batteries',
                   'vrla cell', 'vrla battery cell', 'batteries cell vrla', 'vrla cell',
                   'vrla-cell', 'vrla battery-cell', 'vrla batteries-cell', 'vrla-cell',
                   'battery-cell vrla', 'batteries-cell vrla', 'cell-vrla', 'batteries-cell vrla'

                                                                            ' maintenance free-battery',
                   'maintenance free battery', 'battery maintenance free', 'batteries maintenance free',
                   'maintenance free batteries',
                   'battery-maintenance free', 'batteries-maintenance free', 'maintenance free-batteries',
                   'maintenance free cell', 'maintenance free battery cell', 'batteries cell maintenance free',
                   'maintenance free cell',
                   'maintenance free-cell', 'maintenance free battery-cell', 'maintenance free batteries-cell',
                   'maintenance free-cell',
                   'battery-cell maintenance free', 'batteries-cell maintenance free', 'cell-maintenance free',
                   'batteries-cell maintenance free'
                   ]
Batteries_Nickel_cadmium = ['nickel–cadmium battery', ' ni-cd', ' nicd battery', 'nicad battery',
                            'nickel–cadmium batteries', 'nicd batteries', 'nicad batteries', 'nickel cadmium',
                            'nickel cadmium batteries', 'nickel cadmium battery', 'nickel-cadmium']
Batteries_Nickel_metal_hydride = ['nickel-metal-hydride battery', 'nickel metal hydride battery', ' ni-mh ', ' nimh ',
                                  'nickel-metal hydride battery',
                                  'nickel metal hydride batteries', 'nickel-metal hydride batteries',
                                  'nickel-metal-hydride batteries', 'nickel metal hydride', 'nickel-metal hydride',
                                  'nickel-metal-hydride']
Batteries_lithium_ion = ['Lithium Ion Battery', 'Li ion ', 'Li ions batter', ' lib ', 'lithium-ions batter', 'li ions ', 'Li-ion batter', 'lithium-ions', 'li ion ', 'lithium-ions battery', 'lithium-ion battery', 'Li ions ', 'Li ion batter', 'Li-ion ', 'lithium ions ', 'li-ion ', 'li-ions batter', 'lithium-ion', 'Li-ions batter', 'lithium-ion batter', 'lithium-ions ', 'lithium ion batter', 'li-ion batter', 'Li-ions ', 'lithium ion ', 'li-ions ', 'li ions batter', 'li ion batter', 'lithium ions batter']
Batteries_lithium_Polymer = ['lithium-polymer battery', 'lithium polymer battery', ' li-po ',
                             'lithium polymer batteries', 'lithium-polymer batteries', ' lipo ', ' lip ',
                             'li-poly', 'lithium-poly']
Batteries_lithium_air = ['lithium–air battery', 'lithium–air batteries', 'li–air', ' li air ']
Batteries_sodium_ion = ['Sodium Ion Battery', 'sodium-ions batter', 'na ion ', 'na-ions ', 'sodium-ion battery', ' na batter', 'sodium-ions', 'sodium ion batter', 'sodium ions ', 'na-ion batter', ' na-batter', ' na ions ', 'sodium-ions ', ' na ion ', 'na ions batter', 'sodium ions batter', 'sodium ion', 'sodium-ion batter', 'na-ion ', 'na ions ', 'na-ion', 'sodium-ion', 'na ion batter', 'sodium ion ', 'na-ions batter', ' nib ', 'sodium-ion ']
Batteries_Nickel_Fer = ['nickel–iron battery', 'nickel–iron batteries', 'nickel iron battery', 'nickel iron batteries',
                        ' nife battery', 'ni-fe battery', ' nife batteries', 'ni-fe batteries']
Batteries_Magnesium_Sulfur = ['magnesium–sulfur Batter', 'Magnesium–Sulfur Batter', 'magnesium sulfur batter', 'Mg–S batter', 'mg–s batter', ' mg s batter',
                              'magnesium/sulfur batter', 'Magnesium–sulfur (Mg–S) batter', 'magnesium–sulfur (mg–s) batter']
Batteries_others = ['K-ion batter', 'potassium-ion batter', 'K ion batter', 'potassium ion batter', 'K batter', 'potassium batter', 'Mg-ion batter', 'magnesium-ion batter',
                                    'Mg ion batter', 'magnesium ion batter', 'Mg batter', 'Magnesium batter', 'Al-ion batter', 'aluminium-ion batter', 'Al ion batter', 'aluminium ion batter',
                    'Al batter', 'aluminium batter', 'Ca-ion batter', 'calcium-ion batter', 'Ca ion batter', 'calcium ion batter', 'Ca batter', 'calcium batter'
                    , 'sodium–air batter', 'sodium–air', 'sodium air', 'Na–air batter', 'Na–air', 'Na air', 'sodium–O2 batter', 'sodium–O2', 'sodium air',
                    'Na–O2 batter', 'Na–O2', 'Na O2', 'lithium–air batter', 'lithium–air', 'lithium air', 'Li–air batter', 'Li–air', 'Li air', 'lithium–O2 batter',
                    'lithium–O2', 'lithium air', 'Li–O2 batter', 'Li–O2', 'Li O2', 'K-Ion batter', 'K Ion batter', 'Mg-Ion batter',
                    'Mg Ion batter', 'Al-Ion batter', 'Al Ion batter', 'Ca-Ion batter', 'Ca Ion batter',
                    'Zn-ion batter', 'Zn-Ion batter', 'zinc-ion batter', 'Zn ion batter', 'Zn Ion batter', 'zinc ion batter',
                    'Zn batter', 'Zinc batter', 'solid-state', 'supercapacit', 'capacitor',
                    'Li-S batter', 'Li S batter', 'lithium-sulfur batter', 'lithium sulfur batter',
                    'Na-S batter', 'Na S batter', 'sodium-sulfur batter', 'sodium sulfur batter', 'sulfur batter',
                    'redox flow', 'redox-flow', 'solid state', 'K-ion Batter' , 'K-Ion Batter', 'Potassium-ion Batter' , 'Potassium-Ion Batter' ,
                    'K ion Batter' , 'K Ion Batter' , 'Potassium Ion Batter' , 'K Batter' , 'Potassium Batter' , 'Mg-ion Batter' ,
                    'Mg-Ion Batter', 'Magnesium-ion Batter' , 'Magnesium-Ion Batter' , 'Mg ion Batter' , 'Mg Ion Batter' , 'Magnesium Ion Batter'
                    , 'Mg Batter' , 'Magnesium Batter' , 'Al-ion Batter' , 'Al-Ion Batter', 'Aluminium-ion Batter' , 'Aluminium -Ion Batter' ,
                    'Al ion Batter' , 'Al Ion Batter' , 'Aluminium Ion Batter' , 'Al Batter' , 'Aluminium Batter' , 'Ca-ion Batter' , 'Ca-Ion Batter',
                    'Calcium-ion Batter' , 'Calcium-Ion Batter' , 'Ca ion Batter' , 'Ca Ion Batter' , 'Calcium Ion Batter' , 'Ca Batter' , 'Calcium Batter' ,
                    'Zn-ion Batter' , 'Zn-Ion Batter', 'Zinc-ion Batter' , 'Zinc-Ion Batter' , 'Zn ion Batter' , 'Zn Ion Batter' , 'Zinc Ion Batter' ,
                    'Zn Batter' , 'Zinc Batter' , 'Li-S Batter', 'Li S Batter', 'Lithium-Sulfur Batter', 'Lithium Sulfur Batter', 'Na-S Batter', 'Na S Batter',
                    'Sodium-Sulfur Batter', 'Sodium Sulfur Batter', 'Sulfur Batter', 'Sodium–Air Batter', 'Sodium–Air', ' Sodium Air ', 'Na–Air Batter', 'Na–Air',
                    'Na Air', 'Sodium–O2 Batter', 'Sodium–O2', 'Sodium Air', 'Na–O2 Batter', 'Lithium–Air Batter', 'Lithium–Air', 'Lithium Air', 'Li–Air Batter',
                    'Li–Air', 'Li Air', 'Lithium–O2 Batter', 'Lithium–O2', 'Lithium Air', 'Li–O2 Batter', 'Solid-State', 'Supercapacit', 'Capacitor', 'Redox Flow' , 'Redox-Flow' , 'Solid State']
batteries = [Batteries_lithium_ion, Batteries_sodium_ion]
BATTERIES = [Batteries_plomb, Batteries_Nickel_cadmium, Batteries_Nickel_metal_hydride, Batteries_lithium_Polymer, Batteries_lithium_air, Batteries_Nickel_Fer,
             Batteries_Magnesium_Sulfur, Batteries_others]

Review = ['review']
separator = ['separator', 'membrane']
separator = Capitalize_Liste(separator)
Review = Capitalize_Liste(Review)
for i in range(len(batteries)):
    batteries[i] = Capitalize_Liste(batteries[i])
for i in range(len(BATTERIES)):
    BATTERIES[i] = Capitalize_Liste(BATTERIES[i])

i = 0


def Filtring_Function(files, path):
    """
    :param files: list of all TXTs files
    :param path: Path to save TXT files after filtering
    """
    for file in files:
        text = open(file, 'r', encoding='utf8').read()
        text = Clean_text(text)
        words = text.split()[:350]
        if any(item in words for item in Review):
            pass
        else:
            title, keywords, abstract = Filtring_Classify(file)
            if any(item in title for item in separator):
                pass
            else:
                numbers = []
                Done = False
                for battery in batteries:
                    number = 0
                    for word in battery:
                        num = title.count(word)
                        number = number + num
                    numbers.append(number)
                if max(numbers) > 0:
                    index = max(numbers)
                    liste = [i for i, x in enumerate(numbers) if x == index]
                    for index in liste:
                        name = batteries[index][0]
                        directory = path + '/' + str(name)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        copy_paste_text(file, directory)
                        Done = True
                else:
                    others = False
                    for battery in BATTERIES:
                        if any(item in title for item in battery):
                            others = True
                    if others == False:
                        numbers = []
                        for battery in batteries:
                            number = 0
                            for word in battery:
                                num = keywords.count(word)
                                number = number + num
                            numbers.append(number)
                        if max(numbers) > 0:
                            index = max(numbers)
                            liste = [i for i, x in enumerate(numbers) if x == index]
                            for index in liste:
                                name = batteries[index][0]
                                directory = path + '/' + str(name)
                                if not os.path.exists(directory):
                                    os.makedirs(directory)
                                copy_paste_text(file, directory)
                                Done = True
                        else:
                            for battery in BATTERIES:
                                if any(item in keywords for item in battery):
                                    others = True
                            if others == False:
                                numbers = []
                                for battery in batteries:
                                    number = 0
                                    for word in battery:
                                        num = abstract.count(word)
                                        number = number + num
                                    numbers.append(number)
                                if max(numbers) > 0:
                                    index = max(numbers)
                                    liste = [i for i, x in enumerate(numbers) if x == index]
                                    for index in liste:
                                        name = batteries[index][0]
                                        directory = path + '/' + str(name)
                                        if not os.path.exists(directory):
                                            os.makedirs(directory)
                                        copy_paste_text(file, directory)
                                        Done = True
                                else:
                                    for battery in BATTERIES:
                                        if any(item in abstract for item in battery):
                                            others = True
                                    if others == True:
                                        name = 'Not_Lithium_Not_Sodium'
                                        directory = path + '/' + str(name)
                                        if not os.path.exists(directory):
                                            os.makedirs(directory)
                                        copy_paste_text(file, directory)
                                        Done = None
                            else:
                                name = 'Not_Lithium_Not_Sodium'
                                directory = path + '/' + str(name)
                                if not os.path.exists(directory):
                                    os.makedirs(directory)
                                copy_paste_text(file, directory)
                                Done = None
                    else:
                        name = 'Not_Lithium_Not_Sodium'
                        directory = path + '/' + str(name)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        copy_paste_text(file, directory)
                        Done = None

                if Done == False:
                    text = open(file, 'r', encoding='utf8').read()
                    text = Clean_text(text)
                    title = text.replace('\n', ' ')
                    numbers = []
                    for battery in batteries:
                        number = 0
                        for word in battery:
                            num = title.count(word)
                            number = number + num
                        numbers.append(number)
                    try:
                        maximum = max(numbers)
                        if maximum != 0:
                            liste = [i for i, x in enumerate(numbers) if x == maximum]
                            for index in liste:
                                name = batteries[index][0]
                                directory = path + '/' + str(name)
                                if not os.path.exists(directory):
                                    os.makedirs(directory)
                                copy_paste_text(file, directory)
                        else:
                            others = False
                            for battery in BATTERIES:
                                if any(item in title for item in battery):
                                    others = True
                            if others == False:
                                name = 'Not_Lithium_Not_Sodium'
                                directory = path + '/' + str(name)
                                if not os.path.exists(directory):
                                    os.makedirs(directory)
                                copy_paste_text(file, directory)
                            else:
                                name = 'Not_Lithium_Not_Sodium'
                                directory = path + '/' + str(name)
                                if not os.path.exists(directory):
                                    os.makedirs(directory)
                                copy_paste_text(file, directory)
                    except:
                        name = 'Not_Lithium_Not_Sodium'
                        directory = path + '/' + str(name)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        copy_paste_text(file, directory)
    #print('Filtred function is done')


