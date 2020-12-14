"""
opencadd.structure.pocket.klifs.KlifsPocket

Defines a KLIFS (kinase) pocket.
"""

import pandas as pd

from opencadd.databases.klifs import setup_remote
from .core import Pocket


class KlifsPocket(Pocket):
    """
    Extends Pocket to initialize a kinase pocket from a structure KLIFS ID and define standard
    KLIFS regions.
    Refer to Pocket documentation for more information:
    opencadd.structure.pocket.Pocket
    """

    @classmethod
    def from_structure_klifs_id(
        cls, structure_klifs_id, subpockets=None, extension="pdb", klifs_session=None
    ):
        """
        Get a KLIFS pocket (remotely by a structure KLIFS ID) that defines the KLIFS regions and
        subpockets.

        Parameters
        ----------
        structure_klifs_id : int
            Structure KLIFS ID.
        subpockets : dict
            Dictionary with the following keys and values:
            "anchor_residue.klifs_id" : list of int
                List of anchor residues (KLIFS residue IDs) whose centroid defines the subpocket
                center.
            "subpocket.name" : str
                Subpocket name.
            "subpocket.color" : str
                Subpocket color.
        extension : str
            Structure protein data file format. Defaults to PDB format.
        klifs_session : opencadd.databases.klifs.session.Session or None
            Remote or local KLIFS session. If None, a remote session is initialized.

        Returns
        -------
        opencadd.structure.pocket.KlifsPocket
            KLIFS pocket object.
        """

        # Use existing KLIFS session or set up remote session
        if not klifs_session:
            klifs_session = setup_remote()

        # Get pocket and coordinates for a structure (by a structure KLIFS ID)
        pocket = klifs_session.pockets.by_structure_klifs_id(structure_klifs_id)
        text = klifs_session.coordinates.to_text(
            structure_klifs_id, entity="complex", extension=extension
        )

        pocket_3d = cls.from_text(
            text,
            extension,
            pocket["residue.id"].to_list(),
            pocket["residue.klifs_id"].to_list(),
            structure_klifs_id,
        )

        # Add regions
        for (region, color), group in pocket.groupby(
            ["residue.klifs_region", "residue.klifs_color"]
        ):
            pocket_3d.add_region(
                name=region,
                residue_ixs=group["residue.klifs_id"].to_list(),
                color=color,
            )

        # Map residue KLIFS IDs > residue ID
        if subpockets is not None:
            subpockets = pd.DataFrame(subpockets)
            subpockets["anchor_residue.ids"] = subpockets["anchor_residue.klifs_ids"].apply(
                lambda x: pocket[pocket["residue.klifs_id"].isin(x)]["residue.id"].to_list()
            )

            # Add subpockets
            for _, subpocket in subpockets.iterrows():
                pocket_3d.add_subpocket(
                    name=subpocket["subpocket.name"],
                    anchor_residue_ixs=subpocket["anchor_residue.klifs_ids"],
                    color=subpocket["subpocket.color"],
                )

        return pocket_3d
