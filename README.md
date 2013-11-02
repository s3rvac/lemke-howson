lemke-howson - Implementation of the Lemke-Howson algorithm for finding MNE
===========================================================================

A program for computing mixed Nash equilibrium (MNE) in 2-player games by using
the Lemke-Howson algorithm.

Requirements
============

* python 2.5 (http://www.python.org/)

Usage
=====

```
python lh.py < inputgame.txt
```

The program expects two matrices with payoffs on the standard input in the
following format:
```
a11 a12 ... a1N
...
aM1 aM2 ... aMN

b11 b12 ... b1N
...
bM1 bM2 ... bMN
```
`aXY` are payoffs for the first player and `bXY` are payoffs for
the second player.

Sample Games
============

Sample games are in the `sample-games` directory.

Documentation
=============

Run `make` in the `doc` directory to generate the documentation.

Restrictions
============

* the game must be non-degenerative

Author
======

Petr Zemek <s3rvac@gmail.com>, 2009

License
=======

Copyright (C) 2009 Petr Zemek <s3rvac@gmail.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
USA.
