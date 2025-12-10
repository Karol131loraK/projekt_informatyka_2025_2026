#include "Game.h"
#include <algorithm>
#include <iostream>
#include <fstream>
#include <cmath> 

Game::Game()
    : m_paletka(320.f, 440.f, 100.f, 20.f, 8.f),
    m_pilka(320.f, 200.f, 4.f, 3.f, 8.f)
{
    initBlocks();
}

void Game::initBlocks() {
    const int ILOSC_KOLUMN = 12;
    const int ILOSC_WIERSZY = 3; // liczba warstw
    const float WIDTH = 800.f;
    const float ROZMIAR_BLOKU_X = (WIDTH - (ILOSC_KOLUMN - 1) * 2.f) / ILOSC_KOLUMN;
    const float ROZMIAR_BLOKU_Y = 20.f;

    for (int y = 0; y < ILOSC_WIERSZY; y++) {
        for (int x = 0; x < ILOSC_KOLUMN; x++) {
            float posX = x * (ROZMIAR_BLOKU_X + 2.f);
            float posY = y * (ROZMIAR_BLOKU_Y + 2.f) + 60.f;

            int zycie = 3;//ile razy uderzyc w blok

            m_bloki.emplace_back(sf::Vector2f(posX, posY),
                sf::Vector2f(ROZMIAR_BLOKU_X, ROZMIAR_BLOKU_Y),
                zycie);
        }
    }
}


void Game::updateCollision() {
    for (auto& blk : m_bloki) {
        if (blk.czyZniszczony()) continue;

        sf::FloatRect ballBounds = m_pilka.getGlobalBounds();
        sf::FloatRect blockBounds = blk.getGlobalBounds();
        sf::FloatRect intersection;

        if (ballBounds.intersects(blockBounds, intersection)) {

            blk.trafienie();
            addScore(1);
            std::cout << "Wynik: " << getScore() << "\n";


            
            bool uderzenieWBok = intersection.width < intersection.height;

            if (uderzenieWBok) {   // Kolizja boki
                
                if (ballBounds.left < blockBounds.left) {
                    m_pilka.setPosition(sf::Vector2f(m_pilka.getX() - intersection.width, m_pilka.getY()));
                    
                }
                else {
                    m_pilka.setPosition(sf::Vector2f(m_pilka.getX() + intersection.width, m_pilka.getY()));
                }
                m_pilka.bounceX();
            }
            else { //kolizja gora dol

                if (ballBounds.top < blockBounds.top) {
                    m_pilka.setPosition(sf::Vector2f(m_pilka.getX(), m_pilka.getY() - intersection.height));
                }
                else {
                    m_pilka.setPosition(sf::Vector2f(m_pilka.getX(), m_pilka.getY() + intersection.height));
                }

                m_pilka.bounceY();
                std::cout << "HIT WALL\n";
               
            }

            break;
        }
    }

    // Usuwanie blokow zniszczonych
    m_bloki.erase(std::remove_if(m_bloki.begin(), m_bloki.end(),
        [](const Brick& b) { return b.czyZniszczony(); }),
        m_bloki.end());
}

void Game::update(sf::Time dt) {
    // Sterowanie paletka
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::A) || sf::Keyboard::isKeyPressed(sf::Keyboard::Left))
        m_paletka.moveLeft();
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::D) || sf::Keyboard::isKeyPressed(sf::Keyboard::Right))
        m_paletka.moveRight();

    m_paletka.clampToBounds(800.f);

    m_pilka.move();

    // Odbicia od scian
    m_pilka.collideWalls(800.f, 600.f);


  
    if (m_pilka.collidePaddle(m_paletka)) { // kolizja z paletka

        std::cout << "HIT PADDLE\n";

        int bestScore = 0;
        std::ifstream infile("najlepszy_wynik.txt");
        if (infile.is_open()) {
            infile >> bestScore;
            infile.close();
        }
        if (m_score > bestScore) {
            std::ofstream outfile("najlepszy_wynik.txt");
            if (outfile.is_open()) {
                outfile << m_score;
                outfile.close();
            }
        }
    }

    // MISS 
    if (m_pilka.getY() - m_pilka.getRadius() > 600.f) {
        std::cout << "MISS! KONIEC GRY\n";
        m_przegrana = true;
        return;
    }
    // Kolizje z blokami
    updateCollision();




    if (m_bloki.empty()) {
        std::cout << "PUSTO! WYGRALES!\n";
        m_wygrana = true;
    }
}

void Game::render(sf::RenderTarget& target) {
    m_paletka.draw(target);
    m_pilka.draw(target);
    for (auto& blk : m_bloki)
        blk.draw(target);
}

bool Game::isLost() const {
    return (m_pilka.getY() - m_pilka.getRadius() > 600.f);
}


