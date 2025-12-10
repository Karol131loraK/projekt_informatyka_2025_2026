#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include <string>
#include "Paletka.h"
#include "Pilka.h"
#include "Brick.h"

struct BlockData {
    float x, y;
    int hp;
};

class GameState {
private:
    sf::Vector2f paddlePosition;
    sf::Vector2f ballPosition;
    sf::Vector2f ballVelocity;
    std::vector<BlockData> blocks;

    int savedScore = 0;

public:
    GameState() = default;

    void capture(const Paletka& paletka, const Pilka& pilka, const std::vector<Brick>& bloki, int score);

    void apply(Paletka& paletka, Pilka& pilka, std::vector<Brick>& bloki);

    bool saveToFile(const std::string& filename);
    bool loadFromFile(const std::string& filename);

    int getSavedScore() const { return savedScore; }

    const sf::Vector2f& getPaddlePos() const { return paddlePosition; }
    const sf::Vector2f& getBallPos() const { return ballPosition; }
    const sf::Vector2f& getBallVel() const { return ballVelocity; }
    const std::vector<BlockData>& getBlocks() const { return blocks; }
};



