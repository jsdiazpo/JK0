from manim import *
import numpy as np

# manim -pql scene.py PointAnimation
grid = NumberPlane(
    background_line_style={"stroke_width": 1, "stroke_opacity": 0.5})

def align_ld(mob1, mob2, down=1, right=0):
    return mob1.move_to(mob2).align_to(mob2, LEFT).shift(down*DOWN+right*RIGHT)


def clear_all(self):
    # clear all objects
    for mob in self.mobjects:
        self.remove(mob)
        # self.wait(2)

color_u = YELLOW
color_wien = GREEN
color_rj = PURPLE_A
color_p  = YELLOW

# color_q = YELLOW
# color_r = ORANGE
# color_p = TEAL_B
# color_t = GOLD
color_E = YELLOW
color_title = TEAL_A
# color_a = color_q
# color_B = RED_B

# # quantum numbers
# color_n = YELLOW
# color_k = TEAL_B
# color_m = ORANGE
# color_ms= PINK

color_e = ORANGE



class Average_Energy(Scene):
    def construct(self):
        # ==============================================================================
        # <E>
        # ==============================================================================
        str0 = r"$\langle E \rangle$: average energy" #
        txt0 = Tex(str0, font_size=40, 
                   color=color_title).shift(UP)
        txt0[0][:4].set_color(WHITE)
        txt0[0][1].set_color(color_e)
        
        self.wait(1)
        self.play(Write(txt0))
        self.wait(3)






class GaussianDistribution(Scene):
    def construct(self):
        # self.add(grid)
        # Set up the axes
        xmin, xmax = -1, 8
        axes = Axes(
            x_range=[xmin, xmax, 1],
            y_range=[0, 0.5, 0.1],
            axis_config={"color": BLUE}
        ).scale(0.7).shift(UP)

        # Labels for the axes
        x_label = axes.get_x_axis_label(r"x")
        y_label = axes.get_y_axis_label(r"P(x)")

        # Parameters for the Gaussian function
        mean = 3
        std_dev = 1

        # Define the Gaussian function
        def gaussian(x):
            return (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)

        # Plot the Gaussian curve
        gaussian_graph = axes.plot(gaussian, x_range=[xmin, xmax*0.97], color=YELLOW)

        # Mean line
        mean_line = DashedLine(
            start=axes.c2p(mean, 0),
            end=axes.c2p(mean, gaussian(mean)),
            color=RED
        )
        mean_label = MathTex(r"\mu").next_to(mean_line, UP)

        # Standard deviation lines (mean ± std_dev)
        std_lines = VGroup(
            DashedLine(
                start=axes.c2p(mean - std_dev, 0),
                end=axes.c2p(mean - std_dev, gaussian(mean - std_dev)),
                color=GREEN
            ),
            DashedLine(
                start=axes.c2p(mean + std_dev, 0),
                end=axes.c2p(mean + std_dev, gaussian(mean + std_dev)),
                color=GREEN
            )
        )
        std_labels = VGroup(
            MathTex(r"\mu - \sigma").next_to(std_lines[0], UP),
            MathTex(r"\mu + \sigma").next_to(std_lines[1], UP)
        )

        # Add everything to the scene
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(gaussian_graph), run_time=3)
        self.play(Create(mean_line), Write(mean_label))
        self.play(Create(std_lines), Write(std_labels))
        # self.wait(3)

        eq01 = Tex(r"mean: $\mu = \langle x \rangle$", 
                   font_size=40).shift(3.*RIGHT + 3*UP)
        eq01[0][-2].set_color(color_e)
        
        eq02 = Tex(r"variance: $\sigma^2 = \langle x^2 \rangle - \langle x \rangle^2$", 
                   font_size=40)
        eq02[0][-3].set_color(color_e)
        eq02[0][-8].set_color(color_e)
        eq02 = align_ld(eq02, eq01, down=1., right=0.)
        
        eq03 = Tex(r"skewness", font_size=40)
        eq03 = align_ld(eq03, eq02, down=1., right=0.)

        eq04 = Tex(r"kurtosis", font_size=40)
        eq04 = align_ld(eq04, eq03, down=1., right=0.)

        txt01 = Tex(r"(first moment)", color=BLUE_B,
                   font_size=35).shift(-0.2*RIGHT + 3*UP)

        txt02 = Tex(r"(second moment)", color=BLUE_B, font_size=35)
        txt02 = align_ld(txt02, txt01, down=1., right=0.)

        txt03 = Tex(r"(third moment)", color=BLUE_B, font_size=35)
        txt03 = align_ld(txt03, txt02, down=1., right=0.)

        txt04 = Tex(r"(fourth moment)", color=BLUE_B, font_size=35)
        txt04 = align_ld(txt04, txt03, down=1., right=0.)




        self.play(VGroup(*[axes, x_label, y_label,
                           gaussian_graph, mean_line, mean_label,
                           std_lines, std_labels]).animate.scale(0.8).shift(4*LEFT+0.5*DOWN),
                  Write(eq01), Write(eq02), 
                  Write(eq03), Write(eq04))
        self.wait(1)
        self.play(Write(txt01), Write(txt02),
                  Write(txt03), Write(txt04))




        self.wait(4)






