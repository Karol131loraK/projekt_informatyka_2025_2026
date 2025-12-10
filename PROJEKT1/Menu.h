#pragma once
#include <SFML/Graphics.hpp>
#include <algorithm>
#include <iostream>

class Menu {
private:
    int m_selectedItem = 0; //0=nowa gra, 1=wyczytaj grê, 2=najlepszy wynik, 3=wyjscie
    static const int MAX_ITEMS = 4;
    sf::Font m_font;

public:
    Menu(int windowWidth, int windowHeight) {
        
        if (!m_font.loadFromFile("arial.ttf")) {
            std::cerr << "Nie uda³o siê za³adowaæ fontu!\n";
        }
    }

    void handleEvent(const sf::Event& event) {
        if (event.type == sf::Event::KeyPressed) {
            if (event.key.code == sf::Keyboard::Up)
                m_selectedItem = std::max(0, m_selectedItem - 1);
            else if (event.key.code == sf::Keyboard::Down)
                m_selectedItem = std::min(MAX_ITEMS - 1, m_selectedItem + 1);
        }
    }

    int getSelectedItem() const { return m_selectedItem; }

    void draw(sf::RenderTarget& target) {
    //prostokaty
        sf::RectangleShape option1(sf::Vector2f(200, 50));
        option1.setPosition(300, 180);
        option1.setFillColor(m_selectedItem == 0 ? sf::Color::Green : sf::Color::White);
        target.draw(option1);

        sf::RectangleShape option2(sf::Vector2f(200, 50));
        option2.setPosition(300, 250);
        option2.setFillColor(m_selectedItem == 1 ? sf::Color::Yellow : sf::Color::White);
        target.draw(option2);

        sf::RectangleShape option3(sf::Vector2f(200, 50));
        option3.setPosition(300, 320);
        option3.setFillColor(m_selectedItem == 2 ? sf::Color::Cyan : sf::Color::White);
        target.draw(option3);

        sf::RectangleShape option4(sf::Vector2f(200, 50));
        option4.setPosition(300, 390);
        option4.setFillColor(m_selectedItem == 3 ? sf::Color::Red : sf::Color::White);
        target.draw(option4);

        // teksty
        sf::Text text;
        text.setFont(m_font);
        text.setCharacterSize(24);
        text.setFillColor(sf::Color::Black);

        text.setString("Start");
        text.setPosition(370, 190);
        target.draw(text);

        text.setString("Wczytaj gre");
        text.setPosition(335, 260);
        target.draw(text);

        text.setString("Najlepszy wynik");
        text.setPosition(310, 330);
        target.draw(text);

        text.setString("Wyjscie");
        text.setPosition(360, 400);
        target.draw(text);
    }
};



