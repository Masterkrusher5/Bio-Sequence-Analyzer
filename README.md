# Bio-Sequence-Analyzer

BioSequence Analyzer is an interactive tool that identifies structural DNA motifs like hairpins, pseudoknots, and loops using formal language theory and matrix insertion–deletion rules. Built with Python, Streamlit, and Plotly, it provides real-time visual feedback via 3D node graphs.

🔡 How to Use the BioSequence Analyzer
🧬 Input Format
The tool expects a DNA sequence containing only the characters: A, T, G, C (case-insensitive).

You can paste the sequence directly into the input box in the Streamlit UI.

✅ Valid Example Inputs:

objectivec
Copy
Edit
AACGTCGATT
ATGCGATACGTTAG
CGTATCGCGCTATACG
❌ Invalid Inputs:

pgsql
Copy
Edit
ABCDGHIJK (Contains non-DNA characters)
123456789 (Numeric characters are not allowed)
" " or Empty input (Blank input will raise a warning)
🧪 How Detection Works
The tool uses a matrix insertion–deletion algorithm based on formal grammars to reduce the sequence according to specific structural rules. If the sequence reduces fully to an empty string using those rules, the corresponding structure is said to be detected.

Structures Detected:
Structure	Pattern Logic
Hairpin	Complementary ends with palindromic core
Stem and Loop	Repeats with flanking complementary bases
Pseudoknot	Overlapping nested structures
Cloverleaf	Multiple repeating stem-loop structures

🧭 Step-by-Step Usage
Launch the app:

bash
Copy
Edit
streamlit run F2.py
Enter a DNA sequence in the input field (e.g., AACGTCGATT).

Click the "Detect Structures" button.

The app will:

Validate your sequence

Run detection on four known structures

Display formal grammars used for detection

Show indices where structures are located

Render a 3D node graph using Plotly to visualize the motif’s position in the sequence

📊 Example Output
Sample Input:
nginx
Copy
Edit
AACGTCGATT
Possible Output:
✅ Structure Detected: Hairpin

📜 Formal Grammar:

css
Copy
Edit
Hairpin ->
    A [ATGC]* T
    T [ATGC]* A
    G [ATGC]* C
    C [ATGC]* G
📌 Detected Indices:

Copy
Edit
[0, 3)
[6, 9)
🧩 3D Visualization: Interactive graph showing positions of motifs in red.

⚠️ Notes & Limitations
This version only works with DNA sequences (not RNA).

Results depend on how well the input matches the predefined rule patterns.

Some complex motifs may not be detected due to overlapping or ambiguous patterns.

Currently supports four common motifs, but is modular and extendable.

