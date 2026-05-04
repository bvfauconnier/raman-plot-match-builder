"""
Base de données des pics Raman de référence pour les minéraux communs
en contexte gossan / Mars-analog.

Format : dict[mineral] = {
    'pics'       : [(position_cm⁻¹, mode_LaTeX, intensité_relative), ...],
    'color'      : couleur conventionnelle pour le plot,
    'formula'    : formule chimique LaTeX,
    'reference'  : citation bibliographique,
    'group'      : famille minéralogique (pour grouper visuellement),
}

Conventions :
- Intensité relative : 1.0 = pic principal, 0.1 = pic faible
- 'mode' : notation spectroscopique (factor-group) ou attribution chimique
- Les pics sont ordonnés par position croissante
"""

RAMAN_DB = {
    # ========================================================
    # OXYDES DE Ti
    # ========================================================
    'anatase': {
        'formula'  : r'TiO$_2$',
        'group'    : 'Ti oxides',
        'color'    : '#1f77b4',
        'reference': 'Ohsaka et al. 1978, J. Raman Spectrosc. 7, 321',
        'pics': [
            (144, r'$E_g^{(1)}$',               1.00),
            (197, r'$E_g^{(2)}$',               0.10),
            (399, r'$B_{1g}^{(1)}$',            0.60),
            (519, r'$A_{1g} + B_{1g}^{(2)}$',            0.40),
            (639, r'$E_g^{(3)}$',               0.55),
        ],
    },
    'rutile': {
        'formula'  : r'TiO$_2$',
        'group'    : 'Ti oxides',
        'color'    : '#17becf',
        'reference': 'Porto et al. 1967, Phys. Rev. 154, 522',
        'pics': [
            (143, r'$B_{1g}$',   0.40),
            (235, 'two-phonon',  0.30),
            (447, r'$E_g$',      1.00),
            (612, r'$A_{1g}$',   0.90),
        ],
    },

    # ========================================================
    # OXYDES DE Fe (très fréquents en gossan)
    # ========================================================
    'hematite': {
    'formula'  : r'$\alpha$-Fe$_2$O$_3$',
    'group'    : 'Fe oxides',
    'color'    : '#d62728',
    'reference': 'de Faria et al. 1997, J. Raman Spectrosc. 28, 873; '
                 'Hanesch 2009, Geophys. J. Int. 177, 941; '
                 'Shim & Duffy 2002, Am. Mineral. 87, 318',
    'pics': [
        # ----- Modes Raman-actifs (théorie : 2 A_1g + 5 E_g, groupe R-3c) -----
        (225,  r'$A_{1g}^{(1)}$',                1.00),   # pic principal diagnostique
        (245,  r'$E_g^{(1)}$',                   0.40),
        (293,  r'$E_g^{(2)}$',                   0.95),   # doublet non résolu
        (298,  r'$E_g^{(3)}$',                   0.90),   # avec 293
        (411,  r'$E_g^{(4)}$',                   0.70),
        (497,  r'$A_{1g}^{(2)}$',                0.35),
        (612,  r'$E_g^{(5)}$',                   0.65),
        # ----- Modes "interdits" induits par le désordre -----
        (660,  r'LO (disorder-induced)',         0.20),   # diagnostic des défauts
        # ----- Modes de second ordre / processus multi-phonons -----
        (820,  r'2LO',                           0.15),
        (1100, r'2$A_{1g}$ overtone',            0.10),
        # ----- Diffusion magnon (PIC DIAGNOSTIQUE de l'hématite) -----
        (1320, r'2-magnon scattering',           0.50),
        ],
    },
    'magnetite': {
        'formula'  : r'Fe$_3$O$_4$',
        'group'    : 'Fe oxides',
        'color'    : '#2c2c2c',
        'reference': 'Shebanova & Lazor 2003, J. Solid State Chem. 174, 424',
        'pics': [
            (310, r'$T_{2g}^{(1)}$',  0.30),
            (540, r'$T_{2g}^{(2)}$',  0.40),
            (668, r'$A_{1g}$',        1.00),
        ],
    },
    'goethite': {
    'formula'  : r'$\alpha$-FeO(OH)',
    'group'    : 'Fe oxyhydroxides',
    'color'    : '#8c564b',
    'reference': 'RRUFF R050142; de Faria et al. 1997, J. Raman Spectrosc. 28, 873; '
                 'Hanesch 2009, Geophys. J. Int. 177, 941',
    'pics': [
        # Modes principaux (Raman actifs, groupe Pbnm)
        (240, r'$A_g$ (lattice / Fe–O)',    0.60),  # secondaire
        (296, r'$A_g$ (Fe–O–Fe bend)',      0.68),
        (395, r'$A_g$ (Fe–O stretch)',      1.00),  # pic principal (Hanesch 2009)
        (477, r'$B_{1g}$ (Fe–OH bend)',     0.69),
        (542, r'$A_g$ (Fe–OH stretch)',     0.21),
        # Modes de second ordre / overtones (région > 900 cm⁻¹)
        (685, r'2-phonon',                  0.10),  # cf. littérature (faible ici)
        (994, r'$\nu$(OH) overtone',        0.19),
        ],
    },
    'lepidocrocite': {
        'formula'  : r'$\gamma$-FeO(OH)',
        'group'    : 'Fe oxyhydroxides',
        'color'    : '#ff9896',
        'reference': 'de Faria et al. 1997, J. Raman Spectrosc. 28, 873',
        'pics': [
            (252, '',   1.00),
            (379, '',   0.50),
            (528, '',   0.30),
            (648, '',   0.40),
        ],
    },
    'ferrihydrite': {
        'formula'  : r'Fe$_{10}$O$_{14}$(OH)$_2$',
        'group'    : 'Fe oxyhydroxides',
        'color'    : '#e377c2',
        'reference': 'Hanesch 2009, Geophys. J. Int. 177, 941; '
                     'Drits et al. 2007, Am. Mineral. 92, 946 (formule modernisée)',
        'pics': [
            (370, '',   1.00),
            (510, '',   0.60),
            (710, '',   0.40),
        ],
    },

    # ========================================================
    # SULFATES (jarosite = marqueur gossan par excellence)
    # ========================================================
    'jarosite': {
        'formula'  : r'KFe$_3$(SO$_4$)$_2$(OH)$_6$',
        'group'    : 'sulfates',
        'color'    : '#bcbd22',
        'reference': 'Sasaki et al. 1998, Can. Mineral. 36, 1225',
        'pics': [
            (225,  r'$\nu$(Fe-O)',            0.40),
            (301,  r'$\nu$(Fe-O)',            0.50),
            (434,  r'$\nu_2$(SO$_4$)',        0.60),
            (572,  r'$\nu_4$(SO$_4$)',        0.30),
            (623,  r'$\nu_4$(SO$_4$)',        0.30),
            (1008, r'$\nu_1$(SO$_4$)',        1.00),
            (1106, r'$\nu_3$(SO$_4$)',        0.35),
            (1156, r'$\nu_3$(SO$_4$)',        0.30),
            (3405, r'$\nu$(OH)',              0.25),
        ],
    },
    'gypsum': {
        'formula'  : r'CaSO$_4\!\cdot\!$2H$_2$O',
        'group'    : 'sulfates',
        'color'    : '#f7b6d2',
        'reference': 'Chio et al. 2004, Am. Mineral. 89, 390',
        'pics': [
            (415,  r'$\nu_2$(SO$_4$)',   0.40),
            (493,  r'$\nu_2$(SO$_4$)',   0.35),
            (619,  r'$\nu_4$(SO$_4$)',   0.45),
            (670,  r'$\nu_4$(SO$_4$)',   0.35),
            (1008, r'$\nu_1$(SO$_4$)',   1.00),
            (1137, r'$\nu_3$(SO$_4$)',   0.35),
            (3405, r'$\nu$(H$_2$O)',     0.30),
            (3495, r'$\nu$(H$_2$O)',     0.30),
        ],
    },
    'anhydrite': {
        'formula'  : r'CaSO$_4$',
        'group'    : 'sulfates',
        'color'    : '#c7c7c7',
        'reference': 'Chang et al. 1999, J. Raman Spectrosc. 30, 1049',
        'pics': [
            (417,  r'$\nu_2$(SO$_4$)',   0.40),
            (498,  r'$\nu_2$(SO$_4$)',   0.35),
            (609,  r'$\nu_4$(SO$_4$)',   0.35),
            (625,  r'$\nu_4$(SO$_4$)',   0.30),
            (676,  r'$\nu_4$(SO$_4$)',   0.45),
            (1017, r'$\nu_1$(SO$_4$)',   1.00),
            (1128, r'$\nu_3$(SO$_4$)',   0.35),
        ],
    },
    'schwertmannite': {
    'formula'  : r'Fe$_8$O$_8$(OH)$_6$SO$_4\!\cdot\!n$H$_2$O',
    'group'    : 'Fe oxy-sulfates',
    'color'    : '#ff7f0e',
    'reference': 'Mazzetti & Thistlethwaite 2002, J. Raman Spectrosc. 33, 104',
    'pics': [
        (310,  'Fe-O lattice',       0.40),
        (425,  'Fe-O stretch',       0.80),
        (560,  'Fe-O stretch',       0.40),
        (700,  'Fe-OH bend',         0.35),
        (990,  r'$\nu_1$(SO$_4$)',   1.00),
        (1020, r'$\nu_1$(SO$_4$)',   0.80),
        (1130, r'$\nu_3$(SO$_4$)',   0.30),
        (3390, r'$\nu$(OH)',         0.30),
        ],
    },

    # ========================================================
    # SULFURES (protolithes des gossans)
    # ========================================================
    'pyrite': {
        'formula'  : r'FeS$_2$',
        'group'    : 'sulfides',
        'color'    : '#ffbb78',
        'reference': 'Vogt et al. 1983, Phys. Status Solidi B 120, K11',
        'pics': [
            (342, r'$E_g$',           0.40),
            (378, r'$A_g$',           1.00),
            (429, r'$T_g^{(3)}$',     0.35),
        ],
    },
    'chalcopyrite': {
        'formula'  : r'CuFeS$_2$',
        'group'    : 'sulfides',
        'color'    : '#9467bd',
        'reference': 'Mernagh & Trudu 1993, Chem. Geol. 103, 113',
        'pics': [
            (291, r'$A_1$',   1.00),
            (352, '',         0.30),
        ],
    },

    # ========================================================
    # CARBONATES
    # ========================================================
    'calcite': {
        'formula'  : r'CaCO$_3$',
        'group'    : 'carbonates',
        'color'    : '#aec7e8',
        'reference': 'Rutt & Nicola 1974, J. Phys. C 7, 4522',
        'pics': [
            (156,  r'$E_g$ lattice',    0.30),
            (282,  r'$E_g$ lattice',    0.50),
            (712,  r'$\nu_4$(CO$_3$)',  0.30),
            (1086, r'$\nu_1$(CO$_3$)',  1.00),
            (1436, r'$\nu_3$(CO$_3$)',  0.10),
        ],
    },
    'dolomite': {
        'formula'  : r'CaMg(CO$_3$)$_2$',
        'group'    : 'carbonates',
        'color'    : '#98df8a',
        'reference': 'Gillet et al. 1993, Phys. Chem. Minerals 20, 1',
        'pics': [
            (176,  '',                  0.30),
            (299,  '',                  0.50),
            (725,  r'$\nu_4$(CO$_3$)',  0.30),
            (1098, r'$\nu_1$(CO$_3$)',  1.00),
        ],
    },

    # ========================================================
    # SILICATES
    # ========================================================
    'quartz': {
        'formula'  : r'SiO$_2$',
        'group'    : 'silicates',
        'color'    : '#7f7f7f',
        'reference': 'Etchepare et al. 1974, J. Chem. Phys. 60, 1873',
        'pics': [
            (128,  r'$E$',       0.20),
            (206,  r'$A_1$',     0.20),
            (265,  r'$E$',       0.20),
            (355,  r'$A_1$',     0.15),
            (465,  r'$A_1$',     1.00),
            (696,  r'$E$',       0.05),
            (795,  r'$A_1$',     0.08),
            (808,  r'$A_1$',     0.08),
            (1085, r'$A_1$',     0.05),
        ],
    },
    'kaolinite': {
        'formula'  : r'Al$_2$Si$_2$O$_5$(OH)$_4$',
        'group'    : 'silicates',
        'color'    : '#dbdb8d',
        'reference': 'Frost 1995, Clays Clay Miner. 43, 191',
        'pics': [
            (143,  '',                 0.60),
            (271,  '',                 0.50),
            (395,  '',                 0.90),
            (432,  '',                 1.00),
            (466,  '',                 0.80),
            (638,  '',                 0.30),
            (750,  '',                 0.20),
            (914,  r'$\delta$(AlOH)',  0.30),
            (3620, r'$\nu$(inner-OH)', 0.30),
            (3652, r'$\nu$(OH)',       0.20),
            (3669, r'$\nu$(OH)',       0.25),
            (3685, r'$\nu$(OH)',       0.30),
            (3695, r'$\nu$(OH)',       1.00),
        ],
    },

    # ========================================================
    # CARBONE (signatures biosignatures / maturité thermique)
    # ========================================================
    'carbon_disordered': {
        'formula'  : r'C (sp$^2$/sp$^3$)',
        'group'    : 'carbon',
        'color'    : '#8b0000',
        'reference': 'Ferrari & Robertson 2000, Phys. Rev. B 61, 14095',
        'pics': [
            (1350, 'D band (defects)',       1.00),
            (1580, 'G band (sp$^2$ E$_{2g}$)', 1.00),
            (1620, r"D' band",               0.30),
            (2700, '2D band',                0.40),
        ],
    },
    'graphite': {
        'formula'  : r'C',
        'group'    : 'carbon',
        'color'    : '#2c2c2c',
        'reference': 'Tuinstra & Koenig 1970, J. Chem. Phys. 53, 1126',
        'pics': [
            (1582, r'G (E$_{2g}$)',  1.00),
            (2700, '2D',             0.60),
        ],
    },

    # ========================================================
    # PHOSPHATES
    # ========================================================
    'vivianite': {
        'formula'  : r'Fe$_3$(PO$_4$)$_2\!\cdot\!$8H$_2$O',
        'group'    : 'phosphates',
        'color'    : '#1f9e89',
        'reference': 'Frost et al. 2002, Mineral. Mag. 66, 1063; '
                     'Piriou & Poullen 1984, J. Raman Spectrosc. 15, 343',
        'pics': [
            (175,  r'lattice',                  0.20),
            (381,  r'$\nu_2$(PO$_4$)',          0.45),
            (418,  r'$\nu_2$(PO$_4$)',          0.30),
            (580,  r'$\nu_4$(PO$_4$)',          0.40),
            (946,  r'$\nu_1$(PO$_4$)',          1.00),   # pic principal diagnostique
            (988,  r'$\nu_1$(PO$_4$)',          0.60),
            (1055, r'$\nu_3$(PO$_4$)',          0.35),
            (3262, r'$\nu$(OH) sym.',           0.80),   # OH-stretching le plus intense
            (3460, r'$\nu$(OH) asym.',          0.50),
        ],
    },
    'scorodite': {
        'formula'  : r'FeAsO$_4\!\cdot\!$2H$_2$O',
        'group'    : 'arsenates',
        'color'    : '#35b779',
        'reference': 'Frost et al. 2006, J. Raman Spectrosc. 38, 574; '
                     'Kloprogge et al. 2005, Spectrochim. Acta A 61, 2543',
        'pics': [
            (337,  r'$\nu_2$(AsO$_4$)',         0.40),
            (381,  r'$\nu_2$(AsO$_4$)',         0.50),
            (424,  r'$\nu_4$(AsO$_4$)',         0.35),
            (449,  r'$\nu_4$(AsO$_4$)',         0.30),
            (484,  r'$\nu_4$(AsO$_4$)',         0.25),
            (805,  r'$\nu_1$(AsO$_4$)',         1.00),   # pic principal sym. stretch
            (830,  r'$\nu_3$(AsO$_4$)',         0.55),
            (869,  r'$\nu_3$(AsO$_4$)',         0.45),
            (890,  r'$\nu_3$(AsO$_4$)',         0.40),
            (3082, r'$\nu$(OH) broad',          0.25),
            (3513, r'$\nu$(OH) sharp',          0.30),
        ],
    },

    # ========================================================
    # OXYDES/HYDROXYDES DE Mn
    # ========================================================
    'pyrolusite': {
        'formula'  : r'$\beta$-MnO$_2$',
        'group'    : 'Mn oxides',
        'color'    : '#440154',
        'reference': 'Julien et al. 2004, Spectrochim. Acta A 60, 689; '
                     'Post et al. 2020, Am. Mineral. 105, 1175',
        'pics': [
            # Structure rutile (groupe P4₂/mnm) — modes analogues au rutile mais décalés
            (320,  r'$B_{1g}$',               0.25),
            (480,  r'$E_g$',                  0.30),
            (540,  r'$A_{1g}$ (Mn–O bend)',   0.45),
            (585,  r'$B_{2g}$',               0.30),   # Bernardini et al. 2019
            (660,  r'$A_{1g}$ (Mn–O str.)',   1.00),   # pic principal diagnostique
        ],
    },
    'manganite': {
        'formula'  : r'$\gamma$-MnO(OH)',
        'group'    : 'Mn oxyhydroxides',
        'color'    : '#31688e',
        'reference': 'Julien et al. 2004, Spectrochim. Acta A 60, 689; '
                     'Sepúlveda et al. 2015, Heritage Science 3, 27',
        'pics': [
            (218,  r'lattice',                0.30),
            (259,  r'lattice',                0.25),
            (387,  r'$\delta$(Mn–OH)',        0.85),
            (530,  r'$\nu$(Mn–O)',            0.50),
            (557,  r'$\nu$(Mn–O)',            0.60),
            (621,  r'$\nu$(Mn–OH)',           1.00),   # pic principal
            (760,  r'$\nu$(Mn–O)',            0.40),
        ],
    },
    'birnessite': {
        'formula'  : r'(Na,Ca,K)$_x$Mn$_2$O$_4\!\cdot\!$1.5H$_2$O',
        'group'    : 'Mn oxides',
        'color'    : '#21918c',
        'reference': 'Julien et al. 2003, Solid State Ionics 159, 345; '
                     'Post et al. 2020, Am. Mineral. 105, 1175',
        'pics': [
            # Phyllomanganate — bandes larges caractéristiques
            (490,  r'$\nu$(Mn–O)',            0.50),
            (559,  r'$\nu$(Mn–O) interlayer', 1.00),   # bande caractéristique K-birnessite
            (630,  r'$\nu$(Mn–O)',            0.70),
        ],
    },

    # ========================================================
    # SULFURES SECONDAIRES
    # ========================================================
    'sphalerite': {
        'formula'  : r'(Zn,Fe)S',
        'group'    : 'sulfides',
        'color'    : '#fde725',
        'reference': 'Osadchii & Gorbaty 2010, Geochim. Cosmochim. Acta 74, 1383; '
                     'Buzatu & Buzgar 2013, Anal. Univ. "Al. I. Cuza" Iasi 59, 107',
        'pics': [
            # 3 modes principaux — positions variables selon teneur en Fe
            (300,  r'$A_1$ (Fe–S)',           0.60),   # croît avec xFe
            (331,  r'$A_1$ (mixed)',          0.65),
            (350,  r'LO (Zn–S)',              1.00),   # pic principal pur ZnS
        ],
    },
    'covellite': {
        'formula'  : r'CuS',
        'group'    : 'sulfides',
        'color'    : '#5ec962',
        'reference': 'Mernagh & Trudu 1993, Chem. Geol. 103, 113; '
                     'Vinokurov et al. 2021, Minerals 11, 1271',
        'pics': [
            (259,  r'$\nu$(Cu–S)',            0.35),
            (469,  r'$\nu$(S–S) str.',        1.00),   # mode S–S principal diagnostique
            (918,  r'2$\nu$(S–S) overtone',   0.15),
        ],
    },

    # ========================================================
    # SILICATES SECONDAIRES (PHYLLOSILICATES)
    # ========================================================
    'muscovite': {
        'formula'  : r'KAl$_2$(AlSi$_3$O$_{10}$)(OH)$_2$',
        'group'    : 'silicates',
        'color'    : '#b5cf6b',
        'reference': 'Tlili et al. 1989, Eur. J. Mineral. 1, 7; '
                     'Arbiol & Layne 2021, Appl. Spectrosc. 75, 1475',
        'pics': [
            (179,  r'lattice',                0.25),
            (262,  r'lattice',                0.30),
            (408,  r'Si–O–Al bend',           0.60),
            (477,  r'Si–O–Si bend',           0.50),
            (700,  r'$\nu$(Si–O–Si)',         0.40),
            (754,  r'$\nu$(Si–O–Al)',         0.35),
            (1067, r'$\nu$(Si–O)',            0.55),
            (3627, r'$\nu$(OH)',              1.00),   # Al–OH stretch, très diagnostique
        ],
    },
    'illite': {
        'formula'  : r'K$_{0.65}$Al$_2$(Al$_{0.65}$Si$_{3.35}$O$_{10}$)(OH)$_2$',
        'group'    : 'silicates',
        'color'    : '#8fbc8f',
        'reference': 'Tlili et al. 1989, Eur. J. Mineral. 1, 7; '
                     'Bishop et al. 2004, J. Raman Spectrosc. 35, 480',
        'pics': [
            # Spectre proche muscovite, bandes plus larges (désordre)
            (250,  r'lattice',                0.25),
            (430,  r'Si–O–Al bend',           0.55),
            (700,  r'$\nu$(Si–O–Si)',         0.35),
            (1050, r'$\nu$(Si–O)',            0.50),
            (3620, r'$\nu$(Al–OH)',           1.00),
        ],
    },
    'montmorillonite': {
        'formula'  : r'(Na,Ca)$_{0.3}$(Al,Mg)$_2$Si$_4$O$_{10}$(OH)$_2\!\cdot\!n$H$_2$O',
        'group'    : 'silicates',
        'color'    : '#c5b0d5',
        'reference': 'Bishop et al. 2004, J. Raman Spectrosc. 35, 480; '
                     'Madejová & Komadel 2001, Clays Clay Miner. 49, 410',
        'pics': [
            (213,  r'lattice',                0.20),
            (385,  r'Si–O–Al bend',           0.40),
            (460,  r'Si–O–Si bend',           0.55),
            (715,  r'$\nu$(Si–O–Al)',         0.30),
            (1010, r'$\nu$(Si–O)',            1.00),   # mode ν₃ Si–O dominant
            (3625, r'$\nu$(Al–OH)',           0.65),
            (3695, r'$\nu$(Mg–OH)',           0.40),
        ],
    },
    'chlorite': {
        'formula'  : r'(Mg,Fe,Al)$_6$(Si,Al)$_4$O$_{10}$(OH)$_8$',
        'group'    : 'silicates',
        'color'    : '#2ca02c',
        'reference': 'Tlili et al. 1989, Eur. J. Mineral. 1, 7; '
                     'Arbiol & Layne 2021, Appl. Spectrosc. 75, 1475',
        'pics': [
            (195,  r'lattice',                    0.25),
            (350,  r'$\nu$(Mg–O)',                0.30),
            (447,  r'Si–O–(Mg,Al) bend',          0.60),
            (550,  r'$\nu$(Si–O–Al)',             0.45),
            (679,  r'$\nu$(Si–O)',                0.55),
            (1003, r'$\nu$(Si–O)',                0.70),
            (3560, r'$\nu$(Mg$_3$OH) inner-OH',  1.00),   # diagnostique variété Mg/Fe
            (3622, r'$\nu$(Mg$_2$AlOH)',          0.60),
        ],
    },

    # ========================================================
    # SULFATES SECONDAIRES / ALTERITE
    # ========================================================
    'alunite': {
        'formula'  : r'KAl$_3$(SO$_4$)$_2$(OH)$_6$',
        'group'    : 'sulfates',
        'color'    : '#e7969c',
        'reference': 'Frost et al. 2006, J. Mol. Struct. 785, 59; '
                     'Arbiol & Layne 2021, Appl. Spectrosc. 75, 1475',
        'pics': [
            (380,  r'$\nu_2$(SO$_4$)',        0.45),
            (425,  r'$\nu_2$(SO$_4$)',        0.35),
            (499,  r'$\nu_4$(SO$_4$)',        0.40),
            (641,  r'$\nu_4$(SO$_4$)',        0.45),
            (1003, r'$\nu_1$(SO$_4$)',        1.00),   # pic principal très intense
            (1083, r'$\nu_3$(SO$_4$)',        0.35),
            (1176, r'$\nu_3$(SO$_4$)',        0.30),
            (3487, r'$\nu$(OH)',              0.30),
        ],
    },
    'siderite': {
        'formula'  : r'FeCO$_3$',
        'group'    : 'carbonates',
        'color'    : '#8c6d31',
        'reference': 'Börner et al. 2014, J. Raman Spectrosc. 45, 1065; '
                     'Hanesch 2009, Geophys. J. Int. 177, 941',
        'pics': [
            (185,  r'$E_g$ lattice',         0.25),
            (284,  r'$E_g$ lattice',         0.45),
            (735,  r'$\nu_4$(CO$_3$)',       0.30),
            (1084, r'$\nu_1$(CO$_3$)',       1.00),   # pic principal diagnostique
        ],
    },

    # ========================================================
    # FELDSPATHS
    # ========================================================
    'albite': {
        'formula'  : r'NaAlSi$_3$O$_8$',
        'group'    : 'silicates',
        'color'    : '#d9d9d9',
        'reference': 'Freeman et al. 2008, Can. Mineral. 46, 1477; '
                     'Aliatis et al. 2015, Am. Mineral. 100, 1272',
        'pics': [
            # Groupe "I" (doublet caractéristique du plagioclase Na-riche)
            (290,  r'$\nu_c$ (T–O–T bend)',   0.55),
            (400,  r'lattice',                 0.25),
            (451,  r'lattice',                 0.20),
            (476,  r'$\nu_b$ (T–O–T bend)',   1.00),   # doublet caractéristique
            (509,  r'$\nu_a$ (T–O–T bend)',   0.90),   # doublet caractéristique
            (578,  r'$\delta$(Si–O–Al)',       0.25),
            (763,  r'$\nu$(Al–O)',             0.35),
            (808,  r'$\nu$(Si–O)',             0.30),
        ],
    },

    # ========================================================
    # JAROSITES (groupe alunite)
    # ========================================================
    'natrojarosite': {
        'formula'  : r'NaFe$_3$(SO$_4$)$_2$(OH)$_6$',
        'group'    : 'sulfates',
        'color'    : '#d4a017',
        'reference': 'Frost et al. 2006, J. Raman Spectrosc. 37, 722; '
                     'Sasaki et al. 1998, Can. Mineral. 36, 1225',
        'pics': [
            # Spectre très proche de la jarosite K; décalages légers sur ν1, ν4
            (225,  r'$\nu$(Fe–O)',            0.35),
            (301,  r'$\nu$(Fe–O)',            0.45),
            (436,  r'$\nu_2$(SO$_4$)',        0.55),   # +2 cm⁻¹ vs K-jarosite
            (574,  r'$\nu_4$(SO$_4$)',        0.30),
            (623,  r'$\nu_4$(SO$_4$)',        0.30),
            (1010, r'$\nu_1$(SO$_4$)',        1.00),   # +2 cm⁻¹ vs K-jarosite
            (1104, r'$\nu_3$(SO$_4$)',        0.35),
            (1155, r'$\nu_3$(SO$_4$)',        0.30),
            (3390, r'$\nu$(OH)',              0.20),
        ],
    },

    # ========================================================
    # SULFATES Ca — série de déshydratation (Gypse > Bassanite > Anhydrite)
    # ========================================================
    'bassanite': {
        'formula'  : r'CaSO$_4\!\cdot\!$½H$_2$O',
        'group'    : 'sulfates',
        'color'    : '#f5cba7',
        'reference': 'Liu et al. 2009, LPSC Abstr. 2128; '
                     'Hennings et al. 2014, Anal. Chem. 86, 11849',
        'pics': [
            # Intermédiaire entre gypsum (1008) et anhydrite (1017) → 1015 cm⁻¹
            (130,  r'lattice',                0.15),
            (427,  r'$\nu_2$(SO$_4$)',        0.35),
            (489,  r'$\nu_2$(SO$_4$)',        0.30),
            (628,  r'$\nu_4$(SO$_4$)',        0.40),
            (1015, r'$\nu_1$(SO$_4$)',        1.00),   # pic principal diagnostique
            (1128, r'$\nu_3$(SO$_4$)',        0.30),
            (3610, r'$\nu$(H$_2$O)',          0.25),   # H₂O de canal, faible
        ],
    },

    # ========================================================
    # SULFATES Ba
    # ========================================================
    'baryte': {
        'formula'  : r'BaSO$_4$',
        'group'    : 'sulfates',
        'color'    : '#aaaaff',
        'reference': 'Buzgar & Apopei 2009, An. Şt. Univ. "Al. I. Cuza" Iaşi 55, 5; '
                     'Krishnamurti 1982, J. Raman Spectrosc. 13, 281; '
                     'Sarma et al. 2020, Minerals 10, 260',
        'pics': [
            (137,  r'lattice',                0.20),
            (187,  r'lattice',                0.15),
            (452,  r'$\nu_2$(SO$_4$)',        0.35),
            (461,  r'$\nu_2$(SO$_4$)',        0.30),
            (616,  r'$\nu_4$(SO$_4$)',        0.40),
            (647,  r'$\nu_4$(SO$_4$)',        0.25),
            (987,  r'$\nu_1$(SO$_4$)',        1.00),   # pic principal diagnostique
            (1142, r'$\nu_3$(SO$_4$)',        0.20),
        ],
    },
}

