import os
import re

title_dl = "20180117 - emm budget rijnlandroute v7"

print(re.search(r'\d$', title_dl))

if re.search(r'(?<=v)\d', title_dl):
    index_v = title_dl.find('v')
    print(index_v)
    # Controleren of de naam eindigd op digit. Als dit zo is, is het het laatste getal van versie nummer
    if not re.search(r'\d$', title_dl):
        print('in if')
        if re.search(r'(?<=[.])\d', title_dl):
            print('in if in if')
            index_punt = title_dl.find('.')
            versie = title_dl[index_v + 1:index_punt + 2]  # 'v2' of 'v2.0' ==> '2' of '2.0'
            print(versie)
        else:
            print('in else in if')
            versie = title_dl[index_v + 1::]  # 'v2' of 'v2.0' ==> '2' of '2.0'
            print(versie)
    else:
        print('in else')
        versie = title_dl[index_v + 1::]  # 'v2' of 'v2.0' ==> '2' of '2.0'
        print(versie)
