#include <iostream>
#include <list>

int main() {
    std::list<int> l;

    for(int i = 0; i < 20; i=i+1) {
        l.push_back(i);
    }

    for(auto it : l) {
        std::cout << it << " ";
    }
    std::cout << std::endl;

    for(auto it = l.begin(); it != l.end();) {
        if (*it % 2 == 0) {
            it = l.erase(it);
        } else {
            ++it;
        }
    }
    for(auto it : l) {
        std::cout << it << " ";
    }
    std::cout << std::endl;

    l.front() -= 1;

    for(auto it : l) {
        std::cout << it << " ";
    }
    std::cout << std::endl;




}