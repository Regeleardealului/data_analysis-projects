# 🍳 Gastronomy Network Analysis

### Discovering Hidden Structures in Recipes using Network Science

This project explores the **hidden structure of gastronomy** using
**network theory and graph analytics**.\
By analyzing nearly **40,000 recipes and over 6,700 ingredients**, we
construct a large ingredient co‑occurrence network and investigate its
structural properties, communities, and influential ingredients.

The goal is to understand **which ingredients are most important, how
cuisines are structured, and how ingredients connect different culinary
worlds**.

------------------------------------------------------------------------

# 📊 Dataset

The dataset contains recipes in **JSON format**.

Each recipe includes:

-   `id`
-   `cuisine`
-   `ingredients`

Example:

``` json
{
  "id": 24717,
  "cuisine": "italian",
  "ingredients": ["salt", "olive oil", "garlic", "tomatoes"]
}
```

------------------------------------------------------------------------

# 🧠 Network Modeling

The dataset is converted into a **graph representation**.

### Graph Definition

-   **Nodes (Vertices)** → Ingredients
-   **Edges** → Two ingredients appearing in the same recipe
-   **Edge Weight** → Number of recipes where the pair appears together

Example:

    salt —— pepper (1000)
    chili —— cream (5)

The resulting network is:

-   **Undirected**
-   **Weighted**
-   **Ingredient co-occurrence network**

A **minimum co-occurrence threshold** is used to remove noise and
prevent an overly dense graph.

------------------------------------------------------------------------

# 🔬 Methodology

The analysis follows **six main phases**:

------------------------------------------------------------------------

# 1️⃣ Data Loading and Graph Construction

Recipes are loaded from JSON files and converted into a **NetworkX
graph**.

Key function:

``` python
create_ingredient_network()
```

Steps:

1.  Iterate through every recipe
2.  Normalize ingredient names
3.  Count ingredient occurrences
4.  Create edges for every ingredient pair
5.  Assign edge weights based on frequency

------------------------------------------------------------------------

# 2️⃣ Centrality Analysis

Several **network centrality measures** were calculated to identify the
most important ingredients.

### Degree Centrality

Measures how many ingredients a node connects to.

Interpretation: - Highly versatile ingredients - Used across many
recipes

Examples: - salt - onion - water

------------------------------------------------------------------------

### Betweenness Centrality

Measures how often an ingredient acts as a **bridge between clusters**.

Example interpretation: Garlic may connect **Mediterranean and Asian
cuisine clusters**.

Removing high-betweenness nodes may fragment the network.

------------------------------------------------------------------------

### Closeness Centrality

Measures how close an ingredient is to all others in the network.

High closeness → ingredient is **structurally central in the culinary
universe**.

------------------------------------------------------------------------

### Eigenvector Centrality

Not only counts connections, but also considers **importance of
neighbors**.

Meaning: Being connected to important ingredients increases your
importance.

------------------------------------------------------------------------

# 3️⃣ Graph Metrics

Several structural properties of the network were calculated.

  -------------------------------- ---------
  - Nodes                            6703
  - Edges                            39679
  - Density                          0.0018
  - Average degree                   \~11.84
  - Average clustering coefficient   0.202
  - Average shortest path            \~2.07
  - Diameter                         4

### Key Insight

The network exhibits **Small-World properties**.

Even distant ingredients are connected through only a few steps.

Example path:

    soy sauce → garlic → onion → butter → vanilla

------------------------------------------------------------------------

# 4️⃣ Community Detection

Two algorithms were used to detect ingredient clusters.

## Louvain Algorithm

Detects communities by **maximizing modularity**.

**Modularity** measures how well the graph splits into groups.

High modularity means:

-   dense connections within groups
-   sparse connections between groups

The algorithm automatically identifies **natural flavor groups** such
as:

-   Mediterranean
-   Asian
-   Dessert clusters

------------------------------------------------------------------------

## Girvan-Newman Algorithm

This method:

1.  Identifies **bridge edges**
2.  Removes them iteratively
3.  Observes how the network splits

It reveals deeper hierarchical structures inside the ingredient network.

------------------------------------------------------------------------

# 5️⃣ Cuisine Network Comparison

Separate graphs were constructed for each cuisine.

*Goal was*: Compare structural differences between cuisines.

Three types of culinary networks emerged:

### 1. Dense Networks

Examples:

-   Indian
-   Moroccan

Reason: Heavy use of spice mixtures.

Many ingredients interact simultaneously → dense graph.

------------------------------------------------------------------------

### 2. Large but Sparse Networks

Examples:

-   Italian
-   Mexican
-   Greek

Characteristics:

-   many ingredients
-   fewer connections between them

These cuisines use **large ingredient sets but simpler combinations**.

------------------------------------------------------------------------

### 3. Simpler Networks

Examples:

-   Irish
-   French
-   South American cuisines

Fewer ingredients and lower average degree.

------------------------------------------------------------------------

# 6️⃣ Network Robustness

A robustness experiment simulated **removal of key ingredients**.

Goal: Measure how the network fragments when critical nodes disappear.

Example findings:

-   Removing **salt** causes \~7% fragmentation.
-   Removing **onion** has smaller impact because other ingredients
    compensate.
-   Removing **sugar** may isolate dessert clusters.

This shows the network has:

-   **core ingredients**
-   **peripheral clusters**

------------------------------------------------------------------------

# 📈 Visualizations

The notebook produces several interactive visualizations:

-   Ingredient Network Graph
-   Top Ingredients Centrality Chart
-   Strongest Ingredient Connections
-   Cuisine Network Comparison
-   Network Robustness Simulation
-   Community Structure Treemap
-   Centrality Comparison Heatmap
-   Influence Spread Simulation
-   HITS Algorithm Visualization

------------------------------------------------------------------------

# 🌐 Key Findings

### 1. The Gastronomy Network is Sparse

Density:

    0.0018

Only a small fraction of possible ingredient combinations appear in
recipes.

------------------------------------------------------------------------

### 2. The Network Shows Small‑World Behavior

Average path length:

    ≈ 2.07

Any ingredient can reach another through **very few intermediates**.

------------------------------------------------------------------------

### 3. Strong Hierarchy Exists

Centrality analysis reveals a clear hierarchy:

    salt → onion → water → garlic → oil

Salt acts as the **central backbone of the culinary network**.

------------------------------------------------------------------------

### 4. Hub Ingredients Act as Super‑Spreaders

Influence simulations show that ingredients such as:

-   salt
-   onion
-   water
-   olive oil

can reach most of the network within **3 steps**.

Rare ingredients remain isolated.

------------------------------------------------------------------------

### 5. The Network is Scale‑Free

A small number of ingredients have extremely high connectivity, while
most have very few connections.

This follows a **power‑law distribution**, typical for real-world
networks.

------------------------------------------------------------------------

# 📚 Conclusion

This project demonstrates how **network science can reveal hidden
structures in gastronomy**.

Despite being extremely sparse, the ingredient network exhibits:

-   **small‑world behavior**
-   **scale‑free topology**
-   **strong central ingredients**
-   **distinct cuisine communities**

The results highlight that global cuisine is connected through a small
set of **universal ingredients**, with **salt acting as the central
backbone of the culinary universe**.
