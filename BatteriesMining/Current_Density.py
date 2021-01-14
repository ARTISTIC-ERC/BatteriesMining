#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import numpy as np
import itertools

__all__ = ['get_Crate', 'indices_Crate']


def texttowords(text):
    """
    :param text: text of interest
    :return: list of words after splitting the text
    """
    liste = ['@', '#', '©', '␣', '', '$']
    final_text = ''.join(e for e in text if e not in liste)
    final_text = re.sub('\u242em', 'μm', final_text)
    final_text = re.sub('−', '-', final_text)
    words = final_text.split()
    return words


def Unit_Num(s):
    for i, c in enumerate(s):
        if not c.isdigit() and c != '.':
            break
    numero = s[:i]
    unit = s[i:]
    return unit, numero


def indices_Crate(text):
    """
    :param text: the text of interest
    :return: the index of current densities that has been mentioned in text
    """
    text = text.replace('-', '-')
    text = text.replace('−', '-')
    text = text.replace('-', '-')
    words = texttowords(text)
    cmA_indices = [i for i, s in enumerate(words) if 'mA' in s]
    cmah__g_indices = [i for i, s in enumerate(words) if 'mA/g' in s]
    cmahg_indices = [i for i, s in enumerate(words) if ('mAg-1' in s or 'mAg1' in s)]
    cmah_g__indices = [i for i, s in enumerate(words) if 'mA.g-1' in s]
    cmah_g__1indices = [i for i, s in enumerate(words) if 'Ag-1' in s]
    cmah_g__2indices = [i for i, s in enumerate(words) if 'A.g-1' in s]
    cmah_g__3indices = [i for i, s in enumerate(words) if 'A/g' in s]
    cmah_g__4indices = [i for i, s in enumerate(words) if 'A/kg' in s]
    cmah_g__5indices = [i for i, s in enumerate(words) if 'A.kg-1' in s]
    cmah_cm__4indices = [i for i, s in enumerate(words) if 'mA/cm2' in s]
    cmah_cm__5indices = [i for i, s in enumerate(words) if 'mA.cm2' in s]
    cmah_cm__6indices = [i for i, s in enumerate(words) if 'mA.cm-2' in s]
    cmah_cm__5indices = cmah_cm__5indices + cmah_cm__6indices
    cmah_g__6indices = [i for i, s in enumerate(words) if 'Akg-1' in s]
    cm_indices = [i for i, s in enumerate(words) if 'm' in s]
    cA_indices = [i for i, s in enumerate(words) if 'A' in s]

    cmA_h_g_1 = []
    cmah___g_indices = []
    cmA_h_g = []
    cmA_hg_1 = []
    cmA_h1_g1 = []

    for i in cmA_indices:
        words_yes = ['' for _ in range(len(words))]
        w = i - 5
        while w <= i + 5:
            try:
                words_yes[w] = words[w].replace('(', '').replace(')', '').replace(',', '').replace(';', '')
                if words_yes[w] == '.' or words_yes[w] == '/':
                    words_yes[w] = words_yes[w][:-1]
            except:
                pass
            w += 1
        if words_yes[i].endswith('mA'):
            try:
                if words_yes[i + 1].endswith('g-1'):
                    cmA_h_g_1.append(i)
            except:
                pass
            try:
                if words_yes[i + 1] == '/g':
                    cmah___g_indices.append(i)
            except:
                pass
            try:
                if words_yes[i + 1] == 'g':
                    cmA_h_g.append(i)
            except:
                pass
            try:
                if words_yes[i + 1] == 'g1':
                    cmA_h1_g1.append(i)
            except:
                pass
            try:
                if words_yes[i + 1] == 'g' and words_yes[i + 2] == '1':
                    cmA_hg_1.append(i)
            except:
                pass
    c_rate_indices6 = []
    for i in cm_indices:
        words_yes = ['' for _ in range(len(words))]
        w = i - 5
        while w <= i + 5:
            try:
                words_yes[w] = words[w].replace('(', '').replace(')', '').replace(',', '').replace(';', '')
                if words_yes[w].endswith('.') or words_yes[w].endswith('/'):
                    words_yes[w] = words_yes[w][:-1]
            except:
                pass
            w += 1
        if words_yes[i].endswith('m'):
            try:
                if words_yes[i + 1] == 'A' and (
                    words_yes[i + 2] == 'g' or words_yes[i + 2] == 'g-1' or words_yes[i + 2] == 'g-' or words_yes[i + 2] == 'g1' or
                    words_yes[i + 2] == '/g' or (words_yes[i + 2] == '/' and (words_yes[i + 3] == 'g' or words_yes[i + 3] == 'g1')) or (
                            words_yes[i + 2] == '.' and
                            (words_yes[i + 3] == 'g' or words_yes[i + 3] == 'g1' or words_yes[i + 3] == 'g-1'))):
                    c_rate_indices6.append(i)
            except:
                pass

    c_rate_indices7 = []
    c_rate_indices77 = []
    for i in cA_indices:
        words_yes = ['' for _ in range(len(words))]
        w = i - 5
        while w <= i + 5:
            try:
                words_yes[w] = words[w].replace('(', '').replace(')', '').replace(',', '').replace(';', '')
                if words_yes[w].endswith('.') or words_yes[w].endswith('/'):
                    words_yes[w] = words_yes[w][:-1]
            except:
                pass
            w += 1
        if words_yes[i].endswith('A'):
            try:
                if words_yes[i + 1] == 'kg' or words_yes[i + 1] == 'kg-1' or words_yes[i + 1] == 'kg-' or words_yes[i + 1] == 'kg1' or \
                    words_yes[i + 1] == '/kg' or (
                    words_yes[i + 1] == '/' and (words_yes[i + 1] == 'kg' or words_yes[i + 2] == 'kg1')) or (words_yes[i + 2] == '.' and (words_yes[i + 2] == 'kg' or words_yes[i + 2] == 'kg1' or words_yes[i + 2] == 'kg-1')):
                    c_rate_indices7.append(i)
            except:
                pass
            try:
                if words_yes[i + 1] == 'g' or words_yes[i + 1] == 'g-1' or words_yes[i + 1] == 'g-' or words_yes[i + 1] == 'g1' or \
                        words_yes[i + 1] == '/g' or (words_yes[i + 1] == '/' and (words_yes[i + 1] == 'g' or words_yes[i + 2] == 'g1')) or (words_yes[i + 2] == '.' and (words_yes[i + 2] == 'g' or
                        words_yes[i + 2] == 'g1' or words_yes[i + 2] == 'g-1')):
                    c_rate_indices77.append(i)
            except:
                pass

    indices_Crate_mg = np.append(cmah__g_indices, cmahg_indices).astype(int)
    indices_Crate_Akg = np.append(cmah_g__4indices, cmah_g__5indices).astype(int)
    indices_Crate_Ag = np.append(cmah_g__1indices, cmah_g__2indices).astype(int)
    indices_Crate_cm = np.append(cmah_cm__4indices, cmah_cm__5indices)

    indices_Crate_Ag = np.append(indices_Crate_Ag, cmah_g__3indices).astype(int)
    LL_C_mg = [cmah_g__indices, cmA_h_g_1, cmah___g_indices, cmA_h_g, cmA_h1_g1, cmA_hg_1, c_rate_indices6]
    LL_Akg = [cmah_g__6indices, c_rate_indices7, c_rate_indices77]
    for l in LL_C_mg:
        indices_Crate_mg = np.append(indices_Crate_mg, l).astype(int)
    for l in LL_Akg:
        indices_Crate_Akg = np.append(indices_Crate_Akg, l).astype(int)

    indices_Crate_C = np.append(indices_Crate_Ag, indices_Crate_mg).astype(int)
    indices_Crate_C = np.append(indices_Crate_C, indices_Crate_Akg).astype(int)
    indices_Crate_C = np.append(indices_Crate_C, indices_Crate_cm).astype(int)

    return [indices_Crate_C, indices_Crate_mg, indices_Crate_Akg, indices_Crate_Ag, c_rate_indices77, indices_Crate_cm]