class Fluctuations(Scene):    
    def construct(self):
        # self.add(grid)
        # ==============================================================================
        # Fluctuations
        # ==============================================================================
        txt1 = Tex(r"Fluctuations", font_size=40, color=color_title).to_corner(UL)

        str01 = r"\langle\epsilon^2\rangle \equiv \langle E^2\rangle-\langle E\rangle^2"
        eq01 = MathTex(str01, font_size=40)
        eq01[0][1].set_color(color_e)
        eq01[0][6].set_color(color_e)
        eq01[0][-3].set_color(color_e)
        eq01 = align_ld(eq01, txt1, down=1., right=0.5)
        
        
        
        
        txt2 = Tex(r"Average energy", font_size=40, 
                   color=color_title)#.next_to(txt1).shift(5*RIGHT)
        txt2 = align_ld(txt2, eq01, down=1., right=-0.5)

        str02 = r'''\langle E\rangle
                        = \frac{\displaystyle\int_0^\infty\!E\,e^{-\beta E}\,\omega(E)dE}
                                {\displaystyle\int_0^\infty\!e^{-\beta E}\,\omega(E)\,dE}'''
        eq02a = MathTex(str02, font_size=40)
        eq02a[0][1].set_color(color_e)
        eq02a[0][7].set_color(color_E)
        eq02a[0][11].set_color(color_E)
        eq02a[0][14].set_color(color_E)
        eq02a[0][17].set_color(color_E)
        eq02a[0][-1].set_color(color_E)
        eq02a[0][-4].set_color(color_E)
        eq02a[0][-7].set_color(color_E)
        eq02a = align_ld(eq02a, txt2, down=1., right=0.5)
        

        str02b = r'''\langle E^2\rangle
                        = \frac{\displaystyle\int_0^\infty\!E^2\,e^{-\beta E}\,\omega(E)dE}
                                {\displaystyle\int_0^\infty\!e^{-\beta E}\,\omega(E)\,dE}'''
        eq02b = MathTex(str02b, font_size=40)
        eq02b[0][1].set_color(color_e)
        eq02b[0][8].set_color(color_E)
        eq02b[0][13].set_color(color_E)
        eq02b[0][16].set_color(color_E)
        eq02b[0][19].set_color(color_E)
        eq02b[0][-1].set_color(color_E)
        eq02b[0][-4].set_color(color_E)
        eq02b[0][-7].set_color(color_E)
        eq02b = align_ld(eq02b, eq02a, down=2.5, right=0.)

        eq02c = MathTex(r"\beta=1/(kT)", font_size=30).next_to(eq02a).shift(2.5*RIGHT)

        txt2c = Tex(r"$\omega(E)$: density of states with energy $E$", font_size=30)
        txt2c[0][2].set_color(color_E)
        txt2c[0][-1].set_color(color_E)
        txt2c = align_ld(txt2c, eq02c, down=0.6, right=0)

        g02c = VGroup(*[eq02c, txt2c])

        eq03 = MathTex(r"\frac{\partial\langle E\rangle}{\partial\beta}=", font_size=40)
        eq03[0][2].set_color(color_e)
        eq03 = align_ld(eq03, eq01, down=1.8, right=-0.3)
        
        str03b = r"""-\frac{\displaystyle\int_0^\infty\!E^2\,e^{-\beta E}\,\omega(E)dE}
                           {\displaystyle\int_0^\infty\!e^{-\beta E}\,\omega(E)\,dE}"""
        str03c = r"""+\,\,
                \frac{\left(\displaystyle\int_0^\infty\!E\,e^{-\beta E}\,\omega(E)dE\right)^2}
                {\left(\displaystyle\int_0^\infty\!e^{-\beta E}\,\omega(E)\,dE\right)^2}"""
        eq03b = MathTex(str03b, font_size=40).next_to(eq03)
        eq03b[0][4].set_color(color_E)
        eq03b[0][9].set_color(color_E)
        eq03b[0][12].set_color(color_E)
        eq03b[0][15].set_color(color_E)
        eq03b[0][23].set_color(color_E)
        eq03b[0][26].set_color(color_E)
        eq03b[0][29].set_color(color_E) 

        eq03c = MathTex(str03c, font_size=40).next_to(eq03b)
        eq03c[0][5].set_color(color_E)
        eq03c[0][9].set_color(color_E)
        eq03c[0][12].set_color(color_E)
        eq03c[0][15].set_color(color_E)
        eq03c[0][26].set_color(color_E)
        eq03c[0][29].set_color(color_E)
        eq03c[0][32].set_color(color_E)
        

        str04 = r"""\frac{\partial\langle E\rangle}{\partial\beta} = 
                           -\langle E^2\rangle """
        eq04 = MathTex(str04, font_size=40).next_to(eq03)
        eq04[0][2].set_color(color_e)
        eq04[0][10].set_color(color_e)
        eq04[0][-3].set_color(color_e)
        eq04 = align_ld(eq04, eq03, down=1.7, right=0)

        eq04b = MathTex(r"+ \,\,\langle E\rangle^2", font_size=40).next_to(eq04)
        eq04b[0][-3].set_color(color_e)

        str01b = r"""=-\frac{\partial\langle E\rangle}{\partial\beta}"""
        eq01b = MathTex(str01b, font_size=40).next_to(eq01)
        eq01b[0][4].set_color(color_e)

        box01 = SurroundingRectangle(VGroup(*[eq01, eq01b]), buff=.15)

        txt01c = Tex(r"Einstein-Gibbs fluctuation formula", 
                     font_size=30).next_to(eq01b).shift(RIGHT)
        
        str05 = r"""\langle\epsilon^2\rangle
                  =-\frac{\partial T}{\partial\beta}
                    \frac{\partial\langle E\rangle}{\partial T}
                  =kT^2\frac{\partial\langle E\rangle}{\partial T} """
        eq05 = MathTex(str05, font_size=40).next_to(eq01)
        eq05[0][1].set_color(color_e)
        eq05[0][-5].set_color(color_e)
        eq05[0][-16].set_color(color_e)
        eq05 = align_ld(eq05, eq01, down=2, right=0)






        self.play(Write(txt1))
        self.wait(1)
        self.play(Write(eq01))
        self.wait(1)
        # self.play(Write(txt2))
        self.wait(1)
        # self.play(Write(eq02a))
        # self.play(Write(eq02b))
        # self.play(Write(g02c))
        self.play(Write(eq02a), Write(eq02b))
        self.play(Write(g02c))
        self.wait(1)
        self.play(eq02a.animate.scale(0.7).next_to(txt1).shift(3*RIGHT+0.5*DOWN),
                  eq02b.animate.scale(0.7).next_to(txt1).shift(7*RIGHT+0.5*DOWN),
                  FadeOut(g02c),
                  run_time=2)

        box02a_all = SurroundingRectangle(eq02a, buff=.15, color=GOLD, stroke_width=2)
        box03b = SurroundingRectangle(eq03b[0][1:], buff=.15, color=GOLD, stroke_width=2)
        box02b = SurroundingRectangle(eq02b[0][5:], buff=.15, color=GOLD, stroke_width=2)

        box03c = SurroundingRectangle(eq03c[0][1:], buff=.15, color=MAROON, stroke_width=2)
        box02a = SurroundingRectangle(eq02a[0][4:], buff=.15, color=MAROON, stroke_width=2)

        self.wait(1)
        self.play(Write(eq03))
        self.wait(1)
        self.play(Write(box02a_all))
        self.wait(1)
        self.play(Write(eq03b), FadeOut(box02a_all), run_time=3)
        self.wait(1)
        self.play(Write(eq03c), run_time=3)
        self.wait(1)
        self.play(Write(box03b))
        self.wait(1)
        self.play(Write(box02b))
        self.wait(1)
        self.play(Write(eq04))
        self.wait(1)
        self.play(Write(box03c), FadeOut(box03b, box02b))
        self.wait(1)
        self.play(Write(box02a))
        self.wait(1)
        self.play(Write(eq04b))
        self.wait(1)        
        self.play(FadeOut(box03c, box02a, eq03b, eq03, eq03c, eq02a, eq02b))
        self.wait(1)
        self.play(Write(eq01b))
        self.play(Write(box01), run_time=2)
        self.wait(1)        
        self.play(FadeOut(eq04, eq04b))
        self.wait(1)
        self.play(Write(eq05))
        self.wait(1)
        self.play(Write(txt01c))
        self.wait(3)
        




