from pydantic import BaseModel
from datetime import date, time
from typing import Optional


# =====================
# PASIEN
# =====================

class PasienBase(BaseModel):
    nama_pasien: str
    email: str
    no_telp: Optional[str] = None
    alamat: Optional[str] = None


class PasienCreate(PasienBase):
    password: str


class PasienResponse(PasienBase):
    id_pasien: int

    class Config:
        from_attributes = True


class PasienUpdate(BaseModel):
    nama_pasien: Optional[str] = None
    email: Optional[str] = None
    no_telp: Optional[str] = None
    alamat: Optional[str] = None


# =====================
# DOKTER
# =====================

class DokterBase(BaseModel):
    nama_dokter: str
    spesialis: str


class DokterResponse(DokterBase):
    id_dokter: int

    class Config:
        from_attributes = True


# =====================
# JADWAL DOKTER
# =====================

class JadwalDokterBase(BaseModel):
    id_dokter: int
    hari: str
    jam_mulai: time
    jam_selesai: time


class JadwalDokterCreate(JadwalDokterBase):
    pass


class JadwalDokterResponse(JadwalDokterBase):
    id_jadwal: int

    class Config:
        from_attributes = True

class JadwalDokterHariResponse(BaseModel):
    id_jadwal: int
    id_dokter: int
    nama_dokter: str
    spesialis: str
    hari: str
    jam_mulai: time
    jam_selesai: time

    class Config:
        from_attributes = True


# =====================
# PENDAFTARAN
# =====================

class PendaftaranBase(BaseModel):
    id_pasien: int
    id_dokter: int
    id_jadwal: int
    tanggal: date
    keluhan: str
    status: Optional[str] = "Menunggu"


class PendaftaranCreate(PendaftaranBase):
    pass


class PendaftaranResponse(PendaftaranBase):
    id_pendaftaran: int
    nomor_antrean: int

    class Config:
        from_attributes = True


# =====================
# REKAM MEDIS
# =====================

class RekamMedisBase(BaseModel):
    id_pendaftaran: int
    diagnosa: str
    kode_icd: Optional[str] = None
    catatan: Optional[str] = None
    tanggal_pemeriksaan: date


class RekamMedisCreate(RekamMedisBase):
    pass


class RekamMedisResponse(RekamMedisBase):
    id_rekam_medis: int

    class Config:
        from_attributes = True


# =====================
# OBAT
# =====================

class ObatBase(BaseModel):
    nama_obat: str
    jenis_obat: str
    stok: int


class ObatCreate(ObatBase):
    pass


class ObatResponse(ObatBase):
    id_obat: int


class ObatUpdate(BaseModel):
    nama_obat: Optional[str] = None
    jenis_obat: Optional[str] = None
    stok: Optional[int] = None

    class Config:
        from_attributes = True


# =====================
# DETAIL RESEP
# =====================

class DetailResepBase(BaseModel):
    id_rekam_medis: int
    id_obat: int
    dosis: str
    aturan_pakai: str
    jumlah: int
    keterangan: Optional[str] = None


class DetailResepCreate(DetailResepBase):
    pass


class DetailResepResponse(DetailResepBase):
    id_detail_resep: int

    class Config:
        from_attributes = True

# =====================
# ADMIN
# =====================

class AdminBase(BaseModel):
    email: str


class AdminCreate(AdminBase):
    password: str


class AdminResponse(AdminBase):
    id_admin: int

    class Config:
        from_attributes = True

class AdminAntreanResponse(BaseModel):
    id_pendaftaran: int
    nama_pasien: str
    nama_dokter: str
    spesialis: str
    nomor_antrean: int
    status: str

    class Config:
        from_attributes = True

#RIWAYAT
class RiwayatPasienResponse(BaseModel):
    id_rekam_medis: int
    id_pendaftaran: int
    diagnosa: str
    kode_icd: Optional[str] = None
    catatan: Optional[str] = None
    tanggal_pemeriksaan: date
    nama_dokter: str
    spesialis: str

    class Config:
        from_attributes = True


class ObatCreate(BaseModel):
    nama_obat: str
    jenis_obat: str
    stok: int = 100


class ObatResponse(BaseModel):
    id_obat: int
    nama_obat: str
    jenis_obat: str
    stok: int

    class Config:
        from_attributes = True

class DetailResepObatResponse(BaseModel):
    id_detail_resep: int
    id_rekam_medis: int
    id_obat: int
    nama_obat: str
    jenis_obat: str
    dosis: str
    aturan_pakai: str
    jumlah: int
    keterangan: Optional[str] = None

    class Config:
        from_attributes = True