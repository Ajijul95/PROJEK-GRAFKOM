# Cuplikan kode kunci untuk modul ini

# Kontrol animasi dan pergerakan kendaraan pada ui/app.py
    def _hentikan_animasi(self):
        self.animasi_jalan = False
        self.anim_last_time = None
        self.anim_path = []
        self.anim_cumdist = []
        self.anim_total = 0.0
        self.anim_dist = 0.0

        if self.anim_after_id is not None:
            try:
                self.canvas.after_cancel(self.anim_after_id)
            except Exception:
                pass

            self.anim_after_id = None


    def _siapkan_animasi_dari_rute(self):
        if not self.rute or len(self.rute) < 2:
            self.anim_path = []
            self.anim_cumdist = []
            self.anim_total = 0.0
            self.anim_dist = 0.0
            return

        path = self._buat_rute_membulat(self.rute)
        path = self._padatkan_path(path, step=2.0)

        self.anim_path = path
        self.anim_cumdist = [0.0]

        total = 0.0

        for i in range(len(path) - 1):
            total += self._jarak_titik(path[i], path[i + 1])
            self.anim_cumdist.append(total)

        self.anim_total = total
        self.anim_dist = 0.0


    def mulai_animasi(self):
        if not self.rute:
            self.cari_rute()

        if not self.rute or len(self.rute) < 2:
            return

        self._hentikan_animasi()
        self._siapkan_animasi_dari_rute()

        if len(self.anim_path) < 2:
            return

        self.animasi_jalan = True
        self.anim_dist = 0.0
        self.mobil_pos = self.anim_path[0]
        self.mobil_sudut = self._angle_at_distance(18.0)
        self.anim_last_time = time.perf_counter()

        self._step_animasi()


    def _step_animasi(self):
        if not self.animasi_jalan or len(self.anim_path) < 2:
            return

        now = time.perf_counter()
        dt = now - self.anim_last_time if self.anim_last_time is not None else 0.016
        self.anim_last_time = now

        dt = max(0.001, min(0.030, dt))

        turn_strength = self._turn_strength_at_distance(self.anim_dist)
        speed_factor = 1.0 - (0.45 * turn_strength)

        self.anim_dist += self.anim_speed * speed_factor * dt

        if self.anim_dist >= self.anim_total:
            self.animasi_jalan = False
            self.mobil_pos = self.anim_path[-1]
            self.mobil_sudut = self._angle_at_distance(self.anim_total - 2.0)
            self.lbl_mode.config(text="Kendaraan sampai tujuan")
            self.render()
            self.anim_after_id = None
            return

        self.mobil_pos = self._point_at_distance(self.anim_dist)

        target_sudut = self._angle_at_distance(self.anim_dist)

        self.mobil_sudut = self._smooth_angle(
            self.mobil_sudut,
            target_sudut,
            max_delta=50.0 * dt,
        )

        self.render()
        self.anim_after_id = self.canvas.after(16, self._step_animasi)


    def _point_at_distance(self, d):
        if not self.anim_path:
            return None

        if d <= 0:
            return self.anim_path[0]

        if d >= self.anim_total:
            return self.anim_path[-1]

        idx = 0

        while idx < len(self.anim_cumdist) - 1 and self.anim_cumdist[idx + 1] < d:
            idx += 1

        p1 = self.anim_path[idx]
        p2 = self.anim_path[idx + 1]

        d1 = self.anim_cumdist[idx]
        d2 = self.anim_cumdist[idx + 1]

        if d2 <= d1:
            return p2

        t = (d - d1) / (d2 - d1)

        x = p1[0] + (p2[0] - p1[0]) * t
        y = p1[1] + (p2[1] - p1[1]) * t

        return (x, y)


    def _angle_at_distance(self, d):
        if len(self.anim_path) < 2:
            return self.mobil_sudut

        jarak_sample = 4.0

        d1 = max(0.0, min(self.anim_total, d - jarak_sample))
        d2 = max(0.0, min(self.anim_total, d + jarak_sample))

        a = self._point_at_distance(d1)
        b = self._point_at_distance(d2)

        if a is None or b is None:
            return self.mobil_sudut

        dx = b[0] - a[0]
        dy = b[1] - a[1]

        if abs(dx) < 1e-9 and abs(dy) < 1e-9:
            return self.mobil_sudut

        return math.atan2(dy, dx)


    def _smooth_angle(self, current, target, max_delta):
        diff = (target - current + math.pi) % (2 * math.pi) - math.pi

        if diff > max_delta:
            diff = max_delta

        elif diff < -max_delta:
            diff = -max_delta

        return current + diff


# Renderer dipakai untuk menggambar ulang peta/kendaraan setelah posisi berubah
    def render(self, grid: GridKota):
        c   = self.canvas
        cam = self.cam
        c.delete("all")
        vw = max(1, c.winfo_width())
        vh = max(1, c.winfo_height())

        self._bg(vw, vh)
        self._grid_tipis(vw, vh, grid.CELL_W, grid.CELL_H)
        self._pohon(grid.pohon)
        self._bangunan(grid.bangunan)
        self._semua_jalan(grid)
        self._bundaran(grid.bundaran)
        self._label_bundaran(grid.bundaran)

    # ── Background ───────────────────────────────────────────────


# ============================================================
# FITUR START DAN PAUSE ANIMASI
# ============================================================
# Tombol Start menjalankan animasi dari awal atau melanjutkan animasi yang dipause.
# Tombol Pause menghentikan timer animasi tanpa menghapus rute dan posisi kendaraan.

# Variabel status di __init__:
self.animasi_jalan = False
self.animasi_pause = False
self.anim_after_id = None

# Tombol pada panel:
tk.Button(
    pnl,
    text="▶ Start",
    command=self.mulai_animasi,
    bg="#2980b9",
    fg="white",
    activebackground="#3498db",
    activeforeground="white",
    **kw_btn,
).pack(side="left", padx=4)

tk.Button(
    pnl,
    text="⏸ Pause",
    command=self.pause_animasi,
    bg="#d35400",
    fg="white",
    activebackground="#e67e22",
    activeforeground="white",
    **kw_btn,
).pack(side="left", padx=4)

# Logika Start:
def mulai_animasi(self):
    if self.animasi_pause and self.anim_path and self.anim_dist < self.anim_total:
        self.animasi_pause = False
        self.animasi_jalan = True
        self.anim_last_time = time.perf_counter()
        self.lbl_mode.config(text="Animasi dilanjutkan")
        self._step_animasi()
        return

    if not self.rute:
        self.cari_rute()

    if not self.rute or len(self.rute) < 2:
        return

    self._hentikan_animasi()
    self._siapkan_animasi_dari_rute()

    if len(self.anim_path) < 2:
        return

    self.animasi_jalan = True
    self.animasi_pause = False
    self.anim_dist = 0.0
    self.mobil_pos = self.anim_path[0]
    self.mobil_sudut = self._angle_at_distance(18.0)
    self.anim_last_time = time.perf_counter()
    self.lbl_mode.config(text="Animasi kendaraan berjalan")

    self._step_animasi()

# Logika Pause:
def pause_animasi(self):
    if not self.animasi_jalan:
        return

    self.animasi_jalan = False
    self.animasi_pause = True
    self.anim_last_time = None

    if self.anim_after_id is not None:
        try:
            self.canvas.after_cancel(self.anim_after_id)
        except Exception:
            pass

        self.anim_after_id = None

    self.lbl_mode.config(text="Animasi dipause. Klik Start untuk lanjut.")
    self.render()
