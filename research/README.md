# LLM and Planing

## User imputs

Types: 
- Complete
- Abstract/Generic
- Incomplete

## Finance world models

Synthetic generation of financial world models using LLMs
- Goals
- High level actions
- Low level actions
- Timelines
- Milestones
- Constraints
- Budget
- Resources

## Bib and resources

- [importa]https://github.com/GuanSuns/LLMs-World-Models-for-Planning
- https://github.com/karthikv792/LLMs-Planning/tree/main
- [scraper]https://github.com/AI4Finance-Foundation/FinGPT/blob/master/fingpt/FinGPT_RAG/multisource_retrieval/news_scraper.py 
- [bingsearch](https://github.com/Azure-Samples/cognitive-services-REST-api-samples/blob/master/python/Search/BingWebSearchv7.py)
  
## The goal of LLM in a planing framework ('http://arxiv.org/abs/2402.01817')

- 'Second, we will propose a framework that allows us to leverage LLMs effectively in planning tasks, by combining them with external critics, verifiers and humans. We call this an LLM-Modulo Framework (a name loosely inspired by SAT Modulo Theories (Nieuwenhuis & Oliveras, 2006)); see Figure 3. LLMs play a spectrum of roles in this architecture, from guessing candidate plans, to translating those plans into syntactic forms that are more accessible to external critics, to helping end users flesh out incomplete specifications, to helping expert users acquire domain models (that in turn drive model-based critics). All this leveraging of LLMs is done without ascribing to them any planning or verification abilities. The LLM ideas are vetted by external critics, thus ensuring that the plans generated in this architecture can have formal correctness guarantees where possible.
- "LLMs may likely be good at generating plausible (but not guaranteed to be correct) plan heuristics/suggestions in many more scenarios."
- In this sense, it is more representative of real-world planning problems such as those in NASA mission planning, where the different critics–human and automated–are at best able to give “no objection” certificates, clearing it from their perspective. (Indeed, both deep space network planning and mars rover task planning are done via a collective human blackboard. (Johnston et al., 2014) (Bresina et al., 2004).)