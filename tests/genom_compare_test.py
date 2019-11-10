import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from src.genom_compare import GenomCompare
from src.errors import InvalidSeqLengthError

import numpy as np
import itertools
import pytest


###################### INITIALIZING MATRIX AND GRAPH #####################
def test_init_matrix_size():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    matrix, _ = gc._initialize_structures(seq1, seq2)
    assert matrix.shape == (5, 6)


def test_init_matrix_values():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    matrix, _ = gc._initialize_structures(seq1, seq2)
    assert np.array_equal(matrix, np.array([[0, -2, -4, -6, -8, -10], [-2, 0, 0, 0, 0, 0], [-4, 0, 0, 0, 0, 0], 
                                            [-6, 0, 0, 0, 0, 0], [-8, 0, 0, 0, 0, 0]]))


def test_init_graph_nodes():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    _, G = gc._initialize_structures(seq1, seq2)
    assert list(G.nodes()) == [(0,0), (1,0), (2,0), (3,0), (4,0), (0,1), (0,2), (0,3), (0,4), (0,5)]


def test_init_graph_edges():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    _, G = gc._initialize_structures(seq1, seq2)
    assert list(G.edges()) == [((1,0), (0,0)), ((2,0), (1,0)), ((3,0), (2,0)), ((4,0), (3,0)), 
                               ((0,1), (0,0)), ((0,2), (0,1)), ((0,3), (0,2)), ((0,4), (0,3)), ((0,5), (0,4))]



#######################  SIMPLE EXAMPLE TESTS ##########################
def test_simple_final_score():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    m, _ = gc.run(seq1, seq2)
    assert m[-1, -1] == 9

def test_simple_matrix_values():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    m, _ = gc.run(seq1, seq2)
    assert np.array_equal(m, np.array([[0, -2, -4, -6, -8, -10], [-2, -4, 3, 1, -1, -3], [-4, -6, 1, 8, 6, 4], 
                                       [-6, -8, -1, 6, 13, 11], [-8, -1, -3, 4, 11, 9]]))

def test_simple_graph_nodes():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    _, G = gc.run(seq1, seq2)
    assert set(G.nodes()) == set(itertools.product(range(5), range(6)))

def test_simple_graph_edges():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    _, G = gc.run(seq1, seq2)
    assert list(G.edges()) == [((1, 0), (0, 0)), ((2, 0), (1, 0)), ((3, 0), (2, 0)), ((4, 0), (3, 0)), ((0, 1), 
                                (0, 0)), ((0, 2), (0, 1)), ((0, 3), (0, 2)), ((0, 4), (0, 3)), ((0, 5), (0, 4)), 
                                ((1, 1), (0, 1)), ((1, 1), (1, 0)), ((1, 2), (0, 1)), ((1, 3), (1, 2)), ((1, 4), 
                                (1, 3)), ((1, 5), (1, 4)), ((2, 1), (1, 1)), ((2, 1), (2, 0)), ((2, 2), (1, 2)), 
                                ((2, 3), (1, 2)), ((2, 4), (2, 3)), ((2, 5), (2, 4)), ((3, 1), (2, 1)), ((3, 1), 
                                (3, 0)), ((3, 2), (2, 2)), ((3, 3), (2, 3)), ((3, 4), (2, 3)), ((3, 5), (3, 4)), 
                                ((4, 1), (3, 0)), ((4, 2), (3, 2)), ((4, 2), (4, 1)), ((4, 3), (3, 3)), ((4, 4), 
                                (3, 4)), ((4, 5), (3, 5)), ((4, 5), (4, 4))]

def test_simple_value_after_order_switch():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    m, _ = gc.run(seq1, seq2)
    v1 = m[-1, -1]
    m, _ = gc.run(seq2, seq1)
    v2 = m[-1, -1]
    assert v1 == v2

############## SAVING ####################

def test_check_number_saved_paths(tmpdir):
    path = tmpdir.join("output.txt")
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    _, saved_paths = gc.run_save(seq1, seq2, path)
    assert saved_paths == 2


def test_check_number_less_saved_paths(tmpdir):
    path = tmpdir.join("output.txt")
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=1, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    _, saved_paths = gc.run_save(seq1, seq2, path)
    assert saved_paths == 1


def test_check_saving(tmpdir):
    path = tmpdir.join("output.txt")
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    _ = gc.run_save(seq1, seq2, path)
    with open(path) as f:
        assert f.read() == 'SCORE = 9\n\n-MAR-S\nSMART-\n\n-MARS-\nSMAR-T\n'


def test_check_saving_less_paths(tmpdir):
    path = tmpdir.join("output.txt")
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=1, max_seq_len=100)
    seq1 = 'MARS'
    seq2 = 'SMART'
    _ = gc.run_save(seq1, seq2, path)
    with open(path) as f:
        assert f.read() == 'SCORE = 9\n\n-MAR-S\nSMART-\n'

def test_low_penalty_gap(tmpdir):
    path = tmpdir.join("output.txt")
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=100)
    seq1 = 'SAM'
    seq2 = 'SUM'
    _ = gc.run_save(seq1, seq2, path)
    with open(path) as f:
        assert f.read() == 'SCORE = 6\n\nS-AM\nSU-M\n\nSA-M\nS-UM\n'

def test_high_penalty_gap(tmpdir):
    path = tmpdir.join("output.txt")
    gc = GenomCompare(same=5, diff=-5, gp=-10, max_paths=100, max_seq_len=100)
    seq1 = 'SAM'
    seq2 = 'SUM'
    _ = gc.run_save(seq1, seq2, path)
    with open(path) as f:
        assert f.read() == 'SCORE = 5\n\nSAM\nSUM\n'


############# SEQUENCE LENGTH ###############

def test_too_long_seq1():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=4)
    seq1 = 'SMART'
    seq2 = 'MARS'
    with pytest.raises(InvalidSeqLengthError):
        gc.run(seq1, seq2)


def test_too_long_seq2():
    gc = GenomCompare(same=5, diff=-5, gp=-2, max_paths=100, max_seq_len=4)
    seq1 = 'MARS'
    seq2 = 'SMART'
    with pytest.raises(InvalidSeqLengthError):
        gc.run(seq1, seq2)



########### MORE COMPLICATED EXAMPLES ################