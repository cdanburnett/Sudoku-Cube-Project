/*
315-001:
Title: Middle Earth Graph Search
Name: Caleb Daniel Burnett
Purpose: Implement BFS and Dijkstra's on Middle Earth map

Use of CHATGPT o4-mini-high
consulted for checking if the way syntax had been written would work.
Also used to generate the code to read in from the .txt files into an adjacency list. Code used after tweaks is indicated below. 
AI was prompted by asking it to help me write functions that would help me parse attatched txt files and insert vertexes and distance 
costs. 
*/


#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <queue>
// include unordered_map for adjacency list
#include <unordered_map>
// include limits for numeric_limits
#include <limits>
using namespace std;

// global cost counters
int bfs_cost = 0;
int dijkstra_cost = 0;

// struct for min heap nodes
struct MinHeapNode {
    // name of the vertex
    string vertex;
    // distance weight
    int distance;
};

// minheap using a vector
class MinHeap {
public:
    // iniitalze
    vector<MinHeapNode> heap_node_vector;

    // insert a node into the heap passing by constant reference
    void insert(const MinHeapNode &node) {
        // append
        heap_node_vector.push_back(node);
        
        // heapify up the vector
        heapifyUp(heap_node_vector.size() - 1);
    }

    // extract the node with minimum distance
    MinHeapNode get_min_distance() {
        // save root
        MinHeapNode root = heap_node_vector[0];
        // move last to root
        heap_node_vector[0] = heap_node_vector.back();
        // remove last element
        heap_node_vector.pop_back();
        // restore heap by sifting down
        heapifyDown(0);
        // return the original root
        return root;
    }

    // decrease the key (distance) of a given vertex
    void decreaseKey(const string &vertex, int new_distance) {
        // find the node in the array
        for (int i = 0; i < (int)heap_node_vector.size(); ++i) {
            // if match and new distance smaller than the current known distance
            if (heap_node_vector[i].vertex == vertex && new_distance < heap_node_vector[i].distance) {
                // update distance
                heap_node_vector[i].distance = new_distance;
                // call heapify up from current node index i
                heapifyUp(i);
                // I think we're done here.
                break;
            }
        }
    }

    // check if a vertex exists in heap
    bool contains(const string &vertex) const {
        // linear search (inefficient, but works)
        for (auto &node : heap_node_vector) {
            if (node.vertex == vertex) return true;
        }
        return false;
    }

private:
    // heapify up from index
    void heapifyUp(int i) {
        // while not at root
        while (i > 0) 
        {
            // formula for parent index
            int parent = (i - 1) / 2;
            // if current less than parent, swap them to heapify up.
            if (heap_node_vector[i].distance < heap_node_vector[parent].distance) 
            {
                swap(heap_node_vector[i], heap_node_vector[parent]);
                i = parent;
            } else {
                break; // we can stop
            }
        }
    }

    // heapify down from the parameter i, probably the root.
    void heapifyDown(int i) 
    {
        // compute child indexes
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        int smallest = i;
        // if left child smaller
        if (left < (int)heap_node_vector.size() && heap_node_vector[left].distance < heap_node_vector[smallest].distance)
            {
            smallest = left;
            }
        // if right child smaller
        if (right < (int)heap_node_vector.size() && heap_node_vector[right].distance < heap_node_vector[smallest].distance)
            {
            smallest = right;
            }
        // if swap needed, swap them.
        if (smallest != i) 
        {
            swap(heap_node_vector[i], heap_node_vector[smallest]);
            heapifyDown(smallest);
        }
    }
};


// adjacency list implementation each vertex maps to vector of (neighbor, distance int)
// declare unordered map of string and vector of pairs
unordered_map<string, vector<pair<string,int>>> adjacency_list;

// code from chat GPT
// loadVertices: read vertex names from file
void loadVertices(const string &filename) {
    // open file stream
    ifstream file(filename);
    string line;
    // read each line as a vertex
    while (getline(file, line)) {
        // initialize empty adjacency list entry
        adjacency_list[line] = {};
    }
    // close file
    file.close();
}

