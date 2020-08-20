def discipline(deelsysteem_num, sbs):
    """
    De functie gebruikt het eerder bepaalde SBS nummer uit de geneireke SBS en haalt uit de generieke SBS
    de bijbehorende discipline.
    :param deelsysteem_num: Het generieke SBS nummer van de desbetreffende deelsysteem
    :param sbs: De verwijzing naar de generieke sbs die wordt gehanteert
    :return: discipline_1 of discipline_1 en discipline_2
    """
    discipline_1 = str()
    discipline_2 = str()

    if ',' in str(deelsysteem_num):
        deelsysteem_num_1 = deelsysteem_num[0]
        deelsysteem_num_2 = deelsysteem_num[1]

        for i in range(sbs.shape[0]):
            row_series = sbs.iloc[i]
            if deelsysteem_num_1 == int(row_series.values[2]):
                discipline_1 = row_series.values[0]

            if deelsysteem_num_2 != 9999 and deelsysteem_num_2 != 9009 and deelsysteem_num_2 != 0:
                for x in range(sbs.shape[0]):
                    row_series = sbs.iloc[x]
                    if deelsysteem_num_2 == int(row_series.values[2]):
                        discipline_2 = row_series.values[0]
                        if discipline_2 == discipline_1:
                            return discipline_1
                        else:
                            return discipline_1, discipline_2
            else:
                return discipline_1
    else:
        deelsysteem_num_1 = deelsysteem_num

        for i in range(sbs.shape[0]):
            row_series = sbs.iloc[i]
            if deelsysteem_num_1 == int(row_series.values[2]):
                discipline_1 = row_series.values[0]
                return discipline_1
