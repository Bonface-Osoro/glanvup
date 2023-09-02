'''This scripts provides the classification of countries by continent, region 
and income according to world bank

[1] “World Bank Country and Lending Groups - World Bank Data Help Desk.
” https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups 
(accessed Aug. 09, 2023).
'''

##### CONTINENT CLASSIFICATION ########
asia = ['AFG', 'ARM', 'AZE', 'BHR', 'BGD', 'BTN', 'BRN', 'MMR', 'KHM', 
        'CHN', 'CXR', 'CCK', 'IOT', 'GEO', 'HKG', 'IND', 'IDN', 'IRN', 
        'IRQ', 'ISR', 'JPN', 'JOR', 'KAZ', 'PRK', 'KOR', 'KWT', 'KGZ', 
        'LAO', 'LBN', 'MAC', 'MYS', 'MDV', 'MNG', 'OMN', 'NPL', 'PAK', 
        'PSE', 'PHL', 'QAT', 'SAU', 'SGP', 'LKA', 'SYR', 'TWN', 'TJK', 
        'THA', 'TUR', 'TKM', 'ARE', 'UZB', 'VNM', 'YEM', 'TLS', 'IND']

south_America = ['ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU', 'GUY', 'PRY', 
                 'PER', 'SUR', 'URY', 'VEN']

north_america = ['ATG', 'BHS', 'BRB', 'BLZ', 'CAN', 'CRI', 'CUB', 'DMA', 
                 'DOM', 'SLV', 'GTM', 'HTI', 'HND', 'JAM', 'MEX', 'NIC', 
                 'PAN', 'KNA', 'LCA', 'VCT', 'TTO', 'USA', 'ABW', 'AIA', 
                 'BMU', 'BES', 'VGB', 'CYM', 'CUB', 'CUW', 'DMA', 'DOM', 
                 'GRD', 'GLP', 'GRL', 'MTQ', 'MSR', 'PRI', 'BES', 'BES', 
                 'KNA', 'LCA', 'SPM', 'VCT', 'TTO', 'TCA', 'VIR']

africa = ['DZA', 'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 
          'TCD', 'COM', 'COG', 'COD', 'DJI', 'EGY', 'GNQ', 'ERI', 'SWZ', 
          'ETH', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'CIV', 'KEN', 'LSO', 
          'LBR', 'LBY', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MAR', 'MOZ',
          'NAM', 'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 
          'ZAF', 'SSD', 'SDN', 'TZA', 'TGO', 'TUN', 'UGA', 'ZMB', 'ZWE']

europe = ['ALB', 'AND', 'AUT', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 'CYP', 
          'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'GEO', 'DEU', 'GRC', 'HUN', 
          'ISL', 'IRL', 'ITA', 'KAZ', 'KOS', 'LVA', 'LIE', 'LTU', 'LUX', 
          'MKD', 'MLT', 'MDA', 'MCO', 'MNE', 'NLD', 'NOR', 'POL', 'PRT', 
          'ROU', 'RUS', 'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 
          'UKR', 'GBR', 'VAT', 'ALA', 'FRO', 'GIB', 'GGY', 'IMN', 'JEY', 
          'SJM']

oceania = ['ASM', 'AUS', 'COK', 'FJI', 'PYF', 'GUM', 'KIR', 'MHL', 'FSM', 
           'NRU', 'NCL', 'NZL', 'NIU', 'NFK', 'MNP', 'PLW', 'PNG', 'PCN', 
           'WSM', 'SLB', 'TKL', 'TON', 'TUV', 'UMI', 'VUT', 'WLF']

###### COASTAL CLASSIFICATION ########
asia_coast = ['IDN','PHL', 'BIH', 'PNG', 'MYS', 'VNM', 'THA', 'IRN', 'MMR', 
             'YEM', 'PAK', 'LKA', 'TLS', 'MDV', 'BGD', 'KHM', 'LBN', 'BRN',  
             'GND', 'IRQ', 'IND']

