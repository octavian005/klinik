# crud.py
from sqlalchemy.orm import Session
from datetime import date

import models
import schemas


# =========================
# PASIEN
# =========================

def registrasi_pasien(db: Session, pasien: schemas.PasienCreate):
    db_pasien = models.Pasien(
        nama_pasien=pasien.nama_pasien,
        email=pasien.email,
        password=pasien.password,
        no_telp=pasien.no_telp,
        alamat=pasien.alamat
    )

    db.add(db_pasien)
    db.commit()
    db.refresh(db_pasien)

    return db_pasien

def update_pasien(db: Session, id_pasien: int, pasien_update: schemas.PasienUpdate):
    db_pasien = db.query(models.Pasien).filter(
        models.Pasien.id_pasien == id_pasien
    ).first()

    if not db_pasien:
        return None

    if pasien_update.nama_pasien is not None:
        db_pasien.nama_pasien = pasien_update.nama_pasien

    if pasien_update.password is not None:
        db_pasien.password = pasien_update.password

    if pasien_update.no_telp is not None:
        db_pasien.no_telp = pasien_update.no_telp

    if pasien_update.alamat is not None:
        db_pasien.alamat = pasien_update.alamat

    db.commit()
    db.refresh(db_pasien)

    return db_pasien

def delete_pasien(db: Session, id_pasien: int):
    db_pasien = db.query(models.Pasien).filter(
        models.Pasien.id_pasien == id_pasien
    ).first()

    if not db_pasien:
        return None

    # Ambil semua pendaftaran milik pasien
    daftar_pendaftaran = db.query(models.Pendaftaran).filter(
        models.Pendaftaran.id_pasien == id_pasien
    ).all()

    for pendaftaran in daftar_pendaftaran:
        # Ambil rekam medis dari pendaftaran tersebut
        rekam_medis_list = db.query(models.RekamMedis).filter(
            models.RekamMedis.id_pendaftaran == pendaftaran.id_pendaftaran
        ).all()

        for rekam in rekam_medis_list:
            # Hapus detail resep dari rekam medis
            db.query(models.DetailResep).filter(
                models.DetailResep.id_rekam_medis == rekam.id_rekam_medis
            ).delete()

            # Hapus rekam medis
            db.delete(rekam)

        # Hapus pendaftaran
        db.delete(pendaftaran)

    # Hapus pasien
    db.delete(db_pasien)

    db.commit()

    return db_pasien


def login_pasien(db: Session, email: str, password: str):
    return db.query(models.Pasien).filter(
        models.Pasien.email == email,
        models.Pasien.password == password
    ).first()


def get_pasien_by_id(db: Session, id_pasien: int):
    return db.query(models.Pasien).filter(
        models.Pasien.id_pasien == id_pasien
    ).first()


# =========================
# DOKTER
# =========================

def get_all_dokter(db: Session):
    return db.query(models.Dokter).all()


def get_dokter_by_id(db: Session, id_dokter: int):
    return db.query(models.Dokter).filter(
        models.Dokter.id_dokter == id_dokter
    ).first()


# =========================
# JADWAL DOKTER
# =========================

def create_jadwal_dokter(db: Session, jadwal: schemas.JadwalDokterCreate):
    db_jadwal = models.JadwalDokter(
        id_dokter=jadwal.id_dokter,
        hari=jadwal.hari,
        jam_mulai=jadwal.jam_mulai,
        jam_selesai=jadwal.jam_selesai,
        status=jadwal.status
    )

    db.add(db_jadwal)
    db.commit()
    db.refresh(db_jadwal)

    return db_jadwal


def get_jadwal_by_dokter(db: Session, id_dokter: int):
    return db.query(models.JadwalDokter).filter(
        models.JadwalDokter.id_dokter == id_dokter,
        models.JadwalDokter.status == "Aktif"
    ).all()


def get_all_jadwal_dokter(db: Session):
    return db.query(models.JadwalDokter).all()
    

def get_jadwal_by_hari(db: Session, hari: str):
    return db.query(models.JadwalDokter).filter(
        models.JadwalDokter.hari == hari
    ).all()


# =========================
# PENDAFTARAN / ANTREAN
# =========================

def buat_pendaftaran(db: Session, pendaftaran: schemas.PendaftaranCreate):
    db_pendaftaran = models.Pendaftaran(
        id_pasien=pendaftaran.id_pasien,
        id_dokter=pendaftaran.id_dokter,
        id_jadwal=pendaftaran.id_jadwal,
        tanggal=pendaftaran.tanggal,
        keluhan=pendaftaran.keluhan,
        nomor_antrean=pendaftaran.nomor_antrean,
        status=pendaftaran.status
    )

    db.add(db_pendaftaran)
    db.commit()
    db.refresh(db_pendaftaran)

    return db_pendaftaran


