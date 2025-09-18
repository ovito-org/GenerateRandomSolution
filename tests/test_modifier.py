import numpy as np
import pytest
from ovito.data import DataCollection
from ovito.io import import_file
from ovito.modifiers import ExpressionSelectionModifier

from GenerateRandomSolution import GenerateRandomSolution


@pytest.fixture
def import_data():
    pipe = import_file("examples/fcc.lmp")
    yield pipe.compute()


def test_default_settings(import_data: DataCollection):
    data = import_data
    data.apply(GenerateRandomSolution())
    # fmt: off
    expected = np.array([
        2,2,1,2,1,2,1,1,2,2,1,2,1,2,1,1,2,1,1,2,1,2,1,1,2,2,1,2,2,1,1,1,1,
        2,2,1,2,1,2,1,2,2,1,2,1,1,1,1,2,2,2,1,2,2,1,2,1,2,1,2,1,1,1,2,2,1,
        1,2,1,2,2,1,1,2,2,2,2,1,2,1,1,1,2,1,2,1,1,2,1,2,2,2,1,2,2,1,1,2,2,
        2,2,1,2,2,2,2,1,2,2,2,2,1,1,2,2,1,1,1,1,1,2,2,1,1,1,1,1,1,1,2,2,2,
        1,2,2,1,2,2,1,1,2,1,1,1,1,1,2,2,2,2,2,2,1,1,1,2,1,1,2,1,2,2,1,2,2,
        1,1,2,1,1,2,2,2,1,1,2,1,2,2,2,2,1,1,1,1,2,2,1,1,2,1,1,2,1,1,1,1,2,
        1,2,2,1,2,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1,2,2,2,2,2,2,1,1,2,1,1,
        2,1,2,2,2,2,2,1,1,1,2,2,1,2,2,1,2,1,1,2,1,1,2,2,2,
        ])
    # fmt: on
    assert np.all(data.particles["Particle Type"] == expected)


def test_additional_types(import_data: DataCollection):
    data = import_data
    data.apply(
        GenerateRandomSolution(concentrations=[0.1, 0.1, 0.2, 0.2, 0.3, 0.1], seed=1323)
    )
    # fmt: off
    expected = np.array([
        1,6,5,4,5,4,5,5,3,4,1,1,4,3,4,4,5,4,3,5,5,5,5,4,1,2,3,1,5,1,6,6,3,
        1,5,5,5,3,3,4,2,6,3,4,3,3,5,4,5,6,2,3,4,2,4,3,3,5,4,3,3,2,4,5,2,4,
        5,4,5,6,3,3,6,3,3,1,3,5,6,6,6,4,4,3,4,4,4,2,6,5,5,5,5,3,1,5,6,5,5,
        1,3,1,6,6,5,5,4,4,5,4,2,1,2,5,3,6,5,5,5,2,5,6,4,5,3,5,1,1,2,2,2,2,
        1,6,3,5,1,3,4,4,3,2,2,4,5,5,3,5,4,5,4,5,6,3,2,5,4,3,3,2,3,5,5,5,6,
        5,5,3,3,3,6,4,3,4,3,5,6,1,4,5,5,5,3,3,5,4,4,1,5,4,4,3,1,4,2,4,4,5,
        4,2,1,3,5,3,2,5,5,3,3,5,1,3,5,5,4,5,4,1,3,4,2,4,5,1,5,5,1,5,5,5,3,
        3,4,5,3,5,4,5,3,1,6,2,4,2,3,6,6,1,5,4,5,4,5,5,6,2
        ])
    # fmt: on
    assert np.all(data.particles["Particle Type"] == expected)


def test_same_seed(import_data: DataCollection):
    data = import_data.clone()
    data.apply(GenerateRandomSolution(seed=1323))
    expected = np.array(data.particles["Particle Type"])
    data = import_data.clone()
    data.apply(GenerateRandomSolution(seed=1323))
    assert np.all(data.particles["Particle Type"] == expected)


def test_different_seed(import_data: DataCollection):
    data = import_data.clone()
    data.apply(GenerateRandomSolution(seed=1323))
    expected = np.array(data.particles["Particle Type"])
    data = import_data.clone()
    data.apply(GenerateRandomSolution(seed=1234))
    assert np.any(data.particles["Particle Type"] != expected)


def test_selection(import_data: DataCollection):
    data = import_data
    data.apply(ExpressionSelectionModifier(expression="ReducedPosition.X < 0.5"))
    data.apply(
        GenerateRandomSolution(
            only_selected=True, concentrations=[0.1, 0.1, 0.2, 0.2, 0.3, 0.1], seed=1323
        )
    )
    # fmt: off
    expected = np.array([
        3,5,3,1,3,4,5,5,4,1,4,1,1,1,1,1,3,5,3,1,4,1,6,5,2,1,3,1,1,1,1,1,4,
        1,5,3,2,4,4,5,1,1,1,1,1,1,1,1,5,4,3,5,5,6,4,1,5,1,1,1,1,1,1,1,1,5,
        3,4,5,3,2,5,3,1,5,1,1,1,1,1,6,3,5,3,4,4,2,4,1,1,4,1,1,1,1,1,5,5,5,
        2,4,1,1,3,5,1,5,1,1,1,1,1,4,3,4,5,5,4,6,4,1,1,4,1,1,1,1,1,4,2,3,6,
        5,6,3,6,1,1,5,1,1,1,1,1,3,5,4,3,2,3,2,6,3,1,2,1,1,1,1,1,5,3,1,1,3,
        6,5,3,1,1,1,1,1,1,1,1,4,6,5,5,3,4,5,3,1,1,1,1,1,1,1,1,4,5,3,1,4,6,
        6,5,1,1,1,1,1,1,1,1,5,4,5,5,5,1,5,2,2,1,2,1,1,1,1,1,1,5,4,5,4,5,4,
        2,1,1,1,1,1,1,1,1,3,6,3,5,2,6,5,3,1,1,1,1,1,1,1,1
        ])
    # fmt: on
    assert np.all(data.particles["Particle Type"] == expected)
