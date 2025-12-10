#include "Brick.h"


Brick::Brick(sf::Vector2f startPo, sf::Vector2f rozmiar, int L) {
	punktyZycia = L;
	jestZniszczony = false; 
	this->setFillColor(sf::Color::Yellow);
	this->setOutlineColor(sf::Color::White);
	this->setSize(rozmiar);
	this->setPosition(startPo);

	aktualizujKolor();
}

const std::array<sf::Color, 4> Brick::colorLUT = {
	sf::Color::Transparent,
	sf::Color::Yellow,
	sf::Color::Magenta,
	sf::Color::Red
};

void Brick::trafienie() {
	if (jestZniszczony == true)
		return;
	punktyZycia--;

	if (punktyZycia < 1)
	{
		punktyZycia = 0;
		jestZniszczony = true;
	}
	aktualizujKolor();
}

void Brick::aktualizujKolor() {
	if (punktyZycia > 0)
		this->setFillColor(colorLUT[punktyZycia]);
}

void Brick::draw(sf::RenderTarget& window) {
	window.draw(*this);
}
