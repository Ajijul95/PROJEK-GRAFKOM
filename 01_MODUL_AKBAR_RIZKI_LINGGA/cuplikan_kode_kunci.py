# Cuplikan kode kunci untuk modul ini

# GridKota.bangun dan pembentukan bundaran/jalan
    def bangun(self, seed=42, noise=None, rapat=None):
        if noise is not None:
            self.NOISE = noise

        if rapat is not None:
            self.CELL_W = rapat
            self.CELL_H = rapat

        self._rng = random.Random(seed)

        cx = self.WORLD_W / 2
        cy = self.WORLD_H / 2

        rx1 = self.PAD
        ry1 = self.PAD
        rx2 = self.WORLD_W - self.PAD
        ry2 = self.WORLD_H - self.PAD
        rc = self.CORNER_R

        self.ring_bounds = (rx1, ry1, rx2, ry2, rc)

        self.ring = organic_rounded_rect(
            rx1,
            ry1,
            rx2,
            ry2,
            rc,
            res=28,
            amp=18
        )

        self._buat_grid(cx, cy)
        self._buat_bundaran(cx, cy)
        self._buat_vector_dijkstra()
        self._buat_bangunan(cx, cy)
        self._buat_pohon(cx, cy)


    def _buat_bundaran(self, cx, cy):
        self.bundaran = {
            "cx": cx,
            "cy": cy,
            "r_jalan": self.R_BUND,
            "r_taman": self.R_BUND_IN,
        }

# RoadMixin: grid, jalan horizontal/vertikal, penghubung bundaran
    def _buat_grid(self, cx, cy):
        rx1, ry1, rx2, ry2, rc = self.ring_bounds

        cols = int((rx2 - rx1) / self.CELL_W) + 2
        rows = int((ry2 - ry1) / self.CELL_H) + 2

        node = {}

        for r in range(rows + 1):
            for c in range(cols + 1):
                node[(r, c)] = self._buat_titik_grid(r, c, cols, rows, rx1, ry1)

        self.node_grid = node
        self.jalan_h = []
        self.jalan_v = []
        self.jalan_spoke = []

        self._buat_jalan_horizontal(node, rows, cols)
        self._buat_jalan_vertikal(node, rows, cols)
        self._buat_jalan_penghubung_bundaran(cx, cy, node)


    def _buat_jalan_horizontal(self, node, rows, cols):
        for r in range(rows + 1):
            baris = []

            for c in range(cols + 1):
                titik = node[(r, c)]

                if not baris:
                    baris.append(titik)
                else:
                    p0 = baris[-1]
                    p1 = titik

                    ruas = self._buat_ruas_aman(
                        p0,
                        p1,
                        orientasi="h",
                        index=r * 100 + c
                    )

                    for p in ruas[1:]:
                        baris.append(p)

            clipped = self._clip_polyline(baris)

            for seg in clipped:
                if len(seg) >= 2:
                    self.jalan_h.append(seg)


    def _buat_jalan_vertikal(self, node, rows, cols):
        for c in range(cols + 1):
            kolom = []

            for r in range(rows + 1):
                titik = node[(r, c)]

                if not kolom:
                    kolom.append(titik)
                else:
                    p0 = kolom[-1]
                    p1 = titik

                    ruas = self._buat_ruas_aman(
                        p0,
                        p1,
                        orientasi="v",
                        index=c * 100 + r
                    )

                    for p in ruas[1:]:
                        kolom.append(p)

            clipped = self._clip_polyline(kolom)

            for seg in clipped:
                if len(seg) >= 2:
                    self.jalan_v.append(seg)


    def _buat_jalan_penghubung_bundaran(self, cx, cy, node):
        self.jalan_spoke = []

        daftar_node = list(node.values())

        sudut_list = [
            -math.pi / 2,
            -math.pi / 4,
            0,
            math.pi / 4,
            math.pi / 2,
            3 * math.pi / 4,
            math.pi,
            -3 * math.pi / 4,
        ]

        for sudut in sudut_list:
            ujung = self._cari_node_ujung_spoke(cx, cy, daftar_node, sudut)
            jalur = self._buat_jalur_spoke(cx, cy, sudut, ujung)
            self.jalan_spoke.append(jalur)


# VectorMixin: konversi jalan menjadi node-edge graph
    def _buat_vector_dijkstra(self):
        self.vector_nodes = []
        self.vector_edges = []

        semua_jalan = self._ambil_semua_jalan_untuk_vector()
        semua_segmen = self._ambil_semua_segmen(semua_jalan)
        titik_potong = self._cari_semua_titik_potong(semua_segmen)

        node_map = {}
        edge_set = set()

        for index, segmen in enumerate(semua_segmen):
            a, b = segmen

            daftar_titik = [
                (0.0, a),
                (1.0, b),
            ]

            for t, p in titik_potong.get(index, []):
                if 0.0 < t < 1.0:
                    daftar_titik.append((t, p))

            daftar_titik.sort(key=lambda item: item[0])

            titik_urut = []

            for t, p in daftar_titik:
                if not titik_urut:
                    titik_urut.append(p)
                else:
                    if self._jarak(titik_urut[-1], p) > 2:
                        titik_urut.append(p)

            for i in range(len(titik_urut) - 1):
                p1 = titik_urut[i]
                p2 = titik_urut[i + 1]

                if self._jarak(p1, p2) < 2:
                    continue

                id1 = self._tambah_node_vector(p1, node_map)
                id2 = self._tambah_node_vector(p2, node_map)

                self._tambah_edge_vector(id1, id2, edge_set)


    def get_vector_dijkstra(self):
        return self.vector_nodes, self.vector_edges
