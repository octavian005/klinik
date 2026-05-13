from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Pasien(Base):
    __tablename__ = "pasien"

    id_pasien = Column(Integer, primary_key=True, index=True)
    nama_pasien = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    no_telp = Column(String(20))
    alamat = Column(Text)

    pendaftaran = relationship("Pendaftaran", back_populates="pasien")

class Dokter(Base):
    __tablename__ = "dokter"

    id_dokter = Column(Integer, primary_key=True, index=True)
    nama_dokter = Column(String(100), nullable=False)
    spesialis = Column(String(100), nullable=False)

    jadwal_dokter = relationship("JadwalDokter", back_populates="dokter")
    pendaftaran = relationship("Pendaftaran", back_populates="dokter")


class JadwalDokter(Base):
    __tablename__ = "jadwal_dokter"

    id_jadwal = Column(Integer, primary_key=True, index=True)
    id_dokter = Column(Integer, ForeignKey("dokter.id_dokter"), nullable=False)
    hari = Column(String(20), nullable=False)
    jam_mulai = Column(Time, nullable=False)
    jam_selesai = Column(Time, nullable=False)
    status = Column(String(20), default="Aktif")

    dokter = relationship("Dokter", back_populates="jadwal_dokter")
    pendaftaran = relationship("Pendaftaran", back_populates="jadwal_dokter")


class Pendaftaran(Base):
    __tablename__ = "pendaftaran"

    id_pendaftaran = Column(Integer, primary_key=True, index=True)
    id_pasien = Column(Integer, ForeignKey("pasien.id_pasien"), nullable=False)
    id_dokter = Column(Integer, ForeignKey("dokter.id_dokter"), nullable=False)
    id_jadwal = Column(Integer, ForeignKey("jadwal_dokter.id_jadwal"), nullable=False)

    tanggal = Column(Date, nullable=False)
    keluhan = Column(Text, nullable=False)
    nomor_antrean = Column(Integer, nullable=False)
    status = Column(String(20), default="Menunggu")

    pasien = relationship("Pasien", back_populates="pendaftaran")
    dokter = relationship("Dokter", back_populates="pendaftaran")
    jadwal_dokter = relationship("JadwalDokter", back_populates="pendaftaran")
    rekam_medis = relationship("RekamMedis", back_populates="pendaftaran")


class RekamMedis(Base):
    __tablename__ = "rekam_medis"

    id_rekam_medis = Column(Integer, primary_key=True, index=True)
    id_pendaftaran = Column(Integer, ForeignKey("pendaftaran.id_pendaftaran"), nullable=False)

    diagnosa = Column(Text, nullable=False)
    tanggal_pemeriksaan = Column(Date, nullable=False)

    pendaftaran = relationship("Pendaftaran", back_populates="rekam_medis")
    detail_resep = relationship("DetailResep", back_populates="rekam_medis")


class Obat(Base):
    __tablename__ = "obat"

    id_obat = Column(Integer, primary_key=True, index=True)
    nama_obat = Column(String(100), nullable=False)
    jenis_obat = Column(String(50), nullable=False)
    stok = Column(Integer, nullable=False)

    detail_resep = relationship("DetailResep", back_populates="obat")


class DetailResep(Base):
    __tablename__ = "detail_resep"

    id_detail_resep = Column(Integer, primary_key=True, index=True)
    id_rekam_medis = Column(Integer, ForeignKey("rekam_medis.id_rekam_medis"), nullable=False)
    id_obat = Column(Integer, ForeignKey("obat.id_obat"), nullable=False)

    dosis = Column(String(50), nullable=False)
    aturan_pakai = Column(String(100), nullable=False)
    jumlah = Column(Integer, nullable=False)
    keterangan = Column(Text)

    rekam_medis = relationship("RekamMedis", back_populates="detail_resep")
    obat = relationship("Obat", back_populates="detail_resep")

class Admin(Base):
    __tablename__ = "admin"

    id_admin = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)