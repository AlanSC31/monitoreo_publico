package com.gestion_usuarios_service.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Usuario {
    private String nombre;
    @Id
    private String uid;
    private int rol;
    private boolean status;

    // empty constructor
    public Usuario() {
    }

    public Usuario(String nombre, String uid, int rol, boolean status) {
        this.uid = uid;
        this.nombre = nombre;
        this.rol = rol;
        this.status = status;
    }
    // getters and setters

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getUid() {
        return uid;
    }

    public void setUid(String uid) {
        this.uid = uid;
    }

    public int getRol() {
        return rol;
    }

    public void setRol(int rol) {
        this.rol = rol;
    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }
}