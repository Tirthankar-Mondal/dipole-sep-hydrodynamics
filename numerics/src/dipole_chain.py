"""Dipole-conserving chain: 0110<->1001 active-site dynamics under PBC.

Values are stored as +-1 (+1 <-> '1', -1 <-> '0'). A window starting at
site i is active iff (lattice[i..i+3]) equals PATTERN_A or PATTERN_B; a
move flips an active window between the two patterns, which conserves
both total magnetization and local dipole moment within the window.
"""

import numpy as np

PATTERN_A = (1, -1, -1, 1)
PATTERN_B = (-1, 1, 1, -1)


class DipoleChain:
    """State and update rule for one realization of the chain."""

    def __init__(self, L, density, rng):
        self.L = L
        self.rng = rng

        n_ones = round(density * L)
        values = np.array([1] * n_ones + [-1] * (L - n_ones))
        rng.shuffle(values)
        self.lattice = values

        self.active_sites = []
        self.where = np.full(L, -1)
        for i in range(L):
            if self.is_active(i):
                self._add(i)

    def _window(self, i):
        return [(i + k) % self.L for k in range(4)]

    def is_active(self, i):
        pattern = tuple(self.lattice[s] for s in self._window(i))
        return pattern == PATTERN_A or pattern == PATTERN_B

    def _add(self, j):
        self.active_sites.append(int(j))
        self.where[j] = len(self.active_sites) - 1

    def _remove(self, j):
        idx = self.where[j]
        last = self.active_sites[-1]
        self.active_sites[idx] = last
        self.where[last] = idx
        self.active_sites.pop()
        self.where[j] = -1

    def _flip(self, i):
        sites = self._window(i)
        pattern = tuple(self.lattice[s] for s in sites)
        new = PATTERN_B if pattern == PATTERN_A else PATTERN_A
        for site, val in zip(sites, new):
            self.lattice[site] = val
        return sites

    def step(self):
        """Flip one uniformly-random active window.

        Returns the 4 flipped site indices, or None if no active sites
        remain (the configuration is fully jammed).
        """
        if not self.active_sites:
            return None

        k = self.rng.integers(len(self.active_sites))
        i = self.active_sites[k]
        flipped_sites = self._flip(i)

        affected = [(i + k) % self.L for k in range(-3, 7)]
        for j in affected:
            if self.is_active(j):
                if self.where[j] == -1:
                    self._add(j)
            else:
                if self.where[j] != -1:
                    self._remove(j)

        return flipped_sites
