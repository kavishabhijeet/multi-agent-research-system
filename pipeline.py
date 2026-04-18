from agents import build_reader_agent, build_serach_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    state = {}

    print("Step 1 - Search Agent is working now...")
    search_agent = build_serach_agent()
    search_result = search_agent.invoke({
        "input": f"Find recent, reliable, detailed information about: {topic}"  
    })
    state["search_results"] = search_result['output']  
    print("\nSearch Results:\n", state["search_results"])

    print("\nStep 2 - Reader Agent is scraping resources...")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "input": (                                      
            f"Based on the following search results about {topic}, "
            f"pick the most relevant URL and scrape its deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:500]}"
        )
    })
    state['scraped_content'] = reader_result['output']  
    print("\nScraped Content:\n", state['scraped_content'])

    print("\nStep 3 - Writer is drafting the report...")
    research_combined = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Detailed Scraped Content:\n{state['scraped_content']}"
    )
    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print("\nFinal Report:\n", state['report'])

    print("\nStep 4 - Critic is reviewing the report...")
    state['feedback'] = critic_chain.invoke({
        "report": state['report']
    })
    print("\nCritic Feedback:\n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)