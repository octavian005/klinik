# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import engine, get_db, SessionLocal


models.Base.metadata.create_all(bind=engine)

def init_admin():
    db: Session = SessionLocal()

    try:
        cek_admin = db.query(models.Admin).filter(
            models.Admin.email == "admin@gmail.com"
        ).first()

        if not cek_admin:
            admin = models.Admin(
                email="admin@gmail.com",
                password="admin123"
            )

            db.add(admin)
            db.commit()

            print("Admin berhasil ditambahkan")

    except Exception as e:
        db.rollback()
        print("ERROR INIT ADMIN:", e)

    finally:
        db.close()

def init_dokter():
    db: Session = SessionLocal()

    try:
        dokter_list = [
            {"nama_dokter": "Dr. Dzikri", "spesialis": "Dokter Umum"},
            {"nama_dokter": "Dr. Faiz", "spesialis": "Dokter Gigi"},
            {"nama_dokter": "Dr. Octavian", "spesialis": "Dokter Anak"},
            {"nama_dokter": "Dr. Naila", "spesialis": "Dokter Kulit"},
            {"nama_dokter": "Dr. Hassyifa", "spesialis": "Dokter THT"},
        ]

        for dokter in dokter_list:
            cek = db.query(models.Dokter).filter(
                models.Dokter.nama_dokter == dokter["nama_dokter"]
            ).first()

            if not cek:
                db.add(models.Dokter(**dokter))

        db.commit()
        print("Data dokter berhasil ditambahkan/dicek")

    except Exception as e:
        db.rollback()
        print("ERROR INIT DOKTER:", e)

    finally:
        db.close()


def init_jadwal_dokter():
    db: Session = SessionLocal()

    try:
        jadwal_list = [
            {"id_dokter": 1, "hari": "Senin", "jam_mulai": "08:00:00", "jam_selesai": "10:00:00", "status": "Aktif"},
            {"id_dokter": 2, "hari": "Selasa", "jam_mulai": "10:00:00", "jam_selesai": "12:00:00", "status": "Aktif"},
            {"id_dokter": 3, "hari": "Rabu", "jam_mulai": "08:00:00", "jam_selesai": "10:00:00", "status": "Aktif"},
            {"id_dokter": 4, "hari": "Kamis", "jam_mulai": "13:00:00", "jam_selesai": "15:00:00", "status": "Aktif"},
            {"id_dokter": 5, "hari": "Jumat", "jam_mulai": "09:00:00", "jam_selesai": "11:00:00", "status": "Aktif"},
        ]

        for jadwal in jadwal_list:
            cek = db.query(models.JadwalDokter).filter(
                models.JadwalDokter.id_dokter == jadwal["id_dokter"],
                models.JadwalDokter.hari == jadwal["hari"]
            ).first()

            if not cek:
                db.add(models.JadwalDokter(**jadwal))

        db.commit()
        print("Data jadwal dokter berhasil ditambahkan/dicek")

    except Exception as e:
        db.rollback()
        print("ERROR INIT JADWAL DOKTER:", e)

    finally:
        db.close()

def init_obat():
    db: Session = SessionLocal()

    try:
        obat_list = [
            {"nama_obat": "Paracetamol", "jenis_obat": "Tablet", "stok": 100},
            {"nama_obat": "Amoxicillin", "jenis_obat": "Kapsul", "stok": 80},
            {"nama_obat": "OBH Combi", "jenis_obat": "Sirup", "stok": 50},
            {"nama_obat": "Antasida", "jenis_obat": "Tablet", "stok": 70},
            {"nama_obat": "Cetirizine", "jenis_obat": "Tablet", "stok": 60},
            {"nama_obat": "Vitamin C", "jenis_obat": "Tablet", "stok": 100},
            {"nama_obat": "Betadine", "jenis_obat": "Cairan", "stok": 40},
            {"nama_obat": "Oralit", "jenis_obat": "Sachet", "stok": 90},
            {"nama_obat": "Ibuprofen", "jenis_obat": "Tablet", "stok": 50},
            {"nama_obat": "Salbutamol", "jenis_obat": "Tablet", "stok": 45},
        ]

        for obat in obat_list:
            cek = db.query(models.Obat).filter(
                models.Obat.nama_obat == obat["nama_obat"]
            ).first()

            if not cek:
                db.add(models.Obat(**obat))

        db.commit()
        print("Data obat berhasil ditambahkan/dicek")

    except Exception as e:
        db.rollback()
        print("ERROR INIT OBAT:", e)

    finally:
        db.close()

