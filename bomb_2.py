# ba_meta require api 9
# ba_meta export babase.Plugin

"""
    Bomb Radius Visualizer (Client-Side) by TheMikirog, modified for all servers.

    This version works even when you join other people's servers,
    because it only adds visual effects locally without touching server logic.
"""

from __future__ import annotations
import babase
import bascenev1 as bs


class BombRadiusVisualizer(babase.Plugin):
    def __init__(self):
        # Run a repeating timer to check for bombs in the scene.
        bs.timer(0.1, self._scan_for_bombs, repeat=True)
        self._processed_ids: set[int] = set()

    def _scan_for_bombs(self):
        # Loop through all nodes in the scene.
        for node in bs.getnodes():
            if node.type == 'bomb':
                # Use the node's unique id to avoid reprocessing.
                if id(node) not in self._processed_ids:
                    self._processed_ids.add(id(node))
                    self._add_visuals(node)

    def _add_visuals(self, bomb_node):
        # Try to get blast radius; default to 2.0 if not available.
        blast_radius = getattr(bomb_node, 'blast_radius', 2.0)

        # --- Red filled circle ---
        radius_visualizer = bs.newnode(
            'locator',
            owner=bomb_node,
            attrs={
                'shape': 'circle',
                'color': (1, 0, 0),
                'opacity': 0.05,
                'draw_beauty': False,
                'additive': False
            }
        )
        bomb_node.connectattr('position', radius_visualizer, 'position')

        bs.animate_array(
            radius_visualizer, 'size', 1, {
                0.0: [0.0],
                0.2: [blast_radius * 2.2],
                0.25: [blast_radius * 2.0]
            }
        )

        # --- Yellow outline circle ---
        radius_outline = bs.newnode(
            'locator',
            owner=bomb_node,
            attrs={
                'shape': 'circleOutline',
                'size': [blast_radius * 2.0],
                'color': (1, 1, 0),
                'draw_beauty': False,
                'additive': True
            }
        )
        bomb_node.connectattr('position', radius_outline, 'position')

        bs.animate(
            radius_outline, 'opacity', {
                0.0: 0.0,
                0.4: 0.1
            }
        )
