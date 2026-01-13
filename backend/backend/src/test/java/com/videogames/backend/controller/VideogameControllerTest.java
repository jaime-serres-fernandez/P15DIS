package com.videogames.backend.controller;

import com.videogames.backend.model.Videogame;
import com.videogames.backend.service.VideogameService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import java.math.BigDecimal;
import java.util.Arrays;
import java.util.Optional;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(VideogameController.class)
class VideogameControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private VideogameService service;
    
    @Test
    void getAllVideogames_shouldReturnList() throws Exception {
        Videogame game1 = new Videogame("Zelda", "Action", "Switch", 2017, new BigDecimal("9.5"), new BigDecimal("59.99"));
        Videogame game2 = new Videogame("Mario", "Platform", "Switch", 2017, new BigDecimal("9.0"), new BigDecimal("59.99"));
        
        when(service.findAll()).thenReturn(Arrays.asList(game1, game2));
        
        mockMvc.perform(get("/api/videogames"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].title").value("Zelda"))
            .andExpect(jsonPath("$[1].title").value("Mario"));
    }
    
    @Test
    void getVideogameById_shouldReturnVideogame() throws Exception {
        Videogame game = new Videogame("Zelda", "Action", "Switch", 2017, new BigDecimal("9.5"), new BigDecimal("59.99"));
        game.setId(1L);
        
        when(service.findById(1L)).thenReturn(Optional.of(game));
        
        mockMvc.perform(get("/api/videogames/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.title").value("Zelda"));
    }
    
    @Test
    void createVideogame_shouldReturnCreated() throws Exception {
        Videogame game = new Videogame("New Game", "RPG", "PC", 2023, new BigDecimal("8.5"), new BigDecimal("49.99"));
        game.setId(1L);
        
        when(service.save(any(Videogame.class))).thenReturn(game);
        
        String json = """
            {
                "title": "New Game",
                "genre": "RPG",
                "platform": "PC",
                "releaseYear": 2023,
                "rating": 8.5,
                "price": 49.99
            }
            """;
        
        mockMvc.perform(post("/api/videogames")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.title").value("New Game"));
    }
    
    @Test
    void deleteVideogame_shouldReturnNoContent() throws Exception {
        mockMvc.perform(delete("/api/videogames/1"))
            .andExpect(status().isNoContent());
    }
}