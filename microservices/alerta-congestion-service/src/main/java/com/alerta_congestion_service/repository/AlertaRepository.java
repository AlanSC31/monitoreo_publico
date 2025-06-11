package com.alerta_congestion_service.repository;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.alerta_congestion_service.model.AlertasCongestion;

@Repository
public interface AlertaRepository extends JpaRepository<AlertasCongestion, Long> {
   List<AlertasCongestion> findByFechaCreacionBetween(LocalDateTime desde, LocalDateTime hasta);

 
}
