#pragma once
#include <SFML/Graphics.hpp>
#include "Paletka.h"

class Pilka {
private:
    float x, y;
    float vx, vy;
    float radius;
    sf::CircleShape shape;

public:
    Pilka(float px, float py, float pvx, float pvy, float r);

    void move();
    void bounceX();
    void bounceY();

    void collideWalls(float width, float height);
    bool collidePaddle(const Paletka& p);
    void draw(sf::RenderTarget& target);

    void setPosition(const sf::Vector2f& pos);
    void setVelocity(const sf::Vector2f& vel);


    float getX() const;
    float getY() const;
    float getVx() const;
    float getVy() const;
    float getRadius() const;
    sf::FloatRect getGlobalBounds() const;

};
