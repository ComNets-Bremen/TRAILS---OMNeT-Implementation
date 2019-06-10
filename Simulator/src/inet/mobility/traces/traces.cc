//User behavior for the Traces model
#include "traces.h"

namespace inet {
    Define_Module(TRACES);
    TRACES::TRACES(){}

    //Splits strings into vectors
    //      Input
    //  line: Input String
    //  delimiter: delimiter
    //      Output
    //  vec: String vector
    vector<string> TRACES::splitString(string line, string delimiter) {
        vector<string> vec;
        size_t pos = 0;
        string token;
        while ((pos = line.find(delimiter)) != string::npos) {
            token = line.substr(0, pos);
            vec.push_back(token);
            line.erase(0, pos + delimiter.length());
        }
        vec.push_back(line);
        return vec;
    }

    //Reads a trace from a file
    //      Input
    //  fileName: Trace file
    //      Output
    //  dataTable: Table with the trace
    vector<vector<double>> TRACES::readMatrix(string fileName) {
        string delimiter = "\t";
        ifstream file(fileName);
        vector<vector<string>> dataList;
        string line = "";
        // Iterate through each line and split the content using delimiter
        while (getline(file, line)){
            vector<string> vec;
            vec=splitString(line, delimiter);
            dataList.push_back(vec);
        }
        // Close the File
        file.close();
        vector<vector<double>> dataTable;
        for (unsigned int i=0;i<dataList.size();i++){
            vector<double> vec;
            for (unsigned int j=0;j<dataList[i].size();j++){
                vec.push_back(stod(dataList[i][j]));
            }
            dataTable.push_back(vec);
        }
        return dataTable;
    }

    //It starts at the beginning at the trace
    void TRACES::setInitialPosition(){
        lastPosition.x=dbpositions[0][1];
        lastPosition.y=dbpositions[0][2];
        lastPosition.z=0;
        count=0;
    }

    //Assigns a trace to the user and it imports the trace
    void TRACES::initialize(int stage){
        const char *csvFolder=par("csvFolder").stringValue();
        string csvDirectory(csvFolder);
        int index=getParentModule()->getIndex();
        dbpositions = readMatrix(csvDirectory+"/"+to_string(index)+".csv");
        LineSegmentsMobilityBase::initialize(stage);
    }

    //When it arrives to a new position it chooses the next point in the trace
    void TRACES::setTargetPosition(){
        if (count<dbpositions.size()){
            targetPosition.x=dbpositions[count][1];
            targetPosition.y=dbpositions[count][2];
            nextChange=dbpositions[count][0];
            count++;
        }else{
            nextChange=simTime()+3600;
        }
    }

    void TRACES::move(){
        LineSegmentsMobilityBase::move();
    }
} // namespace inet

