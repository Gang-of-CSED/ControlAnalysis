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
          :font-size="20 * scale" fill="#ff5500" />

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
      <!-- display solution -->
      <h1>Solution</h1>
      <h2>Transfer Function: <br/>{{solution.transFun}}</h2>
      <hr/>
      <h2>System Determinant:<br/> {{solution.systemDet}}</h2>
      <hr/>
      <h2>Forward Paths</h2>
      <hr/>
      <div v-for="path in solution.forwardPaths">
        <h3>{{path.path}}: {{path.gain}}</h3>
        <h3>Path Determinant : {{solution.pathsDet[solution.forwardPaths.indexOf(path)]}}</h3>
        <hr class="inner-hr"/>
      </div>
      <h2>Loops</h2>
      <hr/>
      <div v-for="loop in solution.loops">
        <h3>{{loop.path}}: {{loop.gain}}</h3>
        <hr class="inner-hr"/>
      </div>
      <h2>Non-Touching Loops Combinations</h2>
      <hr/>
      <div v-for="comb in solution.allCombs">
        <h3>{{comb}}</h3>
        <hr class="inner-hr"/>
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
      // this.resetValues();
      // this.solveFlowDiagram();
      // this.adjustOutputs();

      // console.log("loops",JSON.stringify(this.loopsOutPut, null, 2));
      // let combinations = [];
      // this.getNonTouchingloopsCombinations(this.loops,0,combinations,[]);
      // console.log("loop combinations",JSON.stringify(this.allCombsOutput, null, 2));

     
      
      // for(let i=0;i<this.pathsDet.length;i++){
      //   console.log("path: ",this.forwardPathsOutput[i].path,"\ngain:",this.forwardPathsOutput[i].gain,"\ndeterminant:",this.pathsDetOutput[i]);
      // }
      // console.log("system determinant: ",this.systemDet);
      // console.log("transfer function: ",this.transFun);
   
    },
    // resetValues(){
    //   this.forwardPaths = [];
    //   this.loops = [];
    //   this.transFun = null;
    //   this.systemDet = null;
    //   this.pathsDet = [];
    //   this.forwardPathsOutput = [];
      
    // },
    
    // findAllPaths(current, target, visited, path, edges) {
    //   visited[current] = true;
    //   let allPaths = [];

    //   for (const edgeId in edges) {
    //     const edge = edges[edgeId];
    //     if (edge.source === current && !visited[edge.target]) {
    //       path.push(edgeId);
    //       if (edge.target === target) {
    //         allPaths.push({ edges: [...path] });
    //       } else {
    //         allPaths = allPaths.concat(this.findAllPaths(edge.target, target, visited, path, edges));
    //       }
    //       path.pop();
    //     }
    //   }

    //   visited[current] = false;
    //   return allPaths;
    // },
    
    // findAllCycles(visitedMap, stPath, stGain,  nodeID){
    //   stPath = [...stPath, nodeID];
    //   stGain = [...stGain];
    //   if(visitedMap[nodeID]){
    //     let cycle = {path: [], gain: []};
    //     cycle.path.push(stPath.pop());
    //     cycle.gain.push(stGain.pop());
    //     while(stPath[stPath.length - 1] != nodeID){
    //       cycle.path.push(stPath.pop());
    //       cycle.gain.push(stGain.pop());
    //     }
    //     this.loops.push(cycle);
    //     return;
    //   }
    //   visitedMap[nodeID] = true;
    //   // stPath.push(nodeID);
    //   for(let edge of Object.values(this.edges)){
    //     if(edge.source == nodeID && visitedMap[nodeID]){
    //       stGain.push(edge.label);
    //       this.findAllCycles(visitedMap, stPath, stGain, edge.target);
    //       stGain.pop();
    //     }
    //   }
    //   visitedMap[nodeID] = false;
    //   stPath.pop();
    // },

    // getAllDistinctCycles() {
    //   let visitedMap = {};
    //   for (let node of Object.keys(this.nodes)) {
    //     visitedMap[node] = false;
    //   }
    //   let stPath = []; 
    //   let stGain = [];
    //   this.findAllCycles(visitedMap, stPath, stGain, 'node1');

    //   // console.log("loops-------------------\n");
    //     this.loops = Array.from(new Set(this.loops.map(JSON.stringify))).map(JSON.parse);
    //     // console.log(JSON.stringify(this.loops));
    // },

    
    // //bassam section Dont you dare touch it 55 !!
    
   
    // getForwardPaths(){
    //   let startNode = this.findInputNodeId();
    //   let endNode = this.findOutputNodeId();
       
    //   let allPaths = this.findAllPaths(startNode, endNode, {}, [], this.edges);
      
    //   for (const path of allPaths) {
    //     let forwardPath = [];
    //     let forwardGain = [];
    //     forwardPath.push(startNode);
        
    //     for (const edgeId of path.edges) {
    //       forwardPath.push(this.edges[edgeId].target);
    //       forwardGain.push(this.edges[edgeId].label);
    //     }
    //     this.forwardPaths.push({ path: forwardPath, gain: forwardGain });
    //   }
    //   return this.forwardPaths
    // }, 

    // getCyclesNotTouchingPath(path){
    //   let cycles = [];

    //   for(let cycle of this.loops){
    //     let flag = true;

    //     for(let node of path){
    //       if(cycle.path.includes(node)){
    //         flag = false;
    //         break;
    //       }
    //     }
    //     if(flag){
    //       cycles.push(cycle);
    //     }
    //   }
    //   return cycles;
    // },
   
    // getNonTouchingloopsCombinations(cycles,i,res,comb){
    //  if(i >= cycles.length){
    //   if(comb.length > 0) 
    //   res.push(comb);
    //    return;
    //  }
    //  let flag = true;
    //  for(let j=0;j<comb.length;j++){
    //     for(let node of cycles[i].path){
    //       if(comb[j].path.includes(node)){
    //         flag = false;
    //         break;
    //       }
    //     }
    //  }
    //   if(flag){
    //     this.getNonTouchingloopsCombinations(cycles,i+1,res,[...comb,cycles[i]]);
    //   }
    //    this.getNonTouchingloopsCombinations(cycles,i+1,res,[...comb]);
     
    // },
    // getCombinationsSymbols(){
    //   let combs= [];
    //   this.getNonTouchingloopsCombinations(this.loops,0,combs,[]);
    //   for(let comb of combs){
    //     let combSybmol=""
    //     for(let cycle of comb){
    //       let indexOfCycle = this.loops.indexOf(cycle);
    //       combSybmol +="L"+(indexOfCycle+1).toString();
    //     }
    //     if(!this.allCombsOutput[comb.length-1])
    //       this.allCombsOutput[comb.length-1] = [];
    //     this.allCombsOutput[comb.length-1].push(combSybmol);
    //   }
    // },
    // getBranchName(nodes){
    //  let branchName = "";
    //   for(let node of nodes){
    //     branchName += this.nodes[node].name ;
    //     if(node != nodes[nodes.length - 1])
    //       branchName += " -> ";
    //   }
    //   return branchName;
    // },

    // getBranchGain(nodesGains){
    //   const algebra = require('algebra.js');
    //   let branchGain = new algebra.parse("1");
    //   for(let gain of nodesGains){
    //     let eq;
    //     if(isNaN(gain)&& gain[0] == "-"){
    //       gain = gain.substring(1);
    //       eq = new algebra.parse(gain);
    //     }
    //     else
    //       eq = new algebra.parse(gain);

    //     branchGain = eq.multiply(branchGain);
    //   }
    //   return branchGain;
    // },

    // getCombinationsGains(path){
    //   let cycles = this.getCyclesNotTouchingPath(path);
    //   let combinations = [];

    //   this.getNonTouchingloopsCombinations(cycles,0,combinations,[]);
      
    //   let gains= [];
    //   gains[0] = [];
    //   const algebra = require('algebra.js');

    //   for(let comb of combinations){
    //     let combGain = 1;

    //     for(let cycle of comb){
         
    //       for(let gain of cycle.gain){
    //        let eq ;
    //        if(isNaN(gain)){
    //         if(gain[0] == "-")
    //         eq = new algebra.Expression(-1).multiply(gain.substring(1));
    //         else  
    //         eq = new algebra.Expression(gain);
    //        }
    //        else
    //         eq = new algebra.parse(gain.toString());
           
    //         combGain = eq.multiply(combGain);
    //       }
    //     }

    //     if (!gains[comb.length]) {
    //         gains[comb.length] = [];
    //     }
    //     gains[comb.length].push(combGain);
    //   }
    //   return gains;
    // },

    // determinantOfPath(path){

    //   let gains = this.getCombinationsGains(path);

    //   let result = new algebra.parse("1");
    //   for(let i=1;i<gains.length;i++){
    //     let sum =new algebra.parse("0");

    //     for(let j=0;j<gains[i].length;j++){
    //       sum = sum.add(gains[i][j]);
    //     }

    //     if(i%2 == 0)
    //       result = result.add(sum);
    //     else
    //      result = result.subtract(sum);
    //   }
      
    //   result = result.simplify();

    //   return result;

    // },
 
    // findOutputNodeId() {
    //   for (const nodeId in this.nodes) {
    //     if (this.nodes[nodeId].type === 'output') {
    //       return nodeId;
    //     }
    //   }
    // },

    // findInputNodeId() {
    //   let inDegree = new Map();
    
    //   for (const nodeId in this.nodes) {
    //     inDegree.set(nodeId,true);
    //   }
    //   for (const edgeId in this.edges) {
    //     inDegree.set(this.edges[edgeId].target,false);
    //   }
    //   for (const [key,value] of inDegree) {
    //     if (value) 
    //       return key;
        
    //   }
  
      
    // },

    // solveFlowDiagram(){
    //   this.getForwardPaths();
    //   this.getAllDistinctCycles();
      
    //    this.systemDet = this.determinantOfPath([]);
    //     let branchGains = [];
    //    for(let path of this.forwardPaths){

    //       this.pathsDet.push(this.determinantOfPath(path.path));
    //       let branchGain = this.getBranchGain(path.gain);
    //       branchGains.push(branchGain);
    //    }
       
    //     this.transFun=algebra.parse("0");

    //      for(let i=0;i<this.pathsDet.length;i++){
    //        let eq = algebra.parse(this.pathsDet[i].toString());
    //        let pathGain = eq.multiply(branchGains[i]);
    //        this.transFun = this.transFun.add(pathGain);
    //      }
       
    //      this.transFun.simplify();
        
    // },

    // adjustOutputs(){
      
    //   for(let path of this.forwardPaths){
    //     let branchName = this.getBranchName(path.path);
    //     let branchGain = this.getBranchGain(path.gain);
    //     this.forwardPathsOutput.push({path: branchName, gain: branchGain.toString()});
    //   }
    //   for(let pathDet of this.pathsDet){
    //     this.pathsDetOutput.push(pathDet.toString());
    //   }
    //   for(let loop of this.loops){
    //     let loopPath = this.getBranchName(loop.path);
    //     let loopGain = this.getBranchGain(loop.gain).toString();
    //     this.loopsOutPut.push({path: loopPath, gain: loopGain});
    //   }
    //   this.getCombinationsSymbols();
      
    //   this.transFun=this.transFun.toString()+" / ( "+this.systemDet.toString()+" )";
    //   this.systemDet = this.systemDet.toString();
    // },

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