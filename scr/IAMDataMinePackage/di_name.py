def di_name(deelsysteem_num, sbs):
    """
    Functie voor het ophalen van de naam van de deelsysteem aan de hand van het nummer uit de generieke SBS.
    :param deelsysteem_num: Het generieke SBS nummer van de desbetreffende deelsysteem
    :param sbs: De verwijzing naar de generieke sbs die wordt gehanteert
    :return: De naam van de deelsysteem uit de generieke SBS
    """

    if ',' in str(deelsysteem_num):
        deelsysteem_num_1 = deelsysteem_num[0]
        deelsysteem_num_2 = deelsysteem_num[1]

        for g in range(sbs.shape[0]):
            generiek_sbs_row_series = sbs.iloc[g]

            if deelsysteem_num_1 == generiek_sbs_row_series.values[2]:
                deelsysteem_naam_1 = generiek_sbs_row_series.values[1]

                for h in [x for x in range(sbs.shape[0]) if x != g]:
                    generiek_sbs_row_series_2 = sbs.iloc[h]

                    if deelsysteem_num_2 == generiek_sbs_row_series_2.values[2]:
                        deelsysteem_naam_2 = generiek_sbs_row_series_2.values[1]
                        return deelsysteem_naam_1, deelsysteem_naam_2

    else:
        for g in range(sbs.shape[0]):
            generiek_sbs_row_series = sbs.iloc[g]
            if deelsysteem_num == generiek_sbs_row_series.values[2]:
                deelsysteem_naam_1 = generiek_sbs_row_series.values[1]
                return deelsysteem_naam_1
