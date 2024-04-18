<template>
    <div>
        <button @click="solve">Run</button>
    </div>
</template>
<script>
import algebra from 'algebra.js';

 export default {
    props: {
        nodes: Array,
        edges: Array
    },
    data() {
        return {
            forwardPaths: [],
            forwardPathsOutput: [],
            loopsOutPut: [],
            allCombsOutput: [],
            pathsDetOutput:[],
            pathsDet:[],
            systemDet:null,
            transFun:null,
            loops:[],
        }
    },
    methods: {
    solve() {
      this.resetValues();
      this.solveFlowDiagram();
      console.log("loops",JSON.stringify(this.loops, null, 2));
      this.adjustOutputs();

      console.log("loops",JSON.stringify(this.loopsOutPut, null, 2));
      let combinations = [];
      this.getNonTouchingloopsCombinations(this.loops,0,combinations,[]);
      console.log("loop combinations",JSON.stringify(this.allCombsOutput, null, 2));

     
      
      for(let i=0;i<this.pathsDet.length;i++){
        console.log("path: ",this.forwardPathsOutput[i].path,"\ngain:",this.forwardPathsOutput[i].gain,"\ndeterminant:",this.pathsDetOutput[i]);
      }
      console.log("system determinant: ",this.systemDet);
      console.log("transfer function: ",this.transFun);

      // put all data in an object to return it
      let data = {
        forwardPaths: this.forwardPathsOutput,
        loops: this.loopsOutPut,
        allCombs: this.allCombsOutput,
        pathsDet: this.pathsDetOutput,
        systemDet: this.systemDet,
        transFun: this.transFun,
      };
      // emit the data to the parent component
      this.$emit('data', data);
   
    },
    resetValues(){
        this.forwardPaths = [];
        this.forwardPathsOutput = [];
        this.loopsOutPut = [];
        this.allCombsOutput = [];
        this.pathsDetOutput = [];
        this.pathsDet = [];
        this.systemDet = null;
        this.transFun = null;
        this.loops = [];
        
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
    
    findAllCycles(visitedMap, stPath, stGain,edgesIds,nodeID){
      stPath = [...stPath, nodeID];
      stGain = [...stGain];
      edgesIds = [...edgesIds];

      if(visitedMap[nodeID]){
        let cycle = {path: [], gain: [],edgesIds:[]};
        cycle.path.push(stPath.pop());
        cycle.gain.push(stGain.pop());
        cycle.edgesIds.push(edgesIds.pop());

        while(stPath[stPath.length - 1] != nodeID){
          cycle.path.push(stPath.pop());
          cycle.gain.push(stGain.pop());
          cycle.edgesIds.push(edgesIds.pop());
        }

        let diffEdges = true;
        cycle.edgesIds.sort();

        for(let loop of this.loops){
          // console.log("loop",JSON.stringify(loop.edgesIds, null, 2));
          // console.log("cycle",JSON.stringify(cycle.edgesIds, null, 2));
          if(loop.edgesIds.length == cycle.edgesIds.length){
            let i = 0;
            for(i=0;i<loop.edgesIds.length;i++){
              if(loop.edgesIds[i] != cycle.edgesIds[i]){
                break;
              }
            }
            if(i == loop.edgesIds.length){
              diffEdges = false;
              break;
            }
          }
         
        }
        
        if(diffEdges)
         this.loops.push(cycle);
        return;
      }
      visitedMap[nodeID] = true;
      // stPath.push(nodeID);
      for(let edgeId in this.edges){
        let edge = this.edges[edgeId];

        if(edge.source == nodeID && visitedMap[nodeID]){
          // console.log("edge",JSON.stringify(edge, null, 2));
          stGain.push(edge.label);
          edgesIds.push(edgeId);

          this.findAllCycles(visitedMap, stPath, stGain,edgesIds ,edge.target);
          stGain.pop();
          edgesIds.pop();
        }
      }
      visitedMap[nodeID] = false;
      stPath.pop();
    },

    getAllDistinctCycles() {
      let visitedMap = {};
      for (let node of Object.keys(this.nodes)) {
        visitedMap[node] = false;
      }
      let stPath = []; 
      let stGain = [];
      let edgesIds=[];
      this.findAllCycles(visitedMap, stPath, stGain, edgesIds,'node1');

      // console.log("loops-------------------\n");
        this.loops = Array.from(new Set(this.loops.map(JSON.stringify))).map(JSON.parse);
        // console.log(JSON.stringify(this.loops));
    },    
   
    getForwardPaths(){
      let startNode = this.findInputNodeId();
      let endNode = this.findOutputNodeId();
       
      let allPaths = this.findAllPaths(startNode, endNode, {}, [], this.edges);
      
      for (const path of allPaths) {
        let forwardPath = [];
        let forwardGain = [];
        forwardPath.push(startNode);
        
        for (const edgeId of path.edges) {
          forwardPath.push(this.edges[edgeId].target);
          forwardGain.push(this.edges[edgeId].label);
        }
        this.forwardPaths.push({ path: forwardPath, gain: forwardGain });
      }
      return this.forwardPaths
    }, 

    getCyclesNotTouchingPath(path){
      let cycles = [];

      for(let cycle of this.loops){
        let flag = true;

        for(let node of path){
          if(cycle.path.includes(node)){
            flag = false;
            break;
          }
        }
        if(flag){
          cycles.push(cycle);
        }
      }
      return cycles;
    },
   
    getNonTouchingloopsCombinations(cycles,i,res,comb){
     if(i >= cycles.length){
      if(comb.length > 0) 
      res.push(comb);
       return;
     }
     let flag = true;
     for(let j=0;j<comb.length;j++){
        for(let node of cycles[i].path){
          if(comb[j].path.includes(node)){
            flag = false;
            break;
          }
        }
     }
      if(flag){
        this.getNonTouchingloopsCombinations(cycles,i+1,res,[...comb,cycles[i]]);
      }
       this.getNonTouchingloopsCombinations(cycles,i+1,res,[...comb]);
     
    },

    getCombinationsSymbols(){
      let combs= [];
      this.getNonTouchingloopsCombinations(this.loops,0,combs,[]);
      for(let comb of combs){
        let combSybmol=""
        for(let cycle of comb){
          let indexOfCycle = this.loops.indexOf(cycle);
          combSybmol +="L"+(indexOfCycle+1).toString();
        }
        if(!this.allCombsOutput[comb.length-1])
          this.allCombsOutput[comb.length-1] = [];
        this.allCombsOutput[comb.length-1].push(combSybmol);
      }
    },

    getBranchName(nodes){
     let branchName = "";
      for(let i=0;i<nodes.length;i++){
        branchName += this.nodes[nodes[i]].name ;
        
        if(i!=nodes.length-1)
          branchName += " -> ";
      
      }
      return branchName;
    },

    getBranchGain(nodesGains){
      const algebra = require('algebra.js');
      let branchGain = new algebra.parse("1");
      for(let gain of nodesGains){
        let eq;
        if(isNaN(gain)&& gain[0] == "-"){
          gain = gain.substring(1);
          eq = new algebra.parse(gain);
          eq = eq.multiply(-1);
        }
        else
          eq = new algebra.parse(gain);

        branchGain = eq.multiply(branchGain);
      }
      return branchGain;
    },

    getCombinationsGains(path){
      let cycles = this.getCyclesNotTouchingPath(path);
      let combinations = [];

      this.getNonTouchingloopsCombinations(cycles,0,combinations,[]);
      
      let gains= [];
      gains[0] = [];
      const algebra = require('algebra.js');

      for(let comb of combinations){
        let combGain = 1;

        for(let cycle of comb){
         
          for(let gain of cycle.gain){
           let eq ;
           if(isNaN(gain)){
            if(gain[0] == "-")
            eq = new algebra.Expression(-1).multiply(gain.substring(1));
            else  
            eq = new algebra.Expression(gain);
           }
           else
            eq = new algebra.parse(gain.toString());
           
            combGain = eq.multiply(combGain);
          }
        }

        if (!gains[comb.length]) {
            gains[comb.length] = [];
        }
        gains[comb.length].push(combGain);
      }
      return gains;
    },

    determinantOfPath(path){

      let gains = this.getCombinationsGains(path);

      let result = new algebra.parse("1");
      for(let i=1;i<gains.length;i++){
        let sum =new algebra.parse("0");

        for(let j=0;j<gains[i].length;j++){
          sum = sum.add(gains[i][j]);
        }

        if(i%2 == 0)
          result = result.add(sum);
        else
         result = result.subtract(sum);
      }
      
      result = result.simplify();

      return result;

    },
 
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
      for (const edgeId in this.edges) {
        inDegree.set(this.edges[edgeId].target,false);
      }
      for (const [key,value] of inDegree) {
        if (value) 
          return key;
        
      }
  
      
    },

    solveFlowDiagram(){
      this.getForwardPaths();
      this.getAllDistinctCycles();
      
       this.systemDet = this.determinantOfPath([]);
        let branchGains = [];
       for(let path of this.forwardPaths){

          this.pathsDet.push(this.determinantOfPath(path.path));
          let branchGain = this.getBranchGain(path.gain);
          branchGains.push(branchGain);
       }
       
        this.transFun=algebra.parse("0");

         for(let i=0;i<this.pathsDet.length;i++){
           let eq = algebra.parse(this.pathsDet[i].toString());
           let pathGain = eq.multiply(branchGains[i]);
           this.transFun = this.transFun.add(pathGain);
         }
       
         this.transFun.simplify();
        
    },

    adjustOutputs(){
      
      for(let path of this.forwardPaths){
        let branchName = this.getBranchName(path.path);
        let branchGain = this.getBranchGain(path.gain);
        this.forwardPathsOutput.push({path: branchName, gain: branchGain.toString()});
      }
      for(let pathDet of this.pathsDet){
        this.pathsDetOutput.push(pathDet.toString());
      }
      for(let loop of this.loops){
        let dummy=loop;
        dummy.path.push(loop.path[0]);
        let reverseLoop = dummy.path.slice().reverse();
        let loopPath = this.getBranchName(reverseLoop);
        let loopGain = this.getBranchGain(dummy.gain).toString();
        this.loopsOutPut.push({path: loopPath, gain: loopGain});
      }
      this.getCombinationsSymbols();
      if(isNaN(this.systemDet.toString()) || this.systemDet.toString()=="0")
       this.transFun=this.transFun.toString()+" /  "+this.systemDet.toString()+" ";
      else{
        if(this.systemDet!=1)
        this.transFun=this.transFun.divide(Number(this.systemDet));
      }
       this.transFun = this.transFun.toString();
       this.systemDet = this.systemDet.toString();
    }
   }
    
 }
</script>

