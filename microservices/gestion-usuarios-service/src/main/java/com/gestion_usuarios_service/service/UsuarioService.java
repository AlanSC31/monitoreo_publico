package com.gestion_usuarios_service.service;

import com.gestion_usuarios_service.model.Usuario; 
import com.gestion_usuarios_service.repository.UsuarioRepository;

import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class UsuarioService {
    private final UsuarioRepository usuarioRep;

    public UsuarioService(UsuarioRepository usuarioRep){
        this.usuarioRep = usuarioRep;
    }

    public List<Usuario> listarUsuarios(){
        return usuarioRep.findAll();
    }
    
}
