#pragma once
#include <SFML/Graphics.hpp>

class Paletka {
private:
    float x, y;
    float szerokosc, wysokosc;
    float predkosc;
    sf::RectangleShape shape;

public:
    Paletka(float px, float py, float szer, float wys, float spd);

    void moveLeft();
    void moveRight();
    void clampToBounds(float width);
    void draw(sf::RenderTarget& target);

    void setPosition(const sf::Vector2f& pos);

    float getX() const;
    float getY() const;
    float getSzerokosc() const;
    float getWysokosc() const;

    sf::FloatRect getGlobalBounds() const {
        return shape.getGlobalBounds();
    }

};

