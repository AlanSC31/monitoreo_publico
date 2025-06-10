package com.conteo_zona_service.service;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.conteo_zona_service.model.ConteoZona;
import com.conteo_zona_service.repository.ConteoRepository;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ConteoService {

    @Autowired
    private ConteoRepository repository;

    public List<ConteoZona> obtenerPorTimestamp(LocalDateTime timestamp) {
        return repository.findByTimestamp(timestamp);
    }

    public List<ConteoZona> obtenerPorRango(LocalDateTime desde, LocalDateTime hasta) {
        return repository.findByTimestampBetween(desde, hasta);
    }
}
