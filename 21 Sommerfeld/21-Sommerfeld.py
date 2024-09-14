from manim import *
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

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



color_q = YELLOW
color_r = ORANGE
color_p = TEAL_B
color_E = YELLOW
color_title = LIGHT_PINK#PURPLE_A
color_a = color_q



class ElectronLevels(MovingCameraScene):
    color_n = YELLOW
    def construct(self):
        # self.wait()
        # ==============================================================================
        # diagram of Bohr's quantization
        # ==============================================================================
        # self.add(grid)
        a0 = 0.2
        proton = Dot(color=color_p, radius=0.04)#.shift(6*LEFT)
        levels = []
        labels, labels2 = [], []
        t = np.deg2rad(90)
        t2= np.deg2rad(0)
        for i in range(1, 5):
            r = i**2*a0
            levels.append(Circle(radius=r, color=TEAL, stroke_width=2).move_to(proton))
            loc =  r * np.cos(t)*RIGHT + (r * np.sin(t) + 0.12)*UP
            loc2=  r * np.cos(t2)*RIGHT + (r * np.sin(t2) + 0.1)*UP
            labels.append(Tex(f"$n={i}$", font_size=20).shift(loc))
            if i == 1:
                r0 = f"$a_0$"
            else:
                r0 = f"${i**2}a_0$"
            labels2.append(Tex(r0, font_size=20).shift(loc2))

        dr = 0.005
        r = 3**2*a0
        levels_new = [Circle(radius=(1+(i-1)*dr)*r, color=TEAL, 
                             stroke_width=0.5).move_to(levels[2]) 
                             for i in range(3)]

        
        self.play(Write(proton), run_time=1)
        # self.play(Write(level1), Write(level2), Write(level3), Write(level4), run_time=2)
        self.play(Write(VGroup(*levels)), run_time=2)
        self.play(Write(VGroup(*labels)), run_time=1)
        self.wait()
        # self.add(grid)
        # self.play(FadeIn(VGroup(*levels_new)),
        #           FadeOut(levels[2]))

        # self.add(grid)

        self.wait()
        self.play(self.camera.frame.animate.set(width=1.5).move_to(1*RIGHT+1.5*UP), 
                  proton.animate.scale(0.5), 
                  FadeOut(labels[2]),
                #   FadeIn(VGroup(*levels_new)),
                #   FadeOut(levels[2]),
                run_time=2)
        self.wait(1)

        splitting1 = levels[2].animate.become(VGroup(*levels_new))
        splitting2 = VGroup(*levels_new).animate.become(levels[2])
        self.play(splitting1)
        self.wait()
        self.play(splitting2)
        self.wait()

        # E field
        func1 = lambda pos: 2*RIGHT+UP
        vector_field_E1 = ArrowVectorField(func1, x_range=[0, 2, 0.1], 
                                           y_range=[0.9, 2.5, 0.05], 
                                           length_func=lambda x: 0.1,
                                          color=BLUE_A).set_opacity(0.4)

        self.play(FadeIn(vector_field_E1, levels[2]),
                  FadeOut(VGroup(*levels_new)))
        self.wait(1)



class ParticleCircleToEllipse(Scene):
    def construct(self):
        # Create a circle path
        circle_path = Circle(radius=2, color=TEAL, stroke_width=2)
        # Create an ellipse path with the same initial dimensions as the circle
        ellipse_path = Ellipse(width=4, height=2, color=TEAL, 
                               stroke_width=2).move_to(circle_path.get_center())
        # Create a dot to represent the particle
        particle = Dot(color=TEAL)
        # Position the particle at the start of the circular path
        particle.move_to(circle_path.point_from_proportion(0))
        # E field
        func1 = lambda pos: RIGHT
        vector_field_E1 = ArrowVectorField(func1, x_range=[-7, 7, 1], 
                                           y_range=[-3.5, 3.5, 1], 
                                           length_func=lambda x: 0.1,
                                          color=BLUE_A).set_opacity(0.2)
        vector_field_E2 = ArrowVectorField(func1, x_range=[-7, 7, 1],  
                                           y_range=[-3.5, 3.5, 1], 
                                           length_func=lambda x: 0.9,
                                          color=BLUE_A).set_opacity(0.5)
        field_increase = vector_field_E1.animate.become(vector_field_E2)
        
        self.add(circle_path)
        self.play(MoveAlongPath(particle, circle_path, rate_func=linear, run_time=2),
                  FadeIn(vector_field_E1))
        # Animation: Move particle along the circle, then transform the path to an ellipse
        self.play(
            MoveAlongPath(particle, circle_path, rate_func=linear, run_time=4),
            Transform(circle_path, ellipse_path, rate_func=linear, run_time=4),
            # FadeIn(vector_field, run_time=4),
            field_increase, run_time=4,
        )

        # Move the particle along the transformed elliptical path
        for _ in range(5):
            self.play(MoveAlongPath(particle, ellipse_path, 
                                    rate_func=linear, run_time=2))

        # Keep the final scene displayed for 2 seconds
        self.wait(2)



