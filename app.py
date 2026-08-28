import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# WSN Q-LEARNING RECONSTRUCTION — DEMONSTRATION DASHBOARD
# ============================================================

st.set_page_config(
    page_title="3D WSN Q-Learning Reconstruction",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# PROJECT INFORMATION
# ============================================================

REFERENCE_PAPER = (
    "I. Jrhilifa, H. Ouadi, and A. Jilbab, "
    "\"Q-learning-based Optimization of Smart Home's Wireless "
    "Sensors Network Lifetime,\" International Journal of "
    "Renewable Energy Research, Vol. 13, No. 1, 2023."
)

TITLE = (
    "Methodology-Faithful Reconstruction and D0 Sensitivity "
    "Analysis of Q-Learning-Based Routing in a 3D Wireless Sensor Network"
)

# ============================================================
# FROZEN RECONSTRUCTION PARAMETERS
# ============================================================

TOTAL_NODES = 45
SENSOR_COUNT = 44
INITIAL_ENERGY = 0.5

AREA_X = 16.0
AREA_Y = 13.0
AREA_Z = 2.5

PACKET_SIZE = 512
E_ELEC = 5e-8
E_AMP = 1e-10

COORDINATE_SEED = 42
COMMUNICATION_RANGE = 7.0
D0 = 4.0

# ============================================================
# FINAL EXPERIMENT RESULTS
# ============================================================

FINAL_ROUNDS = 9189
FINAL_DATA_KBITS = 4704.768
FINAL_ENERGY_CONSUMED = 4.080833
FINAL_RESIDUAL_ENERGY = 17.919167
FINAL_ALIVE = 44
FINAL_DEAD = 0
MIN_RESIDUAL = 0.000020122862

PUBLISHED_Q_ROUNDS = 6260
PUBLISHED_Q_DATA = 3205.12

PUBLISHED_DIJKSTRA_ROUNDS = 2737
PUBLISHED_DIJKSTRA_DATA = 1401.34

# ============================================================
# D0 EXTENSION RESULTS
# ============================================================

D0_RESULTS = pd.DataFrame({
    "D0 (m)": [2, 3, 4, 5, 6],
    "Rounds": [9088, 9059, 9189, 9512, 10218],
    "Data (Kbits)": [
        4653.056,
        4638.208,
        4704.768,
        4870.144,
        5231.616
    ],
    "Energy Consumed (J)": [
        4.164968,
        4.066465,
        4.080833,
        4.076632,
        3.835497
    ],
    "Final Residual Energy (J)": [
        17.835032,
        17.933535,
        17.919167,
        17.923368,
        18.164503
    ]
})

# ============================================================
# TEST ROUTE FROM YOUR EXPERIMENT
# ============================================================

TEST_PATH = [
    "S1",
    "S3",
    "S6",
    "S7",
    "S8",
    "S17",
    "Sink"
]

# Audited link information from your experiment
ROUTE_DETAILS = pd.DataFrame({
    "Link": [
        "S1 → S3",
        "S3 → S6",
        "S6 → S7",
        "S7 → S8",
        "S8 → S17"
    ],
    "Distance (m)": [
        4.1397,
        5.8356,
        5.0928,
        4.9638,
        1.1785
    ],
    "Hop Count": [
        2,
        1,
        2,
        1,
        1
    ],
    "Beta": [
        4,
        4,
        4,
        4,
        2
    ],
    "Reward": [
        0.0008512480,
        0.0004311532,
        0.0003716285,
        0.0008236092,
        0.3600274312
    ]
})

TOTAL_ROUTE_REWARD = 0.3625050700

# ============================================================
# RECONSTRUCTED COORDINATES
#
# NOTE:
# These are regenerated using the documented seed and area.
# Replace this block with the exact coordinate dictionary
# from your notebook if you want exact geometric reproduction.
# ============================================================

rng = np.random.default_rng(COORDINATE_SEED)

coordinates = {}

for i in range(1, 45):
    coordinates[f"S{i}"] = (
        float(rng.uniform(0, AREA_X)),
        float(rng.uniform(0, AREA_Y)),
        float(rng.uniform(0, AREA_Z))
    )

coordinates["Sink"] = (
    float(rng.uniform(0, AREA_X)),
    float(rng.uniform(0, AREA_Y)),
    float(rng.uniform(0, AREA_Z))
)

# ============================================================
# CREATE GRAPH
# ============================================================

G = nx.Graph()

for node, coord in coordinates.items():
    G.add_node(node, pos=coord)

nodes = list(coordinates.keys())

for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):

        n1 = nodes[i]
        n2 = nodes[j]

        p1 = np.array(coordinates[n1])
        p2 = np.array(coordinates[n2])

        distance = np.linalg.norm(p1 - p2)

        if distance <= COMMUNICATION_RANGE:
            G.add_edge(
                n1,
                n2,
                distance=float(distance)
            )

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_3d_network(selected_path=None):

    fig = go.Figure()

    # --------------------------------------------------------
    # Network edges
    # --------------------------------------------------------

    for u, v in G.edges():

        x1, y1, z1 = coordinates[u]
        x2, y2, z2 = coordinates[v]

        fig.add_trace(
            go.Scatter3d(
                x=[x1, x2],
                y=[y1, y2],
                z=[z1, z2],
                mode="lines",
                line=dict(
                    color="lightgray",
                    width=1
                ),
                hoverinfo="skip",
                showlegend=False
            )
        )

    # --------------------------------------------------------
    # Sensor nodes
    # --------------------------------------------------------

    sensor_x = []
    sensor_y = []
    sensor_z = []
    sensor_names = []

    for node in coordinates:

        if node == "Sink":
            continue

        x, y, z = coordinates[node]

        sensor_x.append(x)
        sensor_y.append(y)
        sensor_z.append(z)
        sensor_names.append(node)

    fig.add_trace(
        go.Scatter3d(
            x=sensor_x,
            y=sensor_y,
            z=sensor_z,
            mode="markers+text",
            text=sensor_names,
            textposition="top center",
            marker=dict(
                size=5,
                color="royalblue"
            ),
            name="Sensor Nodes"
        )
    )

    # --------------------------------------------------------
    # Sink
    # --------------------------------------------------------

    sx, sy, sz = coordinates["Sink"]

    fig.add_trace(
        go.Scatter3d(
            x=[sx],
            y=[sy],
            z=[sz],
            mode="markers+text",
            text=["Sink"],
            textposition="top center",
            marker=dict(
                size=10,
                color="red",
                symbol="diamond"
            ),
            name="Sink"
        )
    )

    # --------------------------------------------------------
    # Selected route
    # --------------------------------------------------------

    if selected_path:

        for i in range(len(selected_path) - 1):

            u = selected_path[i]
            v = selected_path[i + 1]

            x1, y1, z1 = coordinates[u]
            x2, y2, z2 = coordinates[v]

            fig.add_trace(
                go.Scatter3d(
                    x=[x1, x2],
                    y=[y1, y2],
                    z=[z1, z2],
                    mode="lines",
                    line=dict(
                        color="orange",
                        width=7
                    ),
                    name="Selected Q-Learning Route",
                    showlegend=(i == 0)
                )
            )

    fig.update_layout(
        title="3D Wireless Sensor Network",
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Z (m)"
        ),
        height=650,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig


