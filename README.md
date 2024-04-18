# Signal Flow Graphs Solver

## **Overview**


This project involves developing a software application capable of visualizing and analyzing signal flow graphs. The application will allow users to draw nodes and branch gains of a signal flow graph to provide a graphical representation of the graph, list all forward paths and loops, calculate system determinant Δ and paths determinant Δ1,Δ2..Δn , and compute the overall system transfer function. by Manon's rule.

![Untitled](assets/Untitled.png)

## **Features**



1. **Dynamic UI Setup:**
    - Users can graphically add nodes via the UI, connecting them arbitrarily for a flexible simulation setup.
2. **System Analysis:**
    - The software can identify and list all forward paths, loops, and calculate determinants.
3. **Comprehensive Output:**
    - It provides a detailed system transfer function calculation using Mason's rule.
4. **Flexible Input :**
    - The user can enter the gain of edges as numbers , symbols , letters even negative letters like -H3.

### **Algorithms Implemented**



1. **Graph Traversal for Finding All Paths**:
    - **Objective**: Identify all forward paths from an input node to an output node in the signal flow graph.
    - **Method**: Depth-first search (DFS) is used to explore all possible paths from the start node to the end node. As each node is visited, it is marked to prevent revisiting, and the path is recorded. Once the target node is reached, the current path is saved as a forward path.
2. **Cycle Detection for Loops**:
    - **Objective**: Detect all feedback loops within the graph, which are critical for calculating the system’s transfer function.
    - **Method**: A modified depth-first search is used where each node starts a new DFS to find cycles. A cycle is confirmed if a node is revisited before the DFS completes. Each loop is then stored, ensuring no node in the loop has been touched by other loops' paths.
3. **Detection of Non-Touching Loops**:
    - **Objective**: Identify sets of loops that do not share common nodes, which are used to calculate the determinant of the graph.
    - **Method**: Recursive combinations are formed from the list of detected loops, and for each combination, it is checked whether they are non-touching by ensuring no common nodes are present.
4. **Calculation of Transfer Function Using Mason’s Gain Formula**:
    - **Objective**: Compute the overall system transfer function.
    - **Method**:
        - The determinant of the system is first calculated using the identified loops and their combinations.
        - For each forward path, the path gain is multiplied by the determinant of the subgraph formed by removing the nodes in the path (using non-touching loops).
        - The transfer function is the sum of these terms divided by the determinant of the entire graph.
5. **Simplification and Output Adjustment**:
    - **Objective**: Output the paths, loops, and transfer function in a readable format.
    - **Method**: Each path and loop is converted into a human-readable string showing nodes and gains. Algebra.js is used to simplify expressions and convert them to strings for display

## User Guide



![Untitled](assets/Untitled%201.png)

1. **Adding Nodes:**
    - To add a non-output node , click the 🟢 button in the UI.
    - To add a output node , click the 🟨 button in the UI.
2. **Adding Edges (Connections):**
    - To establish connections between nodes
        - Click on the source node (from which the edge originates).
        - Press **Shift + Alt** to enable multi-selection mode.
        - Click on the target node (to which the edge connects).
        - Click the 🔗 button to create the connection.
3. **Deleting Nodes or Edges:**
    - To delete a machine, queue, or edge:
        - Click on the node or edge that you want to delete.
        - Click the ❌ button to remove the selected item.
4. **Solve the System:**
    - Ensure all connections are established correctly.
    - Click the ▶️ button to solve and show outputs
    
    ## Sample Runs
    
    ![Untitled](assets/Untitled%202.png)
    
    ![Untitled](assets/Untitled.png)
    
    ![Untitled](assets/Untitled%203.png)
    
    ![Untitled](assets/Untitled%204.png)
    
    ![Untitled](assets/Untitled%205.png)
