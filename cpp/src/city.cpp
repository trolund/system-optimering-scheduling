#include "city.h"

double City::distanceTo(City* otherCity) {
    return sqrt( ((this->x-otherCity->x) * (this->x-otherCity->x)) + ((this->y-otherCity->y) * (this->y-otherCity->y)) );
}

std::string City::getName() { return this->name; }

double City::getX() { return this->x; }

double City::getY() { return this->y; }