def find_valid_xml(paths):
    """
    Finds the first XML file that follows the 'folder/xml' structure.
    
    Args:
        paths (list): List of file/folder paths.

    Returns:
        str or None: The first matching XML file path, or None if no match is found.
    """
    for path in paths:
        # Ignore non-XML files
        if not path.endswith(".xml"):
            continue

        # Split the path into parts based on "/"
        parts = path.strip("/").split("/")
        # print(parts)

        # Ensure it matches the expected "folder/xml" structure
        if len(parts) == 2:
            # print(path)
            return path  # Return first valid match

    return paths[0]  # No valid file found

# Define categories for better organization
categories = {
    "Structure": ["type_fondation","type_structure_principale", "elements_prefabriques", "materiau_structure"],
    "Facade & Isolation": ["materiau_remplissage_facade", "mur_mode_isolation", "mur_nature_isolant", "mur_revetement_ext"],
    "Fondation & Planchers": [ "type_plancher", "plancher_mode_isolation", "plancher_nature_isolant", "plancher_nature_espace"],
    "Toiture": ["type_toiture", "toiture_mode_isolation", "toiture_nature_isolant", "toiture_vegetalisee", "toiture_couverture"],
    "Menuiserie & Energie": ["type_menuiserie", "type_pm", "stockage_electricite", "gestion_active", "type_eclairage"]
}