def get_Crate(indices_Crate_C, indices_Crate_mg, indices_Crate_Akg, indices_Crate_Ag, c_rate_indices77, indices_Crate_cm, text):
    """
    :param indices_Crate_C: all index of current densities that has been mentioned in text
    :param indices_Crate_mg: all index of current densities that has been mentioned in text using the unit = 'mA/g'
    :param indices_Crate_Akg: all index of current densities that has been mentioned in text using the unit = 'A/kg'
    :param indices_Crate_Ag: all index of current densities that has been mentioned in text using the unit = 'A/g'
    :param c_rate_indices77: all index of current densities that has been mentioned in text using the unit = 'A g-1'
    :param indices_Crate_cm: all index of current densities that has been mentioned in text using the unit = 'mA/cm2'
    :param text: text of interest
    :return: current density and c_rate are reported in the text if yes
    """
    text = text.replace('-', '-')
    text = text.replace('−', '-')
    text = text.replace('-', '-')
    words = texttowords(text)
    T_replace = [',', ';', '.', '(', ')', '[', ']', '{', '}', '/']

    C_rate = []
    for elem in words:
        if elem[0].isdigit() and ('C' in elem) and ('' not in elem) and ('°' not in elem) and ('◦' not in elem):
            if (elem[-1:].isalpha() and ('°' not in elem) and (
                    (elem.endswith('C') and elem[-2:].isdigit()) or elem.endswith('rate') or elem.endswith(
                'Rate') or elem.endswith('discharge') or
                    elem.endswith('capacity') or elem.endswith('Capacity'))) or (
                    (elem[-1:] == ',' or elem[-1:] == ';' or elem[-1:] == '.') and elem[-2] == 'C') \
                    and len(elem) <= 10:
                C_rate.append([elem, words.index(elem)])

        if elem.startswith('C/') and elem.replace('.', '').replace(',', '')[-1:].isdigit():
            nums = list(map(int, ''.join([x if x.isdigit() else ' ' for x in elem.replace('.|≈|=|∼', '')]).split()))
            if len(nums) == 1:
                try:
                    C_rate.append([str(round(1 / nums[0], 2)) + 'C', words.index(elem)])
                except:
                    pass

    c_rate_list = ['C-rate', 'c-rate', 'C-discharge', 'c-discharge', 'C-capacity', 'c-capacity', 'C-Rate', 'c-Rate', 'C-rate.', 'C-rate,'
                   'C-Discharge', 'c-Discharge', 'C-Capacity', 'c-Capacity']
    c_rate_indices = [i for i, s in enumerate(words) if any(elem in s for elem in c_rate_list)]
    C = [i for i, s in enumerate(words) if 'C' in s]

    for i in indices_Crate_C:
        words_yes = ['' for x in range(len(words))]
        w = i - 3
        while w <= i + 3:
            try:
                words_yes[w] = words[w].replace('(', '').replace(')', '').replace(',', '').replace(';', '')
                if words_yes[w].endswith('.') or words_yes[w].endswith('/'):
                    words_yes[w] = words_yes[w][:-1]
            except:
                pass
            w += 1
        if i in indices_Crate_cm:
            if 'e' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('e')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'mA/cm2', i])

            if '-' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('-')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'mA/cm2', i])

            if ('.' in words_yes[i - 1]) and ('e' not in words_yes[i - 1]) and ('-' not in words_yes[i - 1]):
                if words_yes[i - 1].replace('.', '').isdigit():
                    C_rate.append([str(words_yes[i - 1]) + 'mA/cm2', i])
            if list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])) != []:
                for W_Ratio in list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])):
                    C_rate.append([str(W_Ratio) + 'mA/cm2', i])
            val = 0
            try:
                if i > 0 and words_yes[i - 1].replace('.', '', 1).isdigit():
                    val = float(words_yes[i - 1])
                    if i > 1 and len(words_yes[i - 1]) == 3:
                        if words_yes[i - 2].replace('.', '', 1).isdigit():
                            if ((words_yes[i - 2] + words_yes[i - 1]) in text) or ((words_yes[i - 2] + ' ' + words_yes[i - 1]) in text) or ((words_yes[i - 2] + ',' + words_yes[i - 1]) in text):
                                val = float(words_yes[i - 2]) * 1000 + val

                if val > 0:
                    C_rate.append([str(val) + 'mA/cm2', i])
            except:
                pass

        indices_Crate_Akg = [i for i in indices_Crate_Akg if i not in indices_Crate_cm]
        if i in indices_Crate_mg:
            if 'e' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('e')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'mA/g', i])

            if '-' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('-')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'mA/g', i])

            if ('.' in words_yes[i - 1]) and ('e' not in words_yes[i - 1]) and ('-' not in words_yes[i - 1]):
                if words_yes[i - 1].replace('.', '').isdigit():
                    C_rate.append([str(words_yes[i - 1]) + 'mA/g', i])
            if list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])) != []:
                for W_Ratio in list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])):
                    C_rate.append([str(W_Ratio) + 'mA/g', i])
            val = 0
            try:
                if i > 0 and words_yes[i - 1].replace('.', '', 1).isdigit():
                    val = float(words_yes[i - 1])
                    if i > 1 and len(words_yes[i - 1]) == 3:
                        if words_yes[i - 2].replace('.', '', 1).isdigit():
                            if ((words_yes[i - 2] + words_yes[i - 1]) in text) or ((words_yes[i - 2] + ' ' + words_yes[i - 1]) in text) or ((words_yes[i - 2] + ',' + words_yes[i - 1]) in text):
                                val = float(words_yes[i - 2]) * 1000 + val

                if val > 0:
                    C_rate.append([str(val) + 'mA/g', i])
            except:
                pass
        indices_Crate_Akg = [i for i in indices_Crate_Akg if i not in indices_Crate_mg]
        if (i in indices_Crate_Akg) and (i not in c_rate_indices77):
            if 'e' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('e')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'A/kg', i])

            if '-' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('-')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'A/kg', i])

            if ('.' in words_yes[i - 1]) and ('e' not in words_yes[i - 1]) and ('-' not in words_yes[i - 1]):
                if words_yes[i - 1].replace('.', '').isdigit():
                    C_rate.append([str(words_yes[i - 1]) + 'A/kg', i])
            if list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])) != []:
                for W_Ratio in list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])):
                    C_rate.append([str(W_Ratio) + 'A/Kg', i])
            val = 0
            try:
                if i > 0 and words_yes[i - 1].replace('.', '', 1).isdigit():
                    val = float(words_yes[i - 1])
                    if i > 1 and len(words_yes[i - 1]) == 3:
                        if words_yes[i - 2].replace('.', '', 1).isdigit():
                            if ((words_yes[i - 2] + words_yes[i - 1]) in text) or (
                                    (words_yes[i - 2] + ' ' + words_yes[i - 1]) in text) or (
                                    (words_yes[i - 2] + ',' + words_yes[i - 1]) in text):
                                val = float(words_yes[i - 2]) * 1000 + val

                if val > 0:
                    C_rate.append([str(val) + 'A/kg', i])
            except:
                pass
        if i in c_rate_indices77:
            if 'e' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('e')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'A/g', i])

            if '-' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('-')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'A/g', i])

            if ('.' in words_yes[i - 1]) and ('e' not in words_yes[i - 1]) and ('-' not in words_yes[i - 1]):
                if words_yes[i - 1].replace('.', '').isdigit():
                    C_rate.append([str(words_yes[i - 1]) + 'A/g', i])
            if list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])) != []:
                for W_Ratio in list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])):
                    C_rate.append([str(W_Ratio) + 'A/g', i])
            val = 0
            try:
                if i > 0 and words_yes[i - 1].replace('.', '', 1).isdigit():
                    val = float(words_yes[i - 1])
                    if i > 1 and len(words_yes[i - 1]) == 3:
                        if words_yes[i - 2].replace('.', '', 1).isdigit():
                            if ((words_yes[i - 2] + words_yes[i - 1]) in text) or ((words_yes[i - 2] + ' ' + words_yes[i - 1]) in text) or ((words_yes[i - 2] + ',' + words_yes[i - 1]) in text):
                                val = float(words_yes[i - 2]) * 1000 + val

                if val > 0:
                    C_rate.append([str(val) + 'A/g', i])
            except:
                pass

        indices_Crate_Ag = [i for i in indices_Crate_Ag if i not in indices_Crate_Akg]
        indices_Crate_Ag = [i for i in indices_Crate_Ag if i not in indices_Crate_mg]
        if i in indices_Crate_Ag:
            if 'e' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('e')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'A/g', i])

            if '-' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('-')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        C_rate.append([str(item) + 'A/g', i])

            if ('.' in words_yes[i - 1]) and ('e' not in words_yes[i - 1]) and ('-' not in words_yes[i - 1]):
                if words_yes[i - 1].replace('.', '').isdigit():
                    C_rate.append([str(words_yes[i - 1]) + 'A/g', i])

            if list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])) != []:
                for W_Ratio in list(re.findall(r"[-+]?\d*\.\d+|\d+", Multipl_Replace(words[i], T_replace, '')[:-1])):
                    C_rate.append([str(W_Ratio) + 'A/g', i])
            val = 0
            try:
                if i > 0 and words_yes[i - 1].replace('.', '', 1).isdigit():
                    val = float(words_yes[i - 1])
                    if i > 1 and len(words_yes[i - 1]) == 3:
                        if words_yes[i - 2].replace('.', '', 1).isdigit():
                            if ((words_yes[i - 2] + words_yes[i - 1]) in text) or (
                                    (words_yes[i - 2] + ' ' + words_yes[i - 1]) in text) or (
                                    (words_yes[i - 2] + ',' + words_yes[i - 1]) in text):
                                val = float(words_yes[i - 2]) * 1000 + val

                if val > 0:
                    C_rate.append([str(val) + 'A/g', i])
            except:
                pass

    CC = ['C', 'C-rate', 'c-rate', 'C-discharge', 'c-discharge', 'C-capacity', 'c-capacity', 'C-Rate', 'c-Rate',
                   'C-Discharge', 'c-Discharge', 'C-Capacity', 'c-Capacity']
    for i in C:
        done = 0
        words_yes = ['' for _ in range(len(words))]
        w = i - 2
        while w <= i + 2:
            try:
                words_yes[w] = words[w].replace('(', '').replace(')', '').replace(',', '').replace(';', '')
                if words_yes[w].endswith('.') or words_yes[w].endswith('/'):
                    words_yes[w] = words_yes[w][:-1]
            except:
                pass
            w += 1
        unit, num = Unit_Num(words_yes[i])
        if any(x == unit for x in CC):
            try:
                num = float(num)

                if i not in [item[1] for item in C_rate]:
                    C_rate.append([str(num) + 'C', i])
                    done = 1
            except:
                if num.isdigit():
                    if i not in [item[1] for item in C_rate]:
                        C_rate.append([str(num) + 'C', i])
                        done = 1

        if (words_yes[i] == 'C' or words_yes[i] == 'C.' or words_yes[i] == 'C,') and done != 1:
            if 'e' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('e')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        if i not in [item[1] for item in C_rate]:
                            C_rate.append([str(item) + 'C', i])

            if '-' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('-')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        if i not in [item[1] for item in C_rate]:
                            C_rate.append([str(item) + 'C', i])

            if ('.' in words_yes[i - 1]) and ('e' not in words_yes[i - 1]) and ('-' not in words_yes[i - 1]):
                if words_yes[i - 1].replace('.', '').isdigit():
                    if i not in [item[1] for item in C_rate]:
                        C_rate.append([str(words_yes[i - 1]) + 'C', i])
            if words_yes[i - 1].isdigit():
                if i not in [item[1] for item in C_rate]:
                    C_rate.append([str(words_yes[i - 1]) + 'C', i])

    for i in c_rate_indices:
        words_yes = ['' for _ in range(len(words))]
        w = i - 2
        while w <= i + 2:
            try:
                words_yes[w] = words[w].replace('(', '').replace(')', '').replace(',', '').replace(';', '')
                if words_yes[w].endswith('.') or words_yes[w].endswith('/'):
                    words_yes[w] = words_yes[w][:-1]
            except:
                pass
            w += 1
        if words_yes[i][0].isdigit():
            unit, number = Unit_Num(words_yes[i])
            if i not in [item[1] for item in C_rate]:
                C_rate.append([str(number) + 'C', i])
        if 'e' in words_yes[i - 1]:
            words_min = words_yes[i - 1].split('e')
            for item in words_min:
                if item.replace('.', '').isdigit():
                    if i not in [item[1] for item in C_rate]:
                        C_rate.append([str(item) + 'C', i])

        if '-' in words_yes[i - 1]:
            words_min = words_yes[i - 1].split('-')
            for item in words_min:
                if item.replace('.', '').isdigit():
                    if i not in [item[1] for item in C_rate]:
                        C_rate.append([str(item) + 'C', i])

        if ('.' in words_yes[i - 1]) and ('e' not in words_yes[i - 1]) and ('-' not in words_yes[i - 1]):
            if words_yes[i - 1].replace('.', '').isdigit():
                if i not in [item[1] for item in C_rate]:
                    C_rate.append([str(words_yes[i - 1]) + 'C', i])
        if words_yes[i - 1].isdigit():
            if i not in [item[1] for item in C_rate]:
                C_rate.append([str(words_yes[i - 1]) + 'C', i])
    if len(c_rate_indices) != 0:
        words_yes = ['' for _ in range(len(words))]
        for i in c_rate_indices:
            w = i - 2
            while w <= i + 2:
                try:
                    words_yes[w] = words[w].replace('(', '').replace(')', '').replace(',', '').replace(';', '').replace('/', '')
                    if words_yes[w].endswith('.'):
                        words_yes[w] = words_yes[w][:-1]
                except:
                    pass
                w += 1
            if 'e' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('e')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        if i not in [item[1] for item in C_rate]:
                            C_rate.append([str(item) + 'C', i])

            if '-' in words_yes[i - 1]:
                words_min = words_yes[i - 1].split('-')
                for item in words_min:
                    if item.replace('.', '').isdigit():
                        if i not in [item[1] for item in C_rate]:
                            C_rate.append([str(item) + 'C', i])

            if ('.' in words_yes[i - 1]) and ('e' not in words_yes[i - 1]) and ('-' not in words_yes[i - 1]):
                if words_yes[i - 1].replace('.', '').isdigit():
                    if i not in [item[1] for item in C_rate]:
                        C_rate.append([str(words_yes[i - 1]) + 'C', i])

    if len(C_rate) != 0:
        for j in range(len(C_rate)):
            if C_rate[j][0].endswith('.') or C_rate[j][0].endswith(';') or C_rate[j][0].endswith(','):
                C_rate[j][0] = C_rate[j][0][:-1]
    C_rate.sort()
    C_rate = list(C_rate for C_rate, _ in itertools.groupby(C_rate))
    C_rate.sort()
    C_rate = list(C_rate for C_rate, _ in itertools.groupby(C_rate))
    return C_rate


def Multipl_Replace(text, T_replace, new_replace):
    """
    :param text: text of interest
    :param T_replace: list of element that needed to be replaced in the text
    :param new_replace: list of element that we needed to be replaced by.
    :return: text after replacing
    """
    for item in T_replace:
        if item in text:
            text = text.replace(item, new_replace)
    return text

