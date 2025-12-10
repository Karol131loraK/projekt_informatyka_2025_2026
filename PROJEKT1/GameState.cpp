#include "GameState.h"
#include <fstream>
#include <iostream>

void GameState::capture(const Paletka& paletka, const Pilka& pilka, const std::vector<Brick>& bloki, int score) {
    paddlePosition = sf::Vector2f(paletka.getX(), paletka.getY());
    ballPosition = sf::Vector2f(pilka.getX(), pilka.getY());
    ballVelocity = sf::Vector2f(pilka.getVx(), pilka.getVy());

    savedScore = score; // Zapamietany wynik

    blocks.clear();
    blocks.reserve(bloki.size());
    for (const auto& b : bloki) {
        blocks.push_back({ b.getPosition().x, b.getPosition().y, b.getHP() });
    }
}

bool GameState::saveToFile(const std::string& filename) {
    std::ofstream file(filename);
    if (!file.is_open()) return false;

    file << "SCORE " << savedScore << "\n";

    file << "PADDLE " << paddlePosition.x << " " << paddlePosition.y << "\n";
    file << "BALL " << ballPosition.x << " " << ballPosition.y << " " << ballVelocity.x << " " << ballVelocity.y << "\n";
    file << "BLOCKS_COUNT " << blocks.size() << "\n";

    for (const auto& b : blocks)
        file << b.x << " " << b.y << " " << b.hp << "\n";

    file.close();
    return true;
}

bool GameState::loadFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) return false;

    std::string label;
    int blocksCount;
    float x, y;
    int hp;

    
    file >> label >> savedScore;

    file >> label >> paddlePosition.x >> paddlePosition.y;

    file >> label >> ballPosition.x >> ballPosition.y >> ballVelocity.x >> ballVelocity.y;

    file >> label >> blocksCount;
    blocks.clear();
    for (int i = 0; i < blocksCount; ++i) {
        file >> x >> y >> hp;
        blocks.push_back({ x, y, hp });
    }

    file.close();
    return true;
}

void GameState::apply(Paletka& paletka, Pilka& pilka, std::vector<Brick>& bloki) {
    paletka.setPosition(paddlePosition);
    pilka.setPosition(ballPosition);
    pilka.setVelocity(ballVelocity);


    sf::Vector2f blockSize = bloki.empty() ? sf::Vector2f(50, 20) : bloki[0].getSize();

    bloki.clear();
    for (const auto& b : blocks) {
        bloki.emplace_back(sf::Vector2f(b.x, b.y), blockSize, b.hp);
    }
}