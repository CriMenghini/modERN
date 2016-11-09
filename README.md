![alt text](Images/logo_merge.png "Logo Title Text 1")

# modERN : mod-EPFL Researchers Network

*modERN* is a project to be developed during next months. It aims to present a *mod* description, analysis and exploration of the *EPFL Researchers Network*. In order to make it as much *mod* as possible, variety of techniques, representing current *state of the art* in the graph theory, are going to be used. Furthermore, the data visualization tools will be adopted for the purpose of illustrating the results of the analysis. Even despite being pretentious, it may end with some *generative art* exposing the obtained data and results.

But what is [*mod*](https://en.wikipedia.org/wiki/Mod_(subculture)) exactly?

        "the mass media often used the term mod in a wider sense to describe
        anything that was believed to be popular, fashionable or modern"

Stay tuned, the best is coming!

## Abstract

We present *modERN*, an analysis of the research community of the EPFL - a university recognized as an excellence in terms of research - and a visual exploration of the *white hot* topics which the research is addressed to. *modERN* focuses its attention on discovering departments collaboration's connections and the share of information. We are interested in how the interactions between groups change over time and what is the influence of one of them to the other. Using different data sources *modERN* estimates the potential of researches carried out at the EPFL. It checks whether they are acknowledged by the scientific community and guesses the researchers that will work on certain topics in the future. *modERN* represents the network as a graph where nodes are researchers and edges correspond to the relation of being in collaboration with each other.


## Data description

We use two source of data:

* [*infoscience*](https://infoscience.epfl.ch/collection/Infoscience/Research?ln=en): the official EPFL platform that collects the entire scientific production of the university. We will use this data to build the entire, complete graph. Since *infoscience* is an official container of data, we assume that the information retrieved from it is up-to-date, correct, complete and reliable. Hence, we use it as a basis of the network. The information fetched from the *website* are:
 - Authors of the paper
 - Paper's authors that belong to the EPFL community
 - Journal where the paper has been submitted to
 - Title of the paper
 - Abstract
 - Link to related works
 - Key words, topic
 - Laboratory
 - Paper pfd file

* [*Google Scholar*](https://scholar.google.ch/citations?view_op=view_org&hl=it&org=16539297749990713900): the information retrieved from 
this platform will be used on top of those collected from *infoscience*. We do not use *Google Scholar* as starting point since not all researchers necessary have an account there.

Additional data about researchers:
 - University
 - Position in the university
 - Fields of application
 - Number of citations
 - List of co-authors
 - *h*-index
 - List of papers

About paper:
 - Year of publication
 - Number of citations

The data are going to be collected as `html` files, then the information fetched from them will be stored in a `noSQL` database, like *MongoDB*.


## Feasibility and Risks

Scraping *Google Scholar* may be tricky since there are no clear rules related to the query limits that *Google* allows. In order to solve this problem and avoid the excess of allowed queries we will employ some tricks like:
 - Setting random time query
 - Making the request from different browsers
 - Randomizing queries order to get rid off the *causality* between consequential queries
 - Anonymous crawling with Tor


## Deliverable

The work ends up with:
 - Database
 - Graph and analysis
 - Community partition graph
 - Interactive visualization
 - (Generative art/stylized viz)


## Time schedule

1. Data collection (scrapping the data from *infoscience* and *Google Scholar*)
2. Analysis (processing the data and building the graph)
3. Visualization