from dataclasses import dataclass
from typing import Any, TypeAlias
import random
from logic.resource import Resource, ResourceMap
from abc import ABC, abstractmethod
from logic.world import WORLD_HEIGHT, WORLD_WIDTH


JSON: TypeAlias = dict[str, Any]
Coord: TypeAlias = tuple[int, int]  # (x,y) coordinates
Neighbourhood: TypeAlias = list[tuple[Coord, Resource]]


class Strategy(ABC):
    """An abstract class to define the interface that all movement strategies must implement."""

    @abstractmethod
    def next(self, neighbourhood: Neighbourhood) -> Coord:
        """Given a neighbourhood of resources within the drill's movement range, returns the next move."""
        pass


class MaxStrat(Strategy):
    """Moves the drill to the maximum valued resource in its neighbourhood."""

    def next(self, neighbourhood: Neighbourhood) -> Coord:
        """
        Returns the coordinates of the maximum valued resource in the neighbourhood.
        Args:
            neighbourhood: The neighbourhood to chose a move from.
        Returns:
            The coordinate that the drill should move to.
        """

        max_val: float = float("-inf")
        max_coord: Coord = (0, 0)

        for coords, tile in neighbourhood:
            if tile.value > max_val:
                max_val = tile.value
                max_coord = coords

        return max_coord


class RandomStrat(Strategy):
    """Picks a random next move in the set of neighbours."""

    def next(self, neighbourhood: Neighbourhood) -> Coord:
        """
        Returns random coordinates from the neighbourhood of moves.
        Args:
            neighbourhood: The neighbourhood to chose a move from.
        Returns:
            The coordinate that the drill should move to.
        """

        coords, _ = random.choice(neighbourhood)
        return coords


@dataclass
class Drill:
    x: int
    y: int
    strategy: Strategy
    collected: float = 0
    destroyed: float = 0

    def get_neighbourhood(self, resources: ResourceMap) -> Neighbourhood:
        """
        Gets the neighbouring resource tiles within the drill's range of movement.
        Args:
            resources: The resource map to gather the neighbourhood from.
        Returns:
            A list of (x, y) coordinates and a resource tile that represents the drill's neighbouring tiles.
        """

        neighbourhood = []
        for x in range(-5, 6):
            for y in range(-5, 6):
                nx, ny = self.x + x, self.y + y  # Compute neighbour's x and y coordinates

                # Negative indices are not valid
                if nx < 0 or ny < 0:
                    continue

                # Indices outside of map range are not valid
                if nx > WORLD_WIDTH or ny > WORLD_HEIGHT:
                    continue

                try:
                    # Don't include tiles that cannot be moved to to collect resources from
                    if resources[ny][nx] is not None:
                        neighbourhood.append(((nx, ny), resources[ny][nx]))
                except IndexError:
                    continue

        return neighbourhood

    def move(self, resources: ResourceMap) -> None:
        """
        Moves the drill to its next optimal location using its inherent strategy. This updates the drill's (x,y)
        coordinates.
        Args:
            resources: The resource map for deciding where to move.
        """
        neighbourhood = self.get_neighbourhood(resources)
        cx, cy = self.strategy.next(neighbourhood)  # Get the decided x, y coordinates for the next move
        self.x = cx
        self.y = cy

    def collect(self, resources: ResourceMap) -> None:
        """
        Collects the current obtained resource under the drill.
        Args:
            resources: The resource map for collecting resources from.
        """
        self.collected += resources[self.y][self.x].value  # type: ignore

    def destroy(self, resources: ResourceMap) -> None:
        """
        Destroys the current preserved resource under the drill.
        Args:
            resources: The resource map for collecting resources from.
        """

        if resources[self.y][self.x] is not None:
            self.destroyed += resources[self.y][self.x].value  # type: ignore

    def serialize(self) -> JSON:
        """Serializes the drill into JSON data."""
        return {"x": self.x, "y": self.y, "collected": self.collected, "destroyed": self.destroyed}
