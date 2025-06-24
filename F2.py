import streamlit as st
import re
import numpy as np
import plotly.graph_objects as go

rule_matrices = {
    "Hairpin": [
        (r"(A[ATGC]*T)", ""),
        (r"(T[ATGC]*A)", ""),
        (r"(G[ATGC]*C)", ""),
        (r"(C[ATGC]*G)", "")
    ],
    "Stem and Loop": [
        (r"(A[ATGC]+T)", ""),
        (r"(T[ATGC]+A)", ""),
        (r"(G[ATGC]+C)", ""),
        (r"(C[ATGC]+G)", "")
    ],
    "Pseudoknot": [
        (r"A([ATGC])T.*G([ATGC])C", "")
    ],
    "Cloverleaf": [
        (r"(A[ATGC]+T){3,}", ""),
        (r"(T[ATGC]+A){3,}", ""),
        (r"(G[ATGC]+C){3,}", ""),
        (r"(C[ATGC]+G){3,}", "")
    ]
}

formal_grammars = {
    "Hairpin": (
        "Hairpin ->\n"
        "    A [ATGC]* T\n"
        "    T [ATGC]* A\n"
        "    G [ATGC]* C\n"
        "    C [ATGC]* G"
    ),
    "Stem and Loop": (
        "Stem and Loop ->\n"
        "    A [ATGC]+ T\n"
        "    T [ATGC]+ A\n"
        "    G [ATGC]+ C\n"
        "    C [ATGC]+ G"
    ),
    "Pseudoknot": (
        "Pseudoknot ->\n"
        "    A ( [ATGC] ) T ... G ( [ATGC] ) C"
    ),
    "Cloverleaf": (
        "Cloverleaf ->\n"
        "    (A[ATGC]+T){3,}\n"
        "    (T[ATGC]+A){3,}\n"
        "    (G[ATGC]+C){3,}\n"
        "    (C[ATGC]+G){3,}"
    )
}

def validate_dna_sequence(sequence):
    """
    Validates that the DNA sequence contains only valid characters (A, T, G, C).
    """
    if not sequence:
        return False, "The DNA sequence is empty. Please enter a valid sequence."
    valid_chars = set("ATGCatgc")
    invalid_chars = set(sequence) - valid_chars
    if invalid_chars:
        return False, f"Invalid character(s) found: {', '.join(sorted(invalid_chars))}. Please use only A, T, G, C."
    return True, ""

def detect_structures_insertion_deletion(sequence, rule_matrices, max_iterations=10):
    """
    Uses a matrix insertion–deletion approach to detect structures.
    For each structure, it iteratively applies its set of deletion rules.
    If the sequence is completely reduced to an empty string within max_iterations,
    the structure is considered detected.
    """
    detected_structures = {}
    for structure_name, rules in rule_matrices.items():
        current_sequence = sequence
        iteration = 0
        while current_sequence and iteration < max_iterations:
            new_sequence = current_sequence
            for pattern, replacement in rules:
                new_sequence = re.sub(pattern, replacement, new_sequence)
            if new_sequence == current_sequence:
                break
            current_sequence = new_sequence
            iteration += 1
        if current_sequence == "":
            detected_structures[structure_name] = True
    return detected_structures

def get_structure_indices(sequence, rules):
    """
    For each rule in a structure's rule matrix, find all matches in the original sequence.
    Returns a list of (start, end) index tuples.
    """
    indices = []
    for pattern, _ in rules:
        for m in re.finditer(pattern, sequence):
            indices.append((m.start(), m.end()))
    return indices

def plot_structure_3d(sequence, highlighted_indices, structure_name):
    """
    Creates a 3D node graph using Plotly.
    - Each character in the sequence is a node arranged along a helix.
    - Consecutive nodes are connected by gray lines.
    - Nodes whose indices fall in highlighted_indices are colored red.
    """
    num_nodes = len(sequence)
    angles = [i * 0.5 for i in range(num_nodes)]
    x = [np.cos(angle) for angle in angles]
    y = [np.sin(angle) for angle in angles]
    z = [i * 0.2 for i in range(num_nodes)]
    
    edge_x, edge_y, edge_z = [], [], []
    for i in range(num_nodes - 1):
        edge_x.extend([x[i], x[i+1], None])
        edge_y.extend([y[i], y[i+1], None])
        edge_z.extend([z[i], z[i+1], None])
    
    node_colors = ["red" if i in highlighted_indices else "blue" for i in range(num_nodes)]
    
    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='none'
    )
    
    node_trace = go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers+text',
        marker=dict(size=8, color=node_colors, line=dict(width=1)),
        text=list(sequence),
        textposition="bottom center",
        hoverinfo='text'
    )
    
    layout = go.Layout(
        title=f"3D Node Graph for {structure_name}",
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=30),
        scene=dict(
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(showbackground=False)
        )
    )
    
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig

def main():
    st.title("BioSequence Analyzer")

    sequence = st.text_input("Enter DNA Sequence:", value="AACGTCGATT")
    
    if st.button("Detect Structures"):
        is_valid, error_msg = validate_dna_sequence(sequence)
        if not is_valid:
            st.error(error_msg)
            return

        detected = detect_structures_insertion_deletion(sequence, rule_matrices, max_iterations=10)
        
        if detected:
            for structure_name in detected:
                st.markdown(f"### {structure_name}")

                grammar = formal_grammars.get(structure_name, "N/A")
                st.code(grammar, language="text")

                indices = get_structure_indices(sequence, rule_matrices[structure_name])
                if indices:
                    st.markdown("**Detected Indices:**")
                    for start, end in indices:
                        st.write(f"[{start}, {end})")
                else:
                    st.write("No indices detected for this structure.")
 
                highlighted_indices = set()
                for start, end in indices:
                    highlighted_indices.update(range(start, end))
                
                fig = plot_structure_3d(sequence, highlighted_indices, structure_name)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No Structures detected using the matrix insertion–deletion approach.")

if __name__ == "__main__":
    main()
