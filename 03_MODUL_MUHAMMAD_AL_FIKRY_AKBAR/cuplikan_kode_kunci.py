# # Cuplikan kode kunci untuk modul ini

# # Fungsi zoom dan skala pada map/kamera.py
#     def w2s(self, x, y):
#         return (x - self.ox) * self.zoom, (y - self.oy) * self.zoom


#     def scaled(self, v, lo=1.0):
#         return max(lo, v * self.zoom)


#     def flat(self, pts):
#         out = []
#         for x, y in pts:
#             sx, sy = self.w2s(x, y)
#             out += [sx, sy]
#         return out


#     def _zoom_at(self, ex, ey, f):
#         wx = ex / self.zoom + self.ox
#         wy = ey / self.zoom + self.oy
#         self.zoom = max(self.Z_MIN, min(self.Z_MAX, self.zoom * f))
#         self.ox   = wx - ex / self.zoom
#         self.oy   = wy - ey / self.zoom
#         self._clamp()
#         self.app.render()


#     def reset(self):
#         # Reset kamera sekarang mengembalikan tampilan ke zoom-in awal,
#         # bukan zoom-out seluruh peta.
#         self.zoom = self.zoom_awal
#         self.ox = self.ox_awal
#         self.oy = self.oy_awal
#         self._clamp()
#         self.app.render()


#     def _clamp(self):
#         vw = max(1, self.canvas.winfo_width())
#         vh = max(1, self.canvas.winfo_height())
#         vww = vw / self.zoom
#         vhw = vh / self.zoom
#         mx  = self.ww - vww
#         my  = self.wh - vhw
#         self.ox = (max(0, min(mx, self.ox)) if mx >= 0 else mx / 2)
#         self.oy = (max(0, min(my, self.oy)) if my >= 0 else my / 2)

# # Konversi layar ke koordinat dunia pada ui/app.py
#     def _screen_to_world(self, sx, sy):
#         wx = sx / self.cam.zoom + self.cam.ox
#         wy = sy / self.cam.zoom + self.cam.oy
#         return wx, wy
