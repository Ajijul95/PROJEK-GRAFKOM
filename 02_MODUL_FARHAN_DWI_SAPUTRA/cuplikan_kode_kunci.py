# Cuplikan kode kunci untuk modul ini

# Event mouse untuk pan / geser tampilan pada ui/app.py
    def _mouse_down(self, e):
        if self.mode_pilih is not None:
            self._pilih_titik_dari_mouse(e)
            self.sedang_pan = False
            return

        self.sedang_pan = True
        self.cam.start_pan(e)


    def _mouse_drag(self, e):
        if self.sedang_pan:
            self.cam.do_pan(e)


    def _mouse_up(self, e):
        if self.sedang_pan:
            self.cam.end_pan(e)

        self.sedang_pan = False


# Fungsi pan pada map/kamera.py
    def start_pan(self, e):
        self._sx, self._sy   = e.x, e.y
        self._ox0, self._oy0 = self.ox, self.oy
        self.canvas.config(cursor="fleur")


    def do_pan(self, e):
        self.ox = self._ox0 - (e.x - self._sx) / self.zoom
        self.oy = self._oy0 - (e.y - self._sy) / self.zoom
        self._clamp()
        self.app.render()


    def end_pan(self, e):
        self.canvas.config(cursor="")


    def _clamp(self):
        vw = max(1, self.canvas.winfo_width())
        vh = max(1, self.canvas.winfo_height())
        vww = vw / self.zoom
        vhw = vh / self.zoom
        mx  = self.ww - vww
        my  = self.wh - vhw
        self.ox = (max(0, min(mx, self.ox)) if mx >= 0 else mx / 2)
        self.oy = (max(0, min(my, self.oy)) if my >= 0 else my / 2)
