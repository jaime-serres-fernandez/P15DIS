package com.videogames.backend.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;

@Entity
@Table(name = "videogames")
public class Videogame {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotBlank(message = "Title is required")
    @Size(min = 1, max = 200)
    @Column(nullable = false, length = 200)
    private String title;
    
    @NotBlank(message = "Genre is required")
    @Size(max = 50)
    @Column(nullable = false, length = 50)
    private String genre;
    
    @NotBlank(message = "Platform is required")
    @Size(max = 50)
    @Column(nullable = false, length = 50)
    private String platform;
    
    @Min(value = 1970, message = "Release year must be >= 1970")
    @Max(value = 2030, message = "Release year must be <= 2030")
    @Column(name = "release_year")
    private Integer releaseYear;
    
    @DecimalMin(value = "0.0", message = "Rating must be >= 0")
    @DecimalMax(value = "10.0", message = "Rating must be <= 10")
    @Column(precision = 3, scale = 1)
    private BigDecimal rating;
    
    @DecimalMin(value = "0.0", message = "Price must be >= 0")
    @Column(precision = 10, scale = 2)
    private BigDecimal price;
    
    @Column(length = 1000)
    private String description;
    
    // Constructors
    public Videogame() {}
    
    public Videogame(String title, String genre, String platform, Integer releaseYear, BigDecimal rating, BigDecimal price) {
        this.title = title;
        this.genre = genre;
        this.platform = platform;
        this.releaseYear = releaseYear;
        this.rating = rating;
        this.price = price;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getTitle() {
        return title;
    }
    
    public void setTitle(String title) {
        this.title = title;
    }
    
    public String getGenre() {
        return genre;
    }
    
    public void setGenre(String genre) {
        this.genre = genre;
    }
    
    public String getPlatform() {
        return platform;
    }
    
    public void setPlatform(String platform) {
        this.platform = platform;
    }
    
    public Integer getReleaseYear() {
        return releaseYear;
    }
    
    public void setReleaseYear(Integer releaseYear) {
        this.releaseYear = releaseYear;
    }
    
    public BigDecimal getRating() {
        return rating;
    }
    
    public void setRating(BigDecimal rating) {
        this.rating = rating;
    }
    
    public BigDecimal getPrice() {
        return price;
    }
    
    public void setPrice(BigDecimal price) {
        this.price = price;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    @Override
    public String toString() {
        return "Videogame{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", genre='" + genre + '\'' +
                ", platform='" + platform + '\'' +
                ", releaseYear=" + releaseYear +
                ", rating=" + rating +
                ", price=" + price +
                '}';
    }
}