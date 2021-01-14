#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ['Converting_Function']

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LTPage, LTChar, LTAnno, LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator, TextConverter
import pdfminer
import io
from tika import parser
import os
from bs4 import BeautifulSoup
import numpy as np

laparams = pdfminer.layout.LAParams()
setattr(laparams, 'all_texts', True)


def convert_pdf_to_txt(path, pages):
    """
    :param path: path to the PDF file
    :param pages: the page of interest
    :return:
    """
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, converter)
    fp = open(path, 'rb')
    password = ""
    maxpages = 0
    caching = True
    pagenos=set(pages)
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = fake_file_handle.getvalue()
    fp.close()
    converter.close()
    fake_file_handle.close()
    return text


class PDFPageDetailedAggregator(PDFPageAggregator):
    """
    function from: https://stackoverflow.com/questions/15737806/extract-text-using-pdfminer-and-pypdf2-merges-columns?answertab=votes#tab-top
    """
    def __init__(self, rsrcmgr, pageno=1, laparams=None):
        PDFPageAggregator.__init__(self, rsrcmgr, pageno=pageno, laparams=laparams)
        self.rows = []
        self.page_number = 0
    def receive_layout(self, ltpage):
        def render(item, page_number):
            if isinstance(item, LTPage) or isinstance(item, LTTextBox):
                for child in item:
                    render(child, page_number)
            elif isinstance(item, LTTextLine):
                child_str = ''
                for child in item:
                    if isinstance(child, (LTChar, LTAnno)):
                        child_str += child.get_text()
                child_str = ' '.join(child_str.split()).strip()
                if child_str:
                    row = (page_number, item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3], child_str)
                    self.rows.append(row)
                for child in item:
                    render(child, page_number)
            return
        render(ltpage, self.page_number)
        self.page_number += 1
        self.rows = sorted(self.rows, key = lambda x: (x[0], -x[2]))
        self.result = ltpage


def get_text_from_XML_without_saving(path):
    """
    :param path: path to the XML file
    :return: Text extracted  from the path
    """
    tree = open(path, 'r', encoding='utf8')
    soup = BeautifulSoup(tree)
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def most_common(lst):
    """
    :param lst: list of value
    :return: :return: the most common value in the list
    """
    return max(set(lst), key=lst.count)


def average_len(l):
  return sum(map(len, l))/float(len(l))


