from pathlib import Path
import csv
import struct


class ScoreManager:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent / "scores"
        self.base_path.mkdir(exist_ok=True)

        self.champion_file = self.base_path / "champion.dat"
        self.scores_file = self.base_path / "scores.csv"

    def get_global_champion(self):
        if not self.champion_file.exists():
            return {"name": "None", "score": 0}

        with open(self.champion_file, "rb") as f:
            data = f.read()

            if len(data) != 20:
                return {"name": "None", "score": 0}

            name_bytes, score = struct.unpack("16si", data)
            name = name_bytes.decode("utf-8").strip("\x00")

            return {"name": name, "score": score}

    def save_global_champion(self, name, score):
        name_bytes = name.encode("utf-8")[:15]
        name_bytes += b"\x00" * (16 - len(name_bytes))

        with open(self.champion_file, "wb") as f:
            f.write(struct.pack("16si", name_bytes, score))

    def load_player_data(self, player_name):
        global_champ = self.get_global_champion()
        personal_best = 0

        if self.scores_file.exists():
            with open(self.scores_file, "r", newline="") as f:
                reader = csv.reader(f, delimiter=";")
                for row in reader:
                    if len(row) != 2:
                        continue
                    name, score = row[0], int(row[1])
                    if name == player_name:
                        personal_best = max(personal_best, score)

        return {"global": global_champ, "personal_best": personal_best}

    def save_result(self, player_name, score):
        if score <= 0:
            return

        # Global record
        champ = self.get_global_champion()
        if score > champ["score"]:
            self.save_global_champion(player_name, score)

        # Self record
        entries = {}
        if self.scores_file.exists():
            with open(self.scores_file, "r", newline="") as f:
                reader = csv.reader(f, delimiter=";")
                for row in reader:
                    if len(row) != 2:
                        continue
                    entries[row[0]] = int(row[1])

        # update
        if player_name in entries:
            entries[player_name] = max(entries[player_name], score)
        else:
            entries[player_name] = score

        # rewrite file
        with open(self.scores_file, "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            for name, sc in entries.items():
                writer.writerow([name, sc])
