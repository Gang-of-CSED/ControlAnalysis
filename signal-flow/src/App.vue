<template>
  <div class="all">
    <v-network-graph v-model:selected-nodes="selectedNodes" v-model:selected-edges="selectedEdges"
      :selected-edges="selectedEdges" :nodes="nodes" :edges="edges" :paths="paths" :layouts="data.layouts"
      :configs="configs">

      <template #edge-overlay="{ scale, center, position, hovered, selected }">
        <!-- Place the triangle at the center of the edge -->
        <path class="marker" :class="{ hovered, selected }" d="M-5 -5 L5 0 L-5 5 Z " fill="#55aaFF"
          :transform="makeTransform(center, position, scale)" />
      </template>
      <template #edge-label="{ edgeId, edge, scale, ...slotProps }">
        <v-edge-label :text="edge.label" align="center" vertical-align="above" v-bind="slotProps"
          :font-size="30 * scale" fill="#ff5500" />

      </template>

    </v-network-graph>
    <div class="panel" v-bind:style="{ left: `${x}px`, top: `${y}px` }" @mousedown="startDrag" @mousemove="dragging"
      @mouseup="stopDrag" @mouseleave="stopDrag">
      <button @click="AddMachine" class="addm">🟢</button>
      <button @click="AddQueue" class="addq">🟨</button>

      <input type="text" v-model="edgeGain" class="input" placeholder="Edge Gain G1(x)" />
      <button @click="AddEdge" class="adde">🔗</button>
      <button @click="Run" class="run">🔍</button>
      <button @click="remove" class="delete">❌</button>
      <button @click="clear" class="clear">🗑️</button>


    </div>

    <!-- section for analysised data -->
    <div class="data">
      <h1>Analysis</h1>
      <h2>Transfer Function</h2>
      <h2>Paths</h2>
      <h2>Loops</h2>
      <h2>Determinants</h2>

    </div>
  </div>
</template>

<script>
import * as vNG from "v-network-graph"