// loadEdges: read edges (CSV) and add undirected entries
void loadEdges(const string &filename) {
    // open file stream
    ifstream file(filename);
    string line;
    // process each line
    while (getline(file, line)) {
        // use stringstream to parse CSV
        stringstream ss(line);
        string from, to, weightStr;
        getline(ss, from, ',');
        getline(ss, to, ',');
        getline(ss, weightStr);
        // convert weight
        int weight = stoi(weightStr);
        // add both directions
        adjacency_list[from].push_back({to, weight});
        adjacency_list[to].push_back({from, weight});
    }
    // close file
    file.close();
}
// end of GPT code

// implementation of print path from textbook PRINT-PATH(G, s, v)
void printPath(unordered_map<string,string> &G, const string &s, const string &v) {
    // base case: reached source
    if (v == s) 
    {
        cout << s;
    }
    // Error if no path exists
    else if (G[v].empty()) {
        cout << "no path from " << s << " to " << v << " exists";
    }
    // recursive call
    else {
        printPath(G, s, G[v]);
        cout << " -> " << v;
    }
}

// BFS implementation using queue
void BFS(const string &start, const string &destination) 
{
    // track visited nodes in map
    unordered_map<string,bool> visited;

    // store parent parents in map
    unordered_map<string,string> parent;

    // BFS queue
    queue<string> BFS_queue;

    // initialize visited and parent maps and queueu with passed parameters.
    visited[start] = true;
    parent[start] = "";
    BFS_queue.push(start);

    // run while the queue isn't empty, or until current is the destination
    while (!BFS_queue.empty()) 
    {
        
        // get the current
        string current = BFS_queue.front();
        // pop it off the queue
        BFS_queue.pop();

        // if destination, call print path and return
        if (current == destination) 
        {
            // print path
            cout << "BFS path: ";
            printPath(parent, start, destination);
            cout << endl;
            return;
        }
        // check neighbors if current isn't destination
        // auto iterator to iterate through the adjacency list until we reach the current
        for (auto &edge : adjacency_list[current]) 
        {
            // get the first value
            const string &neighbor = edge.first;

            // increment BFS counter
            bfs_cost++;

            // if the neighbor is unvisited, mark them visited and update the parent, and push them on the queue
            if (!visited[neighbor]) 
            {
                visited[neighbor] = true;
                parent[neighbor] = current;
                BFS_queue.push(neighbor);
            }
        }
    }
}

// dijkstra using min-heap
void dijkstra(const string &start, const string &destination) 
{
    // distance map
    unordered_map<string,int> distance;

    // parent map for path
    unordered_map<string,string> parent;
    // min-heap priority queue
    MinHeap heap_priority;

    
    // iterate through the adjacency list
    for (auto &p : adjacency_list) 
    {
        // initialize distances and heap
        distance[p.first] = numeric_limits<int>::max();
        parent[p.first] = "";
        heap_priority.insert({p.first, distance[p.first]});
    }
    // set start distance
    distance[start] = 0;

    // call decrease key
    heap_priority.decreaseKey(start, 0);

    // main loop: while heap not empty
    while (!heap_priority.heap_node_vector.empty()) {
        
        // get the min min
        MinHeapNode min = heap_priority.get_min_distance();
        string sting = min.vertex;

        // if destination, stop early
        if (sting == destination) 
            {
            break;
            }
        // relax edges from sting
        // Code from ChatGPT
        for (auto &edge : adjacency_list[sting]) {
            const string &v = edge.first;
            int w = edge.second;

            // increment cost counter
            dijkstra_cost++; // added by me.

            
            if (distance[sting] + w < distance[v]) {
                distance[v] = distance[sting] + w;
                parent[v] = sting;
                heap_priority.decreaseKey(v, distance[v]);
            }
        }
        // end
    }
    // print result
    cout << "Dijkstra path edge cost = " << distance[destination] << "): "; // ChatGPT
    cout << "Dijkstra path: ";
    printPath(parent, start, destination);
    cout << endl;
}

// main: program entry point
int main(int argc, char* argv[]) {
    
    
    // load graph data
    loadVertices(argv[1]);
    loadEdges(argv[2]);

    // define start and destination
    string start = "Hobbiton";
    string destination = "MountDoom";
    
    // execute BFS
    BFS(start, destination);
    // execute Dijkstra
    dijkstra(start, destination);


    // print the final costs
    cout << "BFS cost count: " << bfs_cost << endl;
    cout << "Dijkstra cost count: " << dijkstra_cost << endl;

    // The main function returns zero, much like Frodo returns the O shaped ring to the fire. :)
    return 0;
}

