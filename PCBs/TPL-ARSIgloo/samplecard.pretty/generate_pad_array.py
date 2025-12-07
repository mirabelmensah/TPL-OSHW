import os, sys
import numpy as np
import KicadModTree as kmt

from KicadModTree.Vector import Vector2D
from KicadModTree import Pad
# from kigadgets

class objview(dict):
  def __getattr__(self, attr):
    return self.__getitem__(attr)
  def __setattr__(self, attr, val):
    return self.__setitem__(attr, val)

u_mm = 40  # Multiply a mm value to get mils

geom = objview(
  width=7 / u_mm,
  pitch=15 / u_mm,
  length=50 / u_mm,
  mask_cov=0.1,
)

opts = objview(
  back_pair=True
)

num_pads = 20

# rect = R(width, length, F.Cu)
# rect = R(width + mask_cov, length + mask_cov, F.Mask)

name = f'WBpadArray-N{num_pads}-P{u_mm*geom.pitch:.1f}-W{u_mm*geom.width:.1f}'
name = name.replace('.0', '')
name = name.replace('.', '_')
if opts.back_pair:
  name += '-paired'

kmod = kmt.Footprint(name)
kmod.setDescription('Wirebond Pad Array')
kmod.append(kmt.Text(type='value', text=name, at=[-2, 0], rotation=90, layer='F.Fab'))
ref_text = kmt.Text(type='reference', text='REF**', at=[2, 0], rotation=270, layer='F.SilkS')
kmod.append(ref_text)

ipad = 1
tot_wid = geom.pitch * (num_pads - 1)
y0 = - tot_wid / 2

for ipad in range(num_pads):
  at = [0, y0 + geom.pitch * ipad]
  kmod.append(Pad(number=ipad+1, at=at,
    type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
    size=[geom.length, geom.width],
    layers=['F.Cu', 'F.Mask'])
  )

if opts.back_pair:
  for ipad in range(num_pads):
    at = [0, -1*(y0 + geom.pitch * ipad)]
    kmod.append(Pad(number=ipad+1+num_pads, at=at,
      type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
      size=[geom.length, geom.width],
      layers=['B.Cu'])
    )

footprint_lib = os.path.join(os.path.dirname(__file__))
def write(kicad_mod, filename=None):
    # write file
    if filename is None:
        filename = kicad_mod.name
    if not filename.endswith('.kicad_mod'):
        filename += '.kicad_mod'
    file_handler = kmt.KicadFileHandler(kicad_mod)
    file_handler.writeFile(os.path.join(footprint_lib, filename))

write(kmod)
