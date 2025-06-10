package com.alerta_congestion_service.model;

import java.sql.Timestamp;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;

@Entity
public class AlertasCongestion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private int fila;
    private int columna;
    private int cantidad;

    @Column(name = "fecha_creacion", nullable = false, updatable = false, columnDefinition = "DATETIME")
    private Timestamp fechaCreacion;

    @PrePersist
    protected void onCreate() {
        this.fechaCreacion = new Timestamp(System.currentTimeMillis());
    }

    public AlertasCongestion() {
    }

    public AlertasCongestion(int id, int fila, int columna, int cantidad, Timestamp fechaCreacion) {
        this.id = id;
        this.fila = fila;
        this.columna = columna;
        this.cantidad = cantidad;
        this.fechaCreacion = fechaCreacion;
    }

    // Getters y setters

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getFila() {
        return fila;
    }

    public void setFila(int fila) {
        this.fila = fila;
    }

    public int getColumna() {
        return columna;
    }

    public void setColumna(int columna) {
        this.columna = columna;
    }

    public int getCantidad() {
        return cantidad;
    }

    public void setCantidad(int cantidad) {
        this.cantidad = cantidad;
    }

    public Timestamp getFechaCreacion() {
        return fechaCreacion;
    }

    public void setFechaCreacion(Timestamp fechaCreacion) {
        this.fechaCreacion = fechaCreacion;
    }
}
