import java.util.*;

class Graph {
    class Edge {
        String target; // 目标状态
        int cost; // 边的权值

        public Edge(String target, int weight) {
            this.target = target;
            this.cost = weight;
        }
    }

    private Map<String, List<Edge>> adjacencyList; // 邻接表

    public Graph() {
        this.adjacencyList = new HashMap<>();
    }

    public void addEdge(String from, String to, int cost) {
        this.adjacencyList.computeIfAbsent(from, k -> new ArrayList<>()).add(new Edge(to, cost));
    }

    public List<Edge> getNeighbors(String node) {
        return this.adjacencyList.getOrDefault(node, Collections.emptyList());
    }
}

class Node {
    String state;
    Node parent;
    int depth; // DFS, BFS 需要
    int pathCost; // UCS 需要
    int estimatedCostToGoal; // Greedy, A* 需要

    public Node(String state, Node parent, int depth, int pathCost, int estimatedCostToGoal) {
        this.state = state;
        this.parent = parent;
        this.depth = depth;
        this.pathCost = pathCost;
        this.estimatedCostToGoal = estimatedCostToGoal;
    }
}

public class Search {
    private Graph graph;
    private String goal;

    public Search(Graph graph, String goal) {
        this.graph = graph;
        this.goal = goal;
    }

    private static int heuristic(String currentState, String goalState) {
        // 模拟的启发式函数，实现细节依赖于问题域
        switch (currentState) {
            case "GOAL":
                return 0;
            case "f", "r", "e", "c":
                return 1;
            case "q", "h":
                return 2;
            case "b", "d", "p", "a":
                return 3;
            case "START":
                return 4;
            default:
                return 0x3f3f3f3f;
        }
    }

    public List<String> search(Comparator<Node> comparator) {
        PriorityQueue<Node> fringe = new PriorityQueue<>(comparator);
        fringe.add(new Node("START", null, 0, 0, heuristic("START", goal))); // 起点
        Set<String> visited = new HashSet<>();

        while (!fringe.isEmpty()) {
            Node currentNode = fringe.poll();
            if (currentNode.state.equals(goal)) {
                return reconstructPath(currentNode);
            }

            if (!visited.contains(currentNode.state)) {
                visited.add(currentNode.state);

                for (Graph.Edge e : graph.getNeighbors(currentNode.state)) {
                    Node n = new Node(e.target, currentNode, currentNode.depth + 1,
                            e.cost + currentNode.pathCost, heuristic(e.target, goal));
                    fringe.add(n);
                }
            }
        }
        return null;
    }

    private List<String> reconstructPath(Node node) {
        LinkedList<String> path = new LinkedList<>();
        while (node != null) {
            path.addFirst(node.state);
            node = node.parent;
        }
        return path;
    }

    public static void main(String[] args) {
        // 实例化图并添加边
        Graph graph = new Graph();
        graph.addEdge("START", "d", 3);
        graph.addEdge("START", "e", 9);
        graph.addEdge("START", "p", 1);
        graph.addEdge("b", "a", 2);
        graph.addEdge("c", "a", 2);
        graph.addEdge("d", "b", 1);
        graph.addEdge("d", "c", 8);
        graph.addEdge("d", "e", 2);
        graph.addEdge("e", "h", 8);
        graph.addEdge("e", "r", 2);
        graph.addEdge("f", "c", 3);
        graph.addEdge("f", "GOAL", 2);
        graph.addEdge("h", "p", 4);
        graph.addEdge("h", "q", 4);
        graph.addEdge("p", "q", 15);
        graph.addEdge("r", "f", 2);

        // 创建不同的搜索策略
        Search dfs = new Search(graph, "GOAL");
        Search bfs = new Search(graph, "GOAL");
        Search ucs = new Search(graph, "GOAL");

        Comparator<Node> dfsComparator = (Node n1, Node n2) -> n2.depth - n1.depth; // LIFO stack, priority: -depth
        Comparator<Node> bfsComparator = Comparator.comparingInt(n -> n.depth); // FIFO queue, priority: depth
        Comparator<Node> ucsComparator = Comparator.comparingInt(n -> n.pathCost); // priority: cumulative cost
        Comparator<Node> greedyComparator = (n1, n2) -> heuristic(n1.state, "GOAL") -
                heuristic(n2.state, "GOAL"); // priority: heuristic
        Comparator<Node> aStarComparator = (n1, n2) -> (n1.pathCost + heuristic(n1.state, "GOAL"))
                - (n2.pathCost + heuristic(n2.state, "GOAL")); // priority: cumulative cost + heuristic

        // 执行搜索
        List<String> dfsPath = dfs.search(dfsComparator);
        List<String> bfsPath = bfs.search(bfsComparator);
        List<String> ucsPath = ucs.search(ucsComparator);
        List<String> greedyPath = ucs.search(greedyComparator);
        List<String> aStarPath = ucs.search(aStarComparator);

        System.out.println("DFS Path: " + dfsPath);
        System.out.println("BFS Path: " + bfsPath);
        System.out.println("UCS Path: " + ucsPath);
        System.out.println("Greedy Path: " + greedyPath);
        System.out.println("A* Path: " + aStarPath);
    }
}
