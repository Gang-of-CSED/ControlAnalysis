<template>
   
  <div class="all">
    <template>
      <solveFlowDiagram ref="childRef" :nodes="nodes" :edges="edges" @data="solution = $event" />
    </template>

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
      <button @click="Run" class="run">▶</button>
      <button @click="remove" class="delete">❌</button>
      <button @click="clear" class="clear">🗑️</button>


    </div>

    <!-- section for analysised data -->
    <div class="data">
      <!-- display solution -->
      <h1>Solution</h1>
      <h3>Transfer Function: {{solution.transFun}}</h3>
      <!-- <hr/> -->
      <!-- <h3>System Determinant: {{solution.systemDet}}</h3> -->
      <h3>△ = {{solution.systemDet}}</h3>
      <hr/>
      <h3>Forward Paths:</h3>
      <!-- <hr/> -->
      
      <div v-for="(path, index) in solution.forwardPaths">
        <h3>P{{index+1}}: {{path.path}}: {{path.gain}}</h3>
        <h3>△{{ index+1 }} = {{solution.pathsDet[index]}}</h3>
        <hr class="inner-hr" v-if="solution.forwardPaths[index + 1]"/>
      </div>
      <hr/>

      <h3>Loops:</h3>
      <!-- <hr/> -->
      <div  v-for="(loop, index) in solution.loops">
        <h3>L{{ index+1 }}:{{loop.path}}: {{loop.gain}}</h3>
        <hr class="inner-hr"  v-if="solution.loops[index + 1]"/>
      </div>
      <hr/>
      <h3>Non-Touching Loops Combinations</h3>
      <hr/>
      <div  v-for="(comb, index) in solution.allCombs">
        <h3>N={{ index +1}}: {{comb}}</h3>
        <hr class="inner-hr"  v-if="solution.allCombs[index + 1]"/>
      </div>

    </div>
  
  </div>

</template>

<script>
import * as vNG from "v-network-graph"
import algebra from 'algebra.js';
import solveFlowDiagram from "./solveFlowDiagram.vue";

export default {
  name: 'App',
  components: {
    solveFlowDiagram
  },
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
      solution:{},
      
      // forwardPaths: [],
      // // to show the output only
      // forwardPathsOutput: [],
      // loopsOutPut: [],
      // allCombsOutput: [],
      // pathsDetOutput:[],

      // // 
      // pathsDet:[],
      // systemDet:null,
      // transFun:null,
      // loops:[],

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
    this.$refs.childRef.solve();
    },

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
      if (this.selectedNodes.length !== 2 && this.selectedNodes.length !== 1) {
        alert('Please select one\\two nodes to connect.');
       
        return;
      }

      if (this.edgeGain === undefined || this.edgeGain === "") {
        alert('Please enter the edge gain.');
        return;
      }
      
       if(this.selectedNodes.length === 1)
          this.selectedNodes.push(this.selectedNodes[0]);

      const [source, target] = this.selectedNodes;
  
      const edgeId = `edge${this.nextEdgeIndex}`;
      this.edges[edgeId] = { source, target, color: '#55aaFF', label: this.edgeGain ,type: 'curve'};
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
 // findAllDistinctCycles() {
    //   let cycles = [];
    //   let visited = {};
    //   let path = [];
    //   let nodes = Object.keys(this.nodes);
    //   for (let node of nodes) {
    //     this.findAllCycles(node, node, visited, path, cycles);
    //   }
    //   return cycles;
    // },
    // findAllCycles(current, start, visited, path, cycles) {
    //   visited[current] = true;
    //   path.push(current);

    //   for (let edgeId in this.edges) {
    //     let edge = this.edges[edgeId];
    //     if (edge.source === current) {
    //       if (!visited[edge.target]) {
    //         this.findAllCycles(edge.target, start, visited, path, cycles);
    //       } else if (edge.target === start) {
    //         cycles.push([...path]);
    //       }
    //     }
    //   }

    //   path.pop();
    //   visited[current] = false;
    // },

    // findAllPaths(current, target, visited, path, edges) {
    //   visited[current] = true;
    //   let allPaths = [];
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