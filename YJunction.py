from .Euler2 import *


class YJunction(nd.Cell):
    cell_name = "YJunction"
    number = 0  # number of instant initiated

    def __init__(self, width, length, gap, xs=GeneralParams.xs, radius=GeneralParams.radius, arrow=False):
        YJunction.number += 1
        super().__init__(name=YJunction.cell_name+"_"+str(YJunction.number))

        with self as _:
            angle_rad = np.arctan((gap / 2) / length)
            length_start = np.sin(angle_rad)*width/2
            angle = np.rad2deg(angle_rad)
            waveguide = nd.strt(length=length, width=width, xs=xs)
            waveguide_input = nd.strt(width=width, xs=xs, length=length_start).put(-length_start)
            waveguide2_put = waveguide.put(0, 0, angle)
            waveguide1_put = waveguide.put(0, 0, -angle)

            # calculate the angle
            euler2 = Euler2(width=width, angle=angle, radius=radius, xs=xs)
            waveguide_output1 = euler2.put(waveguide1_put.pin["b0"], flip=False)
            waveguide_output2 = euler2.put(waveguide2_put.pin["b0"], flip=True)

            # create pin
            nd.Pin('a0', pin=waveguide_input.pin["a0"]).put()
            nd.Pin('b1', pin=waveguide_output1.pin["b0"]).put()
            nd.Pin('b0', pin=waveguide_output2.pin["b0"]).put()

            if arrow:
                nd.put_stub()


# YJunction(width=0.8, length=10, gap=5).put()
# nd.export_gds(filename="test.gds")
