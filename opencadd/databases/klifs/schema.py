"""
opencadd.databases.klifs.schema

Defines schema used across the klifs module.
"""

import pandas as pd


LOCAL_COLUMNS_MAPPING = {
    "klifs_export": {
        "NAME": "kinase.names",  # HGNC and KLIFS (?) name  TODO where is KLIFS name from?
        "FAMILY": "kinase.family",
        "GROUPS": "kinase.group",
        "PDB": "structure.pdb_id",
        "CHAIN": "structure.chain",
        "ALTERNATE_MODEL": "structure.alternate_model",
        "SPECIES": "species.klifs",
        "LIGAND": "ligand.name",
        "PDB_IDENTIFIER": "ligand.expo_id",
        "ALLOSTERIC_NAME": "ligand_allosteric.name",
        "ALLOSTERIC_PDB": "ligand_allosteric.expo_id",
        "DFG": "structure.dfg",
        "AC_HELIX": "structure.ac_helix",
    },
    "klifs_overview": {
        "species": "species.klifs",
        "kinase": "kinase.klifs_name",
        "pdb": "structure.pdb_id",
        "alt": "structure.alternate_model",
        "chain": "structure.chain",
        "orthosteric_PDB": "ligand.expo_id",
        "allosteric_PDB": "ligand_allosteric.expo_id",
        "rmsd1": "structure.rmsd1",
        "rmsd2": "structure.rmsd2",
        "qualityscore": "structure.qualityscore",
        "pocket": "structure.pocket",
        "resolution": "structure.resolution",
        "missing_residues": "structure.missing_residues",
        "missing_atoms": "structure.missing_atoms",
        "full_ifp": "interaction.fingerprint",
        "fp_i": "structure.fp_i",
        "fp_ii": "structure.fp_ii",
        "bp_i_a": "structure.bp_i_a",
        "bp_i_b": "structure.bp_i_b",
        "bp_ii_in": "structure.bp_ii_in",
        "bp_ii_a_in": "structure.bp_ii_a_in",
        "bp_ii_b_in": "structure.bp_ii_b_in",
        "bp_ii_out": "structure.bp_ii_out",
        "bp_ii_b": "structure.bp_ii_b",
        "bp_iii": "structure.bp_iii",
        "bp_iv": "structure.bp_iv",
        "bp_v": "structure.bp_v",
    },
}

REMOTE_COLUMNS_MAPPING = {
    # Information.get_kinase_names()
    "kinases_all": {
        "kinase_ID": "kinase.klifs_id",
        "name": "kinase.klifs_name",  # NEW! Manning name or (if missing) UniProt gene name
        "full_name": "kinase.full_name",  # Manning name or (if missing) UniProt gene name
        "gene_name": "kinase.gene_name",  # RENAMED! HGNC or MGI name
        "accesion": "kinase.uniprot",  # NEW! UniProt accession
        "species": "species.klifs",
    },
    # Information.get_kinase_information()
    "kinases": {
        "kinase_ID": "kinase.klifs_id",
        "name": "kinase.klifs_name",  # NEW! Manning name or (if missing) UniProt gene name
        "gene_name": "kinase.gene_name",  # RENAMED! HGNC or MGI name
        "family": "kinase.family",
        "group": "kinase.group",
        "kinase_class": "kinase.class",
        "species": "species.klifs",
        "full_name": "kinase.full_name",  # Manning name or (if missing) UniProt gene name
        "uniprot": "kinase.uniprot",  # UniProt accession
        "iuphar": "kinase.iuphar",
        "pocket": "kinase.pocket",
    },
    # Ligands.get_ligands_list
    "ligands": {
        "ligand_ID": "ligand.klifs_id",
        "PDB-code": "ligand.expo_id",
        "Name": "ligand.name",
        "SMILES": "ligand.smiles",
        "InChIKey": "ligand.inchikey",
    },
    # Structures.get_structure_list()
    # Structures.get_structure_lists()
    "structures": {
        "structure_ID": "structure.klifs_id",
        "kinase": "kinase.klifs_name",
        "species": "species.klifs",
        "kinase_ID": "kinase.klifs_id",
        "pdb": "structure.pdb_id",
        "alt": "structure.alternate_model",
        "chain": "structure.chain",
        "rmsd1": "structure.rmsd1",
        "rmsd2": "structure.rmsd2",
        "pocket": "structure.pocket",
        "resolution": "structure.resolution",
        "quality_score": "structure.qualityscore",
        "missing_residues": "structure.missing_residues",
        "missing_atoms": "structure.missing_atoms",
        "ligand": "ligand.expo_id",
        "allosteric_ligand": "ligand_allosteric.expo_id",
        "DFG": "structure.dfg",
        "aC_helix": "structure.ac_helix",
        "Grich_distance": "structure.grich_distance",
        "Grich_angle": "structure.grich_angle",
        "Grich_rotation": "structure.grich_rotation",
        "front": "structure.front",
        "gate": "structure.gate",
        "back": "structure.back",
        "fp_I": "structure.fp_i",
        "fp_II": "structure.fp_ii",
        "bp_I_A": "structure.bp_i_a",
        "bp_I_B": "structure.bp_i_b",
        "bp_II_in": "structure.bp_ii_in",
        "bp_II_A_in": "structure.bp_ii_a_in",
        "bp_II_B_in": "structure.bp_ii_b_in",
        "bp_II_out": "structure.bp_ii_out",
        "bp_II_B": "structure.bp_ii_b",
        "bp_III": "structure.bp_iii",
        "bp_IV": "structure.bp_iv",
        "bp_V": "structure.bp_v",
    },
    # Ligands.get_bioactivity_list_id()
    "bioactivities": {
        "pref_name": "kinase.pref_name",
        "accession": "kinase.uniprot",
        "organism": "species.chembl",
        "standard_type": "ligand.bioactivity_standard_type",
        "standard_relation": "ligand.bioactivity_standard_relation",
        "standard_value": "ligand.bioactivity_standard_value",
        "standard_units": "ligand.bioactivity_standard_units",
        "pchembl_value": "ligand.bioactivity_pchembl_value",
    },
    # Interactions.get_interactions_get_IFP()
    "interactions": {
        "structure_ID": "structure.klifs_id",
        "IFP": "interaction.fingerprint",
    },
    # Interactions.get_interactions_get_types()
    "interaction_types": {
        "position": "interaction.id",
        "name": "interaction.name",
    },
    # Interactions.get_interactions_match_residues()
    "pockets": {
        "index": "residue.klifs_id",
        "Xray_position": "residue.id",
        "KLIFS_position": "residue.klifs_region_id",
    },
}

