#include <string>
#include <cmath>

class City {
    private:
        std::string name;
        double x;
        double y;

    public:
        City(std::string name, double x, double y) : name(name), x(x), y(y) {};
        double distanceTo(City* otherCity);
        std::string getName();
        double getX();
        double getY();
};