donnes_techniques_dict = {
    "type_structure_principale": {
        "0": "Autre",
        "1": "Maçonnerie",
        "2": "Poteaux/poutres",
        "3": "Voiles porteurs",
        "4": "Ossature"
    },
    "elements_prefabriques": {
        "0": "non",
        "1": "oui"
    },
    "materiau_structure": {
        "0": "Autre",
        "1": "Béton",
        "2": "Béton cellulaire",
        "3": "Béton de chanvre",
        "4": "Béton de bois",
        "5": "Béton fibré",
        "6": "Béton haute performance",
        "7": "Terre cuite",
        "8": "Terre crue",
        "9": "Bois massif",
        "10": "Bois massif reconstitué",
        "11": "Acier",
        "12": "Mixte: bois-béton",
        "13": "Mixte: béton-acier",
        "14": "Mixte: bois-acier",
        "15": "Pierre"
    },
    "materiau_remplissage_facade": {
        "0": "Autre",
        "1": "béton ordinaire",
        "2": "béton haute performance",
        "3": "bloc de béton manufacturé (parpaing...)",
        "4": "béton cellulaire",
        "5": "béton fibré",
        "6": "béton de chanvre",
        "7": "béton de bois",
        "8": "terre cuite",
        "9": "terre crue",
        "10": "verre",
        "11": "panneaux sandwich",
        "12": "bois massif",
        "13": "bois massif reconstitué",
        "14": "panneaux de particules et de fibres de bois (ossature bois...)",
        "15": "paille",
        "16": "pierre",
        "17": "autre matériau biosourcé"
    },
    "mur_mode_isolation": {
        "0": "Autre",
        "1": "Isolation Thermique Répartie (ITR)",
        "2": "Isolation Thermique entre ossature",
        "3": "Isolation Thermique par l’Intérieur (ITI)",
        "4": "Isolation Thermique par l’Extérieur (ITE)"
    },
    "mur_nature_isolant": {
        "0": "Autre",
        "1": "Polystyrène Expansé (PSE)",
        "2": "Polystyrène Extrudé (XPS)",
        "3": "Polyuréthane (PU)",
        "4": "Laine de roche (LR)",
        "5": "Laine de verre (LV)",
        "6": "Produits réfléchissant",
        "7": "Laine de bois",
        "8": "Laine de lin",
        "9": "Laine de chanvre",
        "10": "Ouate de cellulose",
        "11": "Paille",
        "12": "Laines textiles",
        "13": "Autre matériaux biosourcés",
        "14": "Mix : Laine minérale / biosourcé"
    },
    "mur_revetement_ext": {
        "0": "Autre",
        "1": "Enduit simple",
        "2": "Enduit isolant",
        "3": "Peinture",
        "4": "Bardage métallique",
        "5": "Bardage bois",
        "6": "Bardage composite"
    },
    "type_fondation": {
        "0": "Autre",
        "1": "Superficielle: semelles filantes",
        "2": "Superficielle: plots",
        "3": "Superficielle: radier",
        "4": "Superficielle: micro-pieux",
        "5": "Profonde: pieux",
        "6": "Profonde: parois"
    },
    "type_plancher": {
        "0": "Autre",
        "1": "Poutrelles-hourdis",
        "2": "Bois",
        "3": "Collaborant",
        "4": "Prédalle",
        "5": "Dalle pleine"
    },
    "plancher_mode_isolation": {
        "0": "Autre",
        "1": "Sous face",
        "2": "Sous chape",
        "3": "Entre solive",
        "4": "Duo (sous face et chape)"
    },
    "plancher_nature_isolant": {
        "0": "Autre",
        "1": "Polystyrène Expansé (PSE)",
        "2": "Polystyrène Extrudé (XPS)",
        "3": "Polyuréthane (PU)",
        "4": "Laine de roche (LR)",
        "5": "Laine de verre (LV)",
        "6": "Produits réfléchissant",
        "7": "Laine de bois",
        "8": "Laine de lin",
        "9": "Laine de chanvre",
        "10": "Ouate de cellulose",
        "11": "Paille",
        "12": "Laines textiles",
        "13": "Autre matériaux biosourcés",
        "14": "Mix : Laine minérale / biosourcé"
    },
    "plancher_nature_espace": {
        "0": "Autre",
        "1": "Vide sanitaire",
        "2": "Terre-plein",
        "3": "Sous-sol",
        "4": "Extérieur",
        "5": "Parking"
    },
    "type_toiture": {
        "1": "Monopente",
        "2": "2 pans",
        "3": "3 pans et plus",
        "4": "Terrasse non accessible",
        "5": "Terrasse accessible"
    },
    "toiture_mode_isolation": {
        "0": "Autre",
        "1": "Sarking",
        "2": "En combles perdus",
        "3": "Sous rampants",
        "4": "Isolation conventionnelle (toiture-terrasse)",
        "5": "Isolation inversée (toiture-terrasse)"
    },
    "toiture_nature_isolant": {
        "0": "Autre",
        "1": "Polystyrène Expansé (PSE)",
        "2": "Polystyrène Extrudé (XPS)",
        "3": "Polyuréthane (PU)",
        "4": "Laine de roche (LR)",
        "5": "Laine de verre (LV)",
        "6": "Produits réfléchissant",
        "7": "Laine de bois",
        "8": "Laine de lin",
        "9": "Laine de chanvre",
        "10": "Ouate de cellulose",
        "11": "Paille",
        "12": "Laines textiles",
        "13": "Autre matériaux biosourcés",
        "14": "Mix : Laine minérale / biosourcé"
    },
    "toiture_vegetalisee": {
        "0": "non",
        "1": "oui"
    },
    "toiture_couverture": {
        "0": "Autre",
        "1": "Tuile",
        "2": "Ardoise",
        "3": "Tôles bac acier",
        "4": "Plancher béton",
        "5": "Bois",
        "6": "Verre",
        "7": "Matériaux biosourcés"
    },
    "type_menuiserie": {
        "0": "Autres",
        "1": "Bois",
        "2": "Mixte (Bois / Alu)",
        "3": "PVC",
        "4": "Alu à rupture de pont"
    },
    "type_pm": {
        "0": "Sans protection mobile",
        "1": "Volet battant",
        "2": "Volet roulant",
        "3": "Store vénitien/enroulable",
        "4": "Brise Soleil Orientable"
    },
    "stockage_electricite": {
        "0": "Autre",
        "1": "Aucun",
        "2": "Batteries"
    },
    "gestion_active": {
        "0": "Absence de GTB",
        "1": "Présence de GTB"
    },
    "type_eclairage": {
        "0": "Autre",
        "1": "Halogène",
        "2": "Fluorocompacte",
        "3": "Fluorescente",
        "4": "Halogénures métalliques",
        "5": "Sodium haute pression",
        "6": "LED"
    }
}