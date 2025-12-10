#include <SFML/Graphics.hpp>
#include "Game.h"
#include "Menu.h"
#include "GameState.h"
#include <iostream>
#include <fstream>

void saveBestScore(int score) {
    int bestScore = 0;
    std::ifstream infile("najlepszy_wynik.txt");
    if (infile.is_open()) {
        infile >> bestScore;
        infile.close();
    }
    if (score > bestScore) {
        std::ofstream outfile("najlepszy_wynik.txt");
        if (outfile.is_open()) {
            outfile << score;
            outfile.close();
        }
    }
}

enum class AppState { Menu, Playing, Paused };

int main() {
    
    std::ifstream infile("najlepszy_wynik.txt");
    if (!infile.is_open()) {
        std::ofstream outfile("najlepszy_wynik.txt");
        outfile << 0;
    }
    infile.close();

    sf::RenderWindow window(sf::VideoMode(800, 600), "Arkanoid");
    window.setFramerateLimit(60);

    Menu menu(800, 600);
    Game game;
    AppState currentState = AppState::Menu;

    GameState snapshot;
    sf::Clock clock;

    while (window.isOpen()) {
        sf::Time dt = clock.restart();
        sf::Event event;

        while (window.pollEvent(event)) {


            if (event.type == sf::Event::Closed)
                window.close();

            if (event.type == sf::Event::KeyPressed) {


                if (currentState == AppState::Menu) {
                    menu.handleEvent(event); 

                    // ENTER - Wybór opcji
                    if (event.key.code == sf::Keyboard::Enter) {
                        switch (menu.getSelectedItem()) {
                        case 0: // Nowa gra
                            game = Game();
                            currentState = AppState::Playing;
                            break;

                        case 1: // Wczytaj grê
                            if (snapshot.loadFromFile("zapis.txt")) {
                                // Przywracamy pozycje
                                snapshot.apply(game.getPaddle(), game.getBall(), game.getBlocks());

                                // WA¯NE: Przywracamy wynik
                                game.setScore(snapshot.getSavedScore());

                                currentState = AppState::Playing;
                                std::cout << "Gra wczytana! Wynik: " << game.getScore() << "\n";
                            }
                            else {
                                std::cout << "Nie udalo sie wczytac gry!\n";
                            }
                            break;

                        case 2: { // Najlepszy wynik
                            std::ifstream file("najlepszy_wynik.txt");
                            int bestScore = 0;
                            if (file.is_open()) {
                                file >> bestScore;
                                file.close();
                            }
                            std::cout << "Najlepszy wynik: " << bestScore << "\n";
                            break;
                        }

                        case 3: // Wyjœcie
                            window.close();
                            break;
                        }
                    }
                }

                // --- LOGIKA GRY (PAUZA I ZAPIS) ---

                // Klawisz P - Pauza
                if (event.key.code == sf::Keyboard::P) {
                    if (currentState == AppState::Playing) {
                        currentState = AppState::Paused;
                        std::cout << "Gra pauzowana!\n";
                    }
                    else if (currentState == AppState::Paused) {
                        currentState = AppState::Playing;
                        std::cout << "Gra wznowiona!\n";
                    }
                }

                // Klawisz F5 - Zapis (dzia³a tylko podczas gry lub pauzy)
                // Klawisz F5 - Zapis
                if (event.key.code == sf::Keyboard::F5 && (currentState == AppState::Playing || currentState == AppState::Paused)) {

                    // WA¯NE: Przekazujemy game.getScore() jako czwarty argument!
                    snapshot.capture(game.getPaddle(), game.getBall(), game.getBlocks(), game.getScore());

                    if (snapshot.saveToFile("zapis.txt"))
                        std::cout << "Gra zapisana! Wynik: " << game.getScore() << "\n";
                    else
                        std::cout << "Blad zapisu!\n";
                }
            }
        }
        // --- KONIEC PÊTLI ZDARZEÑ ---


        // Logika gry (ci¹g³a)
        if (currentState == AppState::Playing)
            game.update(dt);

        // Sprawdzenie przegranej
        if (currentState == AppState::Playing && game.isLost()) {
            int playerScore = game.getScore();
            saveBestScore(playerScore);
            currentState = AppState::Menu;
            game = Game(); 
            std::cout << "Przegrana! Powrot do menu.\n";
        }


        if (currentState == AppState::Playing && game.isWon()) {
            int playerScore = game.getScore();

            saveBestScore(playerScore);

            currentState = AppState::Menu;
            game = Game();

            std::cout << "\n=================================\n";
            std::cout << "   GRATULACJE! WYGRALES GRE!     \n";
            std::cout << "   Wszystkie bloki zniszczone.   \n";
            std::cout << "=================================\n\n";
        }



        window.clear();
        if (currentState == AppState::Menu)
            menu.draw(window);
        else
            game.render(window); 

        window.display();
    }

    return 0;
}

