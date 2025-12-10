#pragma once
#include <SFML/Graphics.hpp>
#include<array> 

class Brick : public sf::RectangleShape {
	
private:
	int punktyZycia; //0-3


	bool jestZniszczony; //if zniszczony = true
	static const std::array<sf::Color, 4> colorLUT; 


public:


	sf::Vector2f getSize() const { return sf::RectangleShape::getSize(); }

	int getHP() const { return punktyZycia; }
	Brick(sf::Vector2f startPo, sf::Vector2f rozmiar, int L);
	void aktualizujKolor();//f zmienia kolor klocka w zaleznosci od L
	void trafienie();
	void draw(sf::RenderTarget& window);
	bool czyZniszczony() const { 
		return jestZniszczony;


	}
};

