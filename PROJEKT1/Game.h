#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include <string> 
#include "Paletka.h"
#include "Pilka.h"
#include "Brick.h"

class Game {
private:
    Paletka m_paletka;
    Pilka m_pilka;
    std::vector<Brick> m_bloki;

    
    sf::Font m_font;
    sf::Text m_scoreText;

    void initBlocks();
    void updateCollision();


    bool m_przegrana = false;
    bool m_wygrana = false;
    int m_score = 0;



public:
    Game();

    void update(sf::Time dt);
    void render(sf::RenderTarget& target);
    bool isLost() const;
    bool isWon() const { return m_wygrana; }

    Paletka& getPaddle() { return m_paletka; }
    Pilka& getBall() { return m_pilka; }
    std::vector<Brick>& getBlocks() { return m_bloki; }

    int getScore() const { return m_score; }
    void addScore(int points) { m_score += points; }

    void setScore(int s) {
        m_score = s;
        
        m_scoreText.setString("Score: " + std::to_string(m_score));
    }
    
};




