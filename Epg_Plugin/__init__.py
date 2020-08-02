 
nb_channel=['1101-Aloula', '1120-ART_Aflam_1', '1121-ART_Aflam_2', '1122-ART_Hekayat', 
            '1134-ONDrama', '1135-Emirates', '1136-Abu_Dhabi_TV', '1137-Alhayat_TV', 
            '1138-AlhayatDrama', '1145-Mehwar', '1148-RotanaCinema EGY', '1156-NileDrama', 
            '1157-Nile_Cinema', '1158-NileComedy', '1159-NileLife', '1168-LBCI', '1169-Dubai_TV', 
            '1170-AlraiTV', '1173-Dubai_One', '1174-AlKaheraWalNasTV', '1176-Cima', '1177-SamaDubai', 
            '1177-Sama_Dubai', '1178-Abu_Dhabi_Drama', '1179-Dream', '1182-ART_Hekayat_2', 
            '1188-SharjahTV', '1193-Al_Nahar_TV', '1195-ART_Cinema', '1198-CBC', '1199-CBC_Drama', 
            '1203-ONE', '1204-iFILMTV', '1216-AlJadeedTV', '1217-Rotana_Classic', '1223-Al_Nahar_Drama', 
            '1226-SadaElBalad', '1227-SadaElBaladDrama', '1252-AlKaheraWalNasTV2', '1260-CBC_sofra', 
            '1261-Zee_alwan', '1262-Zee_aflam', '1264-AlDafrah', '1269-Alsharqya', '1279-SadaElBalad+2', 
            '1280-TeNTV', '1283-Dubai_Zaman', '1290-DMC', '1292-DMC_DRAMA', '1296-MTVLebnon', '1297-SBC', 
            '1298-Amman', '1299-Roya', '1300-SyriaDrama', '1301-Alsumaria', '1302-Fujairah', '1304-Nessma', 
            '1308-Watania1', '1310-Kuwait', '1313-Lana', '1314-JordanTV', '1317-Oman', '1321-almanar', 
            '1334-Watania2', '1336-MasperoZaman', '1338-SyriaTV', '1339-AlSaeedah', 
            '1339-Al_Saeedah', '1341-LBC', '1342-LanaPlusTV', '1350-SamaTV', '1352-Saudiya_TV', '1355-Mix']

ch = []
for nb in nb_channel:
    ch.append(nb.split('-')[1])
    
print ch