class Degeneracy(Scene):
    def construct(self):
        # self.add(grid)
        self.wait()
        # ==============================================
        # degeneracy in linear algebra
        # ==============================================
        txt0 = Tex(r"Degeneracy:", font_size=45, color=color_title).to_corner(UL)

        eq00 = MathTex(r"A = "
            r"\begin{bmatrix}"
            r"1 & 0 & 0 \\"
            r"0 & 0 & 1 \\"
            r"0 & 1 & 0"
            r"\end{bmatrix}", font_size=40
        )
        eq00 = align_ld(eq00, txt0, down=1.5, right=1)

        txt0b = Tex(r"Eigenvalues: $\lambda_1=-1$, $\lambda_2=1$, $\lambda_3=1$", 
                    font_size=40).next_to(eq00).shift(RIGHT)
        txt0b[0][12:18].set_color(ORANGE)
        txt0b[0][18:].set_color(color_q)
        
        txt0c = Tex(r"Eigenvectors: ", font_size=40)
        txt0c = align_ld(txt0c, txt0, down=3.5, right=0.5)

        txt00c = Tex(r"$\lambda_1=-1$:", font_size=40, color=ORANGE)
        txt00c = align_ld(txt00c, txt0c, down=1.5, right=0)

        eq00c = MathTex(r"v_1 = "
            r"\begin{bmatrix}"
            r"0 \\"
            r"-1 \\"
            r"1"
            r"\end{bmatrix},", font_size=40, color=ORANGE
        ).next_to(txt00c)
        

        txt0d = Tex(r"$\lambda_2=1$:", font_size=40, 
                    color=color_q).next_to(eq00c).shift(0.5*RIGHT)

        eq00d = MathTex(r"v_2 = "
            r"\begin{bmatrix}"
            r"1 \\"
            r"0 \\"
            r"0"
            r"\end{bmatrix},", font_size=40, color=color_q
        ).next_to(txt0d)
        
        txt0e = Tex(r"$\lambda_3=1$:", font_size=40, 
                    color=color_q).next_to(eq00d).shift(0.5*RIGHT)

        eq00e = MathTex(r"v_3 = "
            r"\begin{bmatrix}"
            r"0 \\"
            r"1 \\"
            r"1"
            r"\end{bmatrix}", font_size=40, color=color_q
        ).next_to(txt0e)






        self.add(txt0)
        self.wait(1)
        self.play(Write(eq00), run_time=1)
        self.wait(1)
        self.play(Write(txt0b), run_time=2)
        self.wait(1)
        self.play(Write(txt0c), Write(txt00c), Write(txt0d), Write(txt0e),
                  Write(eq00c), Write(eq00d), Write(eq00e),
                  run_time=2)

        self.wait(1)






        
        # clear all objects
        for mob in self.mobjects:
            self.remove(mob)
        self.wait(2)
        # ==============================================
        # degeneracy of energies
        # ==============================================
        self.wait()
        txt1 = Tex(r"Degeneracy:", font_size=45, color=color_title).to_corner(UL)

        eq01 = MathTex(r'E(n_1,n_2) = - \frac{E_0}{(n_1+n_2)^2}', font_size=35)
        eq01[0][0].set_color(color_E)
        eq01[0][2:4].set_color(color_p)
        eq01[0][5:7].set_color(color_r)
        eq01[0][-4:-2].set_color(color_r)
        eq01[0][-7:-5].set_color(color_p)
        eq01 = align_ld(eq01, txt1, down=0, right=3)

        eq02a = MathTex(r'''\text{state } (n_1=2, n_2=0):''', font_size=35)
        eq02a[0][-6:-4].set_color(color_r)
        eq02a[0][-3].set_color(color_r)
        eq02a[0][-11:-9].set_color(color_p)
        eq02a[0][-8].set_color(color_p)
        eq02a = align_ld(eq02a, eq01, down=2, right=-1)

        eq02b = MathTex(r'''E(2,0) = - \frac{E_0}{(2+0)^2} = - \frac{E_0}{4}''', 
                            font_size=35).next_to(eq02a).shift(RIGHT)
        eq02b[0][0].set_color(color_E)
        eq02b[0][2].set_color(color_p)
        eq02b[0][4].set_color(color_r)
        eq02b[0][12].set_color(color_p)
        eq02b[0][14].set_color(color_r)

        eq03a = MathTex(r'''\text{state } (n_1=1, n_2=1):''', font_size=35)
        eq03a[0][-6:-4].set_color(color_r)
        eq03a[0][-3].set_color(color_r)
        eq03a[0][-11:-9].set_color(color_p)
        eq03a[0][-8].set_color(color_p)
        eq03a = align_ld(eq03a, eq02a, down=1.5, right=0)

        eq03b = MathTex(r'''E(1,1) = - \frac{E_0}{(1+1)^2} = - \frac{E_0}{4}''', 
                            font_size=35).next_to(eq03a).shift(RIGHT)
        eq03b[0][0].set_color(color_E)
        eq03b[0][2].set_color(color_p)
        eq03b[0][4].set_color(color_r)
        eq03b[0][12].set_color(color_p)
        eq03b[0][14].set_color(color_r)

        self.add(txt1)
        self.wait(1)
        self.play(Write(eq01), run_time=1)
        self.wait(1)
        self.play(Write(eq02a), Write(eq03a), run_time=2)
        self.wait(1)
        self.play(Write(eq02b), Write(eq03b), run_time=2)

        self.wait(1)




class EllipticalOrbit(Scene):
    def construct(self):
        circle = Circle(radius=2, color=BLUE)
        ellipse = Ellipse()
        self.add(circle)
        self.play(Transform(circle, ellipse), run_time=3)
# class Ellipse(Scene):
#     def construct(self):
        # self.add(grid)
        # self.wait()
        # ellipse_1 = Ellipse(color=BLUE_B)
        # ellipse_2 = Ellipse(width=4.0, height=1.0, color=BLUE_D)
        # ellipse_group = Group(ellipse_1,ellipse_2).arrange(buff=1)
        # self.add(ellipse_group)
        # # ==============================================
        # # degeneracy in linear algebra
        # # ==============================================
        # # # Create a circle
        # circle = Circle(radius=2, color=BLUE)

        # # Create an ellipse with the same color
        # ellipse = Ellipse()

        # # Add the circle to the scene
        # self.add(circle)

        # # Transform the circle into the ellipse
        # self.play(Transform(circle, ellipse), run_time=3)

        # # Keep the final scene displayed for 2 seconds
        # self.wait(2)










