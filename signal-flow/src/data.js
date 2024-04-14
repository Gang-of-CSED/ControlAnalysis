import * as Vng from "v-network-graph";

const nodes = {
  node1: { name: "N2", type: 'queue', shape: 'circle', color: '#11ff55', main: true },
  node2: { name: "N3", type: 'queue', shape: 'circle', color: '#11ff55', main: true },
  node3: { name: "N1", type: 'machine', shape: 'circle', color: '#11ff55' },
};

const edges = {
  edge1: { source: "node1", target: "node3", color: '#55aaFF', label: 'G1(x)'},
  edge2: { source: "node3", target: "node2", color: '#55aaFF', label: 'G2(x)'},
};

const layouts = {
  nodes: {
    node1: { x: 300, y: 0 },
    node2: { x: -600, y: 0 },
    node3: { x: 0, y: 150 },
  },
};

const paths = {
  path1: { edges: ["edge1", "edge2"] },
};

const configs = Vng.defineConfigs({
  view: {
    fitView: true,
    scalingObjects: true,
    layoutHandler: new Vng.GridLayout({ grid: 15 }),
  },
  node: {
    selectable: true,
    draggable: node => !node.main,

    hover: {
      color: node => node.color,
      type: node => node.shape,
    },
    normal: {
      color: node => node.color,
      type: node => node.shape,
    },
    label: {
      fontFamily: "Arial",
      margin: 10,
      fontSize: 20
    },
  },

  edge: {
    selectable: true,
    hover: {
      width: 8,
      color: edge => edge.color
    },
    normal: {
      width: 8,
      color: edge => edge.color
    },
    selected: {
      dasharray: null,
    },
    type: "curve",
  },
  path: {
    selectable: false,
    visible: false,
    normal: {
      width: 3,
      dasharray: "10 16",
      animate: true,
      color: "#ffffff",
      animationSpeed: 40,
    },
  },
});


export default {
  nodes,
  edges,
  layouts,
  configs,
  paths,
};
