#include <iostream>
#include <fstream>
#include <vector>
#include <string>

class CSVReader 
{
    private:
        std::string fileName;
        std::ifstream file;
        

    public:
        CSVReader(std::string fileName) : fileName(fileName) {}; 
        int openFile();
        void closeFile();
        std::vector<std::vector<std::string>> getRows(char delim, bool includeFieldName);
        std::vector<std::string> splitString(std::string s, const char delim);
           
};