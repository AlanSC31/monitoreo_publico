package com.alerta_congestion_service.service;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.alerta_congestion_service.model.AlertasCongestion;
import com.alerta_congestion_service.repository.AlertaRepository;

@Service
public class AlertaService {
   @Autowired
   private AlertaRepository alertaRep; 
   

   public List<AlertasCongestion> obtenerPorFechas(LocalDateTime desde, LocalDateTime hasta) {
    return alertaRep.findByFechaCreacionBetween(desde, hasta);
}

}
