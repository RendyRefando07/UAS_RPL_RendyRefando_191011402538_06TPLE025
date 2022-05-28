# Nama   : Rendy Refando Brilliance Abdulloh
# NIM    : 191011402538
# Kelas  : 06TPLE025

# Fuzzy Sugeno
# Studi Kasus : Kipas Angin

# Kecepatan Putaran Kipas Angin : min 1000 rpm dan max 5000 rpm.
# Suhu Ruang : sedikit 100 kelvin dan banyak 600 kelvin.
# Frekuensi Putaran Kipas Angin : rendah 2000, sedang 5000, dan 7000 tinggi.
# Soalnya Hitung Hasil Dari Putaran Kipas Angin Dengan Suhu : 4000 rpm 300 kelvin !!

def down(x, xmin, xmax):
    return (xmax - x) / (xmax - xmin)


def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)


class Suhu():
    minimum = 100
    maximum = 600

    def rendah(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def tinggi(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)


class Kecepatan():
    minimum = 2000
    medium = 5000
    maximum = 7000

    def lambat(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)

    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def cepat(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)


class Putaran():
    minimum = 1000
    maximum = 5000

    def pelan(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def kencang(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    def inferensi(self, jumlah_suhu, jumlah_kecepatan):
        kcptn = Kecepatan()
        suhu = Suhu()
        result = []

        # [R1] Jika kecepatan LAMBAT, dan suhu TINGGI,
        #       MAKA Putaran = 0.5 * jumlah_kecepatan + 1700
        α1 = min(kcptn.lambat(jumlah_kecepatan), suhu.tinggi(jumlah_suhu))
        z1 = 0.5 * jumlah_kecepatan + 1700
        result.append((α1, z1))

        # [R2] Jika kecepatan LAMBAT, dan suhu RENDAH,
        #       MAKA Putaran = 2 * jumlah_kecepatan - 4000
        α2 = min(kcptn.lambat(jumlah_kecepatan), suhu.rendah(jumlah_suhu))
        z2 = 2 * jumlah_kecepatan - 4000
        result.append((α2, z2))

        # [R3] Jika kecepatan CEPAT, dan suhu TINGGI,
        #       MAKA Putaran = 0.5 * jumlah_kecepatan + 2000
        α3 = min(kcptn.cepat(jumlah_kecepatan), suhu.tinggi(jumlah_suhu))
        z3 = 0.5 * jumlah_kecepatan + 2000
        result.append((α3, z3))

        # [R4] Jika kecepatan CEPAT, dan suhu RENDAH,
        #       MAKA Putaran = jumlah_kecepatan + 700
        α4 = min(kcptn.lambat(jumlah_kecepatan), suhu.tinggi(jumlah_suhu))
        z4 = jumlah_kecepatan + 700
        result.append((α4, z4))

        # [R5] Jika kecepatan SEDANG, dan suhu RENDAH,
        #       MAKA Putaran = 0.5 * jumlah_kecepatan + 250
        α5 = min(kcptn.sedang(jumlah_kecepatan), suhu.rendah(jumlah_suhu))
        z5 = 0.5 * jumlah_kecepatan + 250
        result.append((α5, z5))

        # [R6] Jika kecepatan SEDANG, dan suhu TINGGI,
        #       MAKA Putaran = 1.5 * jumlah_kecepatan - 2000
        α6 = min(kcptn.sedang(jumlah_kecepatan), suhu.tinggi(jumlah_suhu))
        z6 = 1.5 * jumlah_kecepatan - 2000
        result.append((α6, z6))

        return result

    def defuzifikasi(self, jumlah_kecepatan, jumlah_suhu):
        inferensi_values = self.inferensi(jumlah_kecepatan, jumlah_suhu)
        return sum([(value[0] * value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])
