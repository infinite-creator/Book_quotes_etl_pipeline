from dataclasses import dataclass
from pathlib import Path

@dataclass
class OutputPaths:
    json: Path
    csv: Path
    db: Path