import sys
from pathlib import Path

# Dodanie katalogu głównego i src do ścieżki
root = Path(__file__).parent.parent.parent
sys.path.append(str(root))
sys.path.append(str(root / "src"))

from src.graph import Graph
from src.node import Node
from src.edge import HyperEdge
from src.visualization import draw
from src.productions.p0 import P0
from src.productions.p1 import P1
from src.productions.p2 import P2
from src.productions.p3 import P3
from src.productions.p4 import P4
from src.productions.p5 import P5
from src.productions.p6 import P6
from src.productions.p7 import P7
from src.productions.p8 import P8
from src.productions.p9 import P9
from src.productions.p10 import P10
from src.productions.p11 import P11
from src.productions.p12 import P12

def run_derivation():
    # Katalog na wyniki
    DRAW_DIR = Path(__file__).parent.parent.parent / "draw" / "G4_initial"
    DRAW_DIR.mkdir(parents=True, exist_ok=True)

    g = Graph()

    # prostokąt
    e1 = Node(2, 6, "e1")
    e2 = Node(6, 6, "e2")
    e3 = Node(6, 3, "e3")
    e4 = Node(2, 3, "e4")

    # zewnętrzne
    e5 = Node(0, 9, "e5")
    e6 = Node(9, 9, "e6")
    e7 = Node(12, 6, "e7")
    e8 = Node(12, 3, "e8")
    e9 = Node(9, 0, "e9")
    e10 = Node(0, 0, "e10")
    e11 = Node(-2, 3, "e11")
    e12 = Node(-2, 6, "e12")


    for n in [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12]:
        g.add_node(n)
    g.add_edge(HyperEdge((e1, e2), "E", b=0))
    g.add_edge(HyperEdge((e2, e3), "E", b=0))
    g.add_edge(HyperEdge((e3, e4), "E", b=0))
    g.add_edge(HyperEdge((e4, e1), "E", b=0))
    g.add_edge(HyperEdge((e1, e2, e3, e4), "Q", r=0))

    g.add_edge(HyperEdge((e1,e5), "E", b=0))
    g.add_edge(HyperEdge((e5,e6), "E", b=1))
    g.add_edge(HyperEdge((e6,e2), "E", b=0))
    g.add_edge(HyperEdge((e6,e7), "E", b=1))
    g.add_edge(HyperEdge((e7,e8), "E", b=1))
    g.add_edge(HyperEdge((e8,e9), "E", b=1))
    g.add_edge(HyperEdge((e9,e10), "E", b=1))
    g.add_edge(HyperEdge((e10,e4), "E", b=0))
    g.add_edge(HyperEdge((e3,e9), "E", b=0))
    g.add_edge(HyperEdge((e4,e10), "E", b=0))
    g.add_edge(HyperEdge((e10,e11), "E", b=1))
    g.add_edge(HyperEdge((e11,e12), "E", b=1))
    g.add_edge(HyperEdge((e12,e5), "E", b=1))

    g.add_edge(HyperEdge((e2, e3, e6, e7, e8, e9), "S", r=0))
    g.add_edge(HyperEdge((e10, e4, e3, e9), "Q", r=0))
    g.add_edge(HyperEdge((e10, e11, e12, e5, e4, e1), "S", r=0))
    g.add_edge(HyperEdge((e5, e6, e1, e2), "Q", r=0))
    # produkcje
    
    # Wizualizacja
    filename = str(DRAW_DIR / "initial_graph.png")
    draw(g, filename)
    print(f"Graf początkowy (ośmiokąt, 12 węzłów) został zapisany w: {filename}")

    # Zastosowanie produkcji
    # Produkcje są stosowalne w każdym możliwym miejscu, a my chcemy w jednym
    # Musimy to zrobić ręcznie lub zmodyfikować co trzeba
    # Graf musi być zgodny z założeniami, więc usuwanie krawędzi, zmiana etykiet nie wchodzi w grę
    
    # Część z prezentacji
    iter = 1
    p9 = P9()
    g.apply_one(p9, "e6")
    filename = str(DRAW_DIR / f"after_{iter}_p9.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P9 został zapisany w: {filename}")
    iter += 1

    p0 = P0()
    g.apply_one(p0, "e5")
    filename = str(DRAW_DIR / f"after_{iter}_p0.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P0 został zapisany w: {filename}")
    iter += 1

    p10 = P10()
    g.apply_one(p10, "e6")
    filename = str(DRAW_DIR / f"after_{iter}_p10.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P10 został zapisany w: {filename}")
    iter += 1

    p4 = P4()
    g.apply_one(p4, "e6")
    g.apply_one(p4, "e8")
    g.apply_one(p4, "e9")
    filename = str(DRAW_DIR / f"after_{iter}_p4.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P4 został zapisany w: {filename}")
    iter += 1

    p3 = P3()
    g.apply_one(p3, "e6")
    g.apply_one(p3, "e2")
    g.apply_one(p3, "e9")
    filename = str(DRAW_DIR / f"after_{iter}_p3.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P3 został zapisany w: {filename}")
    iter += 1

    p11 = P11()
    g.apply_one(p11, "e6")
    filename = str(DRAW_DIR / f"after_{iter}_p11.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P11 został zapisany w: {filename}")
    iter += 1

    p1 = P1()
    g.apply_one(p1, "e6")
    filename = str(DRAW_DIR / f"after_{iter}_p1.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P1 został zapisany w: {filename}")
    iter += 1

    g.apply_one(p4, "e6")
    filename = str(DRAW_DIR / f"after_{iter}_p4.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P4 został zapisany w: {filename}")
    iter += 1

    p2 = P2()
    g.apply_one(p2, "e6")
    filename = str(DRAW_DIR / f"after_{iter}_p2.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P2 został zapisany w: {filename}")
    iter += 1

    g.apply_one(p3, "e5")
    g.apply_one(p3, "e2")
    filename = str(DRAW_DIR / f"after_{iter}_p3.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P3 został zapisany w: {filename}")
    iter += 1

    p5 = P5()
    g.apply_one(p5, "e6")
    filename = str(DRAW_DIR / f"after_{iter}_p5.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P5 został zapisany w: {filename}")
    iter += 1

    # Cześć własna
    g.apply_one(p0, "e3", "e4")
    filename = str(DRAW_DIR / f"after_{iter}_p0.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P0 został zapisany w: {filename}")
    iter += 1

    g.apply_one(p1, "e3", "e4")
    filename = str(DRAW_DIR / f"after_{iter}_p1.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P1 został zapisany w: {filename}")
    iter += 1

    g.apply_one(p3, "e3", "e4")
    g.apply_one(p3, "e1", "e4")
    filename = str(DRAW_DIR / f"after_{iter}_p3.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P3 został zapisany w: {filename}")
    iter += 1

    g.apply_one(p5, "e1", "e4")
    filename = str(DRAW_DIR / f"after_{iter}_p5.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P5 został zapisany w: {filename}")
    iter += 1

    g.apply_one(p0, "e2", "V_e1_e2_e3_e4")
    filename = str(DRAW_DIR / f"after_{iter}_p0.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P0 został zapisany w: {filename}")
    iter += 1

    g.apply_one(p1, "e2", "V_e1_e2_e3_e4")
    filename = str(DRAW_DIR / f"after_{iter}_p1.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P1 został zapisany w: {filename}")
    iter += 1

    g.apply_one(p3, "e2", "n5")
    g.apply_one(p3, "n5", "V_e1_e2_e3_e4")
    g.apply_one(p3, "n2", "V_e1_e2_e3_e4")
    g.apply_one(p3, "e2", "n2")
    filename = str(DRAW_DIR / f"after_{iter}_p3.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P3 został zapisany w: {filename}")
    iter += 1

    g.apply_one(p5, "e2", "V_e1_e2_e3_e4")
    filename = str(DRAW_DIR / f"after_{iter}_p5.png")
    draw(g, filename)
    print(f"Graf po zastosowaniu P5 został zapisany w: {filename}")
    iter += 1

if __name__ == "__main__":
    run_derivation()