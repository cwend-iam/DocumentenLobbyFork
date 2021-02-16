from datetime import date

from bestand_locaties import *

toelichting_main = "Dit tabblad bevat een overzicht van de documenten van projecten die vallen onder het beheer van " \
                   "Croonwolter&dros Infra Asset Management (IAM)."
toelichting_projecten = "Dit tabblad bevat een overzicht van de projecten waarvan documenten aanwezig zijn in de " \
                        "Documenten Lobby van het tabblad 'Main'."
toelichting_sbs = "Dit tabblad bevat de generieke SBS die wordt gehanteerd door IAM. De deelinstallatie namen en" \
                  "nummers uit het tabblad 'Main' zijn hier allemaal terug te vinden"
toelichting_doc_type = "Dit tabblad bevat een overzicht van de vershcillende document klassen en type die zijn/worden" \
                       " toegevoegd aan de Documenten Lobby."
toelichting_status = "Dit tabblad bevat een overzicht van de verschillende status aanduidingen die worden gehanteerd " \
                     "in de Documenten Lobby"
toelichting_personen = "Dit tabblad bevat een overzicht van het team van IAM. Zij die zijn aangewezen als eigenaar" \
                       " van documenten zijn onderdeel van IAM."


# AutoFit voor de breedte van de kolommen # todo: deze functie verbeteren
def get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Now we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