# ============================================================
# HEADER
# ============================================================

st.title("🤖 3D WSN Q-Learning Reconstruction")

st.markdown(
    f"""
### {TITLE}

**Reference paper:**  
{REFERENCE_PAPER}

This dashboard provides a visual demonstration of the reconstructed
45-node 3D Wireless Sensor Network, the Q-learning routing experiment,
and the D0 sensitivity extension.
"""
)

st.info(
    "This dashboard is a demonstration layer for the executed research "
    "notebook. The reported numerical results are the recorded results "
    "of the reconstructed experiments."
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Project Parameters")

st.sidebar.metric("Total Nodes", TOTAL_NODES)
st.sidebar.metric("Sensor Nodes", SENSOR_COUNT)
st.sidebar.metric("Initial Energy / Sensor", "0.5 J")
st.sidebar.metric("Communication Range", "7.0 m")
st.sidebar.metric("D0", "4.0 m")

st.sidebar.markdown("---")

st.sidebar.write("**Energy Model**")
st.sidebar.write(f"E_elec = {E_ELEC:.0e} J/bit")
st.sidebar.write(f"E_amp = {E_AMP:.0e} J/bit/m²")
st.sidebar.write(f"Packet size = {PACKET_SIZE} bits")

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 Network",
    "🧠 Q-Learning Route",
    "⚡ Final Experiment",
    "📈 D0 Extension"
])

