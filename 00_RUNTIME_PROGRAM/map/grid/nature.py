import math

from map.utils import dist, point_in_rounded_rect, circle_pts


class NatureMixin:
    def _buat_pohon(self, cx, cy):
        self.pohon = []
        self._buat_pohon_bundaran(cx, cy)
        self._buat_pohon_kota(cx, cy)

    def _buat_pohon_bundaran(self, cx, cy):
        for i in range(52):
            a = math.pi * 2 * i / 52 + self._rng.uniform(-0.04, 0.04)
            r = self.R_BUND * self._rng.uniform(1.18, 1.40)

            px = cx + math.cos(a) * r
            py = cy + math.sin(a) * r

            if self._titik_dekat_jalan(px, py, clearance=22):
                continue

            self.pohon.append({
                "x": px,
                "y": py,
                "r": self._rng.uniform(7, 12),
            })

    def _buat_pohon_kota(self, cx, cy):
        rx1, ry1, rx2, ry2, rc = self.ring_bounds

        target = 300
        percobaan = 0

        while len(self.pohon) < target and percobaan < target * 25:
            percobaan += 1

            tx = self._rng.uniform(rx1 + 10, rx2 - 10)
            ty = self._rng.uniform(ry1 + 10, ry2 - 10)

            if not point_in_rounded_rect(tx, ty, rx1, ry1, rx2, ry2, rc):
                continue

            if dist((tx, ty), (cx, cy)) < self.R_BUND * 1.7:
                continue

            if self._pohon_menabrak_bangunan(tx, ty):
                continue

            if self._titik_dekat_jalan(tx, ty, clearance=36):
                continue

            self.pohon.append({
                "x": tx,
                "y": ty,
                "r": self._rng.uniform(7, 15),
            })

    def _pohon_menabrak_bangunan(self, tx, ty):
        for b in self.bangunan:
            if (
                b["x"] - 8 < tx < b["x"] + b["w"] + 8 and
                b["y"] - 8 < ty < b["y"] + b["h"] + 8
            ):
                return True

        return False

    def _titik_dekat_jalan(self, x, y, clearance=36):
        for jalan in self._ambil_semua_jalan_untuk_cek_pohon():
            if len(jalan) < 2:
                continue

            for i in range(len(jalan) - 1):
                a = jalan[i]
                b = jalan[i + 1]

                jarak = self._jarak_titik_ke_segmen((x, y), a, b)

                if jarak < clearance:
                    return True

        return False

    def _ambil_semua_jalan_untuk_cek_pohon(self):
        semua_jalan = []

        semua_jalan.extend(self.jalan_h)
        semua_jalan.extend(self.jalan_v)
        semua_jalan.extend(self.jalan_spoke)

        if self.ring:
            semua_jalan.append(self.ring)

        bd = self.bundaran

        if bd:
            semua_jalan.append(
                circle_pts(
                    bd["cx"],
                    bd["cy"],
                    bd["r_jalan"],
                    n=96
                )
            )

        return semua_jalan

    def _jarak_titik_ke_segmen(self, p, a, b):
        px, py = p
        ax, ay = a
        bx, by = b

        vx = bx - ax
        vy = by - ay

        wx = px - ax
        wy = py - ay

        panjang2 = vx * vx + vy * vy

        if panjang2 <= 0.0001:
            return dist(p, a)

        t = (wx * vx + wy * vy) / panjang2
        t = max(0.0, min(1.0, t))

        dekat = (
            ax + vx * t,
            ay + vy * t
        )

        return dist(p, dekat)