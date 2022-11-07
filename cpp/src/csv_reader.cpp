#include "csv_reader.h" 
int CSVReader::openFile() {
    file.open(this->fileName);

    if(file.fail()) {
        std::cerr << "Can't open " << this->fileName << std::endl;
        return 1;
    } 

    return 0;  
}

void CSVReader::closeFile() {
    file.close();
}

// https://stackoverflow.com/questions/14265581/parse-split-a-string-in-c-using-string-delimiter-standard-c
std::vector<std::string> CSVReader::splitString(std::string line, const char delim) {
    std::vector<std::string> tokens;
    size_t curPos = 0, nextPos = 0;

    // find at or after curPos, ignore occurences before
    while ((nextPos = line.find(delim, curPos)) != std::string::npos) {
           // from curPos take the next nextPos-curPos characters 
           std::string subString = line.substr(curPos, nextPos-curPos);
           if (subString.length() != 0) {
            tokens.push_back(subString);
           }  
           //tokens.push_back(line.substr(curPos, nextPos-curPos));
           curPos = nextPos + 1;
        }

    tokens.push_back(line.substr(curPos, std::string::npos));

    return tokens;
}

std::vector<std::vector<std::string>> CSVReader::getRows(char delim, bool includeFieldNames) {
    std::string line;
    std::vector<std::vector<std::string>> rows;

    if(!includeFieldNames)
        std::getline(file, line);

    while(std::getline(file, line)) { rows.push_back(this->splitString(line, delim)); }

    return rows; 
}