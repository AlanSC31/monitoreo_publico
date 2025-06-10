package com.conteo_zona_service.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.conteo_zona_service.model.ConteoZona;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface ConteoRepository extends JpaRepository<ConteoZona, Integer> {

    // Buscar por timestamp exacto
    List<ConteoZona> findByTimestamp(LocalDateTime timestamp);

    // Si quieres rango, también podrías agregar:
    List<ConteoZona> findByTimestampBetween(LocalDateTime desde, LocalDateTime hasta);
}

