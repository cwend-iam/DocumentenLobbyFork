"""
This script is the general place for the setup of the modules used for changing the document properties.
This functions defined here are imported and used in a module.
"""
import os

import openpyxl
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import NameObject, createStringObject
from docx import Document


def change_docx_properties(filename, title=None, subject=None, keywords=None, category=None, comments=None):
    """

    :param filename:
    :param title:
    :param subject:
    :param keywords:
    :param category:
    :param comments:
    :return:
    """
    # Creating an instance of Document
    _doc = Document(docx=filename)

    # Isolating the properties of the document
    document_properties = _doc.core_properties

    # Assigning/rewriting properties of the document if given as an argument
    document_properties.title = document_properties.title if title is None else title
    document_properties.subject = document_properties.subject if subject is None else subject
    document_properties.keywords = document_properties.keywords if keywords is None else keywords
    document_properties.category = document_properties.category if category is None else category
    document_properties.comments = document_properties.comments if comments is None else comments

    # Saving the document and it's properties
    _doc.save(filename)


def change_xlsx_properties(filename, title=None, subject=None, keywords=None, category=None, comments=None):
    """

    :param filename:
    :param title:
    :param subject:
    :param keywords:
    :param category:
    :param comments:
    :return:
    """
    # Creating an instance of Document
    _doc = openpyxl.load_workbook(filename=filename)

    # Isolating the properties of the document
    document_properties = _doc.properties

    # Assigning/rewriting properties of the document if given as an argument
    document_properties.title = document_properties.title if title is None else title
    document_properties.subject = document_properties.subject if subject is None else subject
    document_properties.keywords = document_properties.keywords if keywords is None else keywords
    document_properties.category = document_properties.category if category is None else category
    document_properties.comments = document_properties.comments if comments is None else comments

    # Saving the document and it's properties
    _doc.save(filename=filename)


def change_pdf_properties(filename, title=None, subject=None, keywords=None, category=None, comments=None):
    """

    :param filename:
    :param title:
    :param subject:
    :param keywords:
    :param category:
    :param comments:
    :return:
    """
    # Opening and reading the file
    _file = open(file=filename, mode='rb')
    pdf_in = PdfFileReader(_file)

    # Extracting the document properties
    document_properties = pdf_in.documentInfo

    # Setting up the pdf writer object
    writer = PdfFileWriter()

    # Copying the pages from pdf_in to the writer
    for page in range(pdf_in.getNumPages()):
        writer.addPage(pdf_in.getPage(pageNumber=page))

    # Isolating a protected member of the writer (_info) with the property information of the document
    propertyDict = writer._info.getObject()

    # Copying the existing properties from pdf_in to to the writer
    for key in document_properties:
        propertyDict.update({NameObject(key): createStringObject(document_properties[key])})

    # Assigning/rewriting properties to the writer if given as an argument
    None if title is None else propertyDict.update({NameObject('/Title'): createStringObject(title)})
    None if subject is None else propertyDict.update({NameObject('/Subject'): createStringObject(subject)})
    None if keywords is None else propertyDict.update({NameObject('/Keywords'): createStringObject(keywords)})
    None if category is None else propertyDict.update({NameObject('/Category'): createStringObject(category)})
    None if comments is None else propertyDict.Update({NameObject('/Comments'): createStringObject(comments)})

    # Defining the name of the output file and opening the output file
    output_filename = f'output_{filename}'
    pdf_out = open(file=output_filename, mode='wb')

    # Writing writer content to pdf_out
    writer.write(pdf_out)

    # Closing both _file and pdf_out
    _file.close()
    pdf_out.close()

    # Deleting the original file and renaming the new pdf file to give it the name of the orignal file
    os.unlink(filename)
    os.rename(output_filename, filename)