init_admin()
init_dokter()
init_jadwal_dokter()
init_obat()

app = FastAPI(title="API Klinik")

# =========================
# PASIEN
# =========================

@app.post("/pasien/register", response_model=schemas.PasienResponse)
def register_pasien(pasien: schemas.PasienCreate, db: Session = Depends(get_db)):
    return crud.registrasi_pasien(db, pasien)


@app.post("/pasien/login")
def login_pasien(email: str, password: str, db: Session = Depends(get_db)):
    pasien = crud.login_pasien(db, email, password)

    if not pasien:
        raise HTTPException(status_code=404, detail="Email atau password pasien salah")

    return {
        "message": "Login pasien berhasil",
        "id_pasien": pasien.id_pasien,
        "nama_pasien": pasien.nama_pasien,
        "email": pasien.email
    }

@app.delete("/pasien/{id_pasien}")
def delete_pasien(id_pasien: int, db: Session = Depends(get_db)):
    pasien = crud.delete_pasien(db, id_pasien)

    if not pasien:
        raise HTTPException(status_code=404, detail="Pasien tidak ditemukan")

    return {
        "message": "Data pasien berhasil dihapus",
        "id_pasien": id_pasien
    }


@app.get("/pasien/{id_pasien}", response_model=schemas.PasienResponse)
def get_pasien(id_pasien: int, db: Session = Depends(get_db)):
    pasien = crud.get_pasien_by_id(db, id_pasien)

    if not pasien:
        raise HTTPException(status_code=404, detail="Pasien tidak ditemukan")

    return pasien

@app.put("/pasien/{id_pasien}", response_model=schemas.PasienResponse)
def update_pasien(
    id_pasien: int,
    pasien_update: schemas.PasienUpdate,
    db: Session = Depends(get_db)
):
    pasien = crud.update_pasien(db, id_pasien, pasien_update)

    if not pasien:
        raise HTTPException(status_code=404, detail="Pasien tidak ditemukan")

    return pasien


# =========================
# DOKTER
# =========================

@app.get("/dokter", response_model=List[schemas.DokterResponse])
def get_all_dokter(db: Session = Depends(get_db)):
    return crud.get_all_dokter(db)


@app.get("/dokter/{id_dokter}", response_model=schemas.DokterResponse)
def get_dokter(id_dokter: int, db: Session = Depends(get_db)):
    dokter = crud.get_dokter_by_id(db, id_dokter)

    if not dokter:
        raise HTTPException(status_code=404, detail="Dokter tidak ditemukan")

    return dokter


# =========================
# JADWAL DOKTER
# =========================

@app.post("/jadwal-dokter", response_model=schemas.JadwalDokterResponse)
def create_jadwal_dokter(jadwal: schemas.JadwalDokterCreate, db: Session = Depends(get_db)):
    return crud.create_jadwal_dokter(db, jadwal)


@app.get("/jadwal-dokter", response_model=List[schemas.JadwalDokterResponse])
def get_all_jadwal_dokter(db: Session = Depends(get_db)):
    return crud.get_all_jadwal_dokter(db)


@app.get("/dokter/{id_dokter}/jadwal", response_model=List[schemas.JadwalDokterResponse])
def get_jadwal_by_dokter(id_dokter: int, db: Session = Depends(get_db)):
    return crud.get_jadwal_by_dokter(db, id_dokter)


# =========================
# PENDAFTARAN / ANTREAN
# =========================

@app.post("/pendaftaran", response_model=schemas.PendaftaranResponse)
def buat_pendaftaran(pendaftaran: schemas.PendaftaranCreate, db: Session = Depends(get_db)):
    return crud.buat_pendaftaran(db, pendaftaran)


@app.get("/dokter/{id_dokter}/antrean", response_model=List[schemas.PendaftaranResponse])
def get_antrean_dokter(id_dokter: int, db: Session = Depends(get_db)):
    return crud.get_antrean_by_dokter(db, id_dokter)


