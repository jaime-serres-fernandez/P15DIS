package com.videogames.backend.repository;

import com.videogames.backend.model.Videogame;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface VideogameRepository extends JpaRepository<Videogame, Long> {
    
    // Find by title (case insensitive)
    List<Videogame> findByTitleContainingIgnoreCase(String title);
    
    // Find by genre
    List<Videogame> findByGenreIgnoreCase(String genre);
    
    // Find by platform
    List<Videogame> findByPlatformIgnoreCase(String platform);
    
    // Find by release year
    List<Videogame> findByReleaseYear(Integer year);
    
    // Find games released after a specific year
    List<Videogame> findByReleaseYearGreaterThanEqual(Integer year);
}