africa_coast = ['SOM', 'ZAF', 'EGY', 'LBY', 'AGO', 'NAM', 'TZA', 'TUN',
                'GAB', 'NGA', 'MRT', 'LBR', 'GHA', 'KEN', 'SEN', 'CIV',
                'CMR', 'SLE', 'SEY', 'GNB', 'GIN', 'DJI', 'GNQ', 'COD', 
                'COG', 'GMB', 'TGO', 'MDG', 'BEN', 'ERI', 'CPV', 'STP',
                'DZA', 'MOZ', 'NAM', 'MAR']

europe_coast = ['UKR', 'BGR', 'ALB', 'MNE', 'GEO', 'SVN', 'TUR']

north_coast = ['CUB', 'CRI', 'JAM', 'HND', 'GTM', 'SLV', 'GRD', 'LCA',
                 'BLZ', 'HTI', 'DMA', 'MEX', 'DOM', 'NIC', 'MUS',]

south_coast = ['ARG', 'COL', 'VEN', 'PER', 'ECU', 'URY', 'GUY', 'BRA']

##### INCOME CLASSIFICATION ####
low_income = ['AFG', 'PRK', 'SSD', 'BFA', 'LBR', 'SDN', 'BDI', 'MDG', 'SYR', 
              'CAF', 'MWI', 'TGO', 'TCD', 'MLI', 'UGA', 'COD', 'MOZ', 'YEM', 
              'ERI', 'NER', 'ETH', 'RWA', 'GMB', 'SLE', 'GNB', 'SOM', 'VEN']

low_middle = ['AGO', 'JOR', 'PHL', 'DZA', 'IND', 'WSM', 'BGD', 'IRN', 'STP', 
              'BEN', 'KEN', 'SEN', 'BTN', 'KIR', 'SLB', 'BOL', 'KGZ', 'LKA', 
              'CPV', 'LAO', 'TZA', 'KHM', 'LBN', 'TJK', 'CMR', 'LSO', 'TLS', 
              'COM', 'MRT', 'TUN', 'COG', 'FSM', 'UKR', 'CIV', 'MNG', 'UZB', 
              'DJI', 'MAR', 'VUT', 'EGY', 'MMR', 'VNM', 'SWZ', 'NPL', 'ZMB',
              'GHA', 'NIC', 'ZWE', 'GIN', 'NGA', 'HTI', 'PAK', 'HND', 'PNG']

upper_income = ['ALB', 'FJI', 'MKD', 'ARG', 'GAB', 'PLW', 'ARM', 'GEO', 'PRY', 
                'AZE', 'GRD', 'PER', 'BLR', 'GTM', 'RUS', 'BLZ', 'IDN', 'SRB', 
                'BIH', 'IRQ', 'ZAF', 'BWA', 'JAM', 'LCA', 'BRA', 'KAZ', 'VCT', 
                'BGR', 'XKX', 'SUR', 'CHN', 'LBY', 'THA', 'COL', 'MYS', 'TON', 
                'CRI', 'MDV', 'TUR', 'CUB', 'MHL', 'TKM', 'DMA', 'MUS', 'TUV',
                'DOM', 'MEX', 'PSE', 'SLV', 'MDA', 'GNQ', 'MNE', 'ECU', 'NAM',
                'GUY']

high_income = ['ASM', 'DEU', 'OMN', 'AND', 'GIB', 'PAN', 'ATG', 'GRC', 'POL', 'ABW',
               'GRL', 'PRT', 'AUS', 'GUM', 'PRI', 'AUT', 'HKG', 'QAT', 'BHS', 'HUN',
               'ROU', 'BHR', 'ISL', 'SMR', 'BRB', 'IRL', 'SAU', 'BEL', 'IMN', 'SYC',
               'BMU', 'ISR', 'SGP', 'VGB', 'ITA', 'SXM', 'BRN', 'JPN', 'SVK', 'CAN',
               'KOR', 'SVN', 'CYM', 'KWT', 'ESP', 'JEY', 'LVA', 'KNA', 'CHL', 'LIE',
               'MAF', 'HRV', 'LTU', 'SWE', 'CUW', 'LUX', 'CHE', 'CYP', 'MAC', 'TWN',
               'CZE', 'MLT', 'TTO', 'DNK', 'MCO', 'TCA', 'EST', 'NRU', 'ARE', 'FRO',
               'NLD', 'GBR', 'FIN', 'NCL', 'USA', 'FRA', 'NZL', 'URY', 'PYF', 'MNP',
               'VIR', 'NOR']