class Sommerfeld_Model1915(Scene):
    def construct(self):
        # self.add(grid)
        self.wait()
        # ==============================================================================
        # elastic scattering
        # ==============================================================================
        txt1 = Tex(r"Bohr quantization (1913)", font_size=40, color=color_title).to_corner(UL)

        eq01 = MathTex(r'\oint p_\phi\,d\phi = nh', font_size=35)
        eq01[0][1:3].set_color(color_p)
        eq01[0][4].set_color(color_p)
        eq01[0][-2].set_color(color_p)
        eq01 = align_ld(eq01, txt1, down=1, right=0.5)
        
        eq01b = MathTex(r'\rightarrow l = n\hbar', font_size=35).next_to(eq01)
        eq01b[0][1].set_color(color_p)
        eq01b[0][-2].set_color(color_p)

        txt2 = Tex(r"Sommerfeld quantization (1915)", font_size=40, 
                   color=color_title).to_corner(UR).shift(LEFT)
        # txt2 = align_ld(txt2, txt1, down=2.5, right=0)

        eq02 = MathTex(r'\oint p_k\,dq_k = n_kh, ', font_size=35)
        eq02[0][1:3].set_color(color_q)
        eq02[0][4:6].set_color(color_q)
        eq02[0][-4:-2].set_color(color_q)
        eq02 = align_ld(eq02, txt2, down=1, right=0.5)

        eq02b = MathTex(r'k \text{ degrees of freedom}', 
                        font_size=35).next_to(eq02).shift(0.1*RIGHT)
        eq02b[0][0].set_color(color_q)
        
        eq03 = MathTex(r'k=\phi:', font_size=35)
        eq03[0][0].set_color(color_p)
        eq03[0][2].set_color(color_p)
        eq03 = align_ld(eq03, eq02, down=1.5, right=0.)

        eq03b = MathTex(r'\oint p_\phi\,d\phi = n_\phi h', 
                        font_size=35).next_to(eq03).shift(0.2*RIGHT)
        eq03b[0][1:3].set_color(color_p)
        eq03b[0][4].set_color(color_p)
        eq03b[0][-3:-1].set_color(color_p)
        
        box03b = SurroundingRectangle(eq03b, buff=.15)
        
        eq03c = MathTex(r'\rightarrow l = n_\phi \hbar', font_size=35).next_to(eq03b)
        eq03c[0][1].set_color(color_p)
        eq03c[0][-3:-1].set_color(color_p)
        
        box03c = SurroundingRectangle(eq03c[0][1:], buff=.15)
        
        
        eq04 = MathTex(r'k=r:', font_size=35)
        eq04[0][0].set_color(color_r)
        eq04[0][2].set_color(color_r)
        eq04 = align_ld(eq04, eq03, down=1.5, right=0)

        eq04b = MathTex(r'\oint p_r\,dr = n_r h', 
                        font_size=35).next_to(eq04).shift(0.2*RIGHT)
        eq04b[0][1:3].set_color(color_r)
        eq04b[0][4].set_color(color_r)
        eq04b[0][-3:-1].set_color(color_r)

        box04b = SurroundingRectangle(eq04b, buff=.15)
        



        self.play(Write(txt1), run_time=1)
        self.wait(1)
        self.play(Write(eq01), run_time=1)
        self.wait(1)
        self.play(Write(txt2), run_time=1)
        self.wait(1)
        self.play(Write(eq02), run_time=1)
        self.play(Write(eq02b), run_time=1)
        self.wait(1)
        self.play(Write(eq03), run_time=1)
        self.play(Write(eq03b), run_time=1)
        self.wait(1)
        self.wait(1)
        self.play(Write(eq04), run_time=1)
        self.play(Write(eq04b), run_time=1)
        self.wait(1)
        self.play(Write(box03b), Write(box04b), run_time=2)
        self.wait(1)
        self.remove(box03b, box04b)
        self.wait(1)
        self.play(Write(eq01b), Write(eq03c), run_time=1)
        self.wait(1)

        # ==============================================================================
        # r-quantization
        # ==============================================================================
        eq10 = MathTex(r'\oint p_r\,dr = ', font_size=35)
        eq10 = align_ld(eq10, txt1, down=0, right=0.)
        eq10[0][1:3].set_color(color_r)
        eq10[0][4].set_color(color_r)

        self.play(FadeOut(txt1, txt2, eq01, eq01b, eq02, 
                          eq02b, eq03, eq03b, eq03c, eq04),
                  eq04b.animate.move_to(eq10).shift(0.35*RIGHT), run_time=2)
        self.play(FadeIn(eq10), FadeOut(eq04b))
        self.wait(1)

        str11 = r'''E = \frac12mv^2-\frac{k_eZe^2}{r} 
                        \quad\quad \left(k_e=(4\pi\varepsilon_0)^{-1}\right)'''
        eq11 = MathTex(str11, font_size=35).next_to(eq10).shift(5*RIGHT)
        eq11[0][0].set_color(color_q)
        eq11[0][15].set_color(color_r)
        
        eq12 = MathTex(r'''v^2 = \dot r^2 + r^2\dot \phi''', font_size=35)
        eq12[0][3:5].set_color(color_r)
        eq12[0][7].set_color(color_r)
        eq12[0][9:].set_color(color_p)
        eq12 = align_ld(eq12, eq11, down=1, right=0.5)
        
        str13 = r'''v^2 = \frac{p_r^2}{m^2} + \frac{l^2}{m^2r^2}'''
        eq13 = MathTex(str13, font_size=35)
        eq13[0][3].set_color(color_r)
        eq13[0][5].set_color(color_r)
        eq13[0][10].set_color(color_p)
        eq13[0][-2].set_color(color_r)
        eq13 = align_ld(eq13, eq12, down=.8, right=0.)

        str14 = r'''E = \frac{p_r^2}{2m} + \frac{l^2}{2mr^2} -\frac{k_eZe^2}{r}'''
        eq14 = MathTex(str14, font_size=35)
        eq14[0][0].set_color(color_q)
        eq14[0][2].set_color(color_r)
        eq14[0][4].set_color(color_r)
        eq14[0][9].set_color(color_p)
        eq14[0][14].set_color(color_r)
        eq14[0][-1].set_color(color_r)
        eq14 = align_ld(eq14, eq13, down=1, right=-0.5)

        str15 = r'''p_r = \left(2mE + \frac{2mk_eZe^2}{r} - \frac{l^2}{r^2}\right)^{1/2}'''
        eq15 = MathTex(str15, font_size=35)
        eq15[0][:2].set_color(color_r)
        eq15[0][6].set_color(color_q)
        eq15[0][16].set_color(color_r)
        eq15[0][18].set_color(color_p)
        eq15[0][21].set_color(color_r)
        
        eq15 = align_ld(eq15, eq14, down=1, right=0.)


        self.play(Write(eq11))
        self.wait(1)
        self.play(Write(eq12))
        self.wait(1)
        self.play(Write(eq13))
        self.wait(1)
        self.play(Write(eq14))
        self.wait(1)
        self.play(Write(eq15))
        self.wait(1)
        
        # ==============================================================================
        # r-integration
        # ==============================================================================
        eq15[0][:3].set_opacity(0.)
        self.play(FadeOut(eq11, eq12, eq13, eq14),
                  eq15.animate.next_to(eq10).shift(0.4*LEFT), run_time=2)
        
        eq10b = MathTex(r'\oint', font_size=35).next_to(eq10)
        eq10c = MathTex(r'dr', font_size=35).next_to(eq15).shift(0.2*LEFT)
        eq10c[0][-1].set_color(color_r)

        self.play(Write(eq10b), Write(eq10c))
        self.wait(1)

        str20 = r'''= \oint\left(A + \frac{B}{r} + \frac{C}{r^2}\right)^{1/2} \!dr'''
        eq20 = MathTex(str20, font_size=35)
        eq20[0][7].set_color(color_r)
        eq20[0][11].set_color(color_r)
        eq20[0][-1].set_color(color_r)
        eq20 = align_ld(eq20, eq10b, down=1.2, right=-0.5)

        eq20b = MathTex(r'A &= 2mE\\ B &= 2mk_eZe^2\\ C &= -l^2', 
                       font_size=30).next_to(eq10).to_edge(RIGHT).shift(0.2*DOWN)
        eq20b[0][4].set_color(color_q)
        eq20b[0][-2].set_color(color_p)
        
        eq21 = MathTex(r'=2\pi i\left(\frac{B}{2\sqrt{A}} + \sqrt{C}\right)', font_size=35)
        eq21 = align_ld(eq21, eq20, down=1.2, right=0.)
        
        eq21b = MathTex(r'= 2\pi\left(\frac{mk_eZe^2}{\sqrt{-2mE}} -l\right)', 
                       font_size=35).next_to(eq21)
        eq21b[0][-2].set_color(color_p)
        eq21b[0][-4].set_color(color_q)
        
        eq21c = MathTex(r'= n_rh', font_size=35).next_to(eq21b)
        eq21c[0][1:3].set_color(color_r)
        
        str22 = r'''E(n_\phi, n_r) = -\frac{m}{2}\left(\frac{k_eZe^2}{\hbar}\right)^2
                        \frac{1}{(n_\phi+n_r)^2}'''
        eq22 = MathTex(str22, font_size=35)
        eq22[0][0].set_color(color_q)
        eq22[0][2:4].set_color(color_p)
        eq22[0][5:7].set_color(color_r)
        eq22[0][-4:-2].set_color(color_r)
        eq22[0][-7:-5].set_color(color_p)
        eq22 = align_ld(eq22, eq21, down=1.2, right=0.3)


        self.play(Write(eq20b))
        self.wait(1)
        self.play(Write(eq20))
        self.wait(2)
        self.play(Write(eq21))
        self.wait(1)
        self.play(Write(eq21b), run_time=2)
        self.wait(1)
        self.play(Write(eq21c), run_time=1)
        self.wait(1)
        self.play(Write(eq22), run_time=2)
        self.wait(1)



        self.play(FadeOut(eq10, eq10b, eq10c, eq15, eq20, eq20b, eq21, eq21b, eq21c), 
                  run_time=2)
        self.wait(1)
        # ================================================
        # Bohr vs. Sommerfeld
        # ================================================
        txt22c = Tex(r"Bohr model (1913)", font_size=40, color=color_title).to_corner(UL)
        
        txt22 = Tex(r"Sommerfeld model (1915)", font_size=40, 
                   color=color_title)#.to_corner(UL)
        txt22 = align_ld(txt22, txt22c, down=2.5, right=0)

        str22c = r'''E(n)= -\frac{m}{2}\left(\frac{k_eZe^2}{\hbar}\right)^2\frac{1}{n^2}
                         = -\frac{E_0}{n^2}'''
        eq22c = MathTex(str22c, font_size=35)
        eq22c[0][0].set_color(color_q)
        eq22c[0][2].set_color(color_p)
        eq22c[0][-2].set_color(color_p)
        eq22c[0][-9].set_color(color_p)
        eq22c = align_ld(eq22c, txt22c, down=1, right=0.5)
        

        self.play(Write(txt22c), Write(eq22c), Write(txt22),
                  eq22.animate.move_to(txt22).align_to(txt22, LEFT).shift(DOWN+0.5*RIGHT),)
        self.wait(1)

        eq22b = MathTex(r'=-\frac{E_0}{(n_\phi+n_r)^2}', font_size=35).next_to(eq22) 
        eq22b[0][-4:-2].set_color(color_r)
        eq22b[0][-7:-5].set_color(color_p)

        self.play(Write(eq22b))
        self.wait(3)

        # clear all objects
        for mob in self.mobjects:
            self.remove(mob)
        self.wait(1)
        # ==============================================================================
        # energy levels Bohr vs. Sommerfeld
        # ==============================================================================
        color_b = BLUE
        txt30 = Tex(r"Blue Balmer line of H", font_size=40, color=GRAY_B).to_corner(UL)
        txt30[0][:4].set_color(color_b)

        txt30b = MathTex(r"(\lambda=434 \text{ nm}, \nu=691 \text{ THz})", font_size=30)
        txt30b = align_ld(txt30b, txt30, down=0.5, right=0)

        eq31 = MathTex(r"\Delta E=\frac{hc}{\lambda}=h\nu=2.86 \text{ eV}", font_size=40)
        eq31 = align_ld(eq31, txt30b, down=1, right=0)

        

        # x, y = 6, 0.
        # line_i = Line(start=x*LEFT+y*DOWN, end=(x-1)*LEFT+y*DOWN)
        # line_f = Line(start=x*LEFT+(2+y)*DOWN, end=(x-1)*LEFT+(2+y)*DOWN)
        # txt_li = Tex(r"$-$0.54 eV", font_size=30, 
        #                    color=color_q).move_to((x-0.5)*LEFT+(y-0.2)*DOWN)
        # txt_lf = Tex(r"$-$3.40 eV", font_size=30, 
        #                    color=color_q).move_to((x-0.5)*LEFT+(2+y+0.2)*DOWN)
        # vec_if = Arrow(start=(x-0.5)*LEFT+y*DOWN, end=(x-0.5)*LEFT+(y+2)*DOWN, 
        #                color=color_b, tip_length=0.2, buff=0.05, stroke_width=2)
        



        txt32 = Tex(r"Bohr model", font_size=40, color=color_title)
        txt32 = align_ld(txt32, eq31, down=1., right=3)

        x, y = 3, 0.
        line5_B = Line(start=x*LEFT+y*DOWN, end=(x-1)*LEFT+y*DOWN)
        line2_B = Line(start=x*LEFT+(2+y)*DOWN, end=(x-1)*LEFT+(2+y)*DOWN)
        txt_l5_B = MathTex(r"(5)", font_size=30, 
                           color=color_q).move_to((x-0.5)*LEFT+(y-0.2)*DOWN)
        txt_l2_B = MathTex(r"(2)", font_size=30, 
                           color=color_q).move_to((x-0.5)*LEFT+(2+y+0.2)*DOWN)
        vec_52_B = Arrow(start=(x-0.5)*LEFT+y*DOWN, end=(x-0.5)*LEFT+(y+2)*DOWN, 
                       color=color_b, tip_length=0.2, buff=0.05, stroke_width=2)
        txt_dE = Tex(r"2.86 eV", font_size=30).move_to(txt_l2_B).shift(1.2*UP+0.7*LEFT)
        
        txt32b = Tex(r"Sommerfeld model", font_size=40, 
                     color=color_title).next_to(txt32).shift(3*RIGHT)

        line5_S, line2_S, txt5_S, txt2_S = [], [], [], []
        vec_i, vec_f = [], []
        for i in range(0, 5):
            x, y = -0.5-i*1.2, 0.
            line5 = Line(start=x*LEFT+y*DOWN, end=(x-1)*LEFT+y*DOWN)
            txt_l5 = MathTex(rf"{5-i, i}", font_size=30, 
                             color=color_q).move_to((x-0.5)*LEFT+(y-0.2)*DOWN)
            line5_S.append(line5)
            txt5_S.append(txt_l5)
            vec_i.append((x-0.5)*LEFT+y*DOWN)
        
        for i in range(0, 2):
            x, y = -2-i*1.5, 2-0.
            line2 = Line(start=x*LEFT+y*DOWN, end=(x-1)*LEFT+y*DOWN)
            txt_l2 = MathTex(rf"{2-i, i}", font_size=30, 
                             color=color_q).move_to((x-0.5)*LEFT+(y+0.2)*DOWN)
            txt2_S.append(txt_l2)
            line2_S.append(line2)
            vec_f.append((x-0.5)*LEFT+y*DOWN)

        arrows_S = []
        for d, pi in enumerate(vec_i):
            for pf in vec_f:
                v = Arrow(start=pi, end=pf, color=color_b, tip_length=0.2, 
                          buff=0.05, stroke_width=2)
                arrows_S.append(v)


    #    # Define the photon
    #     sine_wave = FunctionGraph(
    #         lambda x: 0.15 * np.sin(5*x * 2 * PI), x_range=[0, 0.6],
    #         color=BLUE_C
    #     ).shift(6.25*LEFT+DOWN)

    #     level_i1 = DashedLine(start=-4.8*RIGHT, end=-3.2*RIGHT, 
    #                           dashed_ratio=0.5, color=GRAY)
    #     level_f1 = DashedLine(start=-4.8*RIGHT-2*UP, end=-3.2*RIGHT-2*UP, 
    #                           dashed_ratio=0.5, color=GRAY)
        level_i2 = DashedLine(start=-1.8*RIGHT, end=0.3*RIGHT, dashed_ratio=0.5, color=GRAY)
        level_f2 = DashedLine(start=-1.8*RIGHT-2*UP, end=1.8*RIGHT-2*UP, dashed_ratio=0.5, 
                              color=GRAY)


        self.play(Write(txt30))
        self.play(Write(txt30b))
        self.wait(1)
        self.play(Write(eq31))
        self.wait(1)
        # self.wait(1)
        # self.play(Write(line_i), Write(line_f))
        # self.play(Write(txt_li), Write(txt_lf))
        self.wait(1)
        # self.play(LaggedStart(Write(vec_if, run_time=1),
        #                       sine_wave.animate.shift(15*RIGHT), lag_ratio=0.1),
        #             run_time=4)
        # self.wait(1)
        # self.add(grid)
        self.play(Write(txt32))
        self.wait(1)
        # self.play(Write(level_i1), Write(level_f1), run_time=.5)
        self.play(Write(line5_B), Write(line2_B))
        self.play(Write(txt_l5_B), Write(txt_l2_B))
        self.wait(1)
        self.play(Write(vec_52_B), Write(txt_dE))
        self.wait(1)
        self.add(txt32b)
        self.wait(1)
        self.play(Write(level_i2), Write(level_f2), run_time=.5)
        self.play(FadeIn(VGroup(*line5_S)), FadeIn(VGroup(*line2_S)))
        self.play(Write(VGroup(*txt5_S)), Write(VGroup(*txt2_S)))
        self.wait(1)
        self.play(Write(VGroup(*arrows_S)))
        self.wait(2)





