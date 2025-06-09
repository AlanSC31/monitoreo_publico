package com.gestion_usuarios_service.controller;

import com.gestion_usuarios_service.model.Usuario;
import com.gestion_usuarios_service.service.UsuarioService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/usuarios")
public class UsuarioController {
    private final UsuarioService usuarioService;

    public UsuarioController(UsuarioService usuarioService){
        this.usuarioService = usuarioService;
    }

    @GetMapping
    public List<Usuario> getUsuarios() {
        return usuarioService.listarUsuarios();
    }
}
    