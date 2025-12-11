# Gramatyki Grafowe - Grupa 2

Projekt - gramatyki grafowe.

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
│       └── p0.py            # Przykładowa produkcja P0
├── test/
│   └── test_p0.py           # Testy dla produkcji P0
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

Klasa `Graph` jest zbudowana na bibliotece `networkx`. Ponieważ networkx nie wspiera hiperkrawędzi natywnie, konwertujemy każdą hiperkrawędź na specjalny węzeł połączony ze wszystkimi wierzchołkami, które hiperkrawędź łączy. W wizualizacji hiperkrawędź jest odpowiednio odróżniona. Do szukania izomorficznych podgrafów również użyta jest biblioteka `networkx`.

### Konwencje

- Węzły są identyfikowane przez etykiety (labels)
- Hiperkrawędzie mają parametr `hypertag` (E/Q/etc.) określający ich typ

## Jak implementować produkcje

Każda produkcja dziedziczy po klasie `Production` i implementuje dwie metody:
- `get_left_side()` - wzorzec do dopasowania
- `get_right_side(left)` - wynik transformacji

## Jak testować produkcje

Testy używają `pytest`. Każdy przypadek testowy używa fixture do przygotowania grafu - przykładowe testy są w pliku `test_p0.py`.

## Atrybuty węzłów i hiperkrawędzi

### Node
- `x`, `y` - współrzędne
- `label` - unikalna etykieta
- `hyperref` - referencja do hiperkrawędzi (dla węzłów reprezentujących hiperkrawędzie)

### HyperEdge
- `nodes` - krotka połączonych węzłów
- `hypertag` - typ hiperkrawędzi ("E", "Q", etc.)
- `r` - parametr R używany podczas tworzenia siatki