def auto_export(dataframe):
    """
    Functie die de export van het DataFrame automatiseerd. De naam van het document begint met de datum van
    de dag dat het is geëxporteerd.
    :return: print-statement naar de terminal dat de export is volbracht.
    """
    # todo: vaste document lay-out introduceren voor de exports.
    # todo: header vastzetten, documenten scollen door
    print(f'Voorbereiden van export. Breek proces niet af.')

    export_locatie = Front_End_Opslag

    # Genereren van de documentnaam
    excel_export_naam = 'Documenten Lobby.xlsx'

    # Namen van de tabbladen
    main_sheet = 'Main'
    project_sheet = 'Projecten'
    sbs_sheet = 'Generieke SBS'
    doc_type_sheet = 'Document Type'
    status_sheet = "Document Status"
    personen_sheet = 'Personen'

    # Start indiceren van het schrijven naar excel
    print(f'Starten met exporteren')
    export_path = os.path.join(export_locatie, excel_export_naam)
    writer = pd.ExcelWriter(export_path, engine='xlsxwriter')
    workbook = writer.book

    # Schrijven van de data naar het excel bestand
    start_rij = 4
    dataframe.to_excel(writer, sheet_name=main_sheet, startrow=start_rij)
    Referentietabel_Eigenaarschap['Project'].to_excel(writer, sheet_name=project_sheet, startrow=start_rij)
    SBS_Generiek.to_excel(writer, sheet_name=sbs_sheet, startrow=start_rij)
    Document_Klasse_Type.to_excel(writer, sheet_name=doc_type_sheet, startrow=start_rij)
    Status_Aanduiding.to_excel(writer, sheet_name=status_sheet, startrow=start_rij)
    Personen_Informatie.to_excel(writer, sheet_name=personen_sheet, startrow=start_rij)

    # Verwijzen van de tabbladen aan standaard waarden (voor interne verwijzingen)
    worksheet_main = writer.sheets[main_sheet]
    worksheet_projecten = writer.sheets[project_sheet]
    worksheet_sbs = writer.sheets[sbs_sheet]
    worksheet_doctype = writer.sheets[doc_type_sheet]
    worksheet_status = writer.sheets[status_sheet]
    worksheet_personen = writer.sheets[personen_sheet]

    # Genereren van de links naar de documenten # todo: (optioneel) links toevoegen van personen naar persoon info tab
    link_naar_doc_col = 'P'
    doc_link_start_rij = start_rij + 2
    for i in range(dataframe.shape[0]):
        pad = dataframe['Volledige pad naar document'].iloc[i]
        rij = i + doc_link_start_rij
        cell = f'{link_naar_doc_col}{rij}'
        worksheet_main.write_url(cell, pad, string='Klik voor document')

    # todo: filter toevoegen voor de titel van de documenten zodat specifieke documenten opgezocht kunnen worden
    # Invoegen van de fliters voor de kolommen waar dit van belang is
    worksheet_main.autofilter('C5:N5')
    worksheet_sbs.autofilter('B5:D5')
    worksheet_doctype.autofilter('B5:D5')
    worksheet_personen.autofilter('B5:D5')

    for i, width in enumerate(get_col_widths(dataframe)):
        worksheet_main.set_column(i, i, width)
    for i, width in enumerate(get_col_widths(Referentietabel_Eigenaarschap)):
        worksheet_projecten.set_column(i, i, width)
    for i, width in enumerate(get_col_widths(SBS_Generiek)):
        worksheet_sbs.set_column(i, i, width)
    for i, width in enumerate(get_col_widths(Document_Klasse_Type)):
        worksheet_doctype.set_column(i, i, width)
    for i, width in enumerate(get_col_widths(Personen_Informatie)):
        worksheet_personen.set_column(i, i, width)

    # Vastleggen van verschillende formats
    sheet_titel_format = workbook.add_format({'font_size': 18})
    merge_format = workbook.add_format({'align': 'left', 'valign': 'top'})

    # Genereren van de headers
    # header main sheet
    update_datum = date.today().strftime('%d-%m-%Y')
    worksheet_main.write('B1', 'Documenten Lobby', sheet_titel_format)
    worksheet_main.write('B2', f'Laatste update: {update_datum}')
    worksheet_main.merge_range('C1:D1', 'Toelichting tabblad', merge_format)
    worksheet_main.merge_range('C2:G3', toelichting_main, merge_format)
    worksheet_main.set_default_row(hide_unused_rows=True)  # verbergd de niet gebruikte rijen onder de dataset
    # worksheet_main.freeze_panes('C6')  # bevriesd de header en de kolom met de titel van de documenten

    # header projecten sheet
    worksheet_projecten.write('B1', project_sheet, sheet_titel_format)
    worksheet_projecten.merge_range('C1:D1', 'Toelichting tabblad', merge_format)
    worksheet_projecten.merge_range('C2:G3', toelichting_personen, merge_format)
    worksheet_projecten.set_default_row(hide_unused_rows=True)

    # header SBS sheet
    worksheet_sbs.write('B1', sbs_sheet, sheet_titel_format)
    worksheet_sbs.merge_range('C1:D1', 'Toelichting tabblad', merge_format)
    worksheet_sbs.merge_range('C2:G3', toelichting_sbs, merge_format)
    worksheet_sbs.set_default_row(hide_unused_rows=True)

    # header document type sheet
    worksheet_doctype.write('B1', doc_type_sheet, sheet_titel_format)
    worksheet_doctype.merge_range('C1:D1', 'Toelichting tabblad', merge_format)
    worksheet_doctype.merge_range('C2:G3', toelichting_doc_type, merge_format)
    worksheet_doctype.set_default_row(hide_unused_rows=True)

    # header status sheet
    worksheet_status.write('B1', status_sheet, sheet_titel_format)
    worksheet_status.merge_range('C1:D1', 'Toelichting tabblad', merge_format)
    worksheet_status.merge_range('C2:G3', toelichting_status, merge_format)
    worksheet_status.set_default_row(hide_unused_rows=True)

    # header personen sheet
    worksheet_personen.write('B1', personen_sheet, sheet_titel_format)
    worksheet_personen.merge_range('C1:D1', 'Toelichting tabblad', merge_format)
    worksheet_personen.merge_range('C2:G3', toelichting_personen, merge_format)
    worksheet_personen.set_default_row(hide_unused_rows=True)

    # Verbergen van de kolom met de volledige paden
    volle_pad_kolom = 'T'
    worksheet_main.set_column(f'{volle_pad_kolom}:{volle_pad_kolom}', None, None, {'hidden': True})

    # Verbergen van de indexnummers op elk tabblad
    worksheet_main.set_column('A:A', None, None, {'hidden': True})
    worksheet_projecten.set_column('A:A', None, None, {'hidden': True})
    worksheet_sbs.set_column('A:A', None, None, {'hidden': True})
    worksheet_doctype.set_column('A:A', None, None, {'hidden': True})
    worksheet_status.set_column('A:A', None, None, {'hidden': True})
    worksheet_personen.set_column('A:A', None, None, {'hidden': True})

    # Opslaan en afsluiten van het document
    writer.save()
    print(f'Bestand opgeslagen als: {excel_export_naam}')
