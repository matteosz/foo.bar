# Disorderly Escape

>Oh no! You've managed to free the bunny workers and escape Commander Lambdas exploding space station, but Lambda's team of elite starfighters has flanked your ship. If you dont jump to hyperspace, and fast, youll be shot out of the sky!

>Problem is, to avoid detection by galactic law enforcement, Commander Lambda planted the space station in the middle of a quasar quantum flux field. In order to make the jump to hyperspace, you need to know the configuration of celestial bodies in the quadrant you plan to jump through. In order to do *that*, you need to figure out how many configurations each quadrant could possibly have, so that you can pick the optimal quadrant through which youll make your jump. 

>There's something important to note about quasar quantum flux fields' configurations: when drawn on a star grid, configurations are considered equivalent by grouping rather than by order. That is, for a given set of configurations, if you exchange the position of any two columns or any two rows some number of times, youll find that all of those configurations are equivalent in that way -- in grouping, rather than order.

Write a function solution(w, h, s) that takes 3 integers and returns the number of unique, non-equivalent configurations that can be found on a star grid w blocks wide and h blocks tall where each celestial body has s possible states. Equivalency is defined as above: any two star grids with each celestial body in the same state where the actual order of the rows and columns do not matter (and can thus be freely swapped around). Star grid standardization means that the width and height of the grid will always be between 1 and 12, inclusive. And while there are a variety of celestial bodies in each grid, the number of states of those bodies is between 2 and 20, inclusive. The solution can be over 20 digits long, so return it as a decimal string.  The intermediate values can also be large, so you will likely need to use at least 64-bit integers.

For example, consider w=2, h=2, s=2. We have a 2x2 grid where each celestial body is either in state 0 (for instance, silent) or state 1 (for instance, noisy).  We can examine which grids are equivalent by swapping rows and columns.

00
00

In the above configuration, all celestial bodies are "silent" - that is, they have a state of 0 - so any swap of row or column would keep it in the same state.

00 00 01 10
01 10 00 00

1 celestial body is emitting noise - that is, has a state of 1 - so swapping rows and columns can put it in any of the 4 positions.  All four of the above configurations are equivalent.

00 11
11 00

2 celestial bodies are emitting noise side-by-side.  Swapping columns leaves them unchanged, and swapping rows simply moves them between the top and bottom.  In both, the *groupings* are the same: one row with two bodies in state 0, one row with two bodies in state 1, and two columns with one of each state.

01 10
01 10

2 noisy celestial bodies adjacent vertically. This is symmetric to the side-by-side case, but it is different because there's no way to transpose the grid.

01 10
10 01

2 noisy celestial bodies diagonally.  Both have 2 rows and 2 columns that have one of each state, so they are equivalent to each other.

01 10 11 11
11 11 01 10

3 noisy celestial bodies, similar to the case where only one of four is noisy.

11
11

4 noisy celestial bodies.

There are 7 distinct, non-equivalent grids in total, so solution(2, 2, 2) would return 7.

## Test Cases

Test Case 1
```ruby
Inputs: w = 2, h = 3, s = 4
Output: 430
```
Test Case 2
```ruby
Inputs: w = 2, h = 2, s = 2
Output: 7
```

## Solution analysis

