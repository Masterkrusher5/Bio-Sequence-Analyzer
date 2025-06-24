# Bio-Sequence-Analyzer

BioSequence Analyzer is an interactive tool that identifies structural DNA motifs like hairpins, pseudoknots, and loops using formal language theory and matrix insertion–deletion rules. Built with Python, Streamlit, and Plotly, it provides real-time visual feedback via 3D node graphs.

## Citation & Conference
Published at:
17th International Conference on Engineering & Natural Sciences, Prague 🇨🇿

ISBN: 979-8-89695-087-5
DOI: https://doi.org/10.5281/zenodo.15673348

##  How to Use the BioSequence Analyzer

### Input Format

- The tool accepts DNA sequences composed of the characters: `A`, `T`, `G`, `C` (case-insensitive).
- Input must be a **single continuous string** (no spaces, no line breaks).

#### ✅ Valid Inputs
AACGTCGATT
ATGCGATACGTTAG
CGTATCGCGCTATACG

#### ❌ Invalid Inputs
ABCDXYZ123 # Contains invalid characters
" " or empty # Blank input
A T G C # Contains spaces

---

###  Structure Detection Logic

BioSequence Analyzer uses a **matrix insertion–deletion algorithm** to iteratively reduce sequences based on pattern rules. If the sequence fully reduces to an empty string using the defined rule set, the corresponding **motif is considered detected**.

#### Motifs Detected

| Structure     | Detection Rule Pattern Summary             |
|---------------|---------------------------------------------|
| Hairpin       | Palindromic regions with flanking complements |
| Stem and Loop | Complementary stems with loop regions      |
| Pseudoknot    | Overlapping stems, cross-paired            |
| Cloverleaf    | Repeated stem-loop motifs (≥3 times)       |

---

###  Step-by-Step Instructions

1. Run the app:
   ```bash
   streamlit run F2.py
2. Input a DNA sequence when prompted (e.g., AACGTCGATT).

3. Click the "Detect Structures" button.

4. The app will:

a) Validate your sequence

b) Detect structural motifs using insertion–deletion rules

c) Show formal grammars used

d) Highlight motif indices in sequence

e) Render a 3D structure visualization

 ## Example Output

Sample Input:AACGTCGATT

Example Results:

 Structure Detected: Hairpin

 Formal Grammar:

Hairpin ->
    A [ATGC]* T
    T [ATGC]* A
    G [ATGC]* C
    C [ATGC]* G
    
 Detected Indices:
 
[0, 3)
[6, 9)
