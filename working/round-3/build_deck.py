"""HCO Round 3 — identity presentation. 1600 × 1000 boards on a 12 × 6 grid."""
import sys
from base import Deck
import deck1
TOTAL = 24
D = Deck(TOTAL)
for name in sorted(n for n in dir(deck1) if n.startswith("b") and n[1:].isdigit()): getattr(deck1, name)(D)
try:
    import deck2
    for name in sorted(n for n in dir(deck2) if n.startswith("b") and n[1:].isdigit()): getattr(deck2, name)(D)
    import deck3
    for name in sorted(n for n in dir(deck3) if n.startswith("b") and n[1:].isdigit()): getattr(deck3, name)(D)
except ImportError as ex: print("partial:", ex)
open("deck.html", "w").write(D.html("HCO — Identity System, Round 3"))
print("boards", len(D.pages))