COLUMN_NAMES = {
    "kinase_groups": ["kinase.group"],
    "kinase_families": ["kinase.family"],
    "kinases_all": [
        "kinase.klifs_id",
        "kinase.klifs_name",  # Manning name or (if missing) UniProt gene name
        "kinase.full_name",  # Manning name or (if missing) UniProt gene name
        "kinase.gene_name",  # HGNC or MGI name (TODO check kinase KLIFS IDs: 529, 530)
        "kinase.uniprot",  # UniProt accession
        "species.klifs",
    ],
    "kinases": [
        "kinase.klifs_id",
        "kinase.klifs_name",  # Manning name or (if missing) UniProt gene name
        "kinase.full_name",  # Manning name or (if missing) UniProt gene name
        "kinase.gene_name",  # HGNC or MGI name
        "kinase.family",
        "kinase.group",
        "kinase.class",  # TODO where from?
        "species.klifs",
        "kinase.uniprot",  # UniProt accession
        "kinase.iuphar",
        "kinase.pocket",
    ],
    "ligands": [
        "ligand.klifs_id",
        "ligand.expo_id",
        "ligand.name",
        "ligand.smiles",
        "ligand.inchikey",
    ],
    "structures": [
        "structure.klifs_id",
        "structure.pdb_id",
        "structure.alternate_model",
        "structure.chain",
        "species.klifs",
        "kinase.klifs_id",
        "kinase.klifs_name",  # TODO where from?
        # "kinase.names",  # Excluded, otherwise operations like drop_duplicates() do not work
        "kinase.family",
        "kinase.group",
        "structure.pocket",
        "ligand.expo_id",
        "ligand_allosteric.expo_id",
        "ligand.name",
        "ligand_allosteric.name",
        "structure.dfg",
        "structure.ac_helix",
        "structure.resolution",
        "structure.qualityscore",
        "structure.missing_residues",
        "structure.missing_atoms",
        "structure.rmsd1",
        "structure.rmsd2",
        "structure.front",
        "structure.gate",
        "structure.back",
        "structure.fp_i",
        "structure.fp_ii",
        "structure.bp_i_a",
        "structure.bp_i_b",
        "structure.bp_ii_in",
        "structure.bp_ii_a_in",
        "structure.bp_ii_b_in",
        "structure.bp_ii_out",
        "structure.bp_ii_b",
        "structure.bp_iii",
        "structure.bp_iv",
        "structure.bp_v",
        "structure.grich_distance",
        "structure.grich_angle",
        "structure.grich_rotation",
        "structure.filepath",
    ],
    "bioactivities": [
        # TODO in the future: "kinase.klifs_id"  # Add if added to KLIFS API?
        "kinase.pref_name",
        "kinase.uniprot",
        # TODO in the future: "ligand.klifs_id"  # Add if added to KLIFS API?
        "ligand.bioactivity_standard_type",
        "ligand.bioactivity_standard_relation",
        "ligand.bioactivity_standard_value",
        "ligand.bioactivity_standard_units",
        "ligand.bioactivity_pchembl_value",
        "species.chembl",
    ],
    "interactions": ["structure.klifs_id", "interaction.fingerprint"],
    "interaction_types": ["interaction.id", "interaction.name"],
    "pockets": [
        "residue.klifs_id",
        "residue.id",
        "residue.klifs_region_id",
        "residue.klifs_region",
        "residue.klifs_color",
    ],
    "coordinates": [
        "atom.id",
        "atom.name",
        "atom.x",
        "atom.y",
        "atom.z",
        "residue.id",
        "residue.name",
        "residue.klifs_id",
        "residue.klifs_region_id",
        "residue.klifs_region",
        "residue.klifs_color",
    ],
}

