package com.videogames.backend.controller;

import com.videogames.backend.model.Videogame;
import com.videogames.backend.service.VideogameService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/videogames")
@CrossOrigin(origins = "*")
public class VideogameController {
    
    @Autowired
    private VideogameService service;
    
    @GetMapping
    public ResponseEntity<List<Videogame>> getAllVideogames() {
        List<Videogame> videogames = service.findAll();
        return ResponseEntity.ok(videogames);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Videogame> getVideogameById(@PathVariable Long id) {
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<Videogame> createVideogame(@Valid @RequestBody Videogame videogame) {
        Videogame saved = service.save(videogame);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Videogame> updateVideogame(
            @PathVariable Long id, 
            @Valid @RequestBody Videogame videogameDetails) {
        try {
            Videogame updated = service.update(id, videogameDetails);
            return ResponseEntity.ok(updated);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteVideogame(@PathVariable Long id) {
        try {
            service.deleteById(id);
            return ResponseEntity.noContent().build();
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @GetMapping("/search")
    public ResponseEntity<List<Videogame>> searchVideogames(@RequestParam String title) {
        List<Videogame> videogames = service.searchByTitle(title);
        return ResponseEntity.ok(videogames);
    }
    
    @GetMapping("/genre/{genre}")
    public ResponseEntity<List<Videogame>> getByGenre(@PathVariable String genre) {
        List<Videogame> videogames = service.findByGenre(genre);
        return ResponseEntity.ok(videogames);
    }
    
    @GetMapping("/platform/{platform}")
    public ResponseEntity<List<Videogame>> getByPlatform(@PathVariable String platform) {
        List<Videogame> videogames = service.findByPlatform(platform);
        return ResponseEntity.ok(videogames);
    }
}
