from map.utils import dist, circle_pts, point_in_rounded_rect


class BuildingMixin:
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
        dekat = (ax + vx * t, ay + vy * t)
        return dist(p, dekat)

    def _jarak_rect_ke_segmen(self, x, y, w, h, a, b):
        pts = [
            (x, y), (x + w, y), (x + w, y + h), (x, y + h),
            (x + w / 2, y), (x + w, y + h / 2),
            (x + w / 2, y + h), (x, y + h / 2),
            (x + w / 2, y + h / 2),
        ]
        return min(self._jarak_titik_ke_segmen(p, a, b) for p in pts)

    def _rect_aman_dalam_ring(self, x, y, w, h, margin=10):
        rx1, ry1, rx2, ry2, rc = self.ring_bounds
        pts = [
            (x - margin, y - margin),
            (x + w + margin, y - margin),
            (x + w + margin, y + h + margin),
            (x - margin, y + h + margin),
            (x + w / 2, y + h / 2),
        ]
        return all(point_in_rounded_rect(px, py, rx1, ry1, rx2, ry2, rc) for px, py in pts)

    def _rect_dekat_jalan(self, x, y, w, h, clearance=42):
        # bounding box bangunan + clearance, supaya cek segmen jalan lebih ringan
        minx = x - clearance
        maxx = x + w + clearance
        miny = y - clearance
        maxy = y + h + clearance

        for jalan in self._ambil_semua_jalan_untuk_cek_bangunan():
            if len(jalan) < 2:
                continue
            for i in range(len(jalan) - 1):
                a = jalan[i]
                b = jalan[i + 1]

                # skip cepat kalau segmen jauh dari area bangunan
                if max(a[0], b[0]) < minx or min(a[0], b[0]) > maxx:
                    continue
                if max(a[1], b[1]) < miny or min(a[1], b[1]) > maxy:
                    continue

                if self._jarak_rect_ke_segmen(x, y, w, h, a, b) < clearance:
                    return True
        return False

    def _ambil_semua_jalan_untuk_cek_bangunan(self):
        semua_jalan = self.jalan_h + self.jalan_v + self.jalan_spoke

        if self.ring:
            semua_jalan.append(self.ring)

        bd = self.bundaran
        if bd:
            semua_jalan.append(circle_pts(bd["cx"], bd["cy"], bd["r_jalan"], n=96))

        return semua_jalan

    def _buat_bangunan(self, cx, cy):
        self.bangunan = []
        rx1, ry1, rx2, ry2, rc = self.ring_bounds
        r_bebas = self.R_BUND * 2.6

        warna_atap = [
            "#c0392b", "#e74c3c", "#2980b9", "#3498db",
            "#8e44ad", "#9b59b6", "#e67e22", "#f39c12",
            "#16a085", "#1abc9c", "#27ae60", "#7f8c8d",
            "#95a5a6", "#d35400",
        ]

        ditemukan = 0
        percobaan = 0
        target = 220

        while ditemukan < target and percobaan < target * 35:
            percobaan += 1
            bx, by, bw, bh = self._acak_ukuran_bangunan(rx1, ry1, rx2, ry2)

            if not self._boleh_tempatkan_bangunan(bx, by, bw, bh, cx, cy, r_bebas):
                continue

            self.bangunan.append({
                "x": bx,
                "y": by,
                "w": bw,
                "h": bh,
                "atap": self._rng.choice(warna_atap),
            })
            ditemukan += 1

    def _acak_ukuran_bangunan(self, rx1, ry1, rx2, ry2):
        bx = self._rng.uniform(rx1 + 20, rx2 - 20)
        by = self._rng.uniform(ry1 + 20, ry2 - 20)
        bw = self._rng.uniform(24, 70)
        bh = self._rng.uniform(20, 58)
        return bx, by, bw, bh

    def _boleh_tempatkan_bangunan(self, bx, by, bw, bh, cx, cy, r_bebas):
        if not self._rect_aman_dalam_ring(bx, by, bw, bh, margin=14):
            return False
        if dist((bx + bw / 2, by + bh / 2), (cx, cy)) < r_bebas:
            return False
        if self._rect_dekat_jalan(bx, by, bw, bh, clearance=42):
            return False
        if self._tabrakan_dengan_bangunan_lain(bx, by, bw, bh):
            return False
        return True

    def _tabrakan_dengan_bangunan_lain(self, bx, by, bw, bh):
        margin = 8
        for b in self.bangunan:
            if (
                bx - margin < b["x"] + b["w"] and
                bx + bw + margin > b["x"] and
                by - margin < b["y"] + b["h"] and
                by + bh + margin > b["y"]
            ):
                return True
        return False
