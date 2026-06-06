# Cuplikan kode kunci untuk modul ini

# Pemilihan titik awal/tujuan dan pencarian rute pada ui/app.py
    def _mode_awal(self):
        self.mode_pilih = "awal"
        self.lbl_mode.config(text="Mode: klik jalan untuk titik AWAL")


    def _mode_tujuan(self):
        self.mode_pilih = "tujuan"
        self.lbl_mode.config(text="Mode: klik jalan untuk titik TUJUAN")


    def _pilih_titik_dari_mouse(self, e):
        wx, wy = self._screen_to_world(e.x, e.y)
        nodes, edges = self.grid.get_vector_dijkstra()

        titik = snap_klik_ke_jalan(nodes, edges, wx, wy)

        if titik is None:
            self.lbl_mode.config(text="Jalan tidak ditemukan")
            return

        if self.mode_pilih == "awal":
            self.titik_awal = titik
            self.lbl_mode.config(
                text="Titik awal dipilih di ruas jalan. Sekarang pilih tujuan atau cari rute."
            )

        elif self.mode_pilih == "tujuan":
            self.titik_tujuan = titik
            self.lbl_mode.config(
                text="Titik tujuan dipilih di ruas jalan. Klik Cari Rute."
            )

        self.mode_pilih = None
        self.rute = []
        self.total_jarak = 0
        self._hentikan_animasi()
        self.mobil_pos = None
        self.render()


    def _titik_otomatis(self):
        nodes, edges = self.grid.get_vector_dijkstra()

        if len(nodes) < 2:
            self.lbl_mode.config(text="Node jalan belum cukup")
            return

        awal = random.choice(nodes)
        tujuan = random.choice(nodes)

        for _ in range(300):
            kandidat = random.choice(nodes)
            jarak = math.hypot(kandidat[1] - awal[1], kandidat[2] - awal[2])

            if jarak > 550:
                tujuan = kandidat
                break

        self.titik_awal = (awal[1], awal[2])
        self.titik_tujuan = (tujuan[1], tujuan[2])
        self.rute = []
        self.total_jarak = 0
        self._hentikan_animasi()
        self.mobil_pos = None

        self.lbl_mode.config(text="Titik otomatis dibuat. Klik Cari Rute.")
        self.render()


    def cari_rute(self):
        if self.titik_awal is None:
            self.lbl_mode.config(text="Titik awal belum dipilih")
            return

        if self.titik_tujuan is None:
            self.lbl_mode.config(text="Titik tujuan belum dipilih")
            return

        nodes, edges = self.grid.get_vector_dijkstra()

        self.rute, self.total_jarak = cari_rute_koordinat(
            nodes,
            edges,
            self.titik_awal,
            self.titik_tujuan,
        )

        self._hentikan_animasi()

        if not self.rute:
            self.lbl_mode.config(
                text="Rute tidak ditemukan. Coba acak peta atau pilih titik lain."
            )
            self.mobil_pos = None
            self.render()
            return

        self._siapkan_animasi_dari_rute()
        self.mobil_pos = self.anim_path[0] if self.anim_path else self.rute[0]
        self.mobil_sudut = self._angle_at_distance(18.0)

        self.lbl_mode.config(
            text=f"Rute ditemukan | {len(self.rute)} node | jarak {self.total_jarak:.1f} px"
        )

        self.render()


# Algoritma utama pada algo/dijkstra.py
def buat_graph(nodes, edges):
    graph = {}

    for node_id, x, y in nodes:
        graph[node_id] = []

    for asal, tujuan, bobot in edges:
        if asal not in graph:
            graph[asal] = []
        graph[asal].append((tujuan, bobot))

    return graph



def snap_klik_ke_jalan(nodes, edges, x, y):
    info = cari_titik_terdekat_di_jalan(nodes, edges, x, y)

    if info is None:
        return None

    return info["titik"]

def cari_rute_koordinat(nodes, edges, start_xy, goal_xy):
    info_start = cari_titik_terdekat_di_jalan(
        nodes,
        edges,
        start_xy[0],
        start_xy[1],
    )

    nodes1, edges1, start_id, titik_start = tambah_node_sementara(
        nodes,
        edges,
        info_start,
    )

    info_goal = cari_titik_terdekat_di_jalan(
        nodes1,
        edges1,
        goal_xy[0],
        goal_xy[1],
    )

    nodes2, edges2, goal_id, titik_goal = tambah_node_sementara(
        nodes1,
        edges1,
        info_goal,
    )

    if start_id is None or goal_id is None:
        return [], float("inf")

    path_id, total_jarak = dijkstra(nodes2, edges2, start_id, goal_id)
    path_koordinat = path_id_ke_koordinat(nodes2, path_id)

    return path_koordinat, total_jarak



def dijkstra(nodes, edges, start_id, goal_id):
    graph = buat_graph(nodes, edges)

    jarak = {}
    sebelum = {}

    for node_id, x, y in nodes:
        jarak[node_id] = float("inf")
        sebelum[node_id] = None

    if start_id not in jarak or goal_id not in jarak:
        return [], float("inf")

    jarak[start_id] = 0

    antrian = []
    heapq.heappush(antrian, (0, start_id))

    while antrian:
        jarak_saat_ini, node_saat_ini = heapq.heappop(antrian)

        if node_saat_ini == goal_id:
            break

        if jarak_saat_ini > jarak[node_saat_ini]:
            continue

        for tetangga, bobot in graph.get(node_saat_ini, []):
            jarak_baru = jarak_saat_ini + bobot

            if jarak_baru < jarak[tetangga]:
                jarak[tetangga] = jarak_baru
                sebelum[tetangga] = node_saat_ini
                heapq.heappush(antrian, (jarak_baru, tetangga))

    if jarak[goal_id] == float("inf"):
        return [], float("inf")

    path = []
    node = goal_id

    while node is not None:
        path.append(node)
        node = sebelum[node]

    path.reverse()

    return path, jarak[goal_id]
