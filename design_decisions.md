# Path Finding

Unlike traditional path finding problems, this problem does not prescribe a start or end location but simply that the
path must optimize for highest resource collection and lowest destruction of preserved resources.

Because of this, the best approach (knowing with certainty 30 days into the future) would be a brute force path
calculation from every start location. Brute force would need to be completed for each tile of each day in order to see
what the return of the path is.

This requires the selection of a heuristic for tile choice.
