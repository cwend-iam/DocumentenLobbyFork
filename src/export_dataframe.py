import pandas as pd

# Export_data is de lay-out van de kolommen van het uiteindelijk document voor de eindgebruiker
Export_data = pd.DataFrame({"Titel": [],  # naam zonder .pdf etc --> 20200501_Realisatie_DMS_Model
                            "Document klasse": [],  # bijv. Rapport of tekening
                            "Document type": [],  # bijv. FMECA of RAMS
                            "Versie": [],  # Versienummer van doc
                            "Status": [],  # Status van doc
                            "Datum": [],  # Datum van aanmaken doc
                            "Laatst aangepast": [],  # Datum waarop doc voor het laatst is aangepast
                            "Project": [],  # Project van toepassing
                            "Project type": [],  # Type van het project (Nat/Droog/Combinatie)
                            "Deelinstallatie nummer": [],  # Deelinstallatie/SBS num van toepassing
                            "Deelinstallatie naam": [],  # Deelinstallatie naam van toepassing
                            "Discipline": [],  # E, C, W, GWW of combinatie hiervan
                            "Project Fase": [],  # Projectfase van toepasing
                            "Eigenaar": [],  # Naam van eigenaar document
                            "Bestandformat": [],  # .pdf/.xlsx/.docx/.xls
                            "Link naar document": [],  # Directe links naar het document
                            "Opmerking": [],  # Moet in elke rij leeg blijven
                            "Bestand": [],  # volledige naam --> 20200501_Realisatie_DMS_Model.xlsx
                            "Volledige pad naar document": []})  # Voor het realiseren van de hyperlink naar de docs

# todo: een standaard aanpak definiëren voor het verwijzen van de kolommen in het export document
# bovenstaande is ter behoeve van de efficiëntie van de beheerder van de Documenten Lobby
