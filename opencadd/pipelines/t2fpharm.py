"""
T2F-Pharm (Truly Target-Focused Pharmacophore) model.
"""


# Standard library
from typing import Sequence, Union, Optional, Literal, Tuple
from pathlib import Path
# 3rd-party
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
# Self
from opencadd.docking import autogrid
from opencadd.io import pdbqt
from opencadd.io.pdbqt import TYPE_AUTODOCK_ATOM_TYPE, DATA_AUTODOCK_ATOM_TYPE
from opencadd.bindingsite.utils import count_psp_events_from_vacancy_tensor


class T2FPharm:
    """
    Truly Target Focused (T2F) pharmacophore model.
    """

    def __init__(
            self,
            filepath_target_structure: Union[str, Path],
            path_output: Optional[Union[str, Path]] = None,
            type_probes: Sequence[TYPE_AUTODOCK_ATOM_TYPE] = ("A", "C", "HD", "OA"),
            coords_grid_center: Union[Tuple[float, float, float], Literal["auto"]] = "auto",
            spacing_grid_points: float = 0.6,
            dims_grid: Optional[Tuple[float, float, float]] = (16, 16, 16),
            npts: Optional[Tuple[int, int, int]] = None,
    ):
        """
        Get interaction energies between the target structure and each of the input probe types
        (plus electrostatic and desolvation energies), calculated using AutoGrid4 at every point
        on a regular (i.e. evenly spaced) cuboid grid, placed on (usually the binding pocket of)
        the target structure, as defined by the input arguments.


        Parameters
        ----------
        filepath_target_structure : str | pathlib.Path
            Path to the input PDBQT file containing the target structure.
        path_output : str | pathlib.Path, Optional, default: None
            An output path to store the results. If not provided, the output files will be
            stored in the same folder as the input file. If a non-existing path is given,
            a new directory will be created with all necessary parent directories.
        type_probes : Sequence[Literal]
            AutoDock-defined atom types (e.g. "A", "C", "HD", "N", "NA", "OA", "SA", "Cl") of
            the probes, for which interaction energies must be calculated.
            For a full list of atom types, see `opencadd.io.pdbqt.DATA_AUTODOCK_ATOM_TYPE`.
        coords_grid_center : tuple[float, float, float] | "auto"
            Coordinates (x, y, z) of the center of grid, in the reference frame of the target
            structure, in Ångstrom (Å). If set to "auto", AutoGrid automatically centers
            the grid on the target structure's center.
        spacing_grid_points : float, Optional, default: 0.6
            The grid-point spacing, i.e. distance between two adjacent grid points in Å.
            Grid points are orthogonal and uniformly spaced in AutoGrid4, i.e. this value is
            used for all three dimensions.
        dims_grid : tuple[float, float, float], Optional, default: (16, 16, 16)
            Length of the grid (in Å), along x-, y-, and z-axis, respectively.
        npts : tuple[float, float, float], Optional, default: None
            Number of grid points along x-, y-, and z-axis respectively (loosely defined; for an
            accurate definition, see function `opencadd.docking.autogrid.routine_run_autogrid`).
            If not provided, this will be automatically calculated from input arguments
            `dims_grid` and `spacing_grid_points`, since AutoGrid4 actually requires
            `coords_grid_center`, `spacing_grid_points` and `npts`, in order to define a grid.
            Notice that since `npts` values can only be even integers, calculating `npts` may
            result in a grid that is slightly larger than the input dimensions (for more info,
            see the function `opencadd.docking.autogrid.calculate_npts`). Therefore, if this
            argument is provided, the `dims_grid` argument will be ignored.
        """
        # Verify the input file is an existing PDBQT file and assign output path.
        filepath_target = Path(filepath_target_structure)
        if not filepath_target.is_file():
            raise ValueError("Input filepath does not point to a file.")
        try:
            df_pdbqt = pdbqt.parse_pdbqt(filepath_pdbqt=filepath_target)["ATOM"]
        except Exception as e:
            raise ValueError("Could not parse the input PDBQT file.") from e
        if path_output is None:
            path_output = filepath_target.parent / filepath_target.stem
        else:
            path_output = Path(path_output)
            path_output.mkdir(parents=True, exist_ok=True)
        # Verify that all input probe types are valid AutoDock atom types
        type_probes = np.array(type_probes)
        probe_is_invalid = np.isin(
            element=type_probes,
            test_elements=DATA_AUTODOCK_ATOM_TYPE.type.values,
            invert=True
        )
        if np.any(probe_is_invalid):
            raise ValueError(
                f"The following `type_probes` are not valid AutoDock atom types: "
                f"{type_probes[probe_is_invalid]}"
            )
        # Set instance attributes.
        self._filepath_target: Path = filepath_target
        self._path_output: Path = path_output
        self._type_probes: np.ndarray = type_probes
        self._spacing_grid_points: float = spacing_grid_points
        self._df_pdbqt: pd.DataFrame = df_pdbqt
        self._type_energy_grids: np.ndarray = np.concatenate([type_probes, ["e", "d"]])
        # Calculate grid energies using AutoGrid4
        self._grid: np.ndarray = autogrid.routine_run_autogrid(
            receptor=self._filepath_target,
            gridcenter=coords_grid_center,
            npts=npts if npts is not None else autogrid.calculate_npts(
                dimensions_pocket=dims_grid,
                spacing=spacing_grid_points
            ),
            spacing=spacing_grid_points,
            ligand_types=type_probes,
            path_output=self._path_output / self._filepath_target.stem
        )
        return

    @property
    def grid(self):
        """
        The complete grid.

        Returns
        -------
        numpy.ndarray
        A 4-dimensional array, where the first three dimensions represent the grid points,
        and the last dimension contains the data for each grid point. It is the direct
        return value of the function `opencadd.docking.autogrid.routine_run_autogrid`;
        for more information, see the documentation of that function.
        """
        return self._grid

    def calculate_vacancy_from_energy(
            self,
            energy_refs: Sequence[Union[TYPE_AUTODOCK_ATOM_TYPE, Literal["e", "d"]]],
            energy_cutoff: float = +0.6,
            mode: Optional[Literal["max", "min", "avg", "sum"]] = "sum",
            return_copy: bool = False,
    ) -> Optional[np.ndarray]:
        """
        Calculate whether each grid point is vacant (or occupied by a target atom), based on given
        reference energy types, and a cutoff value.

        Parameters
        ----------
        energy_refs : Sequence[Literal]
            Grid-point energy value(s) to take as reference. These can be from the probe
            types for which energy grids were calculated (i.e. elements of input argument
            `type_probes` in method `calculate_energy_grid`), plus "e" and "d", referring to the
            electrostatic potential, and desolvation energy grids, respectively.
        energy_cutoff : float, Optional, default: +0.6
            Cutoff value for energy; grid points with energies lower than cutoff are considered
            vacant.
        mode: Literal["max", "min", "avg", "sum"], Optional, default: "sum"
            If more than one energy type is inputted in `energy_ref`, this parameter defines how
            those different energy values must be processed, before comparing with the cutoff
            value. If only one energy type is entered, then this parameter is ignored.
        return_copy : bool, Optional, default: False
            Whether to also return a copy of the calculated grid values (when True),
            or only store internally (when False).

        Returns
        -------
        grid_vacancy : numpy.ndarray, Optional, default: None
            A 3-dimensional boolean array matching the dimensions of the energy grid,
            indicating whether each grid point is vacant (True), or occupied (False).
            Thus, the vacant grid points can easily be indexed using boolean indexing with this
            array, i.e.: `grid[grid_vacancy]`.

            Only when the input parameter `return_copy` is set to True, a copy of the calculated
            vacancy grid will be returned, otherwise it is stored internally for easier
            further processing.
        """
        # The reducing operations corresponding to each `mode`:
        reducing_op = {"max": np.max, "min": np.min, "avg": np.mean, "sum": np.sum}
        # Depending on whether one or several reference energies were given, transform the input
        # into numpy array and verify `mode` is valid if several energies are given.
        if isinstance(energy_refs, Sequence):
            energy_refs = np.array(energy_refs)
            if mode not in reducing_op:
                raise ValueError("Input argument `mode` not recognized.")
        else:
            energy_refs = np.array([energy_refs])
        # Verify that all given reference energy types are already calculated
        not_calculated = np.isin(energy_refs, self._type_energy_grids, invert=True)
        if np.any(not_calculated):
            raise ValueError(
                f"The following energy grids were not calculated: {energy_refs[not_calculated]}"
            )
        # Take the subgrid corresponding to given energy references
        subgrid_ref = self._grid[..., np.isin(self._type_energy_grids, energy_refs)]
        # If only one energy reference is selected, take that,
        if subgrid_ref.shape[-1] == 1:
            energy_vals = subgrid_ref
        # otherwise reduce the given references using the given operation.
        else:
            energy_vals = reducing_op[mode](subgrid_ref, axis=-1)
        # Apply cutoff
        self._grid_vacancy = energy_vals < energy_cutoff
        return self._grid_vacancy.copy() if return_copy else None

    def calculate_buriedness_from_psp_count(
            self,
            num_directions: Literal[3, 7, 13] = 7,
            psp_len_max: float = 10.0,
            psp_count_min: int = 4,
            return_copy: bool = False,
    ) -> Optional[np.ndarray]:
        """
        Calculate whether each grid point is buried inside the target structure or not, based on
        counting the number of protein-solvent-protein (PSP) events for each point, and applying
        a cutoff.

        Notice that before using this method, a vacancy grid must be calculated using the method
        `calculate_vacancy_from_energy`.

        Parameters
        ----------
        num_directions : Literal[3, 7, 13], Optional, default: 7
            Number of directions to look for PSP events for each grid point. Directions are
            all symmetric around each point, and each direction entails both positive and
            negative directions, along an axis. Directions are defined in a 3x3x3 unit cell,
            i.e. for each point, there are 26 neighbors, and thus max. 13 directions.
            Options are:
            3: x-, y- and z-directions
            7: x, y, z, and four 3d-diagonals (i.e. with absolute unit vector [1, 1, 1])
            13: x, y, z, four 3d-diagonals, and six 2d-diagonals (e.g. [1, 1, 0])
        psp_len_max : float, Optional, default: 10.0
            Maximum acceptable distance for a PSP event, in Ångstrom (Å).
        psp_count_min : int, Optional, default: 4
            Minimum required number of PSP events for a grid point, in order to count as buried.
        return_copy : bool, Optional, default: False
            Whether to also return a copy of the calculated grid values (when True),
            or only store internally (when False).

        Returns
        -------
        grid_buriedness : numpy.ndarray, Optional, default: None
            A 3-dimensional array matching the dimensions of the energy grid,
            indicating whether each grid point is buried (True), or exposed (False).
            Thus, the buried grid points can easily be indexed using boolean indexing with this
            array, i.e.: `grid[grid_buriedness]`.

            Only when the input parameter `return_copy` is set to True, a copy of the calculated
            buriedness grid will be returned, otherwise it is stored internally for easier
            further processing.
        """
        grid_psp_counts = count_psp_events_from_vacancy_tensor(
            grid_vacancy=self._grid_vacancy,
            spacing_grid_points=self._spacing_grid_points,
            num_directions=num_directions,
            psp_len_max=psp_len_max
        )
        self._grid_buriedness = grid_psp_counts >= psp_count_min
        return self._grid_buriedness.copy() if return_copy else None