##### REGIONAL CLASSIFICATION ######
east_asia_pacific = ['ASM', 'KOR', 'PHL', 'AUS', 'LAO', 'WSM', 'BRN', 'MAC', 'SGP', 
                     'KHM', 'MYS', 'SLB', 'CHN', 'MHL', 'TWN', 'FJI', 'FSM', 'THA', 
                     'PYF', 'MNG', 'TLS', 'GUM', 'MMR', 'PNG', 'HKG', 'NRU', 'TON', 
                     'IDN', 'NCL', 'TUV', 'JPN', 'NZL', 'KIR', 'MNP', 'VNM', 'PRK', 
                     'PLW']

europe_central_asia = ['ALB', 'GIB', 'NOR', 'AND', 'GRC', 'POL', 'ARM', 'GRL', 'PRT', 
                       'AUT', 'HUN', 'ROU', 'AZE', 'ISL', 'RUS', 'BLR', 'IRL', 'SMR',
                       'BEL', 'IMN', 'SRB', 'BIH', 'ITA', 'SVK', 'BGR', 'KAZ', 'SVN', 
                       'JEY', 'XKX', 'ESP', 'HRV', 'KGZ', 'SWE', 'CYP', 'LVA', 'CHE',
                       'CZE', 'LIE', 'TJK', 'DNK', 'LTU', 'TUR', 'EST', 'LUX', 'TKM', 
                       'FRO', 'MDA', 'UKR', 'FIN', 'MCO', 'GBR', 'FRA', 'MNE', 'UZB', 
                       'GEO', 'NLD', 'DEU', 'MKD']

latin_and_caribbean = ['ATG', 'CUW', 'PRY', 'ARG', 'DMA', 'PER', 'ABW', 'DOM', 'PRI', 
                       'BHS', 'ECU', 'SXM', 'BRB', 'SLV', 'KNA', 'BLZ', 'GRD', 'LCA',
                       'BOL', 'GTM', 'MAF', 'BRA', 'GUY', 'MAF', 'VGB', 'HTI', 'SUR', 
                       'CYM', 'HND', 'TTO', 'CHL', 'JAM', 'TCA', 'COL', 'MEX', 'URY',
                       'CRI', 'NIC', 'VEN', 'CUB', 'PAN', 'VIR']

middle_north_africa = ['DZA', 'JOR', 'QAT', 'BHR', 'KWT', 'SAU', 'DJI', 'LBN', 'SYR', 
                       'EGY', 'LBY', 'TUN', 'IRN', 'MLT', 'ARE', 'IRQ', 'MAR', 'PSE', 
                       'ISR', 'OMN', 'YEM']

north_america_reg = ['BMU', 'CAN', 'USA']

south_asia = ['AFG', 'IND', 'PAK', 'BGD', 'MDV', 'LKA', 'BTN', 'NPL']

sub_saharan_africa = ['AGO', 'ETH', 'NER', 'BEN', 'GAB', 'NGA', 'BWA', 'GMB', 'RWA', 'BFA', 
                      'GHA', 'STP', 'BDI', 'GIN', 'SEN', 'CPV', 'GNB', 'SYC', 'CMR', 'KEN', 
                      'SLE', 'CAF', 'LSO', 'SOM', 'TCD', 'LBR', 'ZAF', 'COM', 'MDG', 'SSD', 
                      'COD', 'MWI', 'SDN', 'COG', 'MLI', 'TZA', 'CIV', 'MRT', 'TGO', 'GNQ', 
                      'MUS', 'UGA', 'ERI', 'MOZ', 'ZMB', 'SWZ', 'NAM', 'ZWE']