def Converting_Function(Path_To_TXTs, new_file):
    """
    :param Path_To_TXTs: path to PDFs or/and XML files
    :param new_file: the path to save the TXT format
    """
    files_short = np.array([f for f in os.listdir(Path_To_TXTs) if os.path.isfile(os.path.join(Path_To_TXTs, f))])
    files = np.array([Path_To_TXTs + '/' + f for f in files_short])
    for file in files:
        if file.endswith('.pdf'):
            Not_Good = False
            Prob = False
            try:
                fp = open(file, 'rb')
                parser_pdf = PDFParser(fp)
                doc = PDFDocument(parser_pdf)
                rsrcmgr = PDFResourceManager()
                laparams = LAParams()
                device = PDFPageDetailedAggregator(rsrcmgr, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.create_pages(doc):
                    interpreter.process_page(page)
                    device.get_result()
                rows = device.rows
                lines = [item[5] for item in rows]
                if average_len(lines) >= 20:
                    try:
                        text_all = convert_pdf_to_txt(file, pages=[0])
                        rows_pages = [item for item in rows if item[0] != 0]
                        words = [item[1] for item in rows_pages]
                        words_1 = [item for item in words if item <= 200]
                        words_2 = [item for item in words if item > 200]
                        first = most_common(words_1)
                        second = most_common(words_2)
                        pages = [item[0] for item in rows_pages]
                        pages = list(set(pages))
                        pages.sort()
                        for page in pages:
                            page_lines = [line for line in rows_pages if line[0] == page]
                            text1 = ''
                            text2 = ''
                            text_middle = ''
                            for item in page_lines:
                                if item[1] <= (first + 20) and not (item[5].isdigit() and not item[5].endswith('.')):
                                    text1 = text1 + '\n' + item[5]
                                elif item[1] >= (second - 20) and item[1] <= 500 and not (
                                        item[5].isdigit() and not item[5].endswith('.')):
                                    text2 = text2 + '\n' + item[5]
                                else:
                                    if not (item[5].isdigit() and not item[5].endswith('.')):
                                        text_middle = text_middle + '\n' + item[5]
                            if len(text1 + text2) > len(text_middle):
                                text_all = text_all + text1 + text_middle + text2
                            else:
                                Not_Good = True
                        if len(text_all) >= 1500 and Not_Good == False:
                            text_all = text_all.replace(' ac.', '~').replace(' a.c.', '~').replace(' a.c', '~')
                            name = file.split('/')[-1][:-4]
                            path = new_file + '/' + name + '.txt'
                            with open(path, 'w', encoding='utf8') as f:
                                f.write(text_all)
                                f.close()
                            #print('Article ', name, ' is successfully converted')
                        elif len(text_all) >= 1500 and Not_Good == True:
                            rawText = parser.from_file(file)
                            text = rawText['content']
                            text = os.linesep.join([s for s in text.splitlines() if s])
                            text_all = text.replace(' ac.', '~').replace(' a.c.', '~').replace(' a.c', '~')
                            text_all = " ".join(text_all.split())
                            name = file.split('/')[-1][:-4]
                            path = new_file + '/' + name + '.txt'
                            with open(path, 'w', encoding='utf8') as f:
                                f.write(text_all)
                                f.close()
                            #print('Article ', name, ' is successfully converted')
                        else:
                            raw = parser.from_file(file)
                            text_all = raw['content']
                            text_all = "\n".join([ll.rstrip() for ll in text_all.splitlines() if ll.strip()])
                            if len(text_all) >= 1500:
                                text_all = text_all.replace(' ac.', '~').replace(' a.c.', '~').replace(' a.c', '~')
                                name = file.split('/')[-1][:-4]
                                path = new_file + '/' + name + '.txt'
                                with open(path, 'w', encoding='utf8') as f:
                                    f.write(text_all)
                                    f.close()
                                #print('Article ', name, ' is successfully converted')
                            else:
                                pass
                                #print('The PDF "' + file + '" contain less than 1500 characters !!!')
                    except:
                        Prob = True
                elif average_len(lines) < 20 or Prob == True:
                    raw = parser.from_file(file)
                    text_all = raw['content']
                    text_all = "\n".join([ll.rstrip() for ll in text_all.splitlines() if ll.strip()])
                    if len(text_all) >= 1500:
                        text_all = text_all.replace(' ac.', '~').replace(' a.c.', '~').replace(' a.c', '~')
                        name = file.split('/')[-1][:-4]
                        path = new_file + '/' + name + '.txt'
                        with open(path, 'w', encoding='utf8') as f:
                            f.write(text_all)
                            f.close()
                        #print('Article ', name, ' is successfully converted')
                    else:
                        pass
                        #print('The PDF "' + file + '" contain less than 1500 characters !!!')
            except:
                Prob = True
            if Prob == True:
                raw = parser.from_file(file)
                text_all = raw['content']
                text_all = "\n".join([ll.rstrip() for ll in text_all.splitlines() if ll.strip()])
                if len(text_all) >= 1500:
                    text_all = text_all.replace(' ac.', '~').replace(' a.c.', '~').replace(' a.c', '~')
                    name = file.split('/')[-1][:-4]
                    path = new_file + '/' + name + '.txt'
                    with open(path, 'w', encoding='utf8') as f:
                        f.write(text_all)
                        f.close()
                    #print('Article ', name, ' is successfully converted')
                else:
                    pass
                    #print('The PDF "' + file + '" contain less than 1500 characters !!!')
        elif file.endswith('.xml'):
            text_all = get_text_from_XML_without_saving(file)
            text_all = text_all.split('competing financial interest')[0]
            text_all = text_all.replace(' ac.', '~').replace(' a.c.', '~').replace(' a.c', '~')
            name = file.split('/')[-1][:-4]
            path = new_file + '/' + name + '.txt'
            with open(path, 'w', encoding='utf8') as f:
                f.write(text_all)
                f.close()
            #print('Article ', name, ' is successfully converted')