class Alpha(Scene):
    def construct(self):
        # self.add(grid)
        self.wait()
        # ==============================================================================
        # elastic speed
        # ==============================================================================
        txt1 = Tex(r"Electron's orbit speed", font_size=40, color=color_title).to_corner(UL)

        eq01 = MathTex(r'v_1 = \left(\frac{k_eZe^2}{m r_1}\right)^{1/2}', font_size=35)
        eq01[0][:2].set_color(color_r)
        eq01[0][-6:-4].set_color(color_r)
        eq01 = align_ld(eq01, txt1, down=1.3, right=0.5)

        eq01b = MathTex(r'r_1 = \frac{\hbar^2}{k_eZe^2m}', 
                        font_size=35).next_to(eq01).shift(3*RIGHT)
        eq01b[0][:2].set_color(color_r)

        str02 = r'''\frac{v_1}{c} = \left(\frac{k_eZe^2}{m}\, 
                                    \frac{k_eZe^2m}{\hbar^2}\right)^{1/2}'''
        eq02 = MathTex(str02, font_size=35)
        eq02[0][:2].set_color(color_r)
        eq02[0][3].set_color(color_q)
        eq02 = align_ld(eq02, eq01, down=1.5, right=0.0)

        str03 = r'''\frac{v_1}{c} = \frac{k_ee^2}{\hbar c} = 0.0073'''
        eq03 = MathTex(str03, font_size=35)
        eq03[0][:4].set_opacity(0)
        eq03 = align_ld(eq03, eq02, down=1.5, right=0.0)

        eq04 = MathTex(r'\alpha=', font_size=35).shift(DOWN+RIGHT)
        eq04[0][0].set_color(color_a)
        eq04b= MathTex(r'\frac{k_ee^2}{\hbar c} \approx \frac{1}{137}', 
                       font_size=35).next_to(eq04)
        box  = SurroundingRectangle(VGroup(*[eq04, eq04b]), buff=.15, color=LIGHT_PINK)
        txt04 = Tex(r"Fine-structure constant", color=RED_A, font_size=35).shift(2*RIGHT)

        
        self.add(txt1)
        self.wait(1)
        self.play(Write(eq01), run_time=2)
        self.wait(1)
        self.play(Write(eq01b), run_time=1)
        self.wait(1)
        self.play(Write(eq02), run_time=2)
        self.wait(1)
        self.play(Write(eq03), run_time=2)
        self.wait(1)
        self.play(Write(eq04), run_time=1)
        self.play(Write(eq04b), run_time=2)
        self.wait(1)
        # self.add(grid)
        self.play(Write(box), run_time=2)
        self.play(Write(txt04), run_time=1)
        self.wait(1)






