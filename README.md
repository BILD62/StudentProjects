## About Final Projects in BILD 62

Students can choose a topic that extends an application from one of the assignments or in class notebooks, or propose their own topic. Topics largely fall into two categories:
1. Write a program to complete a task. For example:
  * Create a chatbot using the framework from the “guessing game” challenge.
  * Write a program that will generate plots for various datasets of the same format
  * Look for specific gene alleles in complex DNA sequences
2. Analyze & visualize data of the students' choosing
  * [Possible Datasets](https://docs.google.com/spreadsheets/d/1HsgkH2Ok_7ED_WFr9fIJ6PEPsm369L3HNFNUaXKRPX8/edit?usp=sharing)

### Project Scope
There is not a specific amount of code that students have to write for the project. The project must implement some new thing that students design and write the code for. To do so, students are expected to write new code that creates or adds some functionality. A project that appropriately responds to this call will have organized and documented code that:
1. Includes at least three new functions (or methods)
2. Uses code constructs such as loops and conditionals when needed
3. Imports code from available modules when needed

<hr>

## Sample Project Descriptions

### DNA Wordle
As biology majors, we are very familiar with the central dogma and the processes behind how DNA is made into the proteins within our bodies. DNA is first transcribed into RNA which is then translated into an amino acid sequence. The nucleotides, the basic unit of a nucleic acid, are arranged in specific orders which are recognized as codons. A codon is a sequence of three nucleotides that codes for one specific amino acid. These specific amino acids all have a single letter abbreviation which will be utilized in our project code. Given our familiarity with these pathways from our coursework, we wanted to take these principles and design a game that could be fun for users. Our code begins by having a dictionary that contains 10 different DNA sequences. One will be randomly chosen one for the user to participate in the game with. The DNA will then be transcribed into the complementary strand of RNA. From here, the code will loop through that RNA sequence in order to tell the user which amino acids are apart of the RNA strand using their single letter abbreviations. The user then will have to unscramble the single letter abbreviations in order to come up with a random 6 letter word.

### Marine Mammal Sound Game Description
Through interacting with this Notebook, we hope to underscore the importance of recording marine mammal
acoustic data by (1) sharing it directly with you, thanks to the National Oceanic and Atmospheric Administration
(NOAA) Fisheries New England/Mid-Atlantic Sounds in the Ocean database, (2) engaging you in a guessing
game called, Guess Who? Marine Mammal Edition, and (3) providing a feedback plot to help you visualize how
difficult it might be to analyze audio data without bioinformatics (the bar plot will display how many times a
player correctly guesses each marine mammal). Acoustic researchers use the same type of data provided in the
database to conduct new studies and maintain records for status updates on endangered or threatened marine
mammals.

### Quantifying Translation Rate of Mitochondrial mRNA
The goal of our project is to analyze raw data representing protein expression over time and infer translation elongation times of those genes of interest.

After DNA gets transcribed to mRNA in the cytoplasm, mRNA gets translated to protein. The translation elongation process has especially been found to be integral to mRNA localization to the mitochondria. Because the mitochondria is an important organelle for ATP production, our group wanted to calculate the rate of translation elongation of nuclear-encoded mitochondrial genes.

Our raw data contains measurements of luminescence from luciferase assays. This obtained by using an in-vivo elongation reporter containing luciferase to report the protein expression of the gene of interest (GOI). This reporter contains a tetracycline inducible promoter to govern transcription and translation of the GOI and luciferase. This data was imported in dataframe form. We know that protein expression is proportional to mRNA amounts and time, and mRNA amounts are proportional to DNA amounts and time. Knowing that DNA amounts are constant, nLuc expression can then be proportional to time. We can then take the square root of nLuc expression to produce a Schleif plot, which displays a nice linearization to further analyze the data (Schleif et al., 1973). After identifying the linear portion of the Schelif plot, we will produce a line of best fit to calculate the x-intercept, which represents the time it takes for the first protein to be produced. Then, we will take the difference between the x-intercepts of the control and the gene of interest in order to appreciate the elongation time of the gene of interest.
