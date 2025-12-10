#include "Paletka.h"

Paletka::Paletka(float px, float py, float szer, float wys, float spd)
    : x(px), y(py), szerokosc(szer), wysokosc(wys), predkosc(spd) {
    shape.setSize({ szerokosc, wysokosc });
    shape.setOrigin(szerokosc / 2.f, wysokosc / 2.f);
    shape.setPosition(x, y);
    shape.setFillColor(sf::Color::Green);
}

void Paletka::moveLeft() {
    x -= predkosc;
    shape.setPosition(x, y);
}

void Paletka::moveRight() {
    x += predkosc;
    shape.setPosition(x, y);
}

void Paletka::clampToBounds(float width) {
    if (x - szerokosc / 2.f < 0) x = szerokosc / 2.f;
    if (x + szerokosc / 2.f > width) x = width - szerokosc / 2.f;
    shape.setPosition(x, y);
}

void Paletka::draw(sf::RenderTarget& target) {
    target.draw(shape);
}


void Paletka::setPosition(const sf::Vector2f& pos) {
    x = pos.x;
    y = pos.y;
    shape.setPosition(x, y);
}

float Paletka::getX() const { return x; }
float Paletka::getY() const { return y; }
float Paletka::getSzerokosc() const { return szerokosc; }
float Paletka::getWysokosc() const { return wysokosc; }
