"""Run with the ManimGX Python: packet groups must not leak after child removal."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import manimgx as m
from networks.motion.packets import PacketDirector, packet


def check(next_kind):
    scene = m.Scene()
    title = m.Text('Keep the title')
    scene.add(title)
    director = PacketDirector(scene, '01')
    director._ensure('network')
    base = director._own(m.Circle(), persistent=True)
    scene.add(base)
    queue = director._own(m.VGroup(*(packet(str(i)) for i in range(5))))
    scene.add(queue)
    leftovers = set(queue[3].get_family() + queue[4].get_family())
    # Removing sent children splits the on-screen group into independent siblings.
    for item in list(queue.submobjects[:3]):
        scene.remove(item)
    assert leftovers.intersection(scene.get_mobject_family_members())
    director._ensure(next_kind)
    present = set(scene.get_mobject_family_members())
    assert not leftovers.intersection(present), 'Queue items 3 and 4 leaked into the next scene'
    assert title in present
    assert (base in present) == (next_kind == 'network')


if __name__ == '__main__':
    for kind in ('network', 'unpack'):
        check(kind)
    print('PASS: split queue children cleared; intended persistent objects and title preserved.')
