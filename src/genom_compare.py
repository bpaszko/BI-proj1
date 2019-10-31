from .errors import InvalidSeqLengthError

import numpy as np
import networkx as nx


class GenomCompare:
    def __init__(self, same, diff, gp, max_paths, max_seq_len):
        self.same = same
        self.diff = diff
        self.gp = gp
        self.max_seq_len = max_seq_len
        self.max_paths = max_paths
        self.steps = {
            0: ((-1, 0), 'up'),
            1: ((0, -1), 'left'),
            2: ((-1, -1), 'diag'),
        }
        
    def run_save(self, seq1, seq2, output_path):
        matrix, graph = self.run(seq1, seq2)
        value = matrix[-1][-1]
        done = 0
        with open(output_path, 'w') as f:
            f.write(f'SCORE = {value}\n')
            for path in nx.all_simple_paths(graph, source=(len(seq1), len(seq2)), target=(0, 0)):
                if done == self.max_paths:
                    break
                
                seq1_mod, seq2_mod = self._path_to_str(seq1, seq2, path, graph)
                
                f.write('\n')
                f.write(f'{seq1_mod}\n')
                f.write(f'{seq2_mod}\n')

                done += 1
        return value, done

    def run(self, seq1, seq2):
        ok, err = self._check_seq_len(seq1, seq2)
        if not ok:
            raise InvalidSeqLengthError(err)

        matrix, graph = self._initialize_structures(seq1, seq2)

        for i in range(1, len(seq1)+1):
            for j in range(1, len(seq2)+1):
                val, moves = self.compute_value(matrix, seq1, seq2, i, j)
                matrix[i, j] = val
                for move in moves:
                    pos_change, direction = move
                    ancestor = (i + pos_change[0], j + pos_change[1])
                    graph.add_edge((i, j), ancestor)
                    graph[(i, j)][ancestor]['direction'] = direction
        
        return matrix, graph
        
    def compute_value(self, matrix, seq1, seq2, i, j):
        up, left, diag = matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1]
        up_val, left_val = up + self.gp, left + self.gp
        if seq1[i-1] == seq2[j-1]:
            diag_val = diag + self.same  
        else: 
            diag_val = diag + self.diff

        val_arr = np.array([up_val, left_val, diag_val])
        max_val = np.max(val_arr)
        moves = np.nonzero(val_arr == max_val)[0]
        moves = [self.steps[m] for m in moves]
        return max_val, moves
    
    def _check_seq_len(self, seq1, seq2):
        ok = True
        err_msg = f'Invalid sequence length! Maximum allowed length is {self.max_seq_len}. '
        if len(seq1) > self.max_seq_len:
            err_msg += f'Len(seq1) = {len(seq1)}. '
            ok = False
        if len(seq2) > self.max_seq_len:
            err_msg += f'Len(seq2) = {len(seq2)}. '
            ok = False
        return ok, err_msg
 
    def _path_to_str(self, seq1, seq2, path, graph):
        seq1 = '-' + seq1
        seq2 = '-' + seq2
        seq1_mod, seq2_mod = '', ''
        for node1, node2 in zip(path, path[1:]):
            direction = graph[node1][node2]['direction']
            if direction == 'left':
                seq1_mod += '-'
                seq2_mod += seq2[node1[1]]
            elif direction == 'up':
                seq1_mod += seq1[node1[0]]
                seq2_mod += '-'
            elif direction == 'diag':
                seq1_mod += seq1[node1[0]]
                seq2_mod += seq2[node1[1]]
            else: 
                raise RuntimeError(f'Unknown direction: {direction}')
        return seq1_mod[::-1], seq2_mod[::-1]

    def _initialize_structures(self, seq1, seq2):
        # initialize values matrix
        matrix = np.zeros(shape=(len(seq1)+1, len(seq2)+1), dtype=np.int32)
        matrix[0, :] = [self.gp * i for i in range(len(seq2)+1)]
        matrix[:, 0] = [self.gp * i for i in range(len(seq1)+1)]

        # initialize graph
        G = nx.DiGraph()
        G.add_node((0, 0))
        for i in range(1, len(seq1) + 1):
            G.add_node((i, 0))
            G.add_edge((i, 0), (i-1, 0))
            G[(i, 0)][(i-1, 0)]['direction'] = 'up'

        for j in range(1, len(seq2) + 1):
            G.add_node((0, j))
            G.add_edge((0, j), (0, j-1))
            G[(0, j)][(0, j-1)]['direction'] = 'left'
    
        return matrix, G


