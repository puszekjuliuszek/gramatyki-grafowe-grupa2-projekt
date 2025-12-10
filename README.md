# Gramatyki Grafowe - Grupa 2

Projekt implementacji gramatyk grafowych z hiperkrawędziami dla przedmiotu na AGH.

<img width="877" height="493" alt="obraz" src="https://github.com/user-attachments/assets/5c91d7b6-1d32-4644-b55d-c7bf5aa160b3" />

## Struktura projektu

```
├── src/
│   ├── node.py              # Klasa Node (wierzchołek)
│   ├── edge.py              # Klasa HyperEdge (hiperkrawędź)
│   ├── graph.py             # Klasa Graph (graf z hiperkrawędziami)
│   ├── visualization.py     # Funkcje do wizualizacji grafów
│   └── productions/
│       ├── production.py    # Interfejs Production
│       └── p1.py            # Przykładowa produkcja P1
├── test/
│   └── test_p1.py           # Testy dla produkcji P1
├── draw/                    # Folder na wizualizacje grafów
├── pyproject.toml           # Konfiguracja projektu (Poetry)
└── test_run.sh              # Skrypt do uruchamiania testów
```

## Instalacja

Projekt używa [Poetry](https://python-poetry.org/) do zarządzania zależnościami.

```bash
# Instalacja Poetry (jeśli nie masz)
curl -sSL https://install.python-poetry.org | python3 -

# Instalacja zależności projektu
poetry install
```

## Uruchamianie testów

```bash
# Za pomocą poetry
poetry run pytest -v

# Lub za pomocą skryptu
./test_run.sh
```

## Jak działa klasa Graph

Klasa `Graph` jest zbudowana na bibliotece `networkx`. Ponieważ networkx nie wspiera hiperkrawędzi natywnie, konwertujemy każdą hiperkrawędź na specjalny węzeł połączony ze wszystkimi wierzchołkami, które hiperkrawędź łączy.

### Konwencje

- Węzły są identyfikowane przez etykiety (labels)
- Hiperkrawędzie mają parametr `hypertag` (E/Q/etc.) określający ich typ
- Węzły są numerowane przeciwnie do ruchu wskazówek zegara
- **NIE** używaj `src.` w importach - skonfiguruj IDE odpowiednio

## Jak implementować produkcje

Każda produkcja dziedziczy po klasie `Production` i implementuje dwie metody:
- `get_left_side()` - wzorzec do dopasowania
- `get_right_side(left, lvl)` - wynik transformacji

### Przykład minimalny

```python
from edge import HyperEdge
from graph import Graph
from node import Node
from productions.production import Production

@Production.register
class P1(Production):
    def get_left_side(self) -> Graph:
        g = Graph()
        n1 = Node(0, 0, "n1")
        n2 = Node(0, 0, "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(HyperEdge((n1, n2), "E"))
        return g

    def get_right_side(self, left: Graph, lvl: int):
        # Implementacja transformacji
        ...
```

## Jak testować produkcje

Testy używają `pytest`. Każdy przypadek testowy używa fixture do przygotowania grafu:

```python
class TestP1Case1:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.g = Graph()
        n1 = Node(0, 0, "n1")
        n2 = Node(2, 0, "n2")
        self.g.add_node(n1)
        self.g.add_node(n2)
        self.g.add_edge(HyperEdge((n1, n2), "E"))
        self.p1 = P1()

    def test_stage0(self):
        draw(self.g, "draw/test1-case1-stage0.png")
        cnt = self.g.count_nodes()
        assert cnt.normal == 2

    def test_stage1(self):
        applied = self.g.apply(self.p1)
        draw(self.g, "draw/test1-case1-stage1.png")
        assert applied == 1
```

## Atrybuty węzłów i hiperkrawędzi

### Node
- `x`, `y` - współrzędne
- `label` - unikalna etykieta
- `hanging` - czy węzeł jest "wiszący"
- `hyperref` - referencja do hiperkrawędzi (dla węzłów reprezentujących hiperkrawędzie)

### HyperEdge
- `nodes` - krotka połączonych węzłów
- `hypertag` - typ hiperkrawędzi ("E", "Q", etc.)
- `boundary` - czy hiperkrawędź jest na brzegu grafu
