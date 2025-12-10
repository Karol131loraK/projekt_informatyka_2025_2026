#include "Pilka.h"
#include <cmath>

Pilka::Pilka(float px, float py, float pvx, float pvy, float r)
    : x(px), y(py), vx(pvx), vy(pvy), radius(r) {
    shape.setRadius(radius);
    shape.setOrigin(radius, radius);
    shape.setPosition(x, y);
    shape.setFillColor(sf::Color::White);
}

void Pilka::move() {
    x += vx;
    y += vy;
    shape.setPosition(x, y);
}

void Pilka::bounceX() { vx = -vx; }
void Pilka::bounceY() { vy = -vy; }

void Pilka::collideWalls(float width, float height) {
    if (x - radius <= 0) { x = radius; bounceX(); }
    if (x + radius >= width) { x = width - radius; bounceX(); }
    if (y - radius <= 0) { y = radius; bounceY(); }
    // dó³ - brak odbicia, koniec gry
}

bool Pilka::collidePaddle(const Paletka& p) {
    float palX = p.getX();
    float palY = p.getY();
    float palW = p.getSzerokosc();
    float palH = p.getWysokosc();

    // Kolizja tylko jeœli pi³ka idzie w dó³
    if (vy > 0 &&
        x + radius >= palX - palW / 2.f && x - radius <= palX + palW / 2.f &&
        y + radius >= palY - palH / 2.f && y - radius <= palY + palH / 2.f) {

        vy = -std::abs(vy);                    // odbicie w górê
        y = palY - palH / 2.f - radius;       // ustawienie pi³ki nad paletk¹
        shape.setPosition(x, y);
        return true;
    }
    return false;
}



void Pilka::draw(sf::RenderTarget& target) {
    target.draw(shape);
}


void Pilka::setPosition(const sf::Vector2f& pos) { x = pos.x; y = pos.y; shape.setPosition(x, y); }
void Pilka::setVelocity(const sf::Vector2f& vel) { vx = vel.x; vy = vel.y; }


float Pilka::getX() const { return x; }
float Pilka::getY() const { return y; }
float Pilka::getVx() const { return vx; }
float Pilka::getVy() const { return vy; }
float Pilka::getRadius() const { return radius; }



sf::FloatRect Pilka::getGlobalBounds() const {
    return shape.getGlobalBounds();
}
