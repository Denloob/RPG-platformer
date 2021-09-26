import xml.etree.ElementTree as ElTree

with open('main.tsx') as f:
    tree = ElTree.fromstring(f.read())
data = tree.findall('tile')
images = tree.findall('tile/image')

for i, g in zip(data, images):
    print(f"elif tile == '{i.get('id')}':\n    ... #  {g.get('source').replace('../Tiles/frames/', '')}")
