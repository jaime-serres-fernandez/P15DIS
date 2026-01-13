package com.videogames.backend.service;

import com.videogames.backend.model.Videogame;
import com.videogames.backend.repository.VideogameRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class VideogameService {
    
    @Autowired
    private VideogameRepository repository;
    
    public List<Videogame> findAll() {
        return repository.findAll();
    }
    
    public Optional<Videogame> findById(Long id) {
        return repository.findById(id);
    }
    
    public Videogame save(Videogame videogame) {
        return repository.save(videogame);
    }
    
    public Videogame update(Long id, Videogame videogameDetails) {
        Videogame videogame = repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Videogame not found with id: " + id));
        
        videogame.setTitle(videogameDetails.getTitle());
        videogame.setGenre(videogameDetails.getGenre());
        videogame.setPlatform(videogameDetails.getPlatform());
        videogame.setReleaseYear(videogameDetails.getReleaseYear());
        videogame.setRating(videogameDetails.getRating());
        videogame.setPrice(videogameDetails.getPrice());
        videogame.setDescription(videogameDetails.getDescription());
        
        return repository.save(videogame);
    }
    
    public void deleteById(Long id) {
        repository.deleteById(id);
    }
    
    public List<Videogame> searchByTitle(String title) {
        return repository.findByTitleContainingIgnoreCase(title);
    }
    
    public List<Videogame> findByGenre(String genre) {
        return repository.findByGenreIgnoreCase(genre);
    }
    
    public List<Videogame> findByPlatform(String platform) {
        return repository.findByPlatformIgnoreCase(platform);
    }
}
