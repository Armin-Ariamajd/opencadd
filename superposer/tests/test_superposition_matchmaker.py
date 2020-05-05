"""
Tests for superposer.superposition.matchmaker
"""

import pytest
from superposer.api import Structure
from superposer.superposition.matchmaker import MatchMakerAligner


def test_matchmaker_instantiation():
    aligner = MatchMakerAligner()


def test_matchmaker_calculation():
    aligner = MatchMakerAligner()
    structures = [Structure.from_pdbid(pdb_id) for pdb_id in ["4u3y", "4u40"]]
    result = aligner.calculate(structures)

    # Check API compliance
    assert "superposed" in result
    assert "scores" in result
    assert "rmsd" in result["scores"]
    assert "metadata" in result

    # Check RMSD values
    # TODO: pytest.approx is not working reliably - check with Dennis too, he has the same problem
    assert pytest.approx(result["scores"]["rmsd"], 1.989)