POCKET_KLIFS_REGIONS = [
    (1, "I"),
    (2, "I"),
    (3, "I"),
    (4, "g.l"),
    (5, "g.l"),
    (6, "g.l"),
    (7, "g.l"),
    (8, "g.l"),
    (9, "g.l"),
    (10, "II"),
    (11, "II"),
    (12, "II"),
    (13, "II"),
    (14, "III"),
    (15, "III"),
    (16, "III"),
    (17, "III"),
    (18, "III"),
    (19, "III"),
    (20, "αC"),
    (21, "αC"),
    (22, "αC"),
    (23, "αC"),
    (24, "αC"),
    (25, "αC"),
    (26, "αC"),
    (27, "αC"),
    (28, "αC"),
    (29, "αC"),
    (30, "αC"),
    (31, "b.l"),
    (32, "b.l"),
    (33, "b.l"),
    (34, "b.l"),
    (35, "b.l"),
    (36, "b.l"),
    (37, "b.l"),
    (38, "IV"),
    (39, "IV"),
    (40, "IV"),
    (41, "IV"),
    (42, "V"),
    (43, "V"),
    (44, "V"),
    (45, "GK"),
    (46, "hinge"),
    (47, "hinge"),
    (48, "hinge"),
    (49, "linker"),
    (50, "linker"),
    (51, "linker"),
    (52, "linker"),
    (53, "αD"),
    (54, "αD"),
    (55, "αD"),
    (56, "αD"),
    (57, "αD"),
    (58, "αD"),
    (59, "αD"),
    (60, "αE"),
    (61, "αE"),
    (62, "αE"),
    (63, "αE"),
    (64, "αE"),
    (65, "VI"),
    (66, "VI"),
    (67, "VI"),
    (68, "c.l"),
    (69, "c.l"),
    (70, "c.l"),
    (71, "c.l"),
    (72, "c.l"),
    (73, "c.l"),
    (74, "c.l"),
    (75, "c.l"),
    (76, "VII"),
    (77, "VII"),
    (78, "VII"),
    (79, "VIII"),
    (80, "xDFG"),
    (81, "xDFG"),
    (82, "xDFG"),
    (83, "xDFG"),
    (84, "a.l"),
    (85, "a.l"),
]
POCKET_KLIFS_REGIONS = pd.DataFrame(
    [
        (klifs_id, klifs_region, ".".join([klifs_region, str(klifs_id)]))
        for (klifs_id, klifs_region) in POCKET_KLIFS_REGIONS
    ],
    columns=["residue.klifs_id", "residue.klifs_region", "residue.klifs_region_id"],
)

POCKET_KLIFS_REGION_COLORS = {
    "I": "khaki",
    "g.l": "green",
    "II": "khaki",
    "III": "khaki",
    "αC": "red",
    "b.l": "green",
    "IV": "khaki",
    "V": "khaki",
    "GK": "orange",
    "hinge": "magenta",
    "linker": "cyan",
    "αD": "red",
    "αE": "red",
    "VI": "khaki",
    "c.l": "darkorange",
    "VII": "khaki",
    "VIII": "khaki",
    "xDFG": "cornflowerblue",
    "a.l": "cornflowerblue",
}
