<template>
    
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
            outputForwardPaths: [],
            outputloops: [],
            outputAllCombs: [],
            outputpathsDet:[],      
            pathsDet:[],
            loops:[],
            systemDet:null,
            transFun:null,
        }
    },

    
 }
</script>