@app.get("/pasien/{id_pasien}/pendaftaran", response_model=List[schemas.PendaftaranResponse])
def get_pendaftaran_pasien(id_pasien: int, db: Session = Depends(get_db)):
    return crud.get_pendaftaran_by_pasien(db, id_pasien)


@app.put("/pendaftaran/{id_pendaftaran}/status")
def update_status_pendaftaran(
    id_pendaftaran: int,
    status: str,
    db: Session = Depends(get_db)
):
    pendaftaran = crud.update_status_pendaftaran(db, id_pendaftaran, status)

    if not pendaftaran:
        raise HTTPException(status_code=404, detail="Pendaftaran tidak ditemukan")

    return {
        "message": "Status pendaftaran berhasil diubah",
        "status": pendaftaran.status
    }


# =========================
# REKAM MEDIS
# =========================

@app.post("/rekam-medis", response_model=schemas.RekamMedisResponse)
def create_rekam_medis(rekam: schemas.RekamMedisCreate, db: Session = Depends(get_db)):
    return crud.create_rekam_medis(db, rekam)


@app.get("/pasien/{id_pasien}/rekam-medis", response_model=List[schemas.RekamMedisResponse])
def get_riwayat_rekam_medis(id_pasien: int, db: Session = Depends(get_db)):
    return crud.get_riwayat_rekam_medis_by_pasien(db, id_pasien)


@app.get("/rekam-medis/{id_rekam_medis}", response_model=schemas.RekamMedisResponse)
def get_rekam_medis(id_rekam_medis: int, db: Session = Depends(get_db)):
    rekam = crud.get_rekam_medis_by_id(db, id_rekam_medis)

    if not rekam:
        raise HTTPException(status_code=404, detail="Rekam medis tidak ditemukan")

    return rekam


# =========================
# OBAT
# =========================

@app.post("/obat", response_model=schemas.ObatResponse)
def create_obat(obat: schemas.ObatCreate, db: Session = Depends(get_db)):
    return crud.create_obat(db, obat)


@app.get("/obat", response_model=List[schemas.ObatResponse])
def get_all_obat(db: Session = Depends(get_db)):
    return crud.get_all_obat(db)


@app.get("/obat/{id_obat}", response_model=schemas.ObatResponse)
def get_obat(id_obat: int, db: Session = Depends(get_db)):
    obat = crud.get_obat_by_id(db, id_obat)

    if not obat:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")

    return obat

@app.put("/obat/{id_obat}", response_model=schemas.ObatResponse)
def update_obat(
    id_obat: int,
    obat_update: schemas.ObatUpdate,
    db: Session = Depends(get_db)
):
    obat = crud.update_obat(db, id_obat, obat_update)

    if not obat:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")

    return obat

@app.delete("/obat/{id_obat}")
def delete_obat(id_obat: int, db: Session = Depends(get_db)):
    obat = crud.delete_obat(db, id_obat)

    if not obat:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")

    if obat == "dipakai_resep":
        raise HTTPException(
            status_code=400,
            detail="Obat tidak bisa dihapus karena sudah digunakan di detail resep"
        )

    return {
        "message": "Data obat berhasil dihapus",
        "id_obat": id_obat
    }


# =========================
# DETAIL RESEP
# =========================

@app.post("/detail-resep", response_model=schemas.DetailResepResponse)
def create_detail_resep(detail: schemas.DetailResepCreate, db: Session = Depends(get_db)):
    return crud.create_detail_resep(db, detail)


@app.get("/rekam-medis/{id_rekam_medis}/detail-resep", response_model=List[schemas.DetailResepResponse])
def get_detail_resep(id_rekam_medis: int, db: Session = Depends(get_db)):
    return crud.get_detail_resep_by_rekam_medis(db, id_rekam_medis)

@app.post("/admin/login")
def login_admin(email: str, password: str, db: Session = Depends(get_db)):
    admin = crud.login_admin(db, email, password)

    if not admin:
        raise HTTPException(status_code=404, detail="Email atau password admin salah")

    return {
        "message": "Login admin berhasil",
        "role": "admin",
        "id_admin": admin.id_admin,
        "email": admin.email
    }