class Fluctuations_Radiation(Scene):    
    def construct(self):
        # self.add(grid)
        self.wait()
        # ==============================================================================
        # <E>
        # ==============================================================================
        txt1 = Tex(r"Energy density per unit frequency:", font_size=40, 
                   color=color_title).to_corner(UL)

        str01 = r"u(\nu, \beta) = \frac{\langle E\rangle}{V \Delta\nu}"
        eq01 = MathTex(str01, font_size=40).next_to(txt1)
        eq01[0][0].set_color(color_E)
        eq01[0][8].set_color(color_e)

        str01b = r"\langle E\rangle = u(\nu, \beta) V \Delta\nu"
        eq01b = MathTex(str01b, font_size=40).next_to(txt1)
        eq01b[0][1].set_color(color_e)
        eq01b[0][4].set_color(color_E)
        eq01b = align_ld(eq01b, txt1, down=1., right=0.5)

        txt1b = Tex(r"Fluctuations of light:", font_size=40, color=color_title)
        txt1b = align_ld(txt1b, txt1, down=2., right=0.)

        str02 = r"""\langle\epsilon^2\rangle =-\frac{\partial\langle E\rangle}{\partial\beta}
                    = -V \Delta\nu \frac{\partial u}{\partial\beta}"""
        eq02 = MathTex(str02, font_size=40).next_to(txt1)
        eq02[0][1].set_color(color_e)
        eq02[0][8].set_color(color_e)
        eq02[0][-4].set_color(color_E)
        eq02 = align_ld(eq02, txt1b, down=1., right=0.5)

        str02b = r"""\langle\epsilon^2\rangle 
                    = -V \Delta\nu \frac{\partial u}{\partial\beta}"""
        eq02b = MathTex(str02b, font_size=40).next_to(txt1).shift(2*LEFT)
        eq02b[0][1].set_color(color_e)
        eq02b[0][-4].set_color(color_E)
        # eq02b = align_ld(eq02b, txt1, down=1., right=0.5)



        self.play(Write(txt1))
        self.play(Write(eq01))
        self.wait(1)
        self.play(Write(eq01b))
        self.wait(1)
        self.play(Write(txt1b))
        self.wait(1)
        self.play(Write(eq02))
        self.wait(1)
        self.play(FadeOut(txt1, eq01),
                  eq01b.animate.shift(UP+8*RIGHT),
                  txt1b.animate.to_corner(UL),
                  Transform(eq02, eq02b))
        self.wait(1)

        # ==============================================================================
        # low frequency (Rayleigh-Jeans)
        # ==============================================================================
        txt3 = Tex(r"Low frequency:", font_size=40, 
                   color=color_title)
        txt3 = align_ld(txt3, txt1, down=1.3, right=0.)

        str03 = r"""u_\text{RJ}
                    = \frac{8\pi\nu^2}{c^3}kT= \frac{8\pi\nu^2}{c^3\beta}"""
        eq03 = MathTex(str03, font_size=40).next_to(txt3)
        eq03[0][1:3].set_color(color_rj)
        eq03[0][0].set_color(color_E)
        # eq03 = align_ld(eq03, txt1, down=1., right=0.3)
        txt3b = Tex(r"(Rayleigh-Jeans)", font_size=40,
                    color=color_rj).next_to(eq03).shift(2*RIGHT)
        
        str03b = r"""\frac{\partial u_\text{RJ}}{\partial\beta} 
                    = -\frac{8\pi\nu^2}{c^3\beta^2} """
        eq03b = MathTex(str03b, font_size=40)
        eq03b[0][1].set_color(color_u)
        eq03b[0][2:4].set_color(color_rj)
        eq03b = align_ld(eq03b, eq03, down=1.2, right=-0.3)

        eq03c = MathTex(r"= -\frac{c^3}{8\pi\nu^2}u_\text{RJ}^2", 
                        font_size=40).next_to(eq03b)
        eq03c[0][-4].set_color(color_u)
        eq03c[0][-2:].set_color(color_rj)

        eq03d = MathTex(r"""= -\frac{c^3}{8\pi\nu^2}
                               \left(\frac{\langle E_\text{RJ}\rangle}
                                          {V\Delta\nu}\right)^2""", 
                        font_size=40).next_to(eq03c)
        eq03d[0][-10].set_color(color_e)
        eq03d[0][-9:-7].set_color(color_rj)

        str04 = r"""\langle\epsilon^2_\text{RJ}\rangle 
                    = \frac{c^3}{8\pi\nu^2\Delta\nu V}\langle E_\text{RJ}\rangle^2"""
        eq04 = MathTex(str04, font_size=40)
        eq04[0][1].set_color(color_e)
        eq04[0][3:5].set_color(color_rj)
        eq04[0][-5].set_color(color_e)
        eq04[0][-4:-2].set_color(color_rj)
        eq04 = align_ld(eq04, eq03b, down=1.2, right=0.1)

        eq04b = MathTex(r"M = \frac{8\pi\nu^2\Delta\nu V}{c^3}", 
                    font_size=40).next_to(eq04).shift(2*RIGHT)
        eq04b[0][0].set_color(color_rj)

        str05 = r"""\frac{\langle\epsilon^2_\text{RJ}\rangle}{\langle E_\text{RJ}\rangle^2} 
                    = \frac{1}{M}"""
        eq05 = MathTex(str05, font_size=40)
        eq05[0][1].set_color(color_e)
        eq05[0][3:5].set_color(color_rj)
        eq05[0][8].set_color(color_e)
        eq05[0][9:11].set_color(color_rj)
        eq05[0][-1].set_color(color_rj)
        eq05 = align_ld(eq05, eq04, down=1.5, right=0.)

        box05 = SurroundingRectangle(eq05, buff=.15)
        
        txt05 = Tex(r"inverse of the number of wave modes", 
                    font_size=30).next_to(eq05).shift(1*RIGHT)
        txt05[0][-9:].set_color(color_rj)

        self.play(Write(txt3))
        # self.wait(1)
        self.play(Write(eq03))
        self.play(Write(txt3b))
        self.wait(1)
        self.play(Write(eq03b))
        self.wait(1)
        self.play(Write(eq03c))
        self.wait(1)
        self.play(Write(eq03d))
        self.wait(1)
        self.play(Write(eq04))
        self.wait(1)
        self.play(Write(eq04b))
        self.wait(1)
        self.play(Write(eq05))
        self.play(Write(box05), Write(txt05), run_time=2)
        self.wait(3)
        self.remove(txt3, eq03, txt3b, eq03b, eq03c, eq03d, 
                    eq04, eq04b, eq05, box05, txt05)
        self.wait(1)
        # ==============================================================================
        # high frequency (Wien)
        # ==============================================================================
        txt3z = Tex(r"High frequency:", font_size=40, 
                   color=color_title)
        txt3z = align_ld(txt3z, txt1, down=1.3, right=0.)

        str03z = r"""u_\text{W}
                    = \frac{8\pi h\nu^3}{c^3}\,e^{-\beta h\nu}"""
        eq03z = MathTex(str03z, font_size=40).next_to(txt3z)
        eq03z[0][1].set_color(color_wien)
        eq03z[0][0].set_color(color_E)
        
        txt3bz = Tex(r"(Wien)", font_size=40,
                    color=color_wien).next_to(eq03z).shift(3*RIGHT)
        
        str03bz = r"""\frac{\partial u_\text{W}}{\partial\beta} 
                    = -\frac{8\pi h^2\nu^4}{c^3}\,e^{-\beta h\nu} """
        eq03bz = MathTex(str03bz, font_size=40)
        eq03bz[0][1].set_color(color_u)
        eq03bz[0][2].set_color(color_wien)
        eq03bz = align_ld(eq03bz, eq03z, down=1.2, right=-0.3)

        eq03cz = MathTex(r"= -h\nu\, u_\text{W}", 
                        font_size=40).next_to(eq03bz)
        eq03cz[0][-2].set_color(color_u)
        eq03cz[0][-1].set_color(color_wien)

        eq03dz = MathTex(r"""= -h\nu\,\frac{\langle E_\text{W}\rangle}
                                          {V\Delta\nu}""", 
                        font_size=40).next_to(eq03cz)
        eq03dz[0][-7].set_color(color_e)
        eq03dz[0][-6].set_color(color_wien)

        str04z = r"""\langle\epsilon^2_\text{W}\rangle 
                    = h\nu\, \langle E_\text{W}\rangle"""
        eq04z = MathTex(str04z, font_size=40)
        eq04z[0][1].set_color(color_e)
        eq04z[0][3].set_color(color_wien)
        eq04z[0][-3].set_color(color_e)
        eq04z[0][-2].set_color(color_wien)
        eq04z = align_ld(eq04z, eq03bz, down=1.2, right=0.1)

        eq04bz = MathTex(r"\langle E_\text{W}\rangle = Nh\nu", 
                    font_size=40).next_to(eq04z).shift(2*RIGHT)
        eq04bz[0][1].set_color(color_e)
        eq04bz[0][2].set_color(color_wien)
        eq04bz[0][-3].set_color(color_wien)

        str05z = r"""\frac{\langle\epsilon^2_\text{W}\rangle}{\langle E_\text{W}\rangle^2} 
                    = \frac{1}{N}"""
        eq05z = MathTex(str05z, font_size=40)
        eq05z[0][1].set_color(color_e)
        eq05z[0][3].set_color(color_wien)
        eq05z[0][7].set_color(color_e)
        eq05z[0][8].set_color(color_wien)
        eq05z[0][-1].set_color(color_wien)
        eq05z = align_ld(eq05z, eq04z, down=1.5, right=0.)

        box05z = SurroundingRectangle(eq05z, buff=.15)
        
        txt05z = Tex(r"inverse of the number of light quanta", 
                    font_size=30).next_to(eq05z).shift(1*RIGHT)
        txt05z[0][-11:].set_color(color_wien)


        self.play(Write(txt3z))
        # self.wait(1)
        self.play(Write(eq03z))
        self.play(Write(txt3bz))
        self.wait(1)
        self.play(Write(eq03bz))
        self.wait(1)
        self.play(Write(eq03cz))
        self.wait(1)
        self.play(Write(eq03dz))
        self.wait(1)
        self.play(Write(eq04z))
        self.wait(1)
        self.play(Write(eq04bz))
        self.wait(1)
        self.play(Write(eq05z))
        self.play(Write(box05z), Write(txt05z), run_time=2)
        self.wait(3)
        # ==============================================================================
        # summary low and high frequency
        # ==============================================================================
        self.play(FadeOut(eq03z, eq03bz, txt3bz, eq03cz, 
                          eq03dz, eq04z, eq04bz, box05z),
                  txt3z.animate.shift(2.5*DOWN),
                  eq05z.animate.next_to(txt3z).shift(2.5*DOWN),
                  txt05z.animate.shift(1.4*UP+0.3*RIGHT),
                  FadeIn(txt3.shift(0.5*DOWN), 
                         eq05.next_to(txt3), 
                         txt05.next_to(eq05).shift(1*RIGHT))
                  )
        self.wait(3)
        self.remove(txt3z, eq05z, txt05z, txt3, eq05, txt05)
        self.wait(1)
        # ==============================================================================
        # all frequencies (Planck)
        # ==============================================================================
        txt3z = Tex(r".", font_size=40, color=BLACK)
        txt3z = align_ld(txt3z, txt1, down=1.1, right=0.)

        str03z = r"""u
                    = \frac{8\pi h\nu^3}{c^3} \frac{1}{e^{\beta h\nu}-1}"""
        eq03z = MathTex(str03z, font_size=40).next_to(txt3z)
        eq03z[0][0].set_color(color_E)
        
        txt3bz = Tex(r"(Planck)", font_size=40,
                    color=color_p).next_to(eq03z).shift(6*RIGHT)
        
        str03bz = r"""\frac{\partial u}{\partial\beta} 
                    = -\frac{8\pi h^2\nu^4}{c^3}
                       \frac{e^{\beta h\nu}}{(e^{\beta h\nu}-1)^2} """
        eq03bz = MathTex(str03bz, font_size=40)
        eq03bz[0][1].set_color(color_u)
        eq03bz = align_ld(eq03bz, eq03z, down=1.2, right=-0.3)
        
        str03cz = r"""= -\frac{c^3u^2}{8\pi\nu^2}
                       \left(1 + \frac{8\pi h\nu^3}{uc^3}\right)"""
        eq03cz = MathTex(str03cz, font_size=40).next_to(eq03bz)
        eq03cz[0][4].set_color(color_u)
        eq03cz[0][-4].set_color(color_u)

        eq03dz = MathTex(r"""\frac{\partial u}{\partial\beta} 
                         = -\frac{c^3}{8\pi\nu^2}
                            \left(\frac{\langle E\rangle}
                                          {V\Delta\nu}\right)^2
                           -h\nu\,\frac{\langle E\rangle}{V\Delta\nu}
                         """, 
                        font_size=40).next_to(eq03cz)
        eq03dz[0][:5].set_opacity(0)
        eq03dz[0][16].set_color(color_e)
        eq03dz[0][-6].set_color(color_e)
        eq03dz = align_ld(eq03dz, eq03bz, down=1.2, right=0)

        str04z = r"""\langle\epsilon^2\rangle 
                    = \frac{c^3}{8\pi\nu^2\Delta\nu V} \langle E\rangle^2
                    + h\nu\, \langle E\rangle"""
        eq04z = MathTex(str04z, font_size=40)
        eq04z[0][1].set_color(color_e)
        eq04z[0][-9].set_color(color_e)
        eq04z[0][-2].set_color(color_e)
        eq04z = align_ld(eq04z, eq03dz, down=1.2, right=0.1)
        box04z = SurroundingRectangle(eq04z, buff=.15)

        str05z = r"""\frac{\langle\epsilon^2\rangle}{\langle E\rangle^2} 
                    = \frac{1}{M} + \frac{1}{N}"""
        eq05z = MathTex(str05z, font_size=40)
        eq05z[0][1].set_color(color_e)
        eq05z[0][6].set_color(color_e)
        eq05z[0][-5].set_color(color_rj)
        eq05z[0][-1].set_color(color_wien)
        eq05z.next_to(eq04z).shift(2.5*RIGHT+0.5*UP)

        box05z = SurroundingRectangle(eq05z, buff=.15)
        
        txt05za = Tex(r"inverse of the number of", font_size=30)
        txt05za = align_ld(txt05za, eq05z, down=1., right=-0.2)

        txt05zb = Tex(r"wave modes and light quanta", font_size=30)
        txt05zb[0][:9].set_color(color_rj)
        txt05zb[0][9:12].set_color(color_u)
        txt05zb[0][-11:].set_color(color_wien)
        txt05zb = align_ld(txt05zb, txt05za, down=0.4, right=-0.3)


        self.play(Write(txt3z))
        # self.wait(1)
        self.play(Write(eq03z))
        self.play(Write(txt3bz))
        self.wait(1)
        self.play(Write(eq03bz))
        self.wait(1)
        self.play(Write(eq03cz))
        self.wait(1)
        self.play(Write(eq03dz))
        self.wait(1)
        self.play(Write(eq04z))
        self.wait(1)
        # self.play(Write(eq04bz))
        # self.wait(1)
        self.play(Write(eq05z))
        self.play(Write(box05z), Write(txt05za), Write(txt05zb), run_time=2)
        self.wait(3)
        self.play(Write(box04z))
        self.wait(3)









        
        self.wait(10)

