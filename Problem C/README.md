## Project Files

| File | Purpose | 
|---|---|   
| Main.py | Handles user input, input validation, data loading, and interaction with the Trie. |
| tries.py | Contains the Trie data structure and the main algorithms for exact search, autocomplete, fuzzy search, and result ranking. |
| Dictionary.txt | Contains the dictionary entries and their frequencies used to build the Trie. |
| disclosure.ai | Records the use of AI tools during the development process. |
| README.md | Documentation describing the project and its usage. |

## Flowchart
''''Mermaid
flowchart LR
    %%Class init
    classDef startEnd fill:#f9f,stroke:#333,stroke-width:2px;
    classDef process fill:#e1f5fe,stroke:#0288d1,stroke-width:1px;
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:1px;
    classDef io fill:#e8f5e9,stroke:#388e3c,stroke-width:1px;
    classDef Error fill:#ffebee,stroke:#d32f2f,stroke-width:1px;
    classDef Stage fill:#B3EBF2, strok:#F83B72, stroke-width: 1px;

    %%Flowchart
    subgraph Initialization["<font size = 5> <b>Initiating and Reading Dictionary File<b>"]
        direction LR
        Start(["Start"]) --> B["Initiate Trie and environment Varibles"]
        B --> C{"Open Dictionary.txt"}
        C --Fail--> D["File Not Found"]
        C --Success--> E["Process data line by line"]
        E --> G["Input Validation"]
        G --> I{"Validate Word ? <br>(No Empty, No Space, No number)"}
        I --Fail--> G
        I --Success--> J{"Validate Weight ? <br>(Positive Integer)"}
        J --Fail--> G
        J --Success--> K["Add Data into Trie"]
        K --> L["Repeat the process until all data is processed"]
        L --> M["Trie is successfully built"]
    end
    
    subgraph User_Input["<font size = 5> <b> User Input Handling<b>"]
        direction LR
        M --> N["User Input Word"]
        N --> O{"Validate Word ? <br>(No Empty, No Space, No number)"}
        O --Fail--> N
        O --Success--> P["Call Trie.autocomplete() and Trie.fuzzy_search()"]
    end

    subgraph Trie_Search["<font size = 5> <b> Finding, processing and suggesting (Trie)"]
        direction LR
        P --> Search_1["1. Autocomplete (Trie): Finding by best Prefix"]
        P --> Search_2["2. Fuzzy_search (Trie): Finding by Edit distance"]
        Search_1 --> Result["Calculate Score: <br> Accuracy (Least Error) + Frequency"]
        Search_2 --> Result
        Result --> Sort["Sort by Highest Score"]
        Sort --> Output["Take the word with highest score on each method"]
    end

    subgraph Final_Result["<font size = 5> <b>Final Result<b>"]
        direction LR
        Output --> Combine["Compare the result from both method"]
        Combine --> Print["Choose the word with highest score"]
        Print --> Positive_Score{"Score > 0 ?"}
        Positive_Score--True-->Result_1["Print: Do you mean + 'word' "]
        Positive_Score--False-->Result_2["Print: I Don't Know"]
    end

    Result_1 --> End
    Result_2 --> End

    %%Applying class for node.
    class Start startEnd;
    class Initialization,User_Input,Trie_Search,Final_Result Stage;
    class D Error;
    class G,I,J,O decision;
    class B,C,E,K,L,M,N,P,Result,Sort,Output,Combine,Print,Positive_Score,Result_1,Result_2 process;