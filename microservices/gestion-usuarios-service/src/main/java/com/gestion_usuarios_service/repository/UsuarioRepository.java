package com.gestion_usuarios_service.repository;

import com.gestion_usuarios_service.model.Usuario;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    Usuario findByNombre(String nombre);
    List<Usuario> findByStatusTrue();
}