def get_antrean_by_dokter(db: Session, id_dokter: int):
    return db.query(models.Pendaftaran).filter(
        models.Pendaftaran.id_dokter == id_dokter,
        models.Pendaftaran.status == "Menunggu"
    ).all()


def get_pendaftaran_by_pasien(db: Session, id_pasien: int):
    return db.query(models.Pendaftaran).filter(
        models.Pendaftaran.id_pasien == id_pasien
    ).all()


def update_status_pendaftaran(db: Session, id_pendaftaran: int, status: str):
    db_pendaftaran = db.query(models.Pendaftaran).filter(
        models.Pendaftaran.id_pendaftaran == id_pendaftaran
    ).first()

    if db_pendaftaran:
        db_pendaftaran.status = status
        db.commit()
        db.refresh(db_pendaftaran)

    return db_pendaftaran

def get_all_pendaftaran(db: Session):
    return db.query(models.Pendaftaran).all()


# =========================
# REKAM MEDIS
# =========================

def create_rekam_medis(db: Session, rekam: schemas.RekamMedisCreate):
    db_rekam = models.RekamMedis(
        id_pendaftaran=rekam.id_pendaftaran,
        diagnosa=rekam.diagnosa,
        tanggal_pemeriksaan=rekam.tanggal_pemeriksaan
    )

    db.add(db_rekam)

    db_pendaftaran = db.query(models.Pendaftaran).filter(
        models.Pendaftaran.id_pendaftaran == rekam.id_pendaftaran
    ).first()

    if db_pendaftaran:
        db_pendaftaran.status = "Selesai"

    db.commit()
    db.refresh(db_rekam)

    return db_rekam


def get_riwayat_rekam_medis_by_pasien(db: Session, id_pasien: int):
    return db.query(models.RekamMedis).join(models.Pendaftaran).filter(
        models.Pendaftaran.id_pasien == id_pasien
    ).all()


def get_rekam_medis_by_id(db: Session, id_rekam_medis: int):
    return db.query(models.RekamMedis).filter(
        models.RekamMedis.id_rekam_medis == id_rekam_medis
    ).first()


# =========================
# OBAT
# =========================

def create_obat(db: Session, obat: schemas.ObatCreate):
    db_obat = models.Obat(
        nama_obat=obat.nama_obat,
        jenis_obat=obat.jenis_obat,
        stok=obat.stok
    )

    db.add(db_obat)
    db.commit()
    db.refresh(db_obat)

    return db_obat

def update_obat(db: Session, id_obat: int, obat_update: schemas.ObatUpdate):
    db_obat = db.query(models.Obat).filter(
        models.Obat.id_obat == id_obat
    ).first()

    if not db_obat:
        return None

    if obat_update.nama_obat is not None:
        db_obat.nama_obat = obat_update.nama_obat

    if obat_update.jenis_obat is not None:
        db_obat.jenis_obat = obat_update.jenis_obat

    if obat_update.stok is not None:
        db_obat.stok = obat_update.stok

    db.commit()
    db.refresh(db_obat)

    return db_obat


def get_all_obat(db: Session):
    return db.query(models.Obat).all()


def get_obat_by_id(db: Session, id_obat: int):
    return db.query(models.Obat).filter(
        models.Obat.id_obat == id_obat
    ).first()

def delete_obat(db: Session, id_obat: int):
    db_obat = db.query(models.Obat).filter(
        models.Obat.id_obat == id_obat
    ).first()

    if not db_obat:
        return None

    cek_resep = db.query(models.DetailResep).filter(
        models.DetailResep.id_obat == id_obat
    ).first()

    if cek_resep:
        return "dipakai_resep"

    db.delete(db_obat)
    db.commit()

    return db_obat


# =========================
# DETAIL RESEP
# =========================

def create_detail_resep(db: Session, detail: schemas.DetailResepCreate):
    db_detail = models.DetailResep(
        id_rekam_medis=detail.id_rekam_medis,
        id_obat=detail.id_obat,
        dosis=detail.dosis,
        aturan_pakai=detail.aturan_pakai,
        jumlah=detail.jumlah,
        keterangan=detail.keterangan
    )

    db.add(db_detail)

    db_obat = db.query(models.Obat).filter(
        models.Obat.id_obat == detail.id_obat
    ).first()

    if db_obat:
        db_obat.stok = db_obat.stok - detail.jumlah

    db.commit()
    db.refresh(db_detail)

    return db_detail


def get_detail_resep_by_rekam_medis(db: Session, id_rekam_medis: int):
    return db.query(models.DetailResep).filter(
        models.DetailResep.id_rekam_medis == id_rekam_medis
    ).all()

# =========================
# ADMIN
# =========================

def login_admin(db: Session, email: str, password: str):
    return db.query(models.Admin).filter(
        models.Admin.email == email,
        models.Admin.password == password
    ).first()