# ============================================================
# TAB 1 — NETWORK
# ============================================================

with tab1:

    st.header("45-Node 3D WSN")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Network Nodes",
            TOTAL_NODES
        )

    with col2:
        st.metric(
            "Sensor Nodes",
            SENSOR_COUNT
        )

    with col3:
        st.metric(
            "Graph Edges",
            G.number_of_edges()
        )

    st.plotly_chart(
        create_3d_network(),
        use_container_width=True
    )

    st.caption(
        "3D network visualization generated using the documented "
        "16 × 13 × 2.5 m simulation area and coordinate seed 42."
    )

# ============================================================
# TAB 2 — Q-LEARNING ROUTE
# ============================================================

with tab2:

    st.header("Q-Learning Routing Demonstration")

    source = st.selectbox(
        "Select source sensor",
        ["S1", "S2", "S3", "S4"],
        index=0
    )

    st.caption(
        "S1 uses the recorded audited route from the experiment. "
        "For S2–S4, the dashboard demonstrates feasible routing "
        "through the reconstructed network."
    )

    if st.button("▶ Show Route"):

        # ----------------------------------------------------
        # S1 — ACTUAL RECORDED/AUDITED ROUTE
        # ----------------------------------------------------

        if source == "S1":

            selected_path = [
                "S1",
                "S3",
                "S6",
                "S7",
                "S8",
                "S17",
                "Sink"
            ]

            route_type = "Recorded experiment route"

            total_reward = TOTAL_ROUTE_REWARD

            st.success(
                "Recorded route from the reconstructed experiment."
            )

        # ----------------------------------------------------
        # S2–S4 — FEASIBLE ROUTING DEMONSTRATION
        # ----------------------------------------------------

        else:

            try:

                # Find a feasible path to the Sink
                selected_path = nx.shortest_path(
                    G,
                    source=source,
                    target="Sink",
                    weight="distance"
                )

                route_type = (
                    "Feasible route demonstration on "
                    "the reconstructed network"
                )

                # ------------------------------------------------
                # Calculate demonstration reward
                # ------------------------------------------------

                total_reward = 0.0

                for i in range(len(selected_path) - 1):

                    sender = selected_path[i]
                    receiver = selected_path[i + 1]

                    if receiver == "Sink":
                        continue

                    distance = G[sender][receiver]["distance"]

                    if distance <= D0:
                        beta = 2
                    else:
                        beta = 4

                    hop_count = len(selected_path) - i - 1

                    residual_energy = INITIAL_ENERGY

                    total_reward += (
                        residual_energy
                        /
                        (
                            (distance ** beta)
                            * hop_count
                        )
                    )

                st.success(
                    "Feasible route found in the reconstructed network."
                )

            except nx.NetworkXNoPath:

                st.error(
                    f"No feasible graph path was found from "
                    f"{source} to Sink."
                )

                st.stop()

        # ----------------------------------------------------
        # DISPLAY ROUTE
        # ----------------------------------------------------

        st.subheader("Selected Route")

        st.code(
            " → ".join(selected_path)
        )

        # ----------------------------------------------------
        # ROUTE METRICS
        # ----------------------------------------------------

        hop_count_total = len(selected_path) - 1

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Source",
                source
            )

        with col2:
            st.metric(
                "Hop Count",
                hop_count_total
            )

        with col3:
            st.metric(
                "Total Reward",
                f"{total_reward:.6f}"
            )

        with col4:
            st.metric(
                "Initial Energy",
                "0.5 J"
            )

        st.markdown("---")

        st.write(
            f"**Route type:** {route_type}"
        )

        # ----------------------------------------------------
        # 3D ROUTE VISUALIZATION
        # ----------------------------------------------------

        st.plotly_chart(
            create_3d_network(selected_path),
            use_container_width=True
        )

        # ----------------------------------------------------
        # LINK DETAILS
        # ----------------------------------------------------

        st.subheader("Route Link Details")

        route_rows = []

        for i in range(len(selected_path) - 1):

            sender = selected_path[i]
            receiver = selected_path[i + 1]

            distance = np.linalg.norm(
                np.array(coordinates[sender])
                -
                np.array(coordinates[receiver])
            )

            if receiver == "Sink":

                beta = "-"

            else:

                beta = (
                    2
                    if distance <= D0
                    else 4
                )

            route_rows.append({
                "Link":
                    f"{sender} → {receiver}",

                "Distance (m)":
                    round(distance, 4),

                "Beta":
                    beta
            })

        route_table = pd.DataFrame(route_rows)

        st.dataframe(
            route_table,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # S1 SPECIFIC AUDIT DETAILS
        # ----------------------------------------------------

        if source == "S1":

            st.subheader(
                "Recorded S1 Link-Level Audit"
            )

            st.dataframe(
                ROUTE_DETAILS,
                use_container_width=True,
                hide_index=True
            )

            st.metric(
                "Recorded Total Path Reward",
                f"{TOTAL_ROUTE_REWARD:.10f}"
            )

            st.info(
                "This S1 route and reward correspond to the "
                "recorded single-path validation from the experiment."
            )

        else:

            st.info(
                "S2–S4 are shown as routing demonstrations using "
                "the reconstructed network. Their displayed routes "
                "should not be cited as recorded Q-learning "
                "experimental results."
            )

# ============================================================
# TAB 3 — FINAL EXPERIMENT
# ============================================================

with tab3:

    st.header("Final Reconstructed 45-Node Experiment")

    st.markdown(
        """
        The final reconstructed Q-learning experiment was executed
        from a clean energy state with 44 sensor nodes initialized
        to 0.5 J each.
        """
    )

    # --------------------------------------------------------
    # Main metrics
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Completed Rounds",
            f"{FINAL_ROUNDS:,}"
        )

    with col2:
        st.metric(
            "Data Transmitted",
            f"{FINAL_DATA_KBITS:,.2f} Kbits"
        )

    with col3:
        st.metric(
            "Energy Consumed",
            f"{FINAL_ENERGY_CONSUMED:.6f} J"
        )

    with col4:
        st.metric(
            "Final Residual Energy",
            f"{FINAL_RESIDUAL_ENERGY:.6f} J"
        )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Alive Nodes",
            FINAL_ALIVE
        )

    with col2:
        st.metric(
            "Dead Nodes",
            FINAL_DEAD
        )

    with col3:
        st.metric(
            "Minimum Residual Energy",
            f"{MIN_RESIDUAL:.8f} J"
        )

    with col4:
        st.metric(
            "Initial Total Energy",
            "22.0 J"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Energy visualization
    # --------------------------------------------------------

    rounds = np.array([
        0,
        500,
        1000,
        1500,
        2000,
        2500,
        3000,
        3500,
        4000,
        4500,
        5000,
        5500,
        6000,
        6500,
        7000,
        7500,
        8000,
        8500,
        9000,
        9189
    ])

    energies = np.array([
        22.000000,
        21.781995,
        21.564379,
        21.346494,
        21.128649,
        20.911238,
        20.693121,
        20.475457,
        20.257658,
        20.039725,
        19.822004,
        19.604429,
        19.386424,
        19.168808,
        18.950923,
        18.733078,
        18.512790,
        18.270749,
        18.013986,
        17.919167
    ])

    fig_energy = go.Figure()

    fig_energy.add_trace(
        go.Scatter(
            x=rounds,
            y=energies,
            mode="lines+markers",
            name="Residual Energy"
        )
    )

    fig_energy.update_layout(
        title="Residual Energy Variation",
        xaxis_title="Completed Round",
        yaxis_title="Total Residual Energy (J)",
        height=450
    )

    st.plotly_chart(
        fig_energy,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Alive node visualization
    # --------------------------------------------------------

    alive = np.full(len(rounds), 44)

    fig_alive = go.Figure()

    fig_alive.add_trace(
        go.Scatter(
            x=rounds,
            y=alive,
            mode="lines+markers",
            name="Alive Sensors"
        )
    )

    fig_alive.update_layout(
        title="Number of Alive Sensor Nodes",
        xaxis_title="Completed Round",
        yaxis_title="Alive Sensor Nodes",
        yaxis=dict(
            range=[43, 45]
        ),
        height=400
    )

    st.plotly_chart(
        fig_alive,
        use_container_width=True
    )

    st.warning(
        "The experiment terminated because no further complete "
        "feasible route could be selected. No sensor reached exactly "
        "zero energy; therefore all 44 sensors remained technically alive."
    )

    # --------------------------------------------------------
    # Published comparison
    # --------------------------------------------------------

    st.subheader("Published vs Reconstructed Results")

    comparison = pd.DataFrame({
        "Method": [
            "Published Q-learning",
            "Published Dijkstra",
            "Reconstructed Q-learning"
        ],
        "Completed Rounds": [
            PUBLISHED_Q_ROUNDS,
            PUBLISHED_DIJKSTRA_ROUNDS,
            FINAL_ROUNDS
        ],
        "Data (Kbits)": [
            PUBLISHED_Q_DATA,
            PUBLISHED_DIJKSTRA_DATA,
            FINAL_DATA_KBITS
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# TAB 4 — D0 EXTENSION
# ============================================================

with tab4:

    st.header("Extension: D0 Sensitivity Analysis")

    st.markdown(
        """
        D0 was varied from 2 m to 6 m while keeping the remaining
        reconstructed experimental configuration fixed.
        This experiment analyzes the sensitivity of routing performance
        to the propagation-distance threshold.
        """
    )

    st.dataframe(
        D0_RESULTS,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Rounds plot
    # --------------------------------------------------------

    fig_d0_rounds = go.Figure()

    fig_d0_rounds.add_trace(
        go.Scatter(
            x=D0_RESULTS["D0 (m)"],
            y=D0_RESULTS["Rounds"],
            mode="lines+markers",
            name="Completed Rounds"
        )
    )

    fig_d0_rounds.update_layout(
        title="D0 Sensitivity — Completed Transmission Rounds",
        xaxis_title="D0 (m)",
        yaxis_title="Completed Transmission Rounds",
        height=450
    )

    st.plotly_chart(
        fig_d0_rounds,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Data plot
    # --------------------------------------------------------

    fig_d0_data = go.Figure()

    fig_d0_data.add_trace(
        go.Scatter(
            x=D0_RESULTS["D0 (m)"],
            y=D0_RESULTS["Data (Kbits)"],
            mode="lines+markers",
            name="Conveyed Data"
        )
    )

    fig_d0_data.update_layout(
        title="D0 Sensitivity — Total Conveyed Data",
        xaxis_title="D0 (m)",
        yaxis_title="Total Conveyed Data (Kbits)",
        height=450
    )

    st.plotly_chart(
        fig_d0_data,
        use_container_width=True
    )

    st.success(
        "Extension completed: increasing D0 from 2 m to 6 m changed "
        "the completed transmission rounds from 9,088 to 10,218."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Reinforcement Learning Assignment | Q-Learning | "
    "45-Node 3D Wireless Sensor Network | "
    "Reconstruction + D0 Sensitivity Extension"
)