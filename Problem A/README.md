# Problem A: The Word Predictor
## Phase 2: Open Architecture
* **The Training Corpus:** We chose a basic conversational, technical, and general-topic English text file. It provides enough realistic word pairings to demonstrate the predictor's learning capability without requiring massive memory overhead.
* **Context Depth:** We implemented a 2-gram (Bigram) tree. It is highly performant, uses minimal memory, and maps a single `current_word` directly to its most probable candidate next words, which perfectly satisfies the core prediction requirement.
* **Tie-Breaking Logic:** Candidates are primarily ranked by frequency in descending order. When two or more words share the exact same frequency, the engine breaks the tie alphabetically (a → z). The top 5 results from this ranking are then displayed. This ensures the output is always deterministic and predictable rather than relying on random chance.
## Program flow
```mermaid
flowchart TD
    Start([Start Program])
    %% 1. Setup Phase
    subgraph Setup ["1. Initialization & Setup"]
        A[Load 'training_sentences.txt']
        B["Preprocess Text & Generate 2-Grams(clean_tokenize)"]
        C["Build Trie Structure (NGramTree.build_from_2grams)"]
        D["Initialize Predictor Engine (WordPredictor)"]
        
        A --> B --> C --> D
    end

    Start --> A

    %% 2. Main Loop
    subgraph MainLoop ["2. Interactive Loop (predictor.run)"]
        E["Prompt User: Enter a word"]
        F{"Is Input Empty?"}
        
        %% Empty Input Sub-branch
        G{"Empty Count == 2?"}
        H[Increment empty_count]
        I["Print Input History"]
        End([Exit / Terminate Program])
        
        %% Valid Input Sub-branch
        J["Reset empty_count = 0 Append word to input_history"]
        J2["Update History (Dynamic Trie Update)"]
    end

    D --> E
    E --> F
    
    %% Empty input logic
    F -- "Yes" --> H
    H --> G
    G -- "Yes" --> I --> End
    G -- "No" --> E

    %% Process word logic
    F -- "No" --> J
    J --> J2

    %% 3. Prediction Pipeline
    subgraph Prediction ["3. Prediction Engine (predict & search_node)"]
        K{"Does word exist in Trie root?"}
        K2["Create new node in root"]
        L["Return node"]
        
        N{"Has Next-Word Children?"}
        O["Extract Candidate Pairs:(next_word, frequency)"]
        
        P["Sort Candidates:Frequency (Descending) Alphabetical (Ascending)"]
        Q["Slice Top-K Predictions(Top 5)"]
        
        R["Display 'No prediction found, new node created.'"]
        S["Display Top-K Ranked Results"]
    end

    J2 --> K
    
    %% Unknown word branch
    K -- "No" --> K2
    K2 --> L
    
    %% Known word branch
    K -- "Yes" --> L
    L --> N
    
    N -- "No Children" --> R
    N -- "Yes" --> O
    
    O --> P --> Q --> S
    
    %% Loop back to prompt
    S --> E
    R --> E
```

## Project Files
| **File** | **Purpose** |
| :--- | :--- |
| main.py | The program's entry point |
| predictor.py | Manages user input |
| preprocess.py | Tokenizes entry data |
| training_sentences.txt | Training dataset |
|trie.py | Defines TrieNode/NGramTree class |
|README.md | Demonstrate program's flow |
|disclosur.ai | AI usage log |