### Theory behind
The problem can be lead back to find the number of equivalence classes of a matrix (w x h), with entries from the set S = {0,1,2,...,s}, |S| = s+1. 
Substancially, all the possible values of the matrix are the dispositions with repetitions (order matters) of s+1 elements taken in group of w x h. All the possible combinations are, from combinatorics, equal to (s+1)^(w x h). If we consider our upper bound constraints, the maximum number of combinations can reach 13^400 -> infinity for almost all machines.
Luckily, many combinations are equivalent to each others and form a class of equivalency depending on our definition: if, starting from one configuration, by applying a set of permutations of rows and columns we end to another configuration, then we define those 2 configurations as equivalent.
The problem of counting the number of equivalence classes is an application of Polya Enumeration Theorem (see [reference](https://en.wikipedia.org/wiki/P%C3%B3lya_enumeration_theorem)).


Starting from our star grid (i.e. simply a matrix), we can consider the set of all coordinates of the grid as the cartesian product between the sets W={1,2,...,w-1,w} (|W|=w, columns of the grids) and H={1,2,...,h-1,h} (|H|=h, rows of the grid). Let's call this set P: P = W x H.

Now, we define the simmetric groups (see [reference](https://en.wikipedia.org/wiki/Symmetric_group)) of the sets W and H as S_W and S_H. These two sets represent all the possible permutations that can be performed on the sets over which they're respectively defined. From combinatorics, we know that all the possible permutations over a set Y, where |Y|=n, are equal to n!. Consequently, we know that |S_W|=w! and |S_H|=h!.

Then, we define the group G as it follows: G = S_W x S_H.
Each configuration of our grid can be interpreted as a function f:P->S, and we can spot all possible configurations using the notation S^P (set of functions P->S). 
As we want to compute the number of equivalency classes, we need to find the order of the quotient set of S^P by G (Y := |S^P /G|).

To find Y, we use as announced Polya enumeration theorem.
We define as cycle index (see [reference](https://en.wikipedia.org/wiki/Cycle_index)):

![equation](https://latex.codecogs.com/svg.image?Z_G(t_1_,&space;t_2,...,t_n)&space;=&space;\frac{1}{|G|}&space;\sum_{g&space;\in&space;G}&space;t_{1}^{c_1(g)}\cdot\cdot\cdot&space;t_{n}^{c_n(g)})

where n=|P| anc c_k(g) is the number of k-cycles (cycles of length k) of the group element g as a permutation of P.
However, in our configuration, all the s states have the same weight (0), so that we can write a simplified version:

![equation](https://latex.codecogs.com/svg.image?\bg_black&space;Y&space;=&space;|S^P&space;/G|&space;=&space;Z(G,s,s,...,s)&space;=&space;\frac{1}{|G|}&space;\sum_{g&space;\in&space;G}&space;s^{c_k(g)})

Therefore, we need to compute the cycle index of the group G and so of the symmetric groups S_W and S_H.
It's proved that (see [reference](https://franklinvp.github.io/assets/files/WeiXuCycleIndexCartesianProduct.pdf)):

![equation](https://latex.codecogs.com/svg.image?\bg_black&space;Z(A&space;\times&space;B,&space;s_1,s_2,...,s_{n_1}s_{n_2})&space;=&space;Z(A,&space;s_1,...,s_{n_1})&space;\otimes&space;Z(B,&space;s_1,...,s_{n_2}))

For this reason, with a short notation we say that 

![equation](https://latex.codecogs.com/svg.image?\bg_black&space;Z(G)&space;=&space;Z(S_W)&space;\otimes&space;Z(S_H))

and, in particular, considering the type of function f as 

![equation](https://latex.codecogs.com/svg.image?\bg_black&space;f(x_1,...,x_n)&space;=&space;\sum&space;a_{i_1i_2...i_m}x_{1}^{i_1}...x_{n}^{i_n})

![equation](https://latex.codecogs.com/svg.image?f(x_1,...,x_m)\otimes&space;f(x_1,...,x_n)=\sum&space;a_{i_1i_2...i_m}b_{j_1j_2...j_n}\times\prod_{1\leq&space;r\leq&space;m,1\leq&space;s\leq&space;n}&space;(x_{r}^{i_r}\otimes&space;x_{s}^{j_s}))

,where

![equation](https://latex.codecogs.com/svg.image?(x_{r}^{i_r}\otimes&space;x_{s}^{j_s})&space;=&space;x_{lcm(r,s)}^{gcd(r,s)i_rj_s})

So, we define:

![equation](https://latex.codecogs.com/svg.image?\bg_black&space;Z(S_n,&space;s_1,s_2,...,s_n)&space;=&space;\sum_{r_1&plus;2r_2&plus;...&plus;nr_n=n}&space;\frac{s_{1}^{r_1}s_{2}^{r_2}s_{n}^{r_n}}{1^{r_1}r_1!2^{r_2}r_2!...n^{r_n}r_n!})

### Conclusion
Combining the results above, we obtain:

![equation](https://latex.codecogs.com/svg.image?Y=\frac{1}{w!h!}&space;\sum_{i\in&space;PW(W),j\in&space;PW(H)}&space;\frac{w!}{1^{i_1}i_1!2^{i_2}i_2!...w^{i_w}i_w!}\frac{h!}{1^{j_1}j_1!2^{j_2}j_2!...h^{j_h}j_h!}s^{\sum_{a\in&space;i,b\in&space;j}gcd(a,b)})