# ============================================================
# HELPERS
# ============================================================
def get_peaks(mineral, min_intensity=0.0, with_labels=True):
    """
    Retourne la liste des pics d'un minéral filtrés par intensité.
    
    Parameters
    ----------
    mineral : str
        Nom du minéral (clé de RAMAN_DB).
    min_intensity : float
        Seuil d'intensité relative [0-1]. 0.3 = ne garde que les pics
        d'intensité >= 30% du pic principal.
    with_labels : bool
        Si False, renvoie seulement les positions.
    """
    m = mineral.lower()
    if m not in RAMAN_DB:
        raise KeyError(f"Minéral '{mineral}' inconnu. "
                       f"Disponibles : {list(RAMAN_DB.keys())}")
    pics = [(p, lbl, i) for p, lbl, i in RAMAN_DB[m]['pics']
            if i >= min_intensity]
    if with_labels:
        return [(p, lbl) for p, lbl, _ in pics]
    return [p for p, _, _ in pics]


def list_minerals(group=None):
    """Liste les minéraux disponibles, optionnellement filtrés par groupe."""
    if group is None:
        return list(RAMAN_DB.keys())
    return [m for m, d in RAMAN_DB.items() if d.get('group') == group]


def list_groups():
    """Liste les familles minéralogiques disponibles."""
    groups = {}
    for m, d in RAMAN_DB.items():
        g = d.get('group', 'other')
        groups.setdefault(g, []).append(m)
    return groups


def format_citation(mineral):
    """Renvoie la citation formatée pour un minéral."""
    m = mineral.lower()
    if m not in RAMAN_DB:
        return ''
    d = RAMAN_DB[m]
    return f"{m.capitalize()} ({d['formula']}) — {d['reference']}"