export default {
  name: 'App',

  data() {
    return {
      x: window.innerWidth / 3,
      y: 3 * window.innerHeight / 4,
      startX: 0,
      startY: 0,
      isDragging: false,
      isPopupVisible: false,
      running: false,
      nodes,
      edges,
      selectedNodes: sn,
      selectedEdges: se,

      nextMachineIndex: 1,
      nextQueueIndex: 1,
      nextNodeIndex,
      nextEdgeIndex,
      configs,
      data,
      paths,
  
      forwardPaths: [{ path: [], gain: [] }],
   
      //  forWardGains: [],//bassam
      ref
    };
  },
  mounted() {
    console.log("mounted");
    // this.update()
    
    // this.printAllPaths(this.paths);
    

    
  },
  methods: {
    Run() {
      // // bassam bullshit just to test the function 

      //   console.log(JSON.stringify(this.nodes, null, 2));
      //   console.log(JSON.stringify(this.edges, null, 2));
      //    this.findAllForwardPathsAndGains();
      //    this.printAllForwardPathsAndGains(this.forwardPaths);

      // // end of bassam bullshit  

      
   
      const visited = {};
      // this.paths = this.findAllPaths('node1', 'node2', visited, [], this.edges);
      console.log(this.paths);
      this.configs.path.visible = !this.configs.path.visible;
      // this.running = true;

      // create fetch post request with payloads in following format
      // {
      //   "nodes": {
      // "node1":{ "name": "Start Node", "shape": "circle", "color": "green","main": true,"type":"queue","x":0,"y":0},
      // "node2":{ "name": "End Node", "shape": "circle", "color": "green","main": true,"type":"queue","x":0,"y":0},
      // "node3":{ "name": "Q1", "shape": "circle", "color": "green","main": true,"type":"queue","x":0,"y":0},
      // "node4":{ "name": "M1", "shape": "square", "color": "red","main": true,"type":"machine","x":0,"y":0},
      // }
      //   "edges": {
      // "edge1":{ "source": "node1", "target": "node3", "color": "black","label":"G1(x)"},
      // "edge2":{ "source": "node3", "target": "node4", "color": "black","label":"G2(x)"},
      // "edge3":{ "source": "node4", "target": "node2", "color": "black","label":"G3(x)"},
      // }
      // }
      let nodes = {};
      console.log("nodes:", this.nodes);
      for (let nodeI in this.nodes) {
        let node = this.nodes[nodeI];

        console.log(nodeI, node);
        nodes[nodeI] = { "name": node.name.split(":")[0], "shape": node.shape, "color": node.color, "main": node.main, "type": node.type, "x": 0, "y": 0 };
        console.log("node", nodeI, node);
      }

      let edges = {};
      for (let edgeI in this.edges) {
        let edge = this.edges[edgeI];
        console.log(edgeI, edge);
        edges[edgeI] = { "source": edge.source, "target": edge.target, "color": edge.color, "label": edge.label };
      }

      let data = {
        "nodes": nodes,
        "edges": edges
      }

     
    //   // console.log(JSON.stringify(nodes, null, 2));

    
    //   fetch('http://localhost:8080/data', {
    //     method: 'POST',
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(data)
    //   })
    //     .then(response => response.text())
    //     .then(data => {
    //       console.log('Success:', data);
    //     })
     
    },

    findAllPaths(current, target, visited, path, edges) {
      visited[current] = true;
      let allPaths = [];

      for (const edgeId in edges) {
        const edge = edges[edgeId];
        if (edge.source === current && !visited[edge.target]) {
          path.push(edgeId);
          if (edge.target === target) {
            allPaths.push({ edges: [...path] });
          } else {
            allPaths = allPaths.concat(this.findAllPaths(edge.target, target, visited, path, edges));
          }
          path.pop();
        }
      }

      visited[current] = false;
      return allPaths;
    },


    //bassam section Dont you dare touch it 55 !!

    //just findAllForwardPathsAndGains() that you can use to get the forward paths and gains
    //the funtcion will return list of forward paths and gains (every element in the list is a forward path with it's gain)
    //and it's output is in this format [{ path: [nodeId1,nodeId2], gain: [X1,X2] }] 
   
    findOutputNodeId() {
      for (const nodeId in this.nodes) {
        if (this.nodes[nodeId].type === 'output') {
          return nodeId;
        }
      }
    },

    findInputNodeId() {
      let inDegree = new Map();
    
      for (const nodeId in this.nodes) {
        inDegree.set(nodeId,true);
      }
      // console.log(inDegree);

      for (const edgeId in this.edges) {
        inDegree.set(this.edges[edgeId].target,false);
      }
      // console.log(inDegree);

      for (const [key,value] of inDegree) {
        // console.log(key,value);
        if (value) {

          return key;
        }
      }
  
      
    },

    findAllForwardPathsAndGains(){
      let startNode = this.findInputNodeId();
      console.log("startNode",startNode);
      let endNode = this.findOutputNodeId();
       
      let allPaths = this.findAllPaths(startNode, endNode, {}, [], this.edges);
      
      // console.log(JSON.stringify(allPaths, null, 2));

      // let forwardPaths = [];
      
      for (const path of allPaths) {
        let forwardPath = [];
        let forwardGain = [];
        forwardPath.push(startNode);
        
        for (const edgeId of path.edges) {
          // console.log(edgeId);
          // console.log(this.edges[edgeId].label);

          // forwardPath.push(edgeId);
          forwardPath.push(this.edges[edgeId].target);
          forwardGain.push(this.edges[edgeId].label);
        }
        this.forwardPaths.push({ path: forwardPath, gain: forwardGain });
      }
      return this.forwardPaths
    }, 

    printAllForwardPathsAndGains(forwardPaths){
      for (const forwardPath of forwardPaths) {
        console.log(JSON.stringify(forwardPath, null, 2));      }
    },
 
    //end of bassam section mess anything if you want ;)

    remove() {
      if (this.running) {
        alert('Please pause the simulation first.');
        return;
      }

      if (this.selectedNodes.length === 0 && this.selectedEdges.length === 0) {
        alert('Please select a node or an edge to delete.');
        return;
      }
      for (const nodeId of this.selectedNodes) {
        if (!this.nodes[nodeId].main) {

          if (this.nodes[nodeId].type === 'machine') {
            this.nextMachineIndex--;
          } else if (this.nodes[nodeId].type === 'queue') {
            this.nextQueueIndex--;
          }

          delete this.nodes[nodeId];
        }
      }
      for (const edgeId of this.selectedEdges) {
        delete this.edges[edgeId];
      }
    },
    AddMachine() {


      const nodeId = `node${nextNodeIndex.value}`;
      const name = `N${this.nextMachineIndex}`;
      nodes[nodeId] = { name, type: 'non-output', shape: 'circle', color: '#11ff55' };
      this.nextMachineIndex++;
      this.nextNodeIndex++;
    },
    AddQueue() {

      const nodeId = `node${nextNodeIndex.value}`;
      const name = `O${this.nextQueueIndex}`;
      nodes[nodeId] = { name, type: 'output', shape: 'rect', color: '#FFDF64' };

      this.nextQueueIndex++;
      this.nextNodeIndex++;

    },
    AddEdge() {
      if (this.selectedNodes.length !== 2) {
        alert('Please select two nodes to connect.');
        return;
      }

      if (this.edgeGain === undefined || this.edgeGain === "") {
        alert('Please enter the edge gain.');
        return;
      }

      const [source, target] = this.selectedNodes;
      const edgeId = `edge${this.nextEdgeIndex}`;
      this.edges[edgeId] = { source, target, color: '#55aaFF', label: this.edgeGain };
      this.nextEdgeIndex++;
    },
    
    clear() {
      window.location.reload();
    },
    startDrag(event) {
      this.isDragging = true;
      this.startX = event.clientX - this.x;
      this.startY = event.clientY - this.y;
    },
    dragging(event) {
      if (this.isDragging && !this.isPopupVisible) {
        this.x = event.clientX - this.startX;
        this.y = event.clientY - this.startY;
      }
    },
    stopDrag() {
      this.isDragging = false;
    },
    makeTransform(center, edgePos, scale) {
      const radian = Math.atan2(
        edgePos.target.y - edgePos.source.y,
        edgePos.target.x - edgePos.source.x
      )
      const degree = (radian * 180.0) / Math.PI

      return [
        `translate(${center.x} ${center.y})`,
        `scale(${2 * scale}, ${2 * scale})`,
        `rotate(${degree})`,
      ].join(" ")
    },

  }
}

import { reactive, ref } from "vue";
import data from "./data.js";

const nodes = reactive({ ...data.nodes });
const edges = reactive({ ...data.edges });
const configs = reactive({ ...data.configs });
const paths = reactive({ ...data.paths });
const nextNodeIndex = ref(Object.keys(nodes).length + 1);
const nextEdgeIndex = ref(Object.keys(edges).length + 1);

// const nextMIndex = ref(Object.values(nodes).filter(node => node.type === 'machine').length + 1);
// const nextQIndex = ref(Object.values(nodes).filter(node => node.type === 'queue').length + 1);;

const sn = ref([]);
const se = ref([]);

</script>

<style scoped src="./App.css" lang="css"></style>