class Sommerfeld_Model1916(Scene):
    def construct(self):
        # self.add(grid)
        self.wait()
        # ================================================
        # r-quantization
        # ================================================
        txt0 = Tex(r"Relativistic Keplerian electrons (Sommerfeld, 1916)", 
                   font_size=40, color=color_title).to_corner(UL)
        eq01 = MathTex(r'E = \sqrt{c^2p^2 + (mc^2)^2} - \frac{k_eZe^2}{r}', font_size=35)
        eq01[0][0].set_color(color_q)
        eq01[0][-1].set_color(color_r)
        eq01 = align_ld(eq01, txt0, down=0.9, right=0.5)

        eq00 = MathTex(r'\oint p_\phi\,d\phi = n_\phi h \rightarrow l=n_\phi\hbar', 
                        font_size=35).next_to(eq01).to_edge(RIGHT)
        eq00[0][1:3].set_color(color_p)
        eq00[0][4].set_color(color_p)
        eq00[0][6:8].set_color(color_p)
        eq00[0][-3:-1].set_color(color_p)
        eq00[0][-5].set_color(color_p)



        str02 = r'''E = \sqrt{c^2\left(p_r^2 + \frac{l^2}{r^2}\right) + (mc^2)^2} 
                        - \frac{k_eZe^2}{r}'''
        eq02 = MathTex(str02, font_size=35)
        eq02[0][0].set_opacity(0)
        eq02[0][7].set_color(color_r)
        eq02[0][9].set_color(color_r)
        eq02[0][11].set_color(color_p)
        eq02[0][14].set_color(color_r)
        eq02[0][-1].set_color(color_r)
        eq02 = align_ld(eq02, eq01, down=1, right=0.)

        str03 = r'''p_r^2 = \frac{E^2}{c^2} - (mc)^2 + \frac{2Ek_eZe^2}{c^2r} +
                            \frac{k_e^2Z^2e^4}{c^2r^2} - \frac{l^2}{r^2}'''
        eq03 = MathTex(str03, font_size=35)
        eq03[0][0].set_color(color_r)
        eq03[0][2].set_color(color_r)
        eq03[0][4].set_color(color_q)
        eq03[0][17].set_color(color_q)
        eq03[0][26].set_color(color_r)
        eq03[0][38].set_color(color_r)
        eq03[0][-5].set_color(color_p)
        eq03[0][-2].set_color(color_r)
        # eq03[0][0].set_opacity(0)
        eq03 = align_ld(eq03, eq02, down=1.1, right=0.)
        
        str04 = r'''\oint p_r\,dr = \oint\left(A + \frac{B}{r} 
                                    + \frac{C}{r^2}\right)^{1/2} \!dr'''
        eq04 = MathTex(str04, font_size=35)
        eq04[0][1:3].set_color(color_r)
        eq04[0][4].set_color(color_r)
        eq04[0][-1].set_color(color_r)
        eq04[0][-8].set_color(color_r)
        eq04[0][-12].set_color(color_r)
        eq04 = align_ld(eq04, eq03, down=1.1, right=0.)

        str04b = r'''A &= \frac{E^2}{c^2} - (mc)^2\\ 
                     B &= \frac{2Ek_eZe^2}{c^2}\\
                     C &= \frac{k_e^2Z^2e^4}{c^2} - l^2'''
        eq04b = MathTex(str04b, 
                       font_size=30).next_to(eq04).to_edge(RIGHT)
        eq04b[0][2].set_color(color_q)
        eq04b[0][16].set_color(color_q)
        eq04b[0][-2].set_color(color_p)
        
        str04c = r'''= 2\pi i\left(\frac{B}{2\sqrt{A}} + \sqrt{C}\right)'''
        eq04c = MathTex(str04c, font_size=35).next_to(eq04)


        str05 = r'''\oint p_r\,dr = 2\pi \left(\frac{Ek_eZe^2/c}{\sqrt{(mc^2)^2-E^2}}
                    - \sqrt{l^2 - \left(k_eZe^2/c\right)^2} \right)'''
        eq05 = MathTex(str05, font_size=35)
        eq05[0][9].set_color(color_q)
        eq05[0][27].set_color(color_q)
        eq05[0][-14].set_color(color_p)

        eq05 = align_ld(eq05, eq04, down=1.1, right=0.)
        eq052 = eq05.copy()
        eq052[0][1:3].set_color(color_r)
        eq052[0][4].set_color(color_r)
        eq052[0][9].set_color(color_q)
        eq052[0][27].set_color(color_q)
        eq052[0][-14].set_color(color_p)
        eq05[0][:5].set_opacity(0)
                
        eq05b = MathTex(r'=n_rh', font_size=35).next_to(eq05)
        eq05b[0][1:3].set_color(color_r)

        self.play(Write(txt0), run_time=1)
        self.wait(1)
        self.play(Write(eq00), run_time=2)
        self.wait(1)
        self.play(Write(eq01), run_time=1)
        self.wait(1)
        self.play(Write(eq02), run_time=2)
        self.wait(1)
        self.play(Write(eq03), run_time=2)
        self.wait(1)
        self.play(Write(eq04), run_time=2)
        self.wait(1)
        self.play(Write(eq04b), run_time=3)
        self.wait(1)
        self.play(Write(eq04c), run_time=1)
        self.wait(1)
        self.play(Write(eq05), run_time=2)
        self.wait(1)
        
        # eq05[0][1:3].set_color(color_r)
        # eq05[0][4].set_color(color_r)
        self.add(eq052)
        self.play(FadeOut(eq00, eq01, eq02, eq03, eq04, eq04b, eq04c), run_time=1)
        self.wait(1)
        self.play(Write(eq05b), run_time=1)
        self.wait(1)

        
    #     # ===============================================
    #     # r-integration
    #     # ===============================================

        str10 = r'''\frac{Ek_eZe^2/c}{\sqrt{(mc^2)^2-E^2}}
                    - \sqrt{l^2 - \left(k_eZe^2/c\right)^2} = n_r\hbar
                    \qquad\qquad l=n_\phi\hbar'''
        eq10 = MathTex(str10, font_size=35)
        eq10[0][0].set_color(color_q)
        eq10[0][18].set_color(color_q)
        eq10[0][23].set_color(color_p)
        eq10[0][-3:-1].set_color(color_p)
        eq10[0][-5].set_color(color_p)
        eq10[0][-8:-6].set_color(color_r)
        eq10 = align_ld(eq10, txt0, down=0.9, right=0.5)

        eq10b = MathTex(r'''\vdots''', font_size=35)
        eq10b = align_ld(eq10b, eq10, down=.85, right=4)

        str11 = r'''E(n_\phi, n_r) = mc^2\Bigg[1 + 
                            \Bigg(\frac{\alpha Z}{n_r+\sqrt{n_\phi^2-\alpha^2Z^2}}\Bigg)^2 
                        \Bigg]^{-1/2}'''
        # str11 = r'''E = mc^2\Bigg[1 + 
        #                     \Bigg(\frac{\frac{k_eZe^2}{\hbar c}}
        #                                 {n_r+\sqrt{n_\phi^2-
        #                                 \big(\frac{k_eZe^2}{\hbar c}\big)^2}}\Bigg)^2 
        #                 \Bigg]^{-1/2}'''
        eq11 = MathTex(str11, font_size=35)
        eq11[0][0].set_color(color_q)
        eq11[0][2:4].set_color(color_p)
        eq11[0][5:7].set_color(color_r)
        eq11[0][16].set_color(color_a)
        eq11[0][19:21].set_color(color_r)
        eq11[0][24].set_color(color_p)
        eq11[0][26].set_color(color_p)
        eq11[0][28].set_color(color_a)
        eq11 = align_ld(eq11, eq10, down=2, right=1)

        box11 = SurroundingRectangle(eq11, buff=.15)

        
        # str12 = r'''E \approx mc^2 
        #               - \frac{mc^2Z^2\alpha^2}{2(n_r+n_\phi)^2} 
        #                     \bigg(\frac{k_ee^2}{\hbar c}\bigg)^2
        #               + \frac{mc^2Z^4\alpha^4}{2(n_r+n_\phi)^4} 
        #                     \bigg(\frac34-\frac{n_r+n_\phi}{n_\phi}\bigg)
        #                    \bigg(\frac{k_ee^2}{\hbar c}\bigg)^4
        #         '''
        str12 = r'''E(n_\phi, n_r) \approx mc^2 
                - \frac{mc^2Z^2\alpha^2}{2(n_\phi+n_r)^2} 
                + \frac{mc^2Z^4\alpha^4}{2(n_\phi+n_r)^4} 
                    \bigg(\frac34-\frac{n_\phi+n_r}{n_\phi}\bigg)
        '''
        eq12 = MathTex(str12, font_size=35)
        eq12[0][0].set_color(color_q)
        eq12[0][2:4].set_color(color_p)
        eq12[0][5:7].set_color(color_r)
        eq12[0][18].set_color(color_a)
        eq12[0][23:25].set_color(color_p)
        eq12[0][26:28].set_color(color_r)
        eq12[0][36].set_color(color_a)
        eq12[0][41:43].set_color(color_p)
        eq12[0][44:46].set_color(color_r)
        eq12[0][-3:-1].set_color(color_p)
        eq12[0][-6:-4].set_color(color_r)
        eq12[0][-9:-7].set_color(color_p)
        eq12 = align_ld(eq12, eq10, down=3.5, right=1)
        
        box12 = SurroundingRectangle(eq12, buff=.15)
        


        self.play(Write(eq10), run_time=2)
        # self.wait(1)
        self.remove(eq05, eq052, eq05b)
        self.wait(1)
        self.play(Write(eq10b), run_time=1)
        self.wait(1)
        self.play(Write(eq11), run_time=2)
        self.play(Write(box11), run_time=2)
        self.wait(1)
        self.play(Write(eq12), FadeOut(box11), run_time=3)
        self.play(Write(box12), run_time=2)
        self.wait(1)

        clear_all(self)
        self.wait(1)   
        
        
        # ================================================
        # 
        # ================================================
        txt20 = Tex(r"Non-relativistic ellipses (Sommerfeld, 1915)", 
                   font_size=40, color=color_title).to_corner(UL)
        str20 = r'''E(2,0) &= - \frac{mc^2Z^2\alpha^2}{2(2+0)^2} 
                            = \frac{mc^2Z^2\alpha^2}{8}\\
                    E(1,1) &= - \frac{mc^2Z^2\alpha^2}{2(1+1)^2} 
                            = \frac{mc^2Z^2\alpha^2}{8}'''
        eq20 = MathTex(str20, font_size=35)
        eq20[0][0].set_color(color_q)
        eq20[0][2].set_color(color_p)
        eq20[0][4].set_color(color_r)
        eq20[0][13].set_color(color_a)
        eq20[0][18].set_color(color_p)
        eq20[0][20].set_color(color_r)
        eq20[0][29].set_color(color_a)
        eq20[0][0+33].set_color(color_q)
        eq20[0][2+33].set_color(color_p)
        eq20[0][4+33].set_color(color_r)
        eq20[0][13+33].set_color(color_a)
        eq20[0][18+33].set_color(color_p)
        eq20[0][20+33].set_color(color_r)
        eq20[0][-4].set_color(color_a)
        eq20 = align_ld(eq20, txt20, down=1.5, right=0.5)

        eq20b = MathTex(r'\Delta E = 0', 
                        font_size=35).next_to(eq20).shift(2*RIGHT+0.2*UP)

        txt21 = Tex(r"Relativistic ellipses (Sommerfeld, 1916)", 
                   font_size=40, color=color_title)
        txt21 = align_ld(txt21, txt20, down=3.5, right=0)
        
        str21 = r'''E(2, 0) &\approx mc^2 
                            - \frac{mc^2Z^2\alpha^2}{2(2+0)^2} 
                            + \frac{mc^2Z^4\alpha^4}{2(2+0)^4} 
                                \bigg(\frac34-\frac{2+0}{2}\bigg) \\
                    E(1, 1) &\approx mc^2 
                            - \frac{mc^2Z^2\alpha^2}{2(1+1)^2} 
                            + \frac{mc^2Z^4\alpha^4}{2(1+1)^4} 
                                \bigg(\frac34-\frac{1+1}{1}\bigg)
        '''
        eq21 = MathTex(str21, font_size=35)
        eq21[0][0].set_color(color_q)
        eq21[0][2].set_color(color_p)
        eq21[0][4].set_color(color_r)
        eq21[0][16].set_color(color_a)
        eq21[0][21].set_color(color_p)
        eq21[0][23].set_color(color_r)
        eq21[0][32].set_color(color_a)
        eq21[0][37].set_color(color_p)
        eq21[0][39].set_color(color_r)
        eq21[0][47].set_color(color_p)
        eq21[0][49].set_color(color_r)
        eq21[0][51].set_color(color_p)
        eq21[0][0+53].set_color(color_q)
        eq21[0][2+53].set_color(color_p)
        eq21[0][4+53].set_color(color_r)
        eq21[0][16+53].set_color(color_a)
        eq21[0][21+53].set_color(color_p)
        eq21[0][23+53].set_color(color_r)
        eq21[0][32+53].set_color(color_a)
        eq21[0][37+53].set_color(color_p)
        eq21[0][39+53].set_color(color_r)
        eq21[0][47+53].set_color(color_p)
        eq21[0][49+53].set_color(color_r)
        eq21[0][51+53].set_color(color_p)
        eq21 = align_ld(eq21, txt21, down=1.5, right=0.5)

        eq21b = MathTex(r'\Delta E = \frac{mc^2Z^4\alpha^4}{32}', 
                        font_size=35).next_to(eq21).shift(1*RIGHT)
        eq21b[0][1].set_color(color_q)
        eq21b[0][-5].set_color(color_a)

        box21b = SurroundingRectangle(eq21b, buff=.15)


        self.play(Write(txt20))
        self.wait(1)
        self.play(Write(eq20))
        self.wait(1)
        self.play(Write(eq20b))
        self.wait(1)
        self.play(Write(txt21))
        self.wait(1)
        self.play(Write(eq21))
        self.wait(1)
        self.play(Write(eq21b))
        self.play(Write(box21b))
        self.wait(1